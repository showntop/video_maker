# -*- coding:utf8 -*-
import urllib
import json
import os
import requests
import csv
import random
import utils

import config


def read_video_list(filename):
    '''
    读取csv文件第一列为video_id list
    :param filename:
    :return:
    '''
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def download_and_save(download_url, save_path):
    '''
    利用http download_url下载视频
    :param download_url:
    :param save_path:
    :return:
    '''
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"
        }
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(save_path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(save_path)
            res = requests.get(download_url, stream=True, headers=headers)
            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(save_path) and os.path.getsize(save_path) >= content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(save_path, 'ab') as file:
                file.write(res.content)
                file.flush()
                # print('download video %s，file size : %d  total size:%d' % (download_url, os.path.getsize(save_path), content_length))
    except Exception as e:
        print(e)


def get_video_url(video_id):
    '''
    利用video_id获取视频url
    :param video_id:
    :return:
    '''
    try:
        url = 'http://p-vp.autohome.com.cn/api/spi?mid=%s' % (video_id)
        response = urllib.request.urlopen(url)
        result_dict = json.loads(response.read())
        copies = result_dict['result'][
            'mediainfos'][0]['copies']

        video_url = copies[len(copies) - 1]['playurl']
    except:
        video_url = None
    return video_url


def download_videos(video_list):
    video_files = []
    for vid in video_list:
        video_url = get_video_url(vid)
        if video_url is None:
            print(vid, ' cannot get download url')
            continue
        filename_path = os.path.join(config.VIDEO_PATH, vid + '.mp4')
        # config.VIDEO_PAHT + vid + '/' + vid '.mp4'
        if os.path.exists(filename_path) is False:
            download_and_save(video_url, filename_path)
        else:
            pass
        video_files.append(filename_path)
        print('download video %s，file size : %d' %
              (vid, os.path.getsize(filename_path)))
    return video_files

if __name__ == '__main__':
    video_list = read_video_list(config.VIDEO_LIST)
    download_videos(video_list)
