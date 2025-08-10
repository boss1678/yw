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
    headers = {
        'referer': 'https: // www.shicimingju.com /',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    pinyin_list = lazy_pinyin(word)
    pinyin_str = ''.join(pinyin_list)
    url = f'https://www.shicimingju.com/book/{pinyin_str}.html'
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    urls = [urljoin(url, sp.get('href')) for sp in soup.find('div', class_="list").find_all('a')]
    return {
        'urls': urls
    }


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
    # print(get_song('三国演义'))
