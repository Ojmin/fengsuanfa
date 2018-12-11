# coding=utf-8

import traceback
from threading import Thread
import logging.handlers

import redis
from pymongo import MongoClient

from MultiprocessHandler import MultiprocessHandler
from tools import MyThread
from flask import Flask, request
import json
import logging
from engine.derivation_param import param_generate
from tools import save_data, save_score, generateMD5, getInfo
from warningSystem import send_mail

formattler = '%(levelname)s - %(name)s - %(asctime)s - %(message)s'
fmt = logging.Formatter(formattler)

# 获得logger，默认获得root logger对象
# 设置logger级别 debug
# root logger默认的级别是warning级别。
# 不设置的话 只能发送 >= warning级别的日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 使用我们写的多进程版Handler理器，定义日志输出到mylog.log文件内
#   文件打开方式默认为 a
#   按分钟进行日志切割
file_handler = MultiprocessHandler('/home/Model/logs/model_server_logs/flask_log', when='D', backupCount=7)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(fmt)
file_handler.suffix = "%Y-%m-%d.log"
# 对logger增加handler日志处理器
logger.addHandler(file_handler)

app = Flask(__name__)


@app.route('/sendInfo', methods=['POST'])
def baseinfo():
    if request.method == 'POST':
        json_data = request.get_data().decode('utf-8')
        try:
            try:
                # json_data = request.get_data().decode('utf-8')
                url_data = json.loads(json_data)
                sign = url_data.get('sign')

            except Exception as e:
                logger.exception('get sign Error:')
                logger.info(str(traceback.format_exc()))
                error_msg = {'msg': 'sign 获取失败'}
                return json.dumps(error_msg)
            else:
                my_sign = generateMD5('HZRESK001A20181122huichuanghuichuang666!')
                if my_sign == sign:

                    config = {'host': '127.0.0.1', 'port': 6379, 'db': 0, 'table': 'ts_order', 'password': 'foobared'}
                    con_redis = redis.Redis(host=config['host'], port=config['port'], db=config['db'],
                                            password=config['password'])
                    print(url_data.get('baseUrl'))
                    print(url_data.get('operatorUrl'))
                    redis_data = {
                        'reportUrl': url_data.get('reportUrl'),
                        'orderNo': url_data.get('orderNo'),
                        'operatorUrl': url_data.get('operatorUrl'),
                        'baseUrl': url_data.get('baseUrl')
                        # 'resultUrl': url_data['callBackResult']
                    }
                    con_redis.lpush(config['table'], json.dumps(redis_data))
                    logger.info('{0}...to redis Success'.format(url_data.get('orderNo')))
                    return json.dumps({'returnCode': 'SUCCESS'})
                else:

                    error_msg = {'msg': 'sign验证失败'}
                    return json.dumps(error_msg)
        except Exception as e:
            logger.info("{0},programe Error....".format(str(json.loads(json_data).get('orderNo'))))
            logger.info(traceback.format_exc())
            msg_data = {"returnCode": "FAIL", "errCode": " 1002 ", "errMsg": "联系管理员"}
            # send_mail('{0} 获取信息url时出错'.format(json.loads(json_data).get('orderNo')))
            return json.dumps(msg_data)


@app.route('/scores/', methods=['GET'])
def get_scores():
    if request.method == "GET":
        orderNo = request.args.get('orderNo')
        try:
            client = MongoClient(
                'mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
            db = client['test']
            cllection = db['userscore']
            userscore = cllection.find_one({'orderNo': orderNo})
            if userscore:
                score = {"merchantId": userscore['merchantId'],
                         "appId": userscore['appId'],
                         "orderNo": userscore['orderNo'],
                         "desc": userscore['desc'],
                         "status": userscore['status'],
                         "model_score_type": userscore['model_score_type'],
                         "model_score": userscore['model_score'],
                         "rule_score": userscore['rule_score'],
                         "comprehensive_score": userscore['comprehensive_score']}
                logger.info("{0},得分获取成功....".format(orderNo))
                return json.dumps(score)
            else:
                msg = {
                    "status": '处理中',
                    "orderNo": orderNo,
                }
                return json.dumps(msg)
        except Exception as e:
            #send_mail('{0}获取得分异常'.format(orderNo))
            return json.dumps({'msg': '请联系管理员'})


# @app.route('/heartBeat')
# def heartBeat():
#     if request.method == "GET":
#         try:
#             sign = request.args.get('sign')
#             if sign == '1':
#                 return json.dumps({"status": "1"})
#         except Exception as e:
#             return json.dumps({"status": "0"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
