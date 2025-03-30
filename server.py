from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/scrape', methods=['GET'])
def scrape_chapter():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    headers = {"User-Agent": "Mozilla/5.0"}  # Simulate a real browser request
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch the page"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    # Modify this selector based on the novel site
    content = soup.select_one('.chapter-content')
    if not content:
        return jsonify({"error": "Content not found"}), 404

    # Extract next & previous chapter links
    next_chapter = soup.select_one('.next a')
    prev_chapter = soup.select_one('.prev a')

    return jsonify({
        "content": str(content),
        "next": next_chapter['href'] if next_chapter else None,
        "prev": prev_chapter['href'] if prev_chapter else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
