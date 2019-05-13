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
	        else:
	            if maxstemp >= 5:
	                segment = {}
	                segment['subject'] = subject
	                segment['start'] = (int(start_time_point) - maxstemp)
	                segment['end'] = int(start_time_point)
	                segments.append(segment)
	            i += 1
	            maxstemp = 0
	return segments

def save(short_videos, vid):
	import pymysql
	 
	# 打开数据库连接
	db = pymysql.connect("localhost", "root", "", "short_videos" )
	 
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	 
	# SQL 插入语句
	sql = "INSERT INTO videos(url, \
	         subject, content, source_video_id) \
	         VALUES ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE \
	         subject=VALUES(subject), content=VALUES(content)		\
	         "
	for v in short_videos:
		try:
		   # 执行sql语句
		   print(sql %(v['url'], v['subject'], v['content'], v['source']))
		   cursor.execute(sql %(v['url'], v['subject'], v['content'], v['source']))
		   # 提交到数据库执行
		   db.commit()
		except Error as e:
			print(e)
			# 如果发生错误则回滚
			db.rollback()
	# 关闭数据库连接
	db.close()


def process(subjects_file, video_file, output_path, keypoints_file):
	def merge_text(k1, k2, dict):
		texts = []
		for x in range(k1, k2):
			if x not in dict.keys():
				continue
			sss = dict[x].replace("汽车之家", "").replace("之家", "").replace("汽车之", "").replace("看车买车用车", "").replace("家看车", "").replace("家买车用车", "").strip()
			sss = sss.split(" ")[0]
			if x-1 not in dict.keys():
				continue
			sss0 = dict[x-1].replace("汽车之家", "").replace("之家", "").replace("汽车之", "").replace("看车买车用车", "").replace("家看车", "").replace("家买车用车", "").strip()
			sss0 = sss0.split(" ")[0]
			if tf_similarity(sss, sss0) > 0.8:
				# print(sss0, sss)
				continue
			texts.append(sss)
		return texts

	seconds_list, setences_list, subjects_list = preprocess(subjects_file)
	# segments = segment(zip(seconds_list, subjects_list, setences_list))
	segments = segment2(zip(seconds_list, subjects_list))
	print(segments)

	for seg in segments:
		i = seg['start']
		if i - 2 < 0:
		    i = 0
		else:
		    i = i - 2
		seg['source'] = video_file
		seg['start'] = i
		seg['duration'] = 30
		seg['content'] = ''.join(merge_text(i, i+30, dict(zip(seconds_list, setences_list))))
		seg['url'] = output_path + '/' + seg['subject'] + "_" + str(seg['start']) + '.mp4'

	print(segments)

	ffmpeg_cmd_t = 'ffmpeg -y -ss %s -t %s -i %s -vcodec copy -acodec copy %s'
	for seg in segments:
		m, s = divmod(seg['start'], 60) 
		h, m = divmod(m, 60)
		start = "{:0>2}:{:0>2}:{:0>2}".format(h, m, s)
		m, s = divmod(seg['duration'], 60)
		h, m = divmod(m, 60)
		duration = "{:02d}:{:02d}:{:02d}".format(h, m, s)
		out_video_file = seg['url']
		exec_cmd = ffmpeg_cmd_t % (start, duration, video_file, out_video_file)
		# print(exec_cmd)
		os.system(exec_cmd)
	save(segments, video_file)

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