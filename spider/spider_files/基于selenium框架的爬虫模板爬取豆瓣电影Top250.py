from selenium import webdriver  # 打开网页爬取源码
from bs4 import BeautifulSoup  # 解析源码
from tqdm import trange


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
        data_list.append([[j.text.replace("\xa0/\xa0", "") for j in i.find_all('span', ['title', 'other'])]
                          for i in soup.find_all('div', 'hd')])  # 电影名
        wwww = []
        for i in soup.find_all('div', 'bd'):
            tmp = []
            for j in i.find('p', _class=''):
                text = j.text.replace("\xa0\xa0\xa0", '\\')
                text = text.replace("\xa0", "")
                text = text.replace("\n", "")
                text = text.replace(" ", "")
                if text != "" and text != '豆瓣':
                    tmp.append(text)
            if len(tmp) != 0:
                wwww.append(tmp)
        data_list.append(wwww)  # who when where what
        data_list.append([i.text for i in soup.find_all('span', {'class': "rating_num", 'property': "v:average"})])  # 评分
        About = []
        for i in soup.find_all('div', 'info'):
            if i.find('span', 'inq'):
                About.append(i.find('span', 'inq').text)
            else:
                About.append(" ")
        data_list.append(About)  # 简介
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        with open("豆瓣电影Top250.txt", 'a', encoding='utf-8') as file:
            for i in range(25):
                if len(result_list[0][i]) == 2:
                    file.write("Chinese name: " + result_list[0][i][0] + '\n')
                    file.write("Other name: " + result_list[0][i][1] + '\n')
                elif len(result_list[0][i]) == 3:
                    file.write("Chinese name: " + result_list[0][i][0] + '\n')
                    file.write("Foreign name: " + result_list[0][i][1] + '\n')
                    file.write("Other name: " + result_list[0][i][2] + '\n')
                file.write("Who: " + result_list[1][i][0] + '\n')
                file.write("When/Where/What: " + result_list[1][i][1] + '\n')
                file.write("Score: " + result_list[2][i] + '\n')
                file.write("About: " + result_list[3][i] + '\n')
                file.write('=' * 50 + '\n')


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    driver = webdriver.Firefox()  # 打开火狐浏览器
    spider = MySpider()
    url = "https://movie.douban.com/top250?start="
    for page in trange(0, 250, 25):
        target_url = url + str(page)
        html_content = spider.get_html_content(target_url)
        if html_content:
            result_list = spider.parse_html(html_content)
            spider.store_data(result_list)
        else:
            print("网页访问失败")
    driver.close()  # 关闭浏览器
