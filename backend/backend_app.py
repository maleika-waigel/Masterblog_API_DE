from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Fügt einen neuen Blogpost hinzu.

    Erwartet ein JSON-Objekt mit den Feldern 'title' und 'content'.
    Gibt den neuen Blogpost oder eine Fehlermeldung zurück.

    :return: JSON-Antwort mit Statuscode 201 oder 400.
    """
    post_data = request.get_json()

    if not isinstance(post_data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    error_list = []

    if not post_data.get('title'):
        error_list.append('Title is missing')
    if not post_data.get('content'):
        error_list.append('Content is missing')

    if error_list:
        return jsonify({'errors': error_list}), 400

    new_id = max((post['id'] for post in POSTS), default=0) + 1

    new_post = {
        'id': new_id,
        'title': post_data['title'],
        'content': post_data['content']
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
