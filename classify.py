# coding=utf-8
import os
import config
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

# 手动微调


def predict_internal(text):
    match_num = 0
    for word in config.appearance_words.keys():
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '外观'
    match_num = 0
    for word in config.interspace_words.keys():
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '空间'
    match_num = 0
    for word in config.control_words:
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '操控'
    match_num = 0
    for word in config.comfortable_words:
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '舒适性'
    for word in config.power_words:
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '动力'
    for word in config.price_words:
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '价格'
    for word in config.fuel_words:
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
    if match_num >= 1:
        print(text, match_num / len(text))
        return '油耗'


def process(caption_file, output_file, clfins=None):
    if os.path.exists(output_file):
        return output_file

    if clfins is None:
        init(config.jieba_stopwords_path, config.jieba_userdict_path)
        clfins = build(config.naive_bayes_model_path)

    sentence_list = preprocess(caption_file)
    seconds_list, docs_list = zip(*sentence_list)
    predicted_list = clfins.predict_proba(docs_list, 0.5)
    target_list = []

    output = open(output_file, mode='w', encoding='utf-8')
    for second, content, predicted in zip(seconds_list, docs_list, predicted_list):
        name = clfins.target_name(predicted)
        if name == 'Unpredict':
            name = predict_internal(content)
        target_list.append(name)
        output.write("%s\t%s\t%s\n" % (second, content, name))
    output.close()
    return output_file


def main():
    init("./jieba/stopwords_cn.txt", "./jieba/userdict.txt")
    clfins = build(config.naive_bayes_model_path)
    # list all videos
    input_path = './data/output'
    output_path = './data/output'
    for vid in os.listdir(input_path):
        caption_file = os.path.join(input_path, vid, vid + '.captions')
        subject_file = "%s/%s/%s.subjects" % (output_path, vid, vid)
        preprocess(caption_file, subject_file, clfins)

        print(vid, " classify finished.")
        print()
        print()
        print()

if __name__ == '__main__':
    main()
