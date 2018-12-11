import datetime
import hashlib
import json
import logging
import traceback

import requests
from pymongo import MongoClient
from flask import redirect
import logging.handlers

from requests.adapters import HTTPAdapter

filehandler = logging.handlers.TimedRotatingFileHandler(
    # "/Users/bury/work/Spider/Test/logging_test/logs/model_server_log",
    "/home/Model/logs/model_server_logs/tools_log",
    when='D',
    interval=1,
    backupCount=7,
)
logFormatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
filehandler.setFormatter(logFormatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
filehandler.suffix = "%Y-%m-%d.log"
logger.addHandler(filehandler)
import threading


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def save_data(userData):
    '''
    :param new_data:用户初始化数据
    ：func  ：保存到数据库
    :return:
    '''
    try:
        # jsonUserdata = json.dumps(userData).replace(' ', '').replace('\r', '').replace('\n', '')
        # client = MongoClient('mongodb://tanteng:123456@localhost:27017/')
        client = MongoClient('mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
        db = client['test']
        collection = db['user']
        collection.insert(userData)

    except Exception as e:
        logger.exception('save user original data Error:')
        logger.info("{0},origin data Input Error..".format(userData['data']['orderNo']))
        logger.info(str(traceback.format_exc()))


def save_score(data, order_data=None, error_msg=None):
    '''
    :param data: 得到分数的数据
    :param order_data:
    :param error_msg:
    ：func: 把得到分保存到数据库
    :return:
    '''
    client = MongoClient('mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
    db = client['test']
    try:
        # client = MongoClient('mongodb://tanteng:123456@localhost:27017/')
        collection = db['userscore']
        collection.insert(data)



    except Exception as e:
        logger.exception('save user score Error:')
        logger.info("{0},score Input Error..".format(data['orderNo']))
        logger.info(str(traceback.format_exc()))


def generateMD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def getInfo(url, orderNo, my_sign):
    try:
        param = {'orderNo': orderNo, 'sign': my_sign}
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3, pool_connections=10, pool_maxsize=10))
        r = s.get(url, params=param, timeout=200)
        # print(r.text)
        return r.text
    except Exception as e:
        logger.exception('get user info Error:')
        logger.info("{0},getInfo  Error..".format(orderNo))
        logger.info(str(traceback.format_exc()))


def save_error(error_msg):
    try:
        # client = MongoClient('mongodb://tanteng:123456@localhost:27017/')
        client = MongoClient('mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
        db = client['test']
        collection = db['error']
        collection.insert(error_msg)

    except Exception as e:
        logger.exception('save errorInfo Error:')
        logger.info("{0},errorInfo input Error..".format(error_msg['orderNo']))
        logger.info(str(traceback.format_exc()))


def mergeData(orderNo, baseUrl, my_sign, reportUrl, operatorUrl):
    baseInfo = MyThread(getInfo, args=[baseUrl, orderNo, my_sign])
    reportInfo = MyThread(getInfo, args=[reportUrl, orderNo, my_sign])
    operatorInfo = MyThread(getInfo, args=[operatorUrl, orderNo, my_sign])
    baseInfo.start()
    reportInfo.start()
    operatorInfo.start()
    baseInfo.join()
    reportInfo.join()
    operatorInfo.join()

    baseInfo = json.loads(baseInfo.get_result().replace('$', ''))
    reportInfo = json.loads(reportInfo.get_result().replace('$', ''))
    operatorInfo = json.loads(operatorInfo.get_result().replace('$', ''))

    # 合并数据
    _data = {}
    _data.update(baseInfo['data'])
    _data.update(reportInfo['data'])
    _data.update(operatorInfo['data'])
    new_data = {'orderNo': baseInfo['orderNo'],
                'appId': baseInfo['appId'],
                "merchantId": baseInfo['merchantId'],
                'time': datetime.datetime.now()}
    new_data['data'] = _data

    return new_data
    # print(new_data)


# 规则得分入库入库
def saveRuleModelScore(model_data, ruleData):
    client = MongoClient('mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
    db = client['test']
    collection1 = db['rule_score']
    collection = db['model_score']
    collection.insert(model_data)
    collection1.insert(ruleData)
