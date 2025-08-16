from multiprocessing import Pool
import tqdm
from selenium import webdriver  # 打开网页爬取源码
from bs4 import BeautifulSoup  # 解析源码


class MySpider():
    def __init__(self):
        option = webdriver.FirefoxOptions()
        option.add_argument("--headless")
        self.driver = webdriver.Firefox(options=option)  # 打开火狐浏览器

    def __del__(self):
        self.driver.close()

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, url):
        try:
            self.driver.get(url)
            self.driver.set_page_load_timeout(10)  # 设置超时限制10s
            html_content = self.driver.page_source  # 网页内容
            return html_content  # 返回网页内容
        except Exception as e:
            print(f"网页请求异常：{e}")
            return None

    # Step 2: 解析网页并提取目标数据
    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')  # 解析 html 数据
        # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中
        data_list = [soup.find('h1').text,
                     soup.find('div', {'id': 'content', 'name': 'content'}).text.replace(" ", "\n")]
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        with open('元尊/' + result_list[0] + ".txt", 'w', encoding='utf-8') as file:
            file.write(result_list[0] + '\n' + result_list[1])
        pass


def Main(target_url):
    spider = MySpider()
    html_content = spider.get_html_content(target_url)
    if html_content:
        result_list = spider.parse_html(html_content)
        spider.store_data(result_list)
    else:
        print("网页访问失败")


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    url = "https://www.quanben.so/86_86296/"
    with open("元尊/元尊.txt") as file:
        target_url_list = [url + i.replace("\n", '') for i in file.readlines()]
    process = 10
    pool = Pool(process)
    pool.map(Main, tqdm.tqdm(target_url_list))
