# coding=utf-8
import os
from classifier.build import build
from tokenizer import init
from utils.text_similarity import tf_similarity
from summary.extract import extract_summary

def preprocess(file_name):
	seconds_list = []
	content_list = []
	if not os.path.exists(file_name):
		print(file_name, " not exists.")
		return zip(seconds_list, content_list)
	with open(file_name, 'r') as fp:
	   lines = fp.readlines()
	for line in lines:
		arr = line.split("\t")
		time = int(arr[0])
		raw = arr[1].split(" ")[0].replace("\n", "")
		
		seconds_list.append(time)
		content_list.append(raw)

	return sorted(zip(seconds_list, content_list), key=lambda x: x[0])

def main():
	init("./jieba/stopwords_cn.txt", "./jieba/userdict.txt")
	clfins = build('./output')
	### list all videos
	input_path = './data/output'
	output_path = './data/output'
	for vid in os.listdir(input_path):
		caption_file = os.path.join(input_path, vid, vid + '.captions')

		subject_file = "%s/%s/%s.subjects" % (output_path, vid, vid)

		sentence_list = preprocess(caption_file)
		seconds_list, docs_list = zip(*sentence_list)
		predicted_list = clfins.predict_proba(docs_list, 0.5)
		target_list = []

		output = open(subject_file, mode='w', encoding='utf-8')
		for second, content, predicted in zip(seconds_list, docs_list, predicted_list):
			target_list.append(clfins.target_name(predicted))
			output.write("%s\t%s\t%s\n" % (second, content, clfins.target_name(predicted)))
		output.close()
		
		print(vid, " classify finished.")
		print()
		print()
		print()

if __name__ == '__main__':
	main()