"""
app = Flask(__name__) 创建了应用

@app.route('/') 是注册路由

app.run() 启动服务
"""

from flask import Flask, request, jsonify
import requests
import json
app = Flask(__name__)


def get_song(word):

    url = 'https://www.baidu.com'
    resp = requests.get(url).text
    return {
        'resp': resp
    }


@app.route('/get_song', methods=['GET'])
def song():
    word = request.args.get('word')
    try:
        result = get_song(word)
        return jsonify({'results': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    # print(get_song('诺言'))
