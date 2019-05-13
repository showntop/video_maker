# coding=utf-8
import jieba.analyse as analyse

def extract(text, side_words, index, cate, predict):
	if index >= len(side_words):
		return text
	wordx = text.index(side_words[index])
	s1 = text[:wordx].split("，")[-1]
	s2 = text[wordx:].split("，")[:3]
	textx = s1 + ''.join(s2)
	if predict([textx]) != cate:
		extract(text, side_words, index+1, cate, predict)
	return textx

def extract_summary(raw_text, cate, predict):
	### 提取中网、前脸。。。。
	side_words = analyse.extract_tags(raw_text, topK=20, withWeight=False, allowPOS=('n'))
	# print(raw_text, side_words, cate)
	# side_words = analyse.textrank(text, topK=20, withWeight=False, allowPOS=('n'))
	# side_words = analyse.textrank(text, topK=20, withWeight=False, allowPOS=('n', 'vn', 'v', 'a', 'Ag', 'ad'))
	text = extract(raw_text, side_words, 0, cate, predict)
	hwords = analyse.extract_tags(text, topK=20, allowPOS=('c'))
	for x in hwords:
		text = text.replace(x, "，"+x)
	text = text + '...'
	return text
