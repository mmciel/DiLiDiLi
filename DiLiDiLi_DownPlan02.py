"""
    视频音频分离下载
    author:mmciel
    time : 2019-9-15 15:15:50
    version:1.0
    update:

"""
import json
import os
import random
import re
import time

from pyquery import PyQuery as pq
import requests

import DynamicHeaders


class DownVAsp(object):
    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.session = requests.session()
        self.session.keep_alive = False

        self.proxies_list = []

        self.simple_headers = {
            'host': 'api.bilibili.com',
            'User-Agent': DynamicHeaders.USER_AGENT_DICT["apple"]
        }
        self.html_headers = {
            'User-Agent': DynamicHeaders.USER_AGENT_DICT["apple"],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }
        self.down_headers = {
            # 'host': '',
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av',
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

        self.mp3_url=""
        self.mp4_url=""
        self.all_url=""



    def run(self):
        # 随机加载代理数据
        self.lodingProxies()
        # 代理写入session
        self.chooseProxies()
        # 采集数据
        model = self.inputParm()

        if model == 1:
            print(1)
        elif model == 2:
            self.info("正在获取视频队列信息，请稍后...")
            self.getPagelist(self.pagelist_url.format(self.aid))
            self.down_headers["Referer"] = self.down_headers["Referer"] + self.aid
            self.info("正在获取清晰度信息，请稍后...")
            self.inputPn()
            self.info("正在生成下载链接...")
            self.listActive()
            self.info("下载完成")

    def listActive(self):
        for i in range(0, int(self.max_len)):
            self.cid = self.pagelist_json[i]["cid"]
            self.title = self.pagelist_json[i]["part"]
            self.info("开始下载：" + self.title)
            temp_url = "https://www.bilibili.com/video/av"+self.aid+"?p="+str(i+1)
            status = self.pageParsing(temp_url)
            if status == 1:
                self.download("synthetic_success",self.all_url, "mp4")
            elif status == 2 :
                self.download("audio_down",self.mp3_url, "mp3")
                self.download("video_down",self.mp4_url, "mp4")

    def download(self,temp_path,temp_url,suffix):
        filename = self.title + "."+suffix
        path = os.getcwd() + '\\' + temp_path  + '\\'
        if not os.path.exists(path):
            os.mkdir(path)
        start_time = time.time()
        size = 0
        response = self.session.get(temp_url, headers=self.down_headers, stream=True, verify=False)
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))
            with open(path + filename, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + '[下载进度]:%s%.2f%%' % (
                    '>' * int(size * 50 / content_size), float(size / content_size * 100)), end='')
        else:
            print('下载出错')
        end_time = time.time()
        print()
        self.info("用时%.2f秒" % (end_time - start_time))

    def pageParsing(self, url):
        temp_html = self.session.get(url, headers=self.html_headers, verify=False).text
        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        result = re.findall(pattern, temp_html)[0]
        # print(result)
        temp = json.loads(result)["data"]
    #     检查视频属性
        if "durl" in temp.keys():
            self.all_url = temp["durl"][0]["url"]
            return 1
        else :
            temp = temp["dash"]
            self.mp3_url = temp["audio"][0]['baseUrl']
            temp_video_list = temp["video"]
            for i in range(0, len(temp_video_list)):
                if temp_video_list[i]["id"] == self.pn:
                    self.mp4_url = temp_video_list[i]["baseUrl"]
                    # print(temp_video_list[i]["baseUrl"])
                    break
            return 2


    def getPagelist(self, url):
        # print(self.session.get(url, headers=self.simple_headers,verify=False).text)
        self.pagelist_json = self.session.get(url, headers=self.simple_headers, verify=False).json()["data"]
        self.cid = self.pagelist_json[0]["cid"]
        self.title = self.pagelist_json[0]["part"]
        self.max_len = len(self.pagelist_json)

    def inputPn(self):
        data = self.session.get(self.video_url.format(self.aid, self.cid, 0), headers=self.simple_headers,verify=False).json()["data"]
        self.accept_quality = data["accept_quality"]
        self.accept_description = data["accept_description"]
        self.prompt("请输入清晰度:")
        for i in range(0, len(self.accept_quality)):
            self.choose(self.accept_quality[i], self.accept_description[i])
        self.pn = int(input(">>> "))

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


    def lodingProxies(self):
        """加载文件"""
        file = open("ProxiesData.json", "r")
        self.proxies_list = json.load(file)["proxies"]

    def chooseProxies(self):
        """生成代理并写入session"""
        index = random.randint(0, len(self.proxies_list))
        item = self.proxies_list[index]
        # self.session.proxies = {item["agent"]: item["ip"]+":"+item["port"]}
        self.info("代理地址：" + item["agent"] + "://" + item["ip"] + ":" + item["port"])

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
    DownVAsp().run()

