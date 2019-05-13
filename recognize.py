# coding:utf8

import os
import re
import jieba
from aip import AipOcr

from whitelist import whitelist

""" 你的 APPID AK SK """
# APP_ID = '14535492'
# API_KEY = 'XMnvaz6EH6Hk7MpbRAH3OzB2'
# SECRET_KEY = 'ogSe8Ox5wGNSwYioF0WkV8byTxnlnbcQ'


APP_ID = '15171726'
API_KEY = '114CdIoq27VFspbYDGz4Hs0j'
SECRET_KEY = 'yenKoxKZRn1RCRYCF7I2Cf2nBG9MIWLd '

# APP_ID = '15172140'
# API_KEY = 'HUYhwz1BWLwANMYcgGIfKBoT'
# SECRET_KEY = 'lin33LMrgouo8H7pH19DmisBfk8vKWdT'


# APP_ID = '15184946'
# API_KEY = 'iR5dGcA9xcPgZc9XbN7n4fm5'
# SECRET_KEY = 'jbp9KjHCajmyGSjkmnHZIXG2hQMvFIv8'

def read_image(filename):
    with open(filename, 'rb') as fp:
        return fp.read()

def ocr(input_file):
    return 'oooo'
    """
    调用百度ocr
    :param input_file: 
    :param outpath: 
    :return: 
    """
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
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
    print('baidu ocr result: ', result)
    # if result.get('error_code', 0) != 0:
    #     return []
    words_result = result.get("words_result", [])
    
    words = [ '' if re.match(u"[\u4e00-\u9fa5]+", words_result[i]["words"]) is None else words_result[i]["words"] for i in range(len(words_result))]
    return ''.join(words)

def process(frames_path, vid, output_path):
    if os.path.exists(output_path + '/' + vid):
        return
    seconds = []
    sentences = []
    for image_file in os.listdir(frames_path + vid):
        try:
            sentence = ocr(frames_path + vid + '/' + image_file)
        except Exception as e:
            print(vid, image_file, e)
        seconds.append(int(image_file.split(".")[0]))
        sentences.append(sentence)

    contents = sorted(zip(seconds, sentences), key=lambda x: x[0])
    save(output_path, vid, contents)



def save(outpath, vid, contents):
    save_path = os.path.join(outpath, vid)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(save_path + '/' + vid + '.captions', 'w', encoding='UTF-8') as outfile:
        for (t, s) in contents:
            outfile.write(str(t) + '\t' + ''.join(s) + '\n')

def main():
    data_path = './data'
    frames_path = data_path+'/frames/'
    output_path = data_path+'/output/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for vid in os.listdir(frames_path):
        if vid not in whitelist('./data/whitelist.txt'):
            continue
        process(frames_path, vid, output_path)

if __name__ == '__main__':
    main()



