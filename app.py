"""
app = Flask(__name__) 创建了应用

@app.route('/') 是注册路由

app.run() 启动服务
"""
from DrissionPage import ChromiumPage, ChromiumOptions
from flask import Flask, request, jsonify
import json

app = Flask(__name__)


def get_song(word):
    headers = {
        "referer": "https://www.douyin.com/root/search/%E5%88%98%E5%BE%B7%E5%8D%8E?type=video",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    page = ChromiumPage()
    page.set.headers(headers=headers)
    url = f'https://www.douyin.com/search/{word}?aid=2a8efa1c-178b-4a84-a1cf-28ef9e8b230a&type=general'
    page.listen.start('general/search/stream')
    page.get(url)
    page.wait(3)
    res = page.listen.wait()
    resp = res.response.body.split('\n')[1]
    for i in json.loads(resp)['data']:
        if i:
            song_url = i['aweme_info']['video']['play_addr']['url_list'][-1]
            dic = {
                'song_url': song_url
            }
            return dic
        return {'song_url': '未找到'}




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
