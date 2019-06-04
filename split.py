# coding:utf8

import os
import cv2
from whitelist import whitelist

# 每N秒提取一帧


def extract_frames(video_file, output_path, n=1):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    else:
        return output_path
    if not output_path.endswith('/'):
        output_path = output_path + '/'

    # ffmpeg_cmd = "ffmpeg  -i  " + video_file + " -r " + \
    #     str(n) + " -f image2 " + output_path + "%d.jpg"
    ffmpeg_cmd = "ffmpeg  -i  " + video_file + \
        " -f image2 " + output_path + "%d.jpg"

    os.system(ffmpeg_cmd)

    # 截取每张图片的有效区域
    for image_file_name in os.listdir(output_path):
        image_file_path = output_path + image_file_name
        image = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
        height, width, channels = image.shape
        rect = [0, int(height / 3) * 2, int(width), int(height / 3)]
        image_ROI = image[rect[1]:  rect[1] +
                          rect[3], rect[0]: rect[0] + rect[2]]
        cv2.imwrite(image_file_path, image_ROI)
    return output_path


def main():
    data_path = './data'
    frames_path = data_path + '/frames/'
    videos_path = data_path + '/videos/'
    if not os.path.exists(frames_path):
        os.mkdir(frames_path)
    for filename in os.listdir(videos_path):
        if filename not in whitelist('./data/whitelist.txt'):
            continue
        if not os.path.exists(frames_path + filename + "/"):
            os.mkdir(frames_path + filename + "/")
        extract_frames(videos_path + filename, frames_path + filename + "/", 1)

if __name__ == '__main__':
    main()
