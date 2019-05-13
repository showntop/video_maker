VIDEO_LIST = './data/video_list.txt'
VIDEO_PATH = './data/videos'
FRAME_PATH = './data/frames'

OUTPUT_PATH = './data/output'

jieba_stopwords_path = './jieba/stopwords_cn.txt'
jieba_userdict_path = './jieba/userdict.txt'
naive_bayes_model_path = './output'

### 外观......
appearance_words = {
    ## 外观
    '车身': {
        'adjs': [ '流线', '硬朗', '犀利', '漂亮', '精致', '圆润', '大气', '沉稳', '时尚', '极简' ]
    },
    '整车': {},
    '车顶': {
        'adjs': [ '下压式' ]
    },
    '前脸': {
        'adjs': [ '主流', '沉稳', '冲击力', '违和感', '好看', '凶悍', '豪华', 
        '高级', '霸气', '大嘴', '粗狂', '碟翼式', '家族式', '经典', '锐利', '时尚感', '犀利']
    },
    '格栅': {
        'adjs': ['直瀑式', '六边形进气', '封闭式' ]
    },
    '中网': {

    },
    '大灯': {},
    '轮胎': {

    },
    '颜色': {
        'adjs': ['很赞', '好看', '清新', '脱俗']
    },
    '车漆': {}
}