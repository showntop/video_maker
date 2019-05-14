VIDEO_LIST = './data/video_list.txt'
VIDEO_PATH = './data/videos'
FRAME_PATH = './data/frames'

OUTPUT_PATH = './data/output'

jieba_stopwords_path = './jieba/stopwords_cn.txt'
jieba_userdict_path = './jieba/userdict.txt'
naive_bayes_model_path = './models'
train_data_path = './data/train'


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