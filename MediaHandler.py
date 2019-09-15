"""
    音视频合成
    author ： mmciel
    time ： 2019-9-15 20:50:06
    version: 1.0
    update:

"""
from moviepy.editor import *

class Handler(object):
    def __init__(self):
        self.path3 = ".\\audio_down"
        self.path4 = ".\\video_down"
        self.path = ".\\synthetic_success"
        self.mp3_list = []
        self.mp4_list = []
        self.length = 0

    def initDir(self):
        temp_list = []
        for root, dirs, files in os.walk(self.path3):
            temp_list = files
        self.length = len(temp_list)
        for i in range(0, self.length):
            self.mp3_list.append(temp_list[i])
            self.mp4_list.append(temp_list[i][:-4]+".mp4")
    def active(self):
        for i in range(0, self.length):
            audioclip = AudioFileClip(self.path3+"\\"+self.mp3_list[i])
            videoclip = VideoFileClip(self.path4+"\\"+self.mp4_list[i])
            dy_data = videoclip.set_audio(audioclip)
            dy_data.write_videofile(self.path+"\\"+self.mp4_list[i])
            os.remove(self.path3+"\\"+self.mp3_list[i])
            os.remove(self.path4+"\\"+self.mp4_list[i])
    def run(self):
        self.initDir()
        self.active()

if __name__ == "__main__":
    Handler().run()