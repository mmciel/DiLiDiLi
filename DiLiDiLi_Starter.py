"""
    DiLiDiLi(DownLiDownLi)主程序，分配下载任务
    author：mmciel
    time: 2019-9-14 15:38:35
    version: 1.0
    update:
"""

# 欢迎界面
from DiLiDiLi_DownPlan01 import DownAll
from DiLiDiLi_DownPlan02 import DownVAsp
from DynamicProxies import CreateProxies
from MediaHandler import Handler


def welcome():
    print("=================================DiLiDiLi下载工具 V1.0=================================")
    print(">>> author: mmciel")
    print(">>> email:  761998179@qq.com")
    print(">>> github: https://github.com/mmciel/DiLiDiLi")
    print("======================================================================================")

def info(s):
    print(">>> 【Info】"+s)

def error(s):
    print(">>> 【Error】" + s)

def warning(s):
    print(">>> 【Warning】" + s)

def choose(num,s):
    print("["+str(num)+"] " + s)
def prompt(s):
    print(">>> 【提示】" + s)
if __name__ == "__main__":
    welcome()
    while True:
        choose(1,"完整模式（一键下载、无人值守、下载较慢）")
        choose(2,"极速模式（音视频分离下载、下载后需要手动合成、下载较快）")
        choose(3,"更新代理（当下载出现异常，或者首次使用本程序时选择本项）")
        choose(4,"音视频合成（极速模式之后运行）")
        choose(0,"退出程序")
        prompt("请输入命令")
        order = int(input(">>> "))

        if order == 1:
            # 完整模式
            info("进入完整模式...")
            DownAll().run()
        elif order == 2:
            # 极速模式
            info("进入极速模式...")
            DownVAsp().run()
        elif order == 3:
            # 极速模式
            info("正在更新代理...")
            CreateProxies().run()
            info("代理更新成功...")
        elif order == 4:
            # 音视频合成
            info("正在合成...")
            Handler().run()
            info("合成成功...")
        elif order == 0:
            break
        else:
            continue