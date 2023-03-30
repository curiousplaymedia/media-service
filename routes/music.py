from flask import Flask, jsonify, request
from services import musicgrabber

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello!'


@app.route("/grab-album", methods=["POST"])
def grabAlbum():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify(musicgrabber.grab_album(data['url']))


@app.route("/grab-albums", methods=["POST"])
def grabAlbums():
    if request.method == 'POST':
        data = request.get_json()
        return musicgrabber.grab_albums(data['urls'])
