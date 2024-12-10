import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import trange


class MySpider():
    def __init__(self):
        pass

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, url):
        headers = {
            'User-Agent': UserAgent().random
        }  # 请求头，爬虫程序通过加上请求头伪装成浏览器
        data = {'name': 'huoyouxing'}
        try:
            response = requests.get(url, data=data, headers=headers)
            response.raise_for_status()  # 判断返回的Response类型状态是不是200
            response.encoding = response.apparent_encoding  # 从内容中分析出的响应内容编码
            html_content = response.text  # 网页内容
            return html_content  # 返回网页内容
        except Exception as e:
            print(f"网络请求异常：{e}")
            return None

    # Step 2: 解析网页并提取目标数据
    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')  # 解析 html 数据
        # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中
        data_list = []
        data_list.append(
            [i.find('a')['title'] for i in soup.find_all(name='div', attrs={'class': 'pl2'})])  # 书名
        data_list.append([i.text for i in soup.find_all(name='p', attrs={'class': 'pl'})])  # 作者
        data_list.append([i.text for i in soup.find_all(name='span', attrs={'class': 'rating_nums'})])  # 评分
        list = []  # 简介
        for i in soup.find_all(name='tr', attrs={'class': 'item'}):
            if i.find(name='span', attrs={'class': 'inq'}):  # 简介存在
                list.append(i.find(name='span', attrs={'class': 'inq'}).text)
            else:  # 简介可能不存在
                list.append(' ')
        data_list.append(list)
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        with open('豆瓣图书Top250.txt', 'a', encoding='utf-8') as file:
            for i in range(25):
                file.write("书名：" + result_list[0][i] + '\n')
                file.write("作者：" + result_list[1][i] + '\n')
                file.write("评分：" + result_list[2][i] + '\n')
                file.write("简介：" + result_list[3][i] + '\n')
                file.write('=' * 50 + '\n')


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    spider = MySpider()
    url = "https://book.douban.com/top250?start="
    for page in trange(0, 250, 25):
        target_url = url + str(page)
        html_content = spider.get_html_content(target_url)
        if html_content:
            result_list = spider.parse_html(html_content)
            spider.store_data(result_list)
        else:
            print("网页访问失败")
