# coding=utf-8
import os
from classifier.build import build
from tokenizer import init
from utils.text_similarity import tf_similarity
from summary.extract import extract_summary
from keypoint.extract import segment

def preprocess(subjects_file):
	seconds_list = []
	sentences_list = []
	subjects_list = []
	subjects_file = open(subjects_file, mode='r', encoding='utf-8')
	for line in subjects_file.readlines():
		arr = line.split("\t")
		if len(arr) < 3:
			continue
		seconds_list.append(int(arr[0].strip()))
		sentences_list.append((arr[1].strip()))
		subjects_list.append(arr[2].strip())
	subjects_file.close()
	return seconds_list, sentences_list, subjects_list


def segment2(timelines):
	segments = []
	subject2seconds = {}
	for t, subject in timelines:
		if subject in subject2seconds.keys():
			subject2seconds[subject].append(t)
		else:
			subject2seconds[subject] = [t]

	if 'Unpredict' in subject2seconds:
		unpredict = subject2seconds.pop('Unpredict')

	for subject, seconds in subject2seconds.items():
	    i = 0
	    maxstemp = 0
	    acceptable_interval_num = 10
	    while i < (len(seconds) - 2):
	        start_time_point = int(seconds[i])
	        end_time_point = int(seconds[i + 1])
	        if end_time_point - start_time_point <= acceptable_interval_num:
	            maxstemp += end_time_point - start_time_point
	            i += 1
	            print(maxstemp)
	        else:
	            if maxstemp >= 5:
	                sellpoint = {}
	                sellpoint['subject'] = subject
	                sellpoint['start_sec'] = (int(start_time_point) - maxstemp)
	                sellpoint['end_sec'] = int(start_time_point)
	                segments.append(sellpoint)
	            i += 1
	            maxstemp = 0
	return segments

def process(subjects_file, video_file, output_path, keypoints_file):
	seconds_list, setences_list, subjects_list = preprocess(subjects_file)
	# segments = segment(zip(seconds_list, subjects_list, setences_list))
	segments = segment2(zip(seconds_list, subjects_list))
	ffmpeg_cmd_t = 'ffmpeg -ss %s -t %s -i %s -vcodec copy -acodec copy %s'
	for seg in segments:
		i = seg['start_sec']
		if i - 3 < 0:
		    i = 0
		else:
		    i = i - 3
		m, s = divmod(i-2, 60)
		h, m = divmod(m, 60)
		str_start = "{:0>2}:{:0>2}:{:0>2}".format(h, m, s)
		m, s = divmod(30, 60)
		h, m = divmod(m, 60)
		str_during = "{:02d}:{:02d}:{:02d}".format(h, m, s)
		outfilename = output_path + '/' + seg['subject'] + "_" + str(i) + '.mp4'
		exec_cmd = ffmpeg_cmd_t % (str_start, str_during, video_file, outfilename)
		print(exec_cmd)
		os.system(exec_cmd)

def main():
	init("./jieba/stopwords_cn.txt", "./jieba/userdict.txt")
	clfins = build('./output')

	### list all videos
	videos_path = './data/videos'
	subjects = './data/output'
	for vid in os.listdir(subjects):
		vid_path = os.path.join(subjects, vid)
		output_path = "%s/" % (vid_path)

		video_file = os.path.join(videos_path, vid)

		subjects_file = "%s/%s.subjects" % (vid_path, vid)
		keypoints_file = "%s/%s.keypoints" % (vid_path, vid)
		
		process(subjects_file, video_file, output_path, keypoints_file)
		# valid_points = extract_point(zip(seconds_list, subjects_list))

		output = open(keypoints_file, mode='w', encoding='utf-8')
		# for second, keyword in output_points.items():
		# 	text = merge_text2(second, sentence_timeline)
		# 	summary = extract_summary(text, keyword, predict)
		# 	output.write("%s\t%s\t%s|%s\n" % (second, '', keyword, summary))
		output.close()
		print(vid, " cut finished.")
		print()
		print()
		print()

if __name__ == '__main__':
	main()