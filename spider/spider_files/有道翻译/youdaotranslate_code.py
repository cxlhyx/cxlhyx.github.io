import json
import time
import tkinter as tk
from Crypto.Cipher import AES
import hashlib
import base64
from Crypto.Util.Padding import unpad
import requests  # request库爬取源码


# js逆向，理解js代码后，用python实现，对响应内容解码
def decodedData(response):
    decodeKey = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
    decodeIv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
    key_md5 = hashlib.md5(decodeKey.encode('utf-8')).digest()
    iv_md5 = hashlib.md5(decodeIv.encode('utf-8')).digest()
    aes = AES.new(key=key_md5, mode=AES.MODE_CBC, iv=iv_md5)
    code = aes.decrypt(base64.urlsafe_b64decode(response))
    return unpad(code, AES.block_size).decode('utf8')


# 基于爬虫模板的有道翻译类
class YoudaoTranslate():
    def __init__(self, From='auto', To=''):  # 只能从‘auto’到‘’,不然结果错误
        self.f = From
        self.to = To

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, word):
        url = "https://dict.youdao.com/webtranslate"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-648896178@10.55.164.98; OUTFOX_SEARCH_USER_ID_NCOO=1245281847.2676084',
            'Referer': 'https://fanyi.youdao.com/'
        }  # 请求头，爬虫程序通过加上请求头伪装成浏览器
        ts = round(time.time() * 1000)
        data = {
            'i': word,
            'from': self.f,
            'to': self.to,
            'dictResult': 'true',
            'keyid': 'webfanyi',
            'sign': hashlib.md5('client=fanyideskweb&mysticTime={}&product=webfanyi&key=fsdsogkndfokasodnaso'.format(
                ts).encode('utf-8')).hexdigest(),
            'client': 'fanyideskweb',
            'product': 'webfanyi',
            'appVersion': '1.0.0',
            'vendor': 'web',
            'pointParam': 'client,mysticTime,product',  # 没有空格
            'mysticTime': str(ts),
            'keyfrom': 'fanyi.web',
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()  # 判断返回的Response类型状态是不是200
            response.encoding = response.apparent_encoding  # 从内容中分析出的响应内容编码
            html_content = response.text  # 网页内容
            return html_content  # 返回网页内容
        except Exception as e:
            text2.insert('0.0', f"网页请求异常：{e}")
            return None

    # Step 2: 解析网页并提取目标数据
    def parse_html(self, html_content):
        # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中
        data_list = json.loads(decodedData(html_content))
        try:
            text2.insert('0.0', data_list['translateResult'][0][0]['tgt'])
        except:
            text2.insert('0.0', data_list)
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        try:
            with open('history.txt', 'a', encoding='utf-8') as file:
                file.write(
                    result_list['translateResult'][0][0]['src'] + ": " + result_list['translateResult'][0][0][
                        'tgt'] + '\n')
        except:
            pass

    def main(self, word):
        text2.delete('0.0', 'end')
        html_content = youdaotranslate.get_html_content(word)
        if html_content:
            result_list = youdaotranslate.parse_html(html_content)
            youdaotranslate.store_data(result_list)
        else:
            text2.insert('0.0', "网页访问失败")


# 关于函数
def state():
    root_state = tk.Tk()
    root_state.title('关于')
    root_state.geometry('300x300+650+250')
    tk.Label(root_state,
             text='制作者：黄堉轩\n 版本：1.0.0\n Alt+s 快捷翻译\n Alt+d 删除原文\n Alt+w 全部删除\n Alt+e 退出程序').pack()
    root_state.mainloop()


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    youdaotranslate = YoudaoTranslate()

    root = tk.Tk()  # 窗口
    root.title('有道翻译')  # 标题
    root['bg'] = '#e0ffff'  # 背景颜色
    root.geometry('300x300+650+250')  # 大小

    bar = tk.Menu(root)  # 定义菜单
    root.config(menu=bar)  # 配置菜单
    bar.add_command(label='关于', command=state)  # 菜单内容

    tk.Label(root, text='原文').place(x=45, y=50)
    text1 = tk.Text(root, background='white', foreground='black', width=20, height=5)
    text1.place(x=80, y=30)  # 原文输入框

    tk.Label(root, text='译文').place(x=45, y=150)
    text2 = tk.Text(root, background='white', foreground='black', width=20, height=5)
    text2.place(x=80, y=130)  # 译文输出框

    tk.Button(root, text='翻译', command=lambda: youdaotranslate.main(text1.get('0.0', 'end'))).place(x=135,
                                                                                                      y=225)  # 翻译按钮

    root.bind("<Alt-s>", lambda event: youdaotranslate.main(text1.get('0.0', 'end')))  # 快捷翻译
    root.bind("<Alt-d>", lambda event: text1.delete('0.0', 'end'))  # 删除原文
    root.bind('<Alt-w>', lambda event: [text1.delete('0.0', 'end'), text2.delete('0.0', 'end')])  # 全部删除
    root.bind('<Alt-e>', lambda event: root.destroy())  # 退出程序

    root.mainloop()
