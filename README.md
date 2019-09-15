# DiLiDiLi（DownBiLiDownBili）

# 哔哩哔哩视频下载器

## 发布

最新更新时间：2019年9月15日20:57:18

最新测试时间：2019年9月15日20:57:32

## 使用说明

启动`DiLiDiLi_Starter.py`文件

## 测试环境

- window 10 x64
- python 3.6

## 文件说明

| 文件                   | 说明               |
| ---------------------- | ------------------ |
| DiLiDiLi_Starter.py    | 启动主程序         |
| DynamicHeaders.py      | 一些常用请求头     |
| DynamicProxies.py      | 动态代理相关       |
| MediaHandler.py        | 视频合成相关       |
| DiLiDiLi_DownPlan02.py | 音视频分离下载方案 |
| DiLiDiLi_DownPlan01.py | 完全下载           |
| video_down             | 纯视频文件夹       |
| audio_down             | 纯音频文件夹       |
| synthetic_success      | 合成成功           |
| download               | 完全下载文件夹     |
| ProxiesData.json       | 动态代理的数据     |

## 关于作者

- author：mmciel
- QQ：761998179

## 声明

本程序仅用于个人测试，只是恰巧选中了B站，若有其他用途与我啥关系都没有啊！

# 开发思路

## 视频数据初探
### 视频格式

```js
flv
m4s

数据源
2018-08-28之前：flv
2018-08-28之后：m4s
```

 ### 视频数据接口01

```javascript
浏览器数据接口：
样例1
url：
https://cn-hnjz-cu-v-03.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30280.m4s?expires=1568435700&platform=pc&ssig=JH1dsIJq85jtHBct_qA-lw&oi=3061251074&trid=c6d4c238731349c8a3b3ac66c58d291au&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=293301385
param：
expires: 1568435700
platform: pc
ssig: JH1dsIJq85jtHBct_qA-lw
oi: 3061251074
trid: c6d4c238731349c8a3b3ac66c58d291au
nfc: 1
nfb: maPYqpoel5MI3qOUX6YpRA==
mid: 293301385
样例2
https://cn-hnjz-cu-v-01.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30064.m4s?expires=1568435700&platform=pc&ssig=1EUOpEA1QKHUQcpOz6W1pw&oi=3061251074&trid=c6d4c238731349c8a3b3ac66c58d291au&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=293301385
param：
expires: 1568435700
platform: pc
ssig: 1EUOpEA1QKHUQcpOz6W1pw
oi: 3061251074
trid: c6d4c238731349c8a3b3ac66c58d291au
nfc: 1
nfb: maPYqpoel5MI3qOUX6YpRA==
mid: 293301385
```

此接口参数过多，暂停分析

### 视频接口数据02

`https://api.bilibili.com/`

重要域名，很多数据都来自这个api，所以尝试从这个api中找到上述的一些参数

然后找到两个：

```javascript
https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp //返回视频剧集
https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&type=&otype=json //这个接口从github上别人的源码中找到的，我没抓到这个包，猜测已经是废弃的接口（后来利用他下载视频时速度很慢，印证了我的猜测） 
```



### 视频接口数据03

从页面中拿到的数据。

这些数据流可以生成视频+音频，下载到本地后需要后期合成。

```javascript
window.__playinfo__={"code":0,"message":"0","ttl":1,"data":{"from":"local","result":"suee","message":"","quality":32,"format":"flv480","timelength":1120640,"accept_format":"flv720,flv480,flv360","accept_description":["高清 720P","清晰 480P","流畅 360P"],"accept_quality":[64,32,16],"video_codecid":7,"seek_param":"start","seek_type":"offset","dash":{"duration":1121,"minBufferTime":1.5,"min_buffer_time":1.5,"video":[{"id":64,"baseUrl":"http://cn-hnjz-cu-v-01.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30064.m4s?expires=1568440200&platform=pc&ssig=MEWTqOT2d0LJtIWe8gcayg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-hnjz-cu-v-01.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30064.m4s?expires=1568440200&platform=pc&ssig=MEWTqOT2d0LJtIWe8gcayg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":1408488,"mimeType":"video/mp4","mime_type":"video/mp4","codecs":"avc1.64001F","width":1280,"height":720,"frameRate":"25","frame_rate":"25","sar":"1:1","startWithSap":1,"start_with_sap":1,"SegmentBase":{"Initialization":"0-991","indexRange":"992-3711"},"segment_base":{"initialization":"0-991","index_range":"992-3711"},"codecid":7},{"id":64,"baseUrl":"http://cn-sxty2-cu-v-06.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30066.m4s?expires=1568440200&platform=pc&ssig=C_m43MNWp9sL63447C6EOw&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-sxty2-cu-v-06.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30066.m4s?expires=1568440200&platform=pc&ssig=C_m43MNWp9sL63447C6EOw&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":988078,"mimeType":"video/mp4","mime_type":"video/mp4","codecs":"hev1.1.6.L120.90","width":1280,"height":720,"frameRate":"25","frame_rate":"25","sar":"1:1","startWithSap":1,"start_with_sap":1,"SegmentBase":{"Initialization":"0-1171","indexRange":"1172-3891"},"segment_base":{"initialization":"0-1171","index_range":"1172-3891"},"codecid":12},{"id":32,"baseUrl":"http://cn-hbcd2-cu-v-16.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30032.m4s?expires=1568440200&platform=pc&ssig=WFuX0zgEtC8HdQ45pv65Aw&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-hbcd2-cu-v-16.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30032.m4s?expires=1568440200&platform=pc&ssig=WFuX0zgEtC8HdQ45pv65Aw&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":876413,"mimeType":"video/mp4","mime_type":"video/mp4","codecs":"avc1.64001E","width":852,"height":480,"frameRate":"25","frame_rate":"25","sar":"640:639","startWithSap":1,"start_with_sap":1,"SegmentBase":{"Initialization":"0-995","indexRange":"996-3715"},"segment_base":{"initialization":"0-995","index_range":"996-3715"},"codecid":7},{"id":32,"baseUrl":"http://cn-hnjz-cu-v-04.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30033.m4s?expires=1568440200&platform=pc&ssig=NPSvzlbYrLirAiMTclAVKA&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-hnjz-cu-v-04.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30033.m4s?expires=1568440200&platform=pc&ssig=NPSvzlbYrLirAiMTclAVKA&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":615530,"mimeType":"video/mp4","mime_type":"video/mp4","codecs":"hev1.1.6.L120.90","width":852,"height":480,"frameRate":"25","frame_rate":"25","sar":"640:639","startWithSap":1,"start_with_sap":1,"SegmentBase":{"Initialization":"0-1174","indexRange":"1175-3894"},"segment_base":{"initialization":"0-1174","index_range":"1175-3894"},"codecid":12},{"id":16,"baseUrl":"http://cn-hnjz-cu-v-03.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30015.m4s?expires=1568440200&platform=pc&ssig=zVWQlBKq36qHDMYJwFGcAg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-hnjz-cu-v-03.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30015.m4s?expires=1568440200&platform=pc&ssig=zVWQlBKq36qHDMYJwFGcAg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":390576,"mimeType":"video/mp4","mime_type":"video/mp4","codecs":"avc1.64001E","width":640,"height":360,"frameRate":"25","frame_rate":"25","sar":"1:1","startWithSap":1,"start_with_sap":1,"SegmentBase":{"Initialization":"0-991","indexRange":"992-3711"},"segment_base":{"initialization":"0-991","index_range":"992-3711"},"codecid":7},{"id":16,"baseUrl":"http://cn-sxty2-cu-v-04.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30011.m4s?expires=1568440200&platform=pc&ssig=Jc6khnq9inO6Qu-lQzTwyg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-sxty2-cu-v-04.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30011.m4s?expires=1568440200&platform=pc&ssig=Jc6khnq9inO6Qu-lQzTwyg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":275801,"mimeType":"video/mp4","mime_type":"video/mp4","codecs":"hev1.1.6.L120.90","width":640,"height":360,"frameRate":"25","frame_rate":"25","sar":"1:1","startWithSap":1,"start_with_sap":1,"SegmentBase":{"Initialization":"0-1171","indexRange":"1172-3891"},"segment_base":{"initialization":"0-1171","index_range":"1172-3891"},"codecid":12}],"audio":[{"id":30280,"baseUrl":"http://cn-hnjz-cu-v-03.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30280.m4s?expires=1568440200&platform=pc&ssig=JBmihG3W3bIGikIYmgPJYQ&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-hnjz-cu-v-03.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30280.m4s?expires=1568440200&platform=pc&ssig=JBmihG3W3bIGikIYmgPJYQ&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":130005,"mimeType":"audio/mp4","mime_type":"audio/mp4","codecs":"mp4a.40.2","width":0,"height":0,"frameRate":"","frame_rate":"","sar":"","startWithSap":0,"start_with_sap":0,"SegmentBase":{"Initialization":"0-907","indexRange":"908-3639"},"segment_base":{"initialization":"0-907","index_range":"908-3639"},"codecid":0},{"id":30216,"baseUrl":"http://cn-sxty2-cu-v-05.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30216.m4s?expires=1568440200&platform=pc&ssig=9dPIG9CGSgKQCpQCKK7aqg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","base_url":"http://cn-sxty2-cu-v-05.acgvideo.com/upgcxcode/48/18/109631848/109631848-1-30216.m4s?expires=1568440200&platform=pc&ssig=9dPIG9CGSgKQCpQCKK7aqg&oi=3061251074&trid=2b14327a272f492a9107c7f0ffba621du&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0","backupUrl":null,"backup_url":null,"bandwidth":67094,"mimeType":"audio/mp4","mime_type":"audio/mp4","codecs":"mp4a.40.2","width":0,"height":0,"frameRate":"","frame_rate":"","sar":"","startWithSap":0,"start_with_sap":0,"SegmentBase":{"Initialization":"0-907","indexRange":"908-3639"},"segment_base":{"initialization":"0-907","index_range":"908-3639"},"codecid":0}]}},"session":"7d84f2da4084b6183a93512e6cdbd35a","videoFrame":{}}
```

### 视频数据接口06

```javascript
'https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&type=&otype=json'
avid 
cid
qn 清晰度
```

## 下载思路

### 思路一

利用`api.bilibili.com/x/player`下载完整文件

### 思路二

利用流文件下载video+audio，然后本地手动合成



## 注意事项

### SSL Error

- session持久化
- 变更请求头
- 开启网络代理
