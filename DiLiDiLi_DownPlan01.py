"""
    完整下载
    author : mmciel
    time : 2019-9-14 16:34:21
    version : 1.0
    update:

"""
import json
import os
import random
import re
import time

import requests
import DynamicHeaders

class DownAll(object):
    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.session = requests.session()
        self.session.keep_alive = False

        self.proxies_list = []

        self.simple_headers = {
            'host': 'api.bilibili.com',
            'User-Agent': DynamicHeaders.USER_AGENT_DICT["apple"]
        }
        self.down_headers = {
            'host': '',
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/ac{}',
            'User-Agent': DynamicHeaders.USER_AGENT_DICT["apple"]
        }

        self.pagelist_url = 'https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp'
        self.video_url = 'https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&type=&otype=json'

        # 本视频数据
        self.aid = ""
        self.pn = ""
        self.cid = ""
        self.title = ""
        self.url = ""
        self.size = ""
        self.length = ""


        # 视频质量文字
        self.accept_description = []
        # 视频质量pn
        self.accept_quality = []


        # 视频列表
        self.pagelist_json = []
        self.max_len = ""

    def getPagelist(self, url):
        # print(self.session.get(url, headers=self.simple_headers,verify=False).text)
        self.pagelist_json = self.session.get(url, headers=self.simple_headers, verify=False).json()["data"]
        self.cid = self.pagelist_json[0]["cid"]
        self.title = self.pagelist_json[0]["part"]
        self.max_len = len(self.pagelist_json)

    def getVideo(self, url):
        print(self.session.get(url, headers=self.simple_headers, verify=False))
        durl = self.session.get(url, headers=self.simple_headers, verify=False).json()["data"]["durl"][0]
        self.url = durl["url"]
        self.size = durl["size"]
        self.length = durl["length"]
        self.down_headers['host'] = self.url.split('/')[2]

    def lodingProxies(self):
        """加载文件"""
        file = open("ProxiesData.json", "r")
        self.proxies_list = json.load(file)["proxies"]

    def chooseProxies(self):
        """生成代理并写入session"""
        index = random.randint(0, len(self.proxies_list))
        item = self.proxies_list[index]
        # self.session.proxies = {item["agent"]: item["ip"]+":"+item["port"]}
        self.info("代理地址："+item["agent"]+":\\\\" + item["ip"]+":"+item["port"])

    def inputParm(self):
        self.prompt("请输入需要下载视频的AV号：(av63120995)")
        av = input(">>> ")
        self.aid = re.search(r"[0-9]{8}", av).group()
        self.info("获得aid："+self.aid)
        self.prompt("请选择下载方案：")
        self.choose(1, "单集下载")
        self.choose(2, "全集下载")
        model = int(input(">>> "))
        self.info("选择成功")
        return model
    def inputPn(self):
        data = self.session.get(self.video_url.format(self.aid, self.cid, 0), headers=self.simple_headers, verify=False).json()["data"]
        self.accept_quality = data["accept_quality"]
        self.accept_description = data["accept_description"]
        self.prompt("请输入清晰度:")
        for i in range(0, len(self.accept_quality)):
            self.choose(self.accept_quality[i], self.accept_description[i])
        self.pn = int(input(">>> "))

    def download(self):
        filename = self.title + ".flv"
        path = os.getcwd() + '\\' + "download"+'\\'
        if not os.path.exists(path):
            os.mkdir(path)
        start_time = time.time()
        size = 0
        response = self.session.get(self.url, headers=self.down_headers, stream=True, verify=False)
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))
            with open(path+filename, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + '[下载进度]:%s%.2f%%' % ('>'*int(size*50/content_size),float(size / content_size * 100)), end='')
        else:
            print('下载出错')
        end_time = time.time()
        print()
        self.info("用时%.2f秒" % (end_time-start_time))

    def listActive(self):
        for i in range(0, int(self.max_len)):
            self.cid = self.pagelist_json[i]["cid"]
            self.title = self.pagelist_json[i]["part"]
            self.info("开始下载：" + self.title)
            self.getVideo(self.video_url.format(self.aid, self.cid, self.pn))
            self.download()
            self.info("完成下载：" + self.title)

    def run(self):
        # 随机加载代理数据
        self.lodingProxies()

        # 代理写入session
        self.chooseProxies()
        # 采集数据
        model = self.inputParm()

        if model == 1:
            print("error")
        elif model == 2:
            self.info("正在获取视频队列信息，请稍后...")
            self.getPagelist(self.pagelist_url.format(self.aid))
            self.info("正在获取清晰度信息，请稍后...")
            self.inputPn()
            self.info("正在生成下载链接...")
            self.listActive()
            self.info("下载完成")

    def info(self, s):
        print(">>> 【Info】" + s)

    def error(self, s):
        print(">>> 【Error】" + s)

    def warning(self, s):
        print(">>> 【Warning】" + s)

    def choose(self, num, s):
        print("[" + str(num) + "] " + s)

    def prompt(self, s):
        print(">>> 【提示】" + s)

if __name__ == "__main__":
    DownAll().run()