from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Gibt alle Blogbeiträge zurück und sortiert sie optional.

    Die Sortierung erfolgt über die Query-Parameter 'sort' und 'direction'.
    Ohne Angabe eines Sortierfeldes bleibt die ursprüngliche Reihenfolge erhalten.

    sort: Sortierfeld ('title' oder 'content').
    direction: Sortierrichtung ('asc' oder 'desc'). Standardmäßig aufsteigend.

    :return: JSON-Liste der Blogbeiträge (200) oder Fehlermeldung (400).
    """
    sort = request.args.get('sort', '').lower()
    direction = request.args.get('direction', '').lower()

    if direction and direction not in ('asc', 'desc'):
        return jsonify({'error': 'Invalid sort direction'}), 400

    if not sort:
        return jsonify(POSTS)

    if sort not in ('title', 'content'):
        return jsonify({'error': 'Invalid sort field'}), 400

    if direction == "desc":
        sorted_posts = sorted(
            POSTS,
            key=lambda post: post[sort],
            reverse=True
        )
    else:
        sorted_posts = sorted(
            POSTS,
            key=lambda post: post[sort],
            reverse=False
        )

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Fügt einen neuen Blogpost hinzu.

    Erwartet ein JSON-Objekt mit den Pflichtfeldern 'title' und 'content'.
    Die ID wird automatisch vergeben.

    :return: Neuer Blogbeitrag als JSON (201) oder Fehlermeldung (400).
    """
    post_data = request.get_json()

    if not isinstance(post_data, dict):
        return jsonify(
            {'error': 'Request body must be a JSON object'}
        ), 400

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


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Löscht einen Blogbeitrag anhand seiner ID.

    :param post_id: ID des zu löschenden Blogbeitrags.
    :return: JSON-Erfolgsmeldung (200) oder Fehlermeldung (404).
    """
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify(
                {'message': f"Post with id {post_id} has been deleted successfully."}
            ), 200

    return jsonify({'message': f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Aktualisiert einen bestehenden Blogbeitrag anhand seiner ID.

    Erwartet ein JSON-Objekt mit 'title' und/oder 'content'.
    Nur übergebene, nicht leere Felder werden aktualisiert.

    :param post_id: ID des zu aktualisierenden Blogbeitrags.
    :return: Aktualisierter Blogbeitrag als JSON (200)
             oder Fehlermeldung (400 oder 404).
    """
    update_post_data = request.get_json()

    if not isinstance(update_post_data, dict):
        return jsonify(
            {'error': 'Request body must be a JSON object'}
        ), 400

    for post in POSTS:
        if post['id'] == post_id:
            if update_post_data.get('title'):
                post['title'] = update_post_data.get('title')

            if update_post_data.get('content'):
                post['content'] = update_post_data.get('content')

            return jsonify(post), 200

    return jsonify({'message': f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """
    Durchsucht Blogbeiträge nach Titel oder Inhalt.

    Die Suche erfolgt über die Query-Parameter 'title' und 'content'.
    Ein Beitrag wird zurückgegeben, wenn mindestens ein Suchbegriff
    im entsprechenden Feld enthalten ist.

    :return: JSON-Liste der gefundenen Blogbeiträge (200).
             Bei fehlenden Treffern wird eine leere Liste zurückgegeben.
    """
    title = request.args.get('title', '').lower()
    content = request.args.get('content', '').lower()

    matching_posts = []

    for post in POSTS:
        if title:
            if (
                title in post['title'].lower()
                and post not in matching_posts
            ):
                matching_posts.append(post)
        if content:
            if (
                content in post['content'].lower()
                and post not in matching_posts
            ):
                matching_posts.append(post)

    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
