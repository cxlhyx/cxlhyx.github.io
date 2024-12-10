import json
import time
import tkinter as tk
import execjs
import requests  # request库爬取源码


# js逆向,使用execjs分析实现js代码（先扣下js代码），解决sign
def sign(word):
    try:
        with open("百度翻译sign.js", encoding='utf-8') as js:
            js_content = js.read()
    except:
        js_content = r"""
        function e(t, e) {
            (null == e || e > t.length) && (e = t.length);
            for (var n = 0, r = new Array(e); n < e; n++)
                r[n] = t[n];
            return r
        }
        function n(t, e) {
            for (var n = 0; n < e.length - 2; n += 3) {
                var r = e.charAt(n + 2);
                r = "a" <= r ? r.charCodeAt(0) - 87 : Number(r),
                r = "+" === e.charAt(n + 1) ? t >>> r : t << r,
                t = "+" === e.charAt(n) ? t + r & 4294967295 : t ^ r
            }
            return t
        }
        var r = "320305.131321201";
        sign = function(t) {
            var o, i = t.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
            if (null === i) {
                var a = t.length;
                a > 30 && (t = "".concat(t.substr(0, 10)).concat(t.substr(Math.floor(a / 2) - 5, 10)).concat(t.substr(-10, 10)))
            } else {
                for (var s = t.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), c = 0, u = s.length, l = []; c < u; c++)
                    "" !== s[c] && l.push.apply(l, function(t) {
                        if (Array.isArray(t))
                            return e(t)
                    }(o = s[c].split("")) || function(t) {
                        if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"])
                            return Array.from(t)
                    }(o) || function(t, n) {
                        if (t) {
                            if ("string" == typeof t)
                                return e(t, n);
                            var r = Object.prototype.toString.call(t).slice(8, -1);
                            return "Object" === r && t.constructor && (r = t.constructor.name),
                            "Map" === r || "Set" === r ? Array.from(t) : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? e(t, n) : void 0
                        }
                    }(o) || function() {
                        throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
                    }()),
                    c !== u - 1 && l.push(i[c]);
                var p = l.length;
                p > 30 && (t = l.slice(0, 10).join("") + l.slice(Math.floor(p / 2) - 5, Math.floor(p / 2) + 5).join("") + l.slice(-10).join(""))
            }
            for (var d = "".concat(String.fromCharCode(103)).concat(String.fromCharCode(116)).concat(String.fromCharCode(107)), h = (null !== r ? r : (r = window[d] || "") || "").split("."), f = Number(h[0]) || 0, m = Number(h[1]) || 0, g = [], y = 0, v = 0; v < t.length; v++) {
                var _ = t.charCodeAt(v);
                _ < 128 ? g[y++] = _ : (_ < 2048 ? g[y++] = _ >> 6 | 192 : (55296 == (64512 & _) && v + 1 < t.length && 56320 == (64512 & t.charCodeAt(v + 1)) ? (_ = 65536 + ((1023 & _) << 10) + (1023 & t.charCodeAt(++v)),
                g[y++] = _ >> 18 | 240,
                g[y++] = _ >> 12 & 63 | 128) : g[y++] = _ >> 12 | 224,
                g[y++] = _ >> 6 & 63 | 128),
                g[y++] = 63 & _ | 128)
            }
            for (var b = f, w = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(97)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(54)), k = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(51)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(98)) + "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(102)), x = 0; x < g.length; x++)
                b = n(b += g[x], w);
            return b = n(b, k),
            (b ^= m) < 0 && (b = 2147483648 + (2147483647 & b)),
            "".concat((b %= 1e6).toString(), ".").concat(b ^ f)
        }
        """
    compile = execjs.compile(js_content)
    return compile.call("sign", word)


# 基于爬虫模板的百度翻译类
class BaiduTranslate():
    def __init__(self, From='zh', To='en'):
        self.f = From
        self.to = To

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, word):
        url = "https://fanyi.baidu.com/v2transapi?from=zh&to=en"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Cookie': 'BAIDUID=440DB221A934E936F8FDB79991C090A6:FG=1; BAIDUID_BFESS=440DB221A934E936F8FDB79991C090A6:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1701423596,1701446880,1701484763,1701590081; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1701590247; ab_sr=1.0.1_MzBlMDNlMTc0MzBhMDg4MGQ0ZGRkMzFiZjQ5MDk4ZmI1ODdiMDI2MjA1MGMwOTAwNDNjM2MyYzcyYjVmNzI5YjNiYTM2MGU1YzA4MzY3MzFkOTdhYTNkODE0YmUxYmZjYzM1NzdjN2M3ZTJmYjgzZGM5MTBkY2ZmMTk1MWM0Njk2MDViN2I3ZTBmYWRiMmRhMjY5NGQzYzY3ZTIyY2I1MA==',
            'Referer': 'https://fanyi.baidu.com/',
        }  # 请求头，爬虫程序通过加上请求头伪装成浏览器
        data = {
            'from': self.f,
            'to': self.to,
            'query': word,
            'transtype':'realtime',
            'simple_means_flag': 3,
            'sign': sign(word),
            'token': '1de99dcf9ebd73c936dbdecff7f2422f',
            'domain': 'common',
            'ts': round(time.time() * 1000)
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
        data_list = json.loads(html_content)
        try:
            text2.insert('0.0', data_list['trans_result']['data'][0]['dst'])
        except:
            text2.insert('0.0', data_list)
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        try:
            with open('history.txt', 'a', encoding='utf-8') as file:
                file.write(
                    result_list['trans_result']['data'][0]['src'] + ": " + result_list['trans_result']['data'][0][
                        'dst'] + '\n')
        except:
            pass

    def main(self, word):
        text2.delete('0.0', 'end')
        html_content = baidutranslate.get_html_content(word)
        if html_content:
            result_list = baidutranslate.parse_html(html_content)
            baidutranslate.store_data(result_list)
        else:
            text2.insert('0.0', "网页访问失败")


# 关于函数
def state():
    root_state = tk.Tk()
    root_state.title('关于')
    root_state.geometry('300x300+650+250')
    tk.Label(root_state, text='制作者：黄堉轩\n 版本：1.0.0\n Alt+s 快捷翻译\n Alt+d 删除原文\n Alt+w 全部删除\n Alt+e 退出程序').pack()
    root_state.mainloop()


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    baidutranslate = BaiduTranslate()  # 百度翻译类

    root = tk.Tk()  # 窗口
    root.title('百度翻译')  # 标题
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

    tk.Button(root, text='翻译', command=lambda: baidutranslate.main(text1.get('0.0', 'end'))).place(x=135, y=225)  # 翻译按钮

    root.bind("<Alt-s>", lambda event: baidutranslate.main(text1.get('0.0', 'end')))  # 快捷翻译
    root.bind("<Alt-d>", lambda event: text1.delete('0.0', 'end'))  # 删除原文
    root.bind('<Alt-w>', lambda event: [text1.delete('0.0', 'end'), text2.delete('0.0', 'end')])  # 全部删除
    root.bind('<Alt-e>', lambda event: root.destroy())  # 退出程序

    root.mainloop()
