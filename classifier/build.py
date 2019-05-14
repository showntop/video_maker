# coding=utf-8
import re
import json

import sys
sys.path.append("..")
from tokenizer import tokenize2, init
import config

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib

class Classifier(object):
	"""docstring for Classifier"""
	def __init__(self, model_path):
		super(Classifier, self).__init__()
		clf = joblib.load(model_path + '/model.pkl')
		count_vect = joblib.load(model_path + '/count_vect')
		target_names = json.loads(open(model_path + '/training_data.target', 'r', encoding='utf-8').read())
		
		self.clf = clf
		self.count_vect = count_vect
		# print(self.count_vect.get_feature_names())
		self.target_names = target_names

	def target_name(self, predict):
		if predict is None:
			return 'Unpredict'
		return self.target_names[predict]

	def predict(self, docs):
		tfidf_transformer = TfidfTransformer()
		x_new_counts = self.count_vect.transform(docs)
		x_new_tfidf = tfidf_transformer.fit_transform(x_new_counts)
		# 进行预测
		predicted = self.clf.predict(x_new_tfidf)
		return predicted

	def predict_proba(self, docs, threshold):
		tfidf_transformer = TfidfTransformer()
		x_new_counts = self.count_vect.transform(docs)
		x_new_tfidf = tfidf_transformer.fit_transform(x_new_counts)
		# 进行预测
		predicted_list = self.clf.predict_proba(x_new_tfidf)

		# for predicted in predicted_list:
		# 	for x in range(len(predicted)):
		# 		print(self.target_name(x), predicted[x])
		final_list = []
		for x in range(len(predicted_list)):
			predicted = predicted_list[x]
			if max(predicted) < threshold:
				### 手动预测
				# self.predict_internal(docs[x])
				final_list.append(None)
				continue
			# self.predict_internal(docs[x])
			max_proba_index = predicted.tolist().index(max(predicted))
			final_list.append(max_proba_index)

		return final_list

	### 手动微调
	def predict_internal(self, text):
		match_num = 0
		for word in config.appearance_words:
			try:
				pos = text.index(word)
				# print(pos)
			except Exception as e:
				# print(e)
				pass
			else:
				match_num += len(word)
			finally:
				pass
		print(text, match_num/len(text))





def test(clfins):
	##### for test
	docs_new = ['3.0T发动机，推背感强烈，舒适性下降，胎噪明显',
				'因为厂家这次其实也是说了他们会把四驱车型的价格降低因为之前好像是只有顶配23万那款是四驱的现在他说要把四驱版本的车型降到18万左右我觉得有一些竞争力的内饰基本就是这样的咱们去后排看空间空间的部分因为新老款是完全一样的咱们就简单说说像我的身高呢是1米75身高:i75cM重:82KG前排调整好我的驾驶位之后身:i75cM:82KG前排调整好我的驾驶位之后身高:75CM体重:KG后排腿部能有一个超过两拳的腿部空间然后头顶上的空间也完全没问题大概三指左右吧三指然后它这个车',
				'新款迈特威增配了珠光白车款，车辆尾灯变为熏黑灯色',
				'标配带透镜LED灯组，尾灯变成类似C字型',
				'大嘴式中网配上钳形的头灯，看上去极具视觉冲击力',
				'18年轮胎，刹车盘较新，整车没有原车漆但没有事故',
				'一个很大面积的一个这种镀铬的中网然后也是现在比较流行的中网和木灯一体式的一个设计汽中网和大灯一体式的一个设计看车:买车用车一切都做得非常的保险看车买车切都做得非常的保险这都这就是中国非常主流的非常这都这就是中国非常丰流的非常喜欢的一种前脸的设计风格另外它在整个配置上其实也是有一个提升的像老款它的顶配是氙气大灯像老款它的顶配是氙气大灯富但是很多低配都还是卤素灯而到了新款呢']
	predicted = clfins.predict_proba(docs_new, 0.0)
	for doc, category in zip(docs_new, predicted):
		print('%r => %s' % (doc, clfins.target_names[category]))

def test_performence(clfins):
	### test performence
	import numpy as np
	test_data = load_files("../data/test",
		categories=clfins.target_names, shuffle=True, random_state=42)

	test_docs = []
	for i in range(len(test_data.data)):
		test_docs.append(test_data.data[i].decode().strip())

	test_predicted = clfins.predict_proba(test_docs, 0.0)
	total = 0
	right = 0
	for filename, doc, category, predict in zip(test_data.filenames, test_docs, test_data.target, test_predicted):
		if predict is None:
			continue
		total = total + 1
		if test_data.target_names[category] == clfins.target_name(predict):
			right = right + 1
			continue
		print('%r => %s| right:%s, predict:%s, %s' % (filename, doc, test_data.target_names[category], 
			clfins.target_name(predict), (predict)))

	print(total, ",", right, ",", right/total)

def build(model_path):
	clfins = Classifier(model_path)
	return clfins

if __name__ == '__main__':
	init("../jieba/stopwords_cn.txt", "../jieba/userdict.txt")
	clfins = build("../models")
	test(clfins)
	# test_performence(clfins)