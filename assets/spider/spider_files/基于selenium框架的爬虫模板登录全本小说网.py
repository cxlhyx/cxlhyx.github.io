from selenium import webdriver  # 打开网页爬取源码
from bs4 import BeautifulSoup  # 解析源码
from selenium.webdriver.common.by import By  # 标签定位
import ddddocr  # 验证码识别


class MySpider:
    def __init__(self):
        pass

    # 登录
    def login(self):  # 标签值需要修改
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/a[1]").click()
            driver.find_element(By.NAME, 'username').send_keys('货又星')
            driver.find_element(By.NAME, 'password').send_keys('cxl66218.')
            self.captcha()
            driver.find_element(By.NAME, 'submit').click()
            self.login_check()
        except:
            pass

    # 验证码
    def captcha(self):  # 标签值需要修改
        try:
            image = driver.find_element(By.XPATH, '/html/body/div[2]/div/form/table/tbody/tr[1]/td/table/tbody/tr['
                                                  '3]/td[2]/img')
            data = image.screenshot_as_base64
            text = ocr.classification(data)
            driver.find_element(By.NAME, 'checkcode').send_keys(text)
        except:
            pass

    # 检查登录是否成功
    def login_check(self):
        try:
            if driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]").text == "出现错误！":
                driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[1]/a").click()
                self.login()
            elif driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]").text == "登录成功":
                driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/a").click()
        except:
            pass

    # Step 1: 访问网页并获取响应内容
    def get_html_content(self, url):
        try:
            driver.get(url)
            driver.set_page_load_timeout(10)  # 设置超时限制10s
            self.login()
            html_content = driver.page_source  # 网页内容
            return html_content  # 返回网页内容
        except Exception as e:
            print(f"\n网页请求异常：{e}")
            return None

    # Step 2: 解析网页并提取目标数据
    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')  # 解析 html 数据
        # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中
        data_list = []
        return data_list

    # Step 3: 存储数据到本地或其他持久化存储服务器中
    def store_data(self, result_list):
        # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
        pass


# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    driver = webdriver.Firefox()  # 打开火狐浏览器
    ocr = ddddocr.DdddOcr()  # 解决验证码问题，利用ddddocr库的Ddddocr类
    spider = MySpider()
    target_url = "https://www.quanben.so/"
    html_content = spider.get_html_content(target_url)
    if html_content:
        result_list = spider.parse_html(html_content)
        spider.store_data(result_list)
    else:
        print("网页访问失败")
    driver.close()  # 关闭浏览器
