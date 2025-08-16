import re  # 正则表达式
from multiprocessing import Pool  # 多线程
from selenium import webdriver  # 打开网页爬取源码
from bs4 import BeautifulSoup  # 解析源码
from selenium.webdriver.common.by import By  # 标签定位
from datetime import datetime  # 记录日志时间


class MySpider:
    def __init__(self):
        option = webdriver.FirefoxOptions()
        option.add_argument("--headless")
        profile = webdriver.FirefoxProfile(
            r"C:\Users\12977\AppData\Roaming\Mozilla\Firefox\Profiles\ligb9uiu.default-release"
        )
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("useAutomationExtension", False)
        profile.update_preferences()
        option._profile = profile
        self.driver = webdriver.Firefox(options=option)  # 打开火狐浏览器

    def __del__(self):
        self.driver.close()

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, url):
        try:
            self.driver.get(url)  # 访问论文查找网页
            self.driver.set_page_load_timeout(10)  # 设置超时限制10s
            paper = self.driver.find_element(
                By.XPATH, "/html/body/div/div[10]/div[2]/div[3]/div[2]/div[1]"
            )  # 解析论文查找结果
            paper_id = paper.get_attribute("data-cid")  # 获得论文id
            paper_p = paper.get_attribute("data-rp")  # 获得论文p
            # 格式化论文引用链接
            data_u = f"https://scholar.google.com/scholar?q=info:{paper_id}:scholar.google.com/&output=cite&scirp={paper_p}&hl=zh-CN"
            self.driver.get(data_u)  # 访问论文引用页
            # 点击BibTex进入最终网页
            self.driver.find_element(By.XPATH, "/html/body/div[2]/a[1]").click()
            html_content = self.driver.page_source  # 最终网页内容
            return html_content  # 返回最终网页内容
        except Exception as e:
            with open("output\error_papers.log", "a", encoding="utf-8") as file:
                file.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nFailed to retrieval paper.\n{url[62:-6].replace('+', ' ')}\n{url}\n{e}\n"
                )
            return None

    # Step 2: 解析网页并提取目标数据
    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")  # 解析 html 数据
        # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中 √
        data_list = [soup.pre.string + "\n"]
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中 √
        # 将得到的BibTex结果写入references.bib文件
        with open(r"output\references.bib", "a", encoding="utf-8") as file:
            file.writelines(result_list)


def main(target_url):
    spider = MySpider()  # 爬虫
    html_content = spider.get_html_content(target_url)  # 请求网页
    if html_content:  # 请求结果存在
        result_list = spider.parse_html(html_content)  # 解析最终请求结果
        spider.store_data(result_list)  # 存储请求结果


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == "__main__":
    base_url = "https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q={paper}&btnG="  # 谷歌学术查找链接
    # 格式化论文的谷歌学术查找链接
    with open("output\papers.txt", "r", encoding="utf-8") as file:
        papers = [re.sub(r"\s+", "+", line.strip()) for line in file]
        target_url_list = [base_url.format(paper=paper) for paper in papers]
        # print("\n".join(target_url_list))

    process = 2  # 线程数量
    pool = Pool(process)  # 线程池
    pool.map(main, target_url_list)  # 多线程运行
