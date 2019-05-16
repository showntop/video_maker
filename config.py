import random

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

def get_appid(i):
    return [
    ('14535492', 'XMnvaz6EH6Hk7MpbRAH3OzB2', 'ogSe8Ox5wGNSwYioF0WkV8byTxnlnbcQ'),
    ('15171726', '114CdIoq27VFspbYDGz4Hs0j', 'yenKoxKZRn1RCRYCF7I2Cf2nBG9MIWLd'),
    ('15172140', 'HUYhwz1BWLwANMYcgGIfKBoT', 'lin33LMrgouo8H7pH19DmisBfk8vKWdT'),
    ('15184946', 'iR5dGcA9xcPgZc9XbN7n4fm5', 'jbp9KjHCajmyGSjkmnHZIXG2hQMvFIv8'),
    ][rand.%4]

### 外观......
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
    '尾灯': {},
    '轮胎': {

    },
    '颜色': {
        'adjs': ['很赞', '好看', '清新', '脱俗']
    },
    '车漆': {},
    '流线': {},
    '霸气': {}
}

interspace_words = {
    '前排': {},
    '后排': {},
    '中排': {},
    '后备箱': {},
    '轴距': {},
    '腿部': {},
    '头部': {},
    '空间': {},
    '前后排': {},
    '储物': {},
    '载物': {},
    '放倒': {},
    '行李箱': {},
    '压迫感': {},
    '规整度': {}
}

interiors_words = [
    "内饰","皮饰","皮质","用料","塑料感","内饰","塑料","装潢","装饰","材质","材料","手感","质感","化妆镜","做工",
]

control_words = [
    "稳重感","稳定","吃风","路感","调教","人车","扭矩","操控","操控性","指向性","方向","顿挫","顿挫感","操纵",
]

comfortable_words = [
    "空调","出风口","花粉","冷气","暖气","制冷","制热","舒适","舒适性","舒适度"
]

power_words = [
    "发动机","马力","四驱","前驱","前置","共振","涡轮","动力","变速","提速","起步","速度","超车","上坡","爬坡","推背感","后劲","推背","加速快","速度快","迅速"
]

price_words = [
    "性价比","优惠","实惠","很值","值得","便宜"
]

fuel_words = [
    "油箱","油耗","省油","节油","环保","排量"
]












