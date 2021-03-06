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


def extract_point(sorted_list):
    # param
    #### [(1, '空间')]
    points = {}
    # 分组
    dict1 = {}
    for tp in sorted_list:
        # if tp[1] == 'empty':
        #     for x in dict1:
        #         dict1[x].append(tp[0])
        #     continue
        if tp[1] in dict1.keys():
            dict1[tp[1]].append(tp[0])
        else:
            dict1[tp[1]] = [tp[0]]
    #
    empty = dict1['Unpredict']
    dict1.pop('Unpredict')

    for k in dict1:
        if len(dict1[k]) < 5:
            continue
        points[dict1[k][0]] = k

    lastk = 0
    deleted = []
    for k in points:
        if int(k) - lastk < 5:
            deleted.append(k)
        lastk = int(k)
    for x in deleted:
        points.pop(x)

    return points


def main():
    clfins = build('./output')
    init("./jieba/stopwords_cn.txt", "./jieba/userdict.txt")
    # list all videos
    videos_folder_path = './data/captions'
    for folder in os.listdir(videos_folder_path):
        if folder != '24CFC579E390B590':
            # if folder != '11AFCABB49FADB3D':
            pass
            # continue

        one_video_folder_path = os.path.join(videos_folder_path, folder)
        caption_file = "./%s/%s_baidu_ocr_result.txt" % (
            one_video_folder_path, folder)
        file_name_output = "./%s/%s_category_result.txt" % (
            one_video_folder_path, folder)
        classify_result_file = "./%s/classify_result.txt" % (
            one_video_folder_path)
        keypoint_result_file = "./%s/keypoint_result.txt" % (
            one_video_folder_path)

        sentence_list = preprocess(caption_file)
        seconds_list, docs_list = zip(*sentence_list)
        predicted_list = clfins.predict_proba(docs_list, 0.5)
        target_list = []

        output = open(classify_result_file, mode='w', encoding='utf-8')
        for second, content, predicted in zip(seconds_list, docs_list, predicted_list):
            target_list.append(clfins.target_name(predicted))
            output.write("%s\t%s\t%s\n" %
                         (second, content, clfins.target_name(predicted)))
        output.close()

        valid_points = extract_point(zip(seconds_list, target_list))
        print(valid_points)

        def merge_text2(k, dict):  # 以k点为中轴，获取30s内容
            texts = []
            for x in range(k - 2, k + 30):
                if x not in dict.keys():
                    continue
                sss = dict[x].replace("汽车之家", "").replace("之家", "").replace("汽车之", "").replace(
                    "看车买车用车", "").replace("家看车", "").replace("家买车用车", "").strip()
                sss = sss.split(" ")[0]
                if x == k - 2:
                    texts.append(sss)
                    continue
                if x - 1 not in dict.keys():
                    continue
                sss0 = dict[x - 1].replace("汽车之家", "").replace("之家", "").replace(
                    "汽车之", "").replace("看车买车用车", "").replace("家看车", "").replace("家买车用车", "").strip()
                sss0 = sss0.split(" ")[0]
                if tf_similarity(sss, sss0) > 0.8:
                    # print(sss0, sss)
                    continue
                texts.append(sss)
            return '，'.join(texts)

        # 重新预测一遍
        sentence_timeline = dict(sentence_list)
        for k in valid_points:
            new_text = merge_text2(k, sentence_timeline)
            # 重新计算分类
            predicted_list = clfins.predict_proba([new_text], 0.5)
            # predicted_list = clfins.predict([new_text])
            valid_points[k] = clfins.target_name(predicted_list[0])
            # print(new_text, clfins.target_name(predicted_list[0]))
        # print(valid_points)

        def merge_points(points):
            reverse_points = {}
            for k, v in points.items():
                if v in reverse_points.keys():
                    reverse_points[v].append(k)
                else:
                    reverse_points[v] = [k]
            if 'Unpredict' in reverse_points.keys():
                reverse_points.pop('Unpredict')

            new_points = {}
            for ks, v in reverse_points.items():
                sortedv = list(v).sort()
                new_points[int(v[0])] = ks

            return new_points

        def predict(docs_list):
            predicted_list = clfins.predict(docs_list)
            return clfins.target_name(predicted_list[0])

        output_points = merge_points(valid_points)
        print(output_points)

        output = open(keypoint_result_file, mode='w', encoding='utf-8')
        for second, keyword in output_points.items():
            text = merge_text2(second, sentence_timeline)
            summary = extract_summary(text, keyword, predict)
            output.write("%s\t%s\t%s|%s\n" % (second, '', keyword, summary))
        output.close()
        print(folder, " finished.")
        print()
        print()
        print()

if __name__ == '__main__':
    main()
