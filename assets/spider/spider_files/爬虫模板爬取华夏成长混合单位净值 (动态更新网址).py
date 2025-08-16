import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import pandas as pd

# Step 1: 访问网页并获取响应内容
def get_html_content(url):
    headers = {
        'User-Agent': UserAgent().random
    } # 请求头，爬虫程序通过加上请求头伪装成浏览器
    data={'name':'huoyouxing'}
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # 判断返回的Response类型状态是不是200
        response.encoding = response.apparent_encoding  # 从内容中分析出的响应内容编码
        html_content = response.text # 网页内容
        return html_content # 返回网页内容
    except Exception as e:
        print(f"网络请求异常：{e}")
        return None

# Step 2: 解析网页并提取目标数据
def parse_html(html_content):
    # TODO：根据需求编写解析代码，并将结果保存到合适的数据结构中
    data_list=json.loads(html_content[16:])
    return data_list

# Step 3: 存储数据到本地或其他持久化存储服务器中
def store_data(result_list):
    # TODO：编写存储代码，将数据结果保存到本地或其他服务器中
    with open('华夏成长混合单位净值.csv','w') as file:
        data = pd.DataFrame(result_list)
        data.columns=('日期','单位净值')
        print(data)
        data.to_csv(file,line_terminator='\n',index=False)
    pass

# Step 4: 控制流程，调用上述函数完成数据抓取任务
if __name__ == '__main__':
    target_url = "https://fund.10jqka.com.cn/000001/json/jsondwjz.json"
    html_content = get_html_content(target_url)
    if html_content:
        result_list = parse_html(html_content)
        store_data(result_list)
    else:
        print("网页访问失败")