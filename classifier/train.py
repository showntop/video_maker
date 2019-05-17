# coding=utf-8
import os
import json

import sys
sys.path.append("..")
from tokenizer import tokenize2

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.decomposition import PCA


def train(train_path, model_path):
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    train_data = load_files(train_path, shuffle=True, random_state=42)
    print('开始建模.....')
    with open(model_path + '/training_data.target', 'w', encoding='utf-8') as f:
        f.write(json.dumps(train_data.target_names))
    # count_vect = CountVectorizer(min_df=2, tokenizer=tokenize, max_features=2350, stop_words=stop_words)
    count_vect = CountVectorizer(
        min_df=2, tokenizer=tokenize2, max_features=2350)
    x_train_counts = count_vect.fit_transform(train_data.data)
    tfidf_transformer = TfidfTransformer()
    x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)

    clf = MultinomialNB().fit(x_train_tfidf, train_data.target)
    # 保存分类器（好在其它程序中使用）
    joblib.dump(clf, model_path + '/model.pkl')
    # 保存矢量化（坑在这儿！！需要使用和训练器相同的 矢量器 不然会报错！！！！！！ 提示 ValueError dimension
    # mismatch··）
    joblib.dump(count_vect, model_path + '/count_vect')
    print("分类器的相关信息：")
    print(clf)

if __name__ == '__main__':
    train('../data/train', '../models')
