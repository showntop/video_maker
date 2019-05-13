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
		frames_path = split.extract_frames(file, os.path.join(config.FRAME_PATH, vid) )
		caption_path = recognize.process(frames_path, os.path.join(config.OUTPUT_PATH, vid))
		subject_path = classify.process(caption_path,  "%s/subjects.txt" % (os.path.join(config.OUTPUT_PATH, vid)))
		reap.process(subject_path, file, os.path.join(config.OUTPUT_PATH, vid), '')

if __name__ == '__main__':
	print('main')
	main(['061C69650C43A779'])
