import time

import requests
import json
from lxml import etree
import ffmpeg
import os
from moviepy.editor import *

# 防止因https证书问题报错
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'cookie' : "buvid3=128016E0-988D-7EF4-D9AF-1AE2B0C178B860857infoc; b_nut=1681112060; CURRENT_FNVAL=4048; CURRENT_PID=20a6a870-d772-11ed-b703-475de4ede2e9; _uuid=D9A4F1FC-B34B-2F16-B391-4A6448F3618369442infoc; buvid_fp=6ecc131ba01162b1e86f3e1b3fb37384; buvid4=1D03A6E8-D149-FF1E-64A7-80724CEB5EBF69884-023041015-zwH65RBAGsqP3IG5CjDVKg%3D%3D; rpdid=|(umu)~|YuYJ0J'uY)uuuk|)u; DedeUserID=38964494; DedeUserID__ckMd5=39034d30f6a8526f; SESSDATA=8430c9e1%2C1696664342%2Cbbf07%2A42; bili_jct=405c6ca98d4733f5b95d381ac146b4e4; CURRENT_QUALITY=80; PVID=1; i-wanna-go-back=-1; b_ut=5; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; nostalgia_conf=-1; b_lsid=BD98DF610_187EFE156B2; sid=61h8r74r; innersign=0; browser_resolution=668-569"
}


def GetBiliVideo(homeurl, num, session=requests.session()):
    res = session.get(url=homeurl, headers=headers, verify=False)
    html = etree.HTML(res.content)
    videoinforms = str(html.xpath('//head/script[3]/text()')[0])[20:]
    videojson = json.loads(videoinforms)

    # 获取详情信息列表
    # listinform = str(html.xpath('//head/script[4]/text()')[0])
    listinform = str(
        html.xpath('//head/script[4]/text()')[0].encode('utf8').decode('utf8'))[25:-122]
    listjson = json.loads(listinform)

    # 获取视频链接和音频链接
    try:
        # 2018年以后的b站视频，音频和视频分离
        VideoURL = videojson['data']['dash']['video'][0]['baseUrl']
        AudioURl = videojson['data']['dash']['audio'][0]['baseUrl']
        flag = 0

    except Exception:
        # 2018年以前的b站视频，格式为flv
        VideoURL = videojson['data']['durl'][0]['url']
        flag = 1

    # 获取文件夹的名称
    dirname = str(html.xpath("//h1/@title")[0].encode('utf8').decode('utf-8'))
    if not os.path.exists(dirname):
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(dirname)
        print('目录文件创建成功!')

    # 获取每一集的名称
    name = listjson['videoData']['pages'][num]['part']
    print(name)

    # 下载视频和音频
    print('正在下载 "' + name + '" 的视频····')
    BiliBiliDownload(homeurl=homeurl, url=VideoURL, name=os.getcwd() + '/' + dirname + '/' + name + '_Video.mp4',
                     session=session)
    if flag == 0:
        print('正在下载 "' + name + '" 的音频····')
        BiliBiliDownload(homeurl=homeurl, url=AudioURl, name=os.getcwd() + '/' + dirname + '/' + name + '_Audio.mp3',
                         session=session)
        print('正在组合 "' + name + '" 的视频和音频····')
        CombineVideoAudio(dirname+'/'+name + '_Video.mp4.mp4', dirname+'/'+name + '_Audio.mp3.mp4', dirname+'/'+name + '_output.mp4')
    print(' "' + name + '" 下载完成！')


def BiliBiliDownload(homeurl, url, name, session=requests.session()):
    headers.update({'Referer': homeurl})
    session.options(url=url, headers=headers, verify=False)
    # 每次下载1M的数据
    begin = 0
    end = 1024 * 512 - 1
    flag = 0
    while True:
        headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
        res = session.get(url=url, headers=headers, verify=False)
        if res.status_code != 416:
            begin = end + 1
            end = end + 1024 * 512
        else:
            headers.update({'Range': str(end + 1) + '-'})
            res = session.get(url=url, headers=headers, verify=False)
            flag = 1

        with open(name + '.mp4', 'ab') as fp:
            fp.write(res.content)
            fp.flush()
            # data=data+res.content
            if flag == 1:
                fp.close()
                break


def CombineVideoAudio(videopath, audiopath, outpath):
    input_video = ffmpeg.input(videopath)
    input_audio = ffmpeg.input(audiopath)
    video = VideoFileClip(videopath)
    audio = AudioFileClip(audiopath)
    video_with_audio = video.set_audio(audio)
    video_with_audio.write_videofile(outpath)
    video.close()
    audio.close()
    # os.remove(videopath)
    # os.remove(audiopath)




if __name__ == '__main__':
    av =  'BV1ym4y117u4'
    #BV1iq4y1R7sd
    #BV1ym4y117u4
    #av = input('请输入视频号：')
    url = 'https://www.bilibili.com/video/' + av

# 视频选集
range_start = 1#input('从第几集开始？')
range_end = 1#input('到第几集结束？')
if int(range_start) <= int(range_end):
    for i in range(int(range_start), int(range_end) + 1):
        GetBiliVideo(url + '?p=' + str(i), i - 1)
else:
    print('选集不合法！')
