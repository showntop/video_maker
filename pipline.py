#!/usr/bin/env python
# import sys

# print('__main__')
# print('__main__.__name__', __name__)
# print('__main__.__package__', __package__)

# print('sys.path', sys.path)

import os
import config
import download
import split
import recognize
import classify
import reap


def main(vids):
    if not os.path.exists(config.OUTPUT_PATH):
        os.mkdir(config.OUTPUT_PATH)
    if not os.path.exists(config.FRAME_PATH):
        os.mkdir(config.FRAME_PATH)

    video_files = download.download_videos(vids)
    for (vid, file) in zip(vids, video_files):
        if not os.path.exists(os.path.join(config.OUTPUT_PATH, vid)):
            os.mkdir(os.path.join(config.OUTPUT_PATH, vid))
        frames_path = split.extract_frames(
            file, os.path.join(config.FRAME_PATH, vid))
        caption_path = recognize.process(frames_path, os.path.join(
            config.OUTPUT_PATH, vid, 'captions.txt'))
        subject_path = classify.process(
            caption_path,  "%s/subjects.txt" % (os.path.join(config.OUTPUT_PATH, vid)))
        reap.process(subject_path, file, os.path.join(
            config.OUTPUT_PATH, vid), '')


def videolist(filename):
    listset = set([])
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        listset.add(line.strip())
    return listset

if __name__ == '__main__':
    print('main')
    # main(videolist('./data/video_list.txt'))
    main(['D0D8A516FF2B215E'])
