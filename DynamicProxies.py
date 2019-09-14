"""
    查找免费代理，写入文件供下载使用
    author: mmciel
    time： 2019-9-14 12:29:59
    version: 1.0
    update：
        2019-9-14 12:31:50：采用西刺代理，并筛选出合理的IP
"""
import requests
import DynamicHeaders
from bs4 import BeautifulSoup
import json
# 配置信息
config = {
    # 代理属性 nn:高匿 nt：普通 wn：HTTPS wt：HTTP
    "ip_property": "wt",
    # 请求头
    "user_agent": DynamicHeaders.USER_AGENT_DICT["chrome"],
    # 范围爬取 1 -> 2-1
    "start_page": 1,
    "end_page": 2,
    # 速度筛选
    "screen_speed": 0.3
}


class CreateProxies(object):
    def __init__(self):
        self.session = requests.session()
        self.session.keep_alive = False

        self.base_url = "https://www.xicidaili.com/"
        self.headers = {"User-Agent": config["user_agent"]}

        self.data = []

    def getHtml(self,page_num):
        url = self.base_url + config["ip_property"]+"/"+str(page_num)
        response = self.session.get(url,headers = self.headers)
        # print(response.text)
        return response.text

    def parseHtml(self,html):
        soup = BeautifulSoup(html, 'lxml')
        # 获取每页中101行数据
        table_dom = soup.find_all('tr')
        for item in range(1,len(table_dom)):
            # 获取每行 10 项数据
            row = table_dom[item].select('td')
            # print(row)
            # 处理：
            self.data.append({
                "ip": row[1].string,
                "port": row[2].string,
                "agent": row[5].string,
                # "address": row[3].a.string,
                "link_speed": float(row[6].div["title"][0:-1]),
                "data_speed": float(row[7].div["title"][0:-1]),
                "flag": 1 # 标记是否可用
            })
        # print(self.data)

    def screenData(self):

        for i in range(0,len(self.data)):
            if self.data[i]["link_speed"] > config["screen_speed"] or self.data[i]["data_speed"] > config["screen_speed"]:
                # 筛选掉时间长的IP
                self.data[i]["flag"] = 0
                # print(self.data[i])

    def outputData(self):
        s = "{\"proxies\":["
        for i in range(0, len(self.data)):
            if self.data[i]["flag"] == 1:
                s = s + json.dumps(self.data[i])+","
        s = s[0:-1] + "]}"
        with open("ProxiesData.json", "w") as fp:
            fp.write(s)

    def run(self):
        for i in range(config["start_page"], config["end_page"]):
            self.parseHtml(self.getHtml(i))
        self.screenData()
        self.outputData()
pass



if __name__ == '__main__':
    proxiesInstance = CreateProxies()
    for i in range(config["start_page"],config["end_page"]):
        print("正在获取第"+ str(i) +"页...")
        proxiesInstance.parseHtml(proxiesInstance.getHtml(i))
    proxiesInstance.screenData()
    proxiesInstance.outputData()
    print("输出成功")