from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_song')
def get_song():
    word = request.args.get('word', '')
    song_url = f"https://www.douyin.com/search/{word}"
    return jsonify({
        "结果": {
            "song_url": song_url
        }
    })
