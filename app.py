"""
app = Flask(__name__) 创建了应用

@app.route('/') 是注册路由

app.run() 启动服务
from DrissionPage import ChromiumOptions

def get_chrome_options():
    co = ChromiumOptions()

    # ✅ 启用远程调试端口（必须）
    co.set_argument('--remote-debugging-port=9222')

    # ✅ 禁用沙箱（适用于 root 用户）
    co.set_argument('--no-sandbox')

    # ✅ 避免共享内存问题（服务器常见）
    co.set_argument('--disable-dev-shm-usage')

    # ✅ 无头模式（服务器无图形界面时必须）
    co.set_argument('--headless')

    # ✅ 禁用 GPU 加速（无头模式下建议）
    co.set_argument('--disable-gpu')

    # ✅ 禁用扩展（提高稳定性）
    co.set_argument('--disable-extensions')

    # ✅ 禁用信息栏（防止“Chrome 正由自动化软件控制”提示）
    co.set_argument('--disable-infobars')

    return co

"""

from flask import Flask, request, jsonify
from DrissionPage import ChromiumOptions, ChromiumPage

app = Flask(__name__)


def get_song(word):
    """
    歌曲下载
    :return:
    """
    song_urls = []
    co = ChromiumOptions()
    co.headless(True)
    co.set_argument('--remote-debugging-port=9222')
    co.set_browser_path('/usr/bin/google-chrome')
    co.set_argument('--headless=new')
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-gpu')
    co.set_argument('--disable-dev-shm-usage')
    co.set_argument('--no-first-run')
    co.set_argument('--user-data-dir=/tmp/chrome-profile')
    co.set_user_agent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
    page = ChromiumPage(co)
    url = f'https://www.douyin.com/search/{word}?type=general'
    if url:
        print(f'准备下载 --> {word}....')
    page.listen.start('general/search')
    page.get(url)
    page.wait(2)
    try:
        while 1:
            page.run_js('window.scrollBy(0, 1200)')
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

                for i in resp.get('data'):
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
                    song_url = url_list[-1]
                    song_urls.append(song_url)
                    if len(song_urls) >= 5:
                        break
            if len(song_urls) >= 5:
                break
    except Exception as e:
        print(e)
    finally:
        page.quit()
    return {
        'song_urls': song_urls
    }


@app.route('/')
def index():
    return "Flask 服务运行正常"


@app.route('/get_song', methods=['POST', 'GET'])
def song():
    word = request.args.get('input')
    try:
        result = get_song(word)
        return jsonify({word: result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
