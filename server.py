from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['GET'])
def scrape_chapter():
    url = request.args.get('url')
    content_selector = request.args.get('content')
    prev_selector = request.args.get('prev')
    next_selector = request.args.get('next')

    if not url or not content_selector or not prev_selector or not next_selector:
        return jsonify({"error": "Missing parameters"}), 400

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch the page"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.select_one(content_selector)
    if not content:
        return jsonify({"error": "Content not found"}), 404

    next_chapter = soup.select_one(next_selector)
    prev_chapter = soup.select_one(prev_selector)

    return jsonify({
        "content": str(content),
        "next": next_chapter['href'] if next_chapter else None,
        "prev": prev_chapter['href'] if prev_chapter else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
