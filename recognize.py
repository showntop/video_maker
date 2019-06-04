# coding:utf8

import os
import re
import jieba
from aip import AipOcr
import config

from whitelist import whitelist


def for_test_ocr(input_file):
    vid = input_file.split('/')[3].split('.')[0]
    file = './data/captions.bak/%s/%s_baidu_ocr_result.txt' % (vid, vid)

    x1 = []
    x2 = []
    with open(file, 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        arr = line.split("\t")
        x1.append(int(arr[0]))
        x2.append((arr[1]).strip())
    return x1, x2


def read_image(filename):
    with open(filename, 'rb') as fp:
        return fp.read()


def ocr(input_file):
    """
    调用百度ocr
    :param input_file: 
    :param outpath: 
    :return: 
    """
    # client = AipOcr(config.APP_ID, config.API_KEY, config.SECRET_KEY)
    xi = input_file.split("/")[-1].split(".")[0]
    zzz = config.get_appid(int(xi))
    client = AipOcr(zzz[0], zzz[1], zzz[2])

    """ 调用通用文字识别（高精度版） """
    image = read_image(input_file)
    client.basicGeneral(image)
    # client.basicAccurate(image);
    """ 如果有可选参数 """
    options = {}
    options["detect_direction"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别（高精度版） """
    result = client.basicAccurate(image, options)
    print(input_file, 'result: ', result)
    # if result.get('error_code', 0) != 0:
    #     return []
    words_result = result.get("words_result", [])

    words = ['' if re.match(u"[\u4e00-\u9fa5]+", words_result[i]["words"])
             is None else words_result[i]["words"] for i in range(len(words_result))]
    return ''.join(words)


def ocr_ours(input_file):
    """
    调用自研ocr服务
    :param input_file: 
    :param outpath: 
    :return: 
    """
    import urllib.parse
    import requests
    import base64

    url = 'http://10.27.214.67:8080/ocr'
    encodedZip = base64.b64encode(read_image(input_file))
    # print(encodedZip.decode())
    body = {
        "imgString": encodedZip.decode(),
        "billModel": "通用OCR",
        "textAngle": False,
        "textLine": False,
    }
    resp = requests.post(url, json=body)  # 发送post请求，第一个参数是URL，第二个参数是请求数据
    # print("resp", resp)
    result = resp.json()
    # params = urllib.parse.urlencode(
    #     {'@imgString': encodedZip, '@billModel': '通用OCR', '@textAngle': False, '@textLine': False})
    # headers = {"Content-type": "application/x-www-form-urlencoded",
    # "Accept": "text/plain"}
    # conn = http.client.HTTPConnection('10.27.214.177', '8080')
    # conn.request("POST", "/ocr", params, headers)
    # response = conn.getresponse()
    # print(response)
    # result = response.read()
    print(input_file, 'result: ', result)
    # data = json.loads(result)

    words_result = result.get("res", [])

    words = ['' if re.match(u"[\u4e00-\u9fa5]+", words_result[i]["text"])
             is None else words_result[i]["text"] for i in range(len(words_result))]
    return ''.join(words)


def save(caption_file, contents):
    with open(caption_file, 'w', encoding='UTF-8') as outfile:
        for (t, s) in contents:
            outfile.write(str(t) + '\t' + ''.join(s) + '\n')
    return caption_file

from skimage.measure import compare_ssim
import cv2


class CompareImage():

    def compare_image(self, path_image1, path_image2):

        imageA = cv2.imread(path_image1)
        imageB = cv2.imread(path_image2)

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        # print("SSIM: {}".format(score))
        return score


def process(frames_path, output_path):
    if os.path.exists(output_path):
        return output_path
    compare_image = CompareImage()

    seconds = []
    sentences = []

    last_image = ''
    last_sentence = ''
    # print(frames_path)
    frames = [int(x.split('.')[0]) for x in os.listdir(frames_path)]
    frames.sort()
    for frame_index in frames:
        image_file = str(frame_index) + '.jpg'
        # print(image_file)
        if frame_index > 1:
            score = compare_image.compare_image(
                frames_path + '/' + image_file, frames_path + '/' + last_image)
            if score > 0.8:
                # print(frames_path + '/' + image_file,
                      # frames_path + '/' + last_image)
                sentences.append(last_sentence)
                # last_image = image_file
                continue
        last_image = image_file
        try:
            sentence = ocr_ours(frames_path + '/' + image_file)
            # sentence = ocr(frames_path + '/' + image_file)
            seconds.append(int(image_file.split(".")[0]))
            sentences.append(sentence)
            last_sentence = sentence
        except Exception as e:
            print(image_file, e)
            seconds.append(int(image_file.split(".")[0]))
            sentences.append('')
            last_sentence = ''
        finally:
            pass
        # print(sentences)

    # seconds, sentences = for_test_ocr(output_path)

    contents = sorted(zip(seconds, sentences), key=lambda x: x[0])
    print(contents)
    return save(output_path, contents)


def main():
    frames_path = './data/frames/'
    output_path = './data/output/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for vid in os.listdir(frames_path):
        # if vid not in whitelist('./data/whitelist.txt'):
        #     continue
        if not os.path.exists(os.path.join(output_path, vid)):
            os.mkdir(os.path.join(output_path, vid))
        process(frames_path + vid, os.path.join(output_path, vid, 'captions.txt'))
        print(os.path.join(output_path, vid, 'captions.txt'))

if __name__ == '__main__':
    main()
