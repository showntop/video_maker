import jieba
import jieba.analyse as analyse

def init(userdict_file, stop_words_file):
	jieba.load_userdict(userdict_file)
	# print("loading....")
	analyse.set_stop_words(stop_words_file)

# def tokenize(text):
# 	raw = text.replace("\n", '').replace(' ', '').replace('\xa0', '')
# 	tokens = jieba.cut(raw, cut_all=False)
# 	return list(tokens)

def tokenize2(text):
	text = text.replace("看车买车", "").replace("看车", "").replace("买车", "").replace("用车", "")
	tokens = analyse.extract_tags(text, topK=10000, allowPOS=('n', 'a', 'v'))
	# print(text, list(tokens))
	return list(tokens)
