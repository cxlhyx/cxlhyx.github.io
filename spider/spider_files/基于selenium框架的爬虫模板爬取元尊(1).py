import re
import requests
from selenium import webdriver  # 打开网页爬取源码
from bs4 import BeautifulSoup  # 解析源码


class MySpider():
    def __init__(self):
        pass

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, url):
        try:
            driver.get(url)
            driver.set_page_load_timeout(10)  # 设置超时限制10s
            html_content = driver.page_source  # 网页内容
            return html_content  # 返回网页内容
        except Exception as e:
            print(f"网页请求异常：{e}")
            return None

    # Step 2: 解析网页并提取目标数据
    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')  # 解析 html 数据
        # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中
        data_list = []
        img = soup.find("img", attrs={"alt": "元尊"})['src']  # 封面
        data_list.append([img])
        info = []
        for i in soup.find_all("div", id="info"):
            info.append(i.find("h1").text)  # 书名
            for j in i.find_all('p'):
                info.append(re.sub(r"<a.*>|</a>", '', j.text))  # 作者、动作、更新时间、最新
            info.append(i.find("div", id='intro').text.replace(" ", "\n"))  # 简介
        data_list.append(info)
        url = []
        for i in soup.find_all('dd'):
            try:
                url.append(i.find('a')['href'])
            except:
                pass
        data_list.append(list(set(url)))
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        img = requests.get(result_list[0][0])
        with open("元尊/元尊.png", 'wb') as file:
            file.write(img.content)
        with open("元尊/元尊.docx", 'w', encoding='utf-8') as file:
            for i in result_list[1]:
                file.write(i+'\n')
        with open("元尊/元尊.txt", 'w', encoding='utf-8') as file:
            for i in result_list[2]:
                file.write(i + '\n')
        pass


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    driver = webdriver.Firefox()  # 打开火狐浏览器
    spider = MySpider()
    target_url = "https://www.quanben.so/86_86296/"
    html_content = spider.get_html_content(target_url)
    if html_content:
        result_list = spider.parse_html(html_content)
        spider.store_data(result_list)
    else:
        print("网页访问失败")
    driver.close()  # 关闭浏览器
