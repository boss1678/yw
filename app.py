"""
app = Flask(__name__) 创建了应用

@app.route('/') 是注册路由

app.run() 启动服务
"""

from flask import Flask, request, jsonify
import requests
from pypinyin import lazy_pinyin
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from DrissionPage import ChromiumOptions, ChromiumPage
# 导包
import logging

app = Flask(__name__)


# 修改函数
def get_song(word):
    """
    歌曲下载
    :return:
    """
    song_url_lst = []
    try:
        co = ChromiumOptions()
        co.set_argument('--no-sandbox')
        co.set_argument('--headless=new')
        co.set_argument('--disable-gpu')
        co.set_argument('--disable-software-rasterizer')
        co.set_argument('--disable-dev-shm-usage')
        co.set_argument('--window-size=1920,1080')
        co.set_argument('--user-data-dir=/tmp/chromium-data')
        co.set_argument('referer', "https://www.douyin.com/")
        co.set_user_agent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
        page = ChromiumPage(co)
        url = f'https://www.douyin.com/search/{word}?type=general'
        page.listen.start('general/search')
        page.get(url)
        page.wait(2)
        while 1:
            page.run_js('window.scrollBy(0, 1500)')
            page.wait(3)
            if page.run_js(
                    'return (window.innerHeight + document.scrollingElement.scrollTop) >= document.scrollingElement.scrollHeight - 10'):
                break
            while 1:
                res = page.listen.wait(timeout=0.5)
                if not res or isinstance(res, bool):
                    break
                resp = res.response.body
                if not isinstance(resp, dict):
                    continue
                for i in resp['data']:
                    if not i:
                        continue
                    aweme_info = i.get('aweme_info')
                    if not aweme_info:
                        continue
                    video = aweme_info.get('video')
                    if not video:
                        continue
                    play_addr = video.get('play_addr')
                    if not play_addr:
                        continue
                    url_list = play_addr.get('url_list')
                    if not url_list:
                        continue
                    song_url = url_list[0]
                    song_url_lst.append(song_url)
                    if len(song_url_lst) >= 5:
                        break
            break
        page.quit()
        return {'song_url_lst': song_url_lst}
    except Exception as e:
        logging.error(f'抓取失败: {e}')
        return {'error': '抓取失败，请稍后重试'}


@app.route('/')
def index():
    return "Flask 服务运行正常"


@app.route('/get_song', methods=['POST', 'GET'])
def song():
    word = request.args.get('input')
    try:
        result = get_song(word)
        return jsonify({'results': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # print(get_song('情罪'))
