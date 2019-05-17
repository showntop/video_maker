import sys
sys.path.append("..")

import config
from utils.text_similarity import tf_similarity
from classifier.build import build
from tokenizer import init
clfins = build('./output')
init("./jieba/stopwords_cn.txt", "./jieba/userdict.txt")


class Keypoint(object):
    """docstring for Keypoint"""

    def __init__(self, arg):
        super(Keypoint, self).__init__()
        self.arg = arg


class Segment(object):

    def __init__(self, start_position, end_position, subject, content):
        super(Segment, self).__init__()
        self.start_position = start_position
        self.end_position = end_position
        self.subject = subject
        self.contents = [content]

    def __str__(self):  # 定义打印对象时打印的字符串
        return ("start: %d, end: %d, subject: %s, content: %s" %
                (self.start_position, self.end_position, self.subject, '，'.join(self.contents)))

    def get_content(self, position):
        # print(self.contents)
        # print(position - self.start_position)
        # print(self.contents[position - self.start_position])
        return self.contents[position - self.start_position]

    def add_content(self, c):
        self.contents.append(c)

    def digest_content(self, content):
        if tf_similarity(self.contents[-1], content) > 0.8:
            return
        self.contents.append(content)

    def repredict(self):
        new_contents = []
        for c in self.contents:
            if len(new_contents) <= 1:
                new_contents.append(c)
                continue
            if tf_similarity(new_contents[-1], c) >= 0.8:
                continue
            new_contents.append(c)
        text = ''.join(new_contents)
        test_predicted = clfins.predict_proba([text], 0.5)
        print(test_predicted)
        print(text, clfins.target_name(predicted[0]))

    # 合并段落
    # s 与之相邻  并且紧邻其后
    def merge(self, s):
        if s.start_position - self.end_position != 1:
            raise Exception('segment s not after me',
                            s.start_position, self.end_position)
        # print(self)
        text = self.get_content(self.end_position) + \
            s.get_content(s.start_position)
        # print(text)
        predicted = clfins.predict([text])
        print(text, clfins.target_name(predicted[0]))
        if clfins.target_name(predicted[0]) == s.subject:  # 向前蔓延
            s.contents.insert(0, self.get_content(self.end_position))
            self.contents.pop(self.end_position - self.start_position)
            s.start_position = s.start_position - 1
            self.end_position = self.end_position - 1
        elif clfins.target_name(predicted[0]) == self.subject:  # 向后退缩
            self.add_content(s.get_content(s.start_position))
            s.contents = s.contents[1:]
            self.end_position = self.end_position + 1
            s.start_position = s.start_position + 1
        else:
            pass

        print('s:', s)
        print('self:', self)
        self.merge(s)
        # print(s.start_position, s.get_content(s.start_position))


def segment(timelines):

    # make segment
    segments = [Segment(0, 0, 'Unpredict', '')]
    for (time, subject, content) in timelines:
        # 计算连续段
        if subject == segments[-1].subject:
            segments[-1].end_position = time  # 结束 + 1
            segments[-1].add_content(content)
        else:
            segments.append(Segment(time, time, subject, content))
    # make segment
    print(*segments, sep='\n')
    # for i in range(1,len(segments)):
    for i in range(len(segments)):
        pass
        # segments[i-1].repredict()
        # if sg.subject == 'Unpredict':
        # segments[i-1].merge(segments[i])


def predict():
    pass


def main():
    primary_classify_file = open("../data/output/061C69650C43A779.mp4/061C69650C43A779.mp4.subjects",
                                 mode='r', encoding='utf-8')

    seconds_list = []
    subject_list = []
    content_list = []
    for line in primary_classify_file.readlines():
        arr = line.split("\t")
        time = int(arr[0])
        raw = arr[1].split(" ")[0].replace(
            "\n", "").replace("汽车之家", '').replace("之家", "")
        cat = arr[2].split(" ")[0].replace("\n", "")

        seconds_list.append(time)
        subject_list.append(cat)
        content_list.append(raw)

    # print(zip(seconds_list, subject_list))
    segments = segment(zip(seconds_list, subject_list, content_list))
    primary_classify_file.close()


if __name__ == '__main__':
    main()
