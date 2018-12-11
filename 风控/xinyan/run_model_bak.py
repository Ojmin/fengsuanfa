# encoding:utf-8
import os
import sys
import traceback
import datetime
import json
from threading import Thread

import requests
import redis
import time
from warningSystem import send_mail

from engine.risk_20181202 import param_generate, rule_data, final_score

# -- logging ---
import logging.handlers
import logging

from tools import MyThread, getInfo, generateMD5, save_data, save_score, save_error, mergeData, saveRuleModelScore

# logging.basicConfig(
#     format='%(asctime)s-%(levelname)s-%(name)s-%(message)s'
# )
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# filehandler = logging.handlers.TimedRotatingFileHandler(
#     "/home/Model/logs/model_server_logs/model_log",
#     when='D',
#     interval=1,
#     backupCount=7,
# )
# filehandler.suffix = "%Y-%m-%d.log"
# logFormatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
# filehandler.setFormatter(logFormatter)
# logger.addHandler(filehandler)

from MultiprocessHandler import MultiprocessHandler

# 定义日志输出格式
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
file_handler = MultiprocessHandler('/home/Model/logs/model_server_logs/model_log', when='D', backupCount=7)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(fmt)
file_handler.suffix = "%Y-%m-%d.log"
# 对logger增加handler日志处理器
logger.addHandler(file_handler)


class Task_Dis():
    def __init__(self):
        self.error_data = {'mode_type': '00', "comprehensive_score": '', "desc": u"新户A卡评分", "status": "DENY"}

    # 获取模型源数据-- 征信报告 接口
    def source_data(self, redis_data):
        order_data = json.loads(redis_data)  # 订单号，推送接口，征信接口
        try:
            # 获取数据
            orderNo = order_data['orderNo']
            reportUrl = order_data['reportUrl']
            operatorUrl = order_data['operatorUrl']
            baseUrl = order_data['baseUrl']

            my_sign = generateMD5('HZRESK001A20181122huichuanghuichuang666!')
            try:
                # 合并数据
                new_data = mergeData(orderNo, baseUrl, my_sign, reportUrl, operatorUrl)
                # 保存数据
                logger.info('save {0} original data ...'.format(str(new_data['orderNo'])))

                save_data(new_data)
                logger.info('{0}-SUCCESS'.format(str(new_data['orderNo'])))

            except Exception as e:
                msg = '{0} 保存 数据失败 {1}'.format(str(order_data['orderNo']), datetime.datetime.now())
                logger.info(msg)
                result_data = {
                    "desc": '-1',
                    "status": "内部错误",
                    "orderNo": order_data['orderNo'],
                    "mode_type": '',
                    "comprehensive_score": "0"}
                save_score(result_data)
                # send_mail('msg')

            else:

                # 计算

                try:
                    model_type = 3
                    r_data = MyThread(rule_data, [new_data, ])
                    p_data = MyThread(param_generate, [new_data, model_type])
                    r_data.start()
                    p_data.start()
                    r_data.join()
                    p_data.join()
                    logger.info('{0}-get ruleData:'.format(order_data['orderNo']))

                    ruleData = r_data.get_result()
                    logger.info('{0}-get model_data:'.format(order_data['orderNo']))
                    model_data = p_data.get_result()

                    # 规则得分入库入库
                    logger.info('{0}-save ruleData and model_data:'.format(order_data['orderNo']))
                    ths = Thread(target=saveRuleModelScore, args=(json.loads(model_data), ruleData))
                    ths.start()
                    score = final_score(model_data, ruleData)
                    result_data = {"merchantId": new_data['merchantId'],
                                   "appId": new_data['appId'],
                                   "Time": datetime.datetime.now()}
                    result_data.update(json.loads(score))
                    logger.info('{0}-save finally score...:'.format(order_data['orderNo']))
                    save_score(result_data)
                    logger.info('{0}-save finally score SUCCESS:'.format(order_data['orderNo']))


                except Exception as e:
                    msg1 = '{0} param_generate or rule_data ERROR'.format(new_data['orderNo'])
                    logger.info(msg1)
                    result_data = {
                        "merchantId": "",
                        "appId": "",
                        "desc": '-3',
                        "status": "内部错误",
                        "orderNo": order_data['orderNo'],
                        "mode_type": '',
                        "comprehensive_score": "0"}
                    save_score(result_data)
                    # send_mail(msg1)
        except Exception as e:
            #  返回模型分数 为 0
            msg2 = '{0}-source_data Error:'.format(order_data['orderNo'])
            logger.info(msg2)
            logger.info(traceback.format_exc())
            # 保存本地
            error_msg = str(traceback.format_exc()).replace('"', "'").replace('\n', '')
            error_msg_dict = {
                'orderNo': order_data['orderNo'],
                "error_msg": str(error_msg),
                'error_type': 2
            }
            save_error(error_msg_dict)
            result_data = {
                "merchantId": "",
                "appId": "",
                "desc": '-2',
                "status": "内部错误",
                "orderNo": order_data['orderNo'],
                "mode_type": '',
                "comprehensive_score": "0"}
            save_score(result_data)
            # send_mail(msg2)

def run(data=None):
    try:
        # 测试服务器
        # config = {"host": "127.0.0.1", "port": 6379, "db": 0, "table": "ts_order", "password": ""}
        config = {"host": "127.0.0.1", "port": 6379, "db": 0, "table": "ts_order", "password": ""}
        r = redis.StrictRedis(host=config['host'], port=config['port'], db=config['db'], password=config['password'])
        class_func = Task_Dis()

        order_data1 = r.brpop(config['table'])
        order_data = order_data1[1]
        if order_data:
            class_func.source_data(order_data)
        else:
            pass
        while True:
            order_data1 = r.brpop(config['table'])
            order_data = order_data1[1]
            if order_data:
                class_func.source_data(order_data)
            else:
                time.sleep(1)
    except Exception as e:
        error_msg = traceback.format_exc()
        # send_mail(error_msg)


if __name__ == "__main__":
    from multiprocessing import Pool

    p = Pool(10)
    program_number = 10
    for x in range(program_number):
        p.apply_async(run, args=(x,))
    p.close()
    p.join()
    run()
