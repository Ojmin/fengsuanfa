import datetime
import json
import os

import requests
from pymongo import MongoClient

from engine.risk_20181202 import param_generate, rule_data, final_score

# #
# 读数据库
from risk_20181202_bak import final_score
from tools import MyThread


# client = MongoClient(
#     'mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
# db = client['test']
# collection = db['user']
# cur = collection.find()
# j = 1
# for i in cur[:1000]:
#     # print(i)
#     i.pop('_id')
#     if 'time' in i.keys():
#         i.pop('time')

# model_type = 3
# r_data = MyThread(rule_data, [i, ])
# p_data = MyThread(param_generate, [i, model_type])
# r_data.start()
# p_data.start()
# r_data.join()
# p_data.join()
# # logger.info('{0}-get ruleData:'.format(order_data['orderNo']))
#
# ruleData = r_data.get_result()
# # logger.info('{0}-get model_data:'.format(order_data['orderNo']))
# model_data = p_data.get_result()
def run():
    client = MongoClient('mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717/')
    db = client.test
    # rule = db.rule_score  # 策略得分
    # model = db.model_score  # 模型得分
    userscore = db.userscore  ##最终得分

    # print('总体通过率:' + str(t / (sl - len(fail))))
    #
    # print('新户通过率:' + str(new_pa})ss / new))


if __name__ == "__main__":
    # from multiprocessing import Pool
    #
    # p = Pool(10)
    # program_number = 10
    # for x in range(program_number):
    #     p.apply_async(run)
    # p.close()
    # p.join()
    run()
# 规则得分入库入库
# logger.info('{0}-save ruleData and model_data:'.format(order_data['orderNo']))
# ths = Thread(target=saveRuleModelScore, args=(json.loads(model_data), ruleData))
# ths.start()
#     score = final_score(model_data, ruleData)
#     result_data = {"merchantId": i['merchantId'],
#                    "appId": i['appId'],
#                    "Time": datetime.datetime.now()}
#     result_data.update(json.loads(score))
#     # logger.info('{0}-save finally score...:'.format(order_data['orderNo']))
#     # # save_score(result_data)
#     # logger.info('{0}-save finally score SUCCESS:'.format(order_data['orderNo']))
#     print(result_data)
#     j += 1
#  cur.pop('_id')
# cur.pop('time')
# 算分
# i = 1
# for i in range(len([name for name in os.listdir('../aaa')])):
#     with open('../aaa/'+str(i+1)+'aaa.json', 'r', encoding='utf-8') as f:
#         cur = f.read()
#
#     # print(type(cur))
#         cur1 = json.loads(cur)
#         print(param_generate(cur1,3))
# b = rule_data(cur1)
# print(b)
#         i+=1
# r = requests.get('http://www.cnblogs.com/mvc/blog/GetComments.aspx?postId=8052579&blogApp=i-honey&pageIndex=0&anchorCommentId=0&_=1543564942220')
# print(r)
# print(r.text)
# j = 0
# print(len([name for name in os.listdir('../aaa')]))
# for i in range(len([name for name in os.listdir('../aaa')])):
#     with open('../aaa/' + str(i + 1) + 'aaa.json', 'r', encoding='utf-8') as f:
#         cur1 = f.read()
#         cur = json.loads(cur1)
#
#     if cur['data']['isAgain'] == 1:
#         j += 1
#     print(j)
# client = MongoClient('mongodb://root:Ii1mNI&1191^$(Y@dds-bp1da1e2b98c33b41436-pub.mongodb.rds.aliyuncs.com:3717')
# # client.adb.authenticate("test", "test", mechanism='MONGODB-CR')
# db=client['test']
# collection=db['ceshi']
# collection.insert({'name':"ceshi"})
# import smtplib
# smtp = smtplib
