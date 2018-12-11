# encoding:utf-8
import datetime
import os
import sys

from pymongo import MongoClient

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import traceback
import json
import pandas as pd
from pandasql import sqldf
import numpy as np
import time
from .ASC20180512003001 import score_card  # tongyong V1
from .ASC20180512003002 import score_card_2  # tongyong V2
from .ASC20180522004001 import score_card_xmall  # shangcheng
from .ASC20180522005001 import score_card_recycle  # huishou maibei
from .ASC20180801_hdd import score_card_0801  # 长期表现
from .ASC20181121_new_xinyan import score_card_xinyan_nods  # 新新颜评分卡
from .Model_V4_2_ascore_20180803 import score_card_tc  # 天创数据
# from engine.ASC20180512003001 import score_card  # tongyong V1
# from engine.ASC20180512003002 import score_card_2  # tongyong V2
# from engine.ASC20180522004001 import score_card_xmall  # shangcheng
# from engine.ASC20180522005001 import score_card_recycle  # huishou maibei
# from engine.ASC20180801_hdd import score_card_0801  # 长期表现
# from engine.ASC20181121_new_xinyan import score_card_xinyan_nods  # 新新颜评分卡
# from engine.Model_V4_2_ascore_20180803 import score_card_tc  # 天创数据
import random

# -- logging ---
import logging
import logging.handlers

logging.basicConfig(
    format='%(asctime)s-%(levelname)s-%(name)s-%(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler(
    # '/home/Model/logs/model_server_logs/model_log',
    "model_log1",
    when='D',
    interval=1,
    backupCount=7,
)
filehandler.suffix = "%Y-%m-%d.log"
logFormatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
filehandler.setFormatter(logFormatter)
logger.addHandler(filehandler)


def param_generate(text, model_type):
    try:
        appId = str(text['appId'])
        merchantId = str(text['merchantId'])
        zw_order = str(text['data']['orderNo'])
        userid = str(text['data']['userid'])  # 用户中心
        productCode = str(text['data']['productCode'])
        order_time = str(text['data']['order_time'])
        error_data = {'mode_type': '00', "userid": str(userid), "comprehensive_score": '200', "desc": u"新户A卡评分",
                      "status": "DENY", "loanOrderNo": str(zw_order), "productCode": str(productCode)}

        if text['data']:
            if text['data']['isAgain'] == 0:
                # 花呗额度
                # 已删
                huabei_base_data = text['data']['moxieTaobao']
                if huabei_base_data:
                    huabei_totalcreditamount = huabei_base_data[
                        'alipaywealth'] if 'alipaywealth' in huabei_base_data.keys() else ''
                    # 判断 花呗值 单位
                    huabei_totalcreditamount = str(float(
                        huabei_totalcreditamount) / 1) if 'MB' in productCode and huabei_totalcreditamount != '' else str(
                        huabei_totalcreditamount)
                else:
                    huabei_totalcreditamount = ''
                logger.info('{0},花呗额度，huabei_totalcreditamount:{1}'.format(zw_order, str(huabei_totalcreditamount)))
                # 通话记录
                try:
                    order_time = int(text["data"]["order_time"])
                    time_local = time.localtime(order_time)
                    order_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    if text["data"]["scorpionOriginalData"]:
                        call_list = []
                        for i in range(len(text["data"]["scorpionOriginalData"]["calls"])):
                            for j in range(len(text["data"]["scorpionOriginalData"]["calls"][i]["items"])):
                                call_info = {}
                                call_info["order_time"] = order_time
                                call_info["fee"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j]["fee"]
                                call_info["duration"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j][
                                    "duration"]
                                call_info["location"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j][
                                    "location"]
                                call_info["time"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j]["time"]
                                call_info["details_id"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j][
                                    "details_id"]
                                call_info["dial_type"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j][
                                    "dial_type"]
                                call_info["location_type"] = \
                                    text["data"]["scorpionOriginalData"]["calls"][i]["items"][j][
                                        "location_type"]
                                call_info["peer_number"] = text["data"]["scorpionOriginalData"]["calls"][i]["items"][j][
                                    "peer_number"]
                                call_list.append(call_info)
                        data1 = pd.DataFrame(call_list)
                    else:
                        # call_base_list = text['data']['loanBondOrignalData']['data'][0]['calls'] if text['data']['loanBondOrignalData'] else []
                        call_base_param = text['data']['loanBondOrignalData'][1]['message']
                        logger.info('{0},calls:{1}'.format(str(zw_order), call_base_param))
                        call_base_list = text['data']['loanBondOrignalData'][0]['calls'] if '获取原始数据成功' else []
                        if call_base_list:
                            logger.info('{0},calls:{1}'.format(str(zw_order), json.dumps(call_base_list[0])))
                            call_list = list(map(lambda x: {
                                'duration': 0 if x['use_time'] == None else int(
                                    x['use_time'] if x['use_time'] != '' else 0),
                                'location': x['place'],
                                'time': x['start_time'],
                                'dial_type': x['init_type'],
                                'location_type': x['call_type'],
                                'peer_number': x['other_cell_phone'],
                                'order_time': order_time,
                                'update_time': x['update_time']
                            }, call_base_list))
                            logger.info('{0},通话记录{1}个'.format(zw_order, str(len(call_list))))
                        else:
                            # 运营商数据 为空
                            call_list = []
                            logger.info('{0},loanBondOrignalData.data.calls is empty'.format(str(zw_order)))
                except Exception as e:
                    call_list = []
                    logger.info('{0},通话记录解析错误'.format(zw_order))
                    logger.info(traceback.format_exc())
                finally:
                    columns_base = ['duration', 'location', 'time', 'dial_type', 'location_type', 'peer_number',
                                    'order_time', 'update_time']
                    data1 = pd.DataFrame(call_list, columns=columns_base)

                # 通讯录
                try:
                    mail_list = text['data']['mailList']
                    mail_data = {'contact_phone': list(map(lambda x: x['phone'], mail_list)),
                                 'name': list(map(lambda x: x['name'], mail_list))}
                    data4 = pd.DataFrame(mail_data)
                except Exception as e:
                    logger.info(traceback.format_exc())

                # 电商 -- 20180523
                try:
                    order_time = int(text["data"]["order_time"])
                    time_local = time.localtime(order_time)
                    order_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    if text['data']['moxieTaobao']:
                        tb_base_list = text['data']['moxieTaobao']['tradedetails']['tradedetails']
                        tb_list = list(map(lambda x: {
                            'trade_text': x['trade_text'],
                            #                    'time':x['trade_createtime'].split('T')[0],
                            'time': x['trade_createtime'].replace('T', ' ').replace('.000+08', '').strip(),
                            'actual_fee': float(x['actual_fee']) / 100 if 'MB' in productCode and x[
                                'actual_fee'] != '' else float(x['actual_fee']),
                            'order_time': order_time
                        }, tb_base_list))
                    else:
                        tb_list = []
                    logger.info('{0},电商交易{1}个'.format(zw_order, str(len(tb_list))))
                except Exception as e:
                    tb_list = []
                    logger.info('{0},电商记录解析错误'.format(zw_order))
                    logger.info(traceback.format_exc())
                finally:
                    columns_base_tb = ['trade_text', 'time', 'actual_fee', 'order_time']
                    data3 = pd.DataFrame(tb_list, columns=columns_base_tb)

                if call_list:
                    # 静默超过1天次数
                    try:
                        time_next = []
                        for i in range(len(data1) - 1):
                            time_info = {}
                            time_info['next'] = data1['time'][i]
                            time_next.append(time_info)
                        data2 = pd.DataFrame(time_next)
                        data2 = pd.DataFrame(sqldf("select next from data2 order by next asc"))
                        time_next_1 = []
                        for i in range(len(data2) - 1):
                            time_info_1 = {}
                            time_info_1['next'] = data2['next'][i]
                            time_info_1['current'] = data2['next'][i + 1]
                            time_next_1.append(time_info_1)
                        data2 = pd.DataFrame(time_next_1)
                        # datediff(next_start_time, start_time, 'hh') > 24
                        # silent_ge_1 = np.array(sqldf("select sum(case when next>datetime(current,'1 days') then 1 else 0 end)  from data2;"))
                        silent_ge_1 = np.array(sqldf(
                            "select sum(case when abs(julianday(next)-julianday(current))>1 then 1 else 0 end)  from data2;"))
                        silent_ge_2 = np.array(sqldf(
                            "select sum(case when abs(julianday(next)-julianday(current))>2 then 1 else 0 end)  from data2;"))
                        silent_ge_1 = float(silent_ge_1)
                        silent_ge_2 = float(silent_ge_2)
                    except Exception as e:
                        silent_ge_1 = ''
                        silent_ge_2 = ''
                        logger.info('{0},silent_ge_1 param Error...'.format(zw_order))
                        logger.info(traceback.format_exc())
                    logger.info(
                        '{0},静默超过1天次数,silent_ge_1:{1},静默超过2天次数,silent_ge_2:{2}'.format(zw_order, str(silent_ge_1),
                                                                                       str(silent_ge_2)))

                    # 最近1个月和3个月的比值，最近3个月和6个月的比值，（被叫)
                    try:
                        (
                            month1_called,
                            month3_called,
                            month6_called,
                            month3_called_update,
                            month6_called_update,
                            month1_called_update
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-30 days') and time<order_time and dial_type like '%被叫%' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and dial_type like '%被叫%' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-180 days') and time<order_time and dial_type like '%被叫%' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-90 days') and time<update_time and dial_type like '%被叫%' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-180 days') and time<update_time and dial_type like '%被叫%' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-30 days') and time<update_time and dial_type like '%被叫%' THEN 1 ELSE 0 END)  from data1;"))
                        )

                        contimes_called_90_180_rate = float(month3_called) / float(month6_called) if float(
                            month6_called) != float(0) else ''
                        contimes_called_30_90_rate = float(month1_called) / float(month3_called) if float(
                            month3_called) != float(0) else ''
                        contimes_called_90_180_rate_new = float(month3_called_update) / float(
                            month6_called_update) if float(month6_called_update) != float(0) else ''
                        contimes_called_30_90_rate_new = float(month1_called_update) / float(
                            month3_called_update) if float(
                            month3_called_update) != float(0) else ''
                    except Exception as e:
                        contimes_called_90_180_rate = contimes_called_30_90_rate = contimes_called_90_180_rate_new = contimes_called_30_90_rate_new = ''
                        logger.info('{0}最近1个月和3个月的比值，最近3个月和6个月的比值, 最近3个月和6个月的比值(新) 获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},最近3个月被叫个数,month3_called:{1},6个月的被叫个数,month6_called:{2},比值:{3}'.format(zw_order,
                                                                                                               str(
                                                                                                                   float(
                                                                                                                       month3_called)),
                                                                                                               str(
                                                                                                                   float(
                                                                                                                       month6_called)),
                                                                                                               str(
                                                                                                                   contimes_called_90_180_rate)))
                        logger.info('{0},最近1个月被叫个数,month1_called:{1},3个月的被叫个数,month3_called:{2},比值:{3}'.format(zw_order,
                                                                                                               str(
                                                                                                                   float(
                                                                                                                       month1_called)),
                                                                                                               str(
                                                                                                                   float(
                                                                                                                       month3_called)),
                                                                                                               str(
                                                                                                                   contimes_called_30_90_rate)))
                        logger.info(
                            '{0},最近3个月被叫个数,month3_called_update:{1},6个月的被叫个数,month6_called_update:{2},比值:{3}'.format(
                                zw_order, str(float(month3_called_update)), str(float(month6_called_update)),
                                str(contimes_called_90_180_rate_new)))
                        logger.info(
                            '{0},最近1个月被叫个数,month1_called_update:{1},3个月的被叫个数,month3_called_update:{2},比值:{3}'.format(
                                zw_order, str(float(month1_called_update)), str(float(month3_called_update)),
                                str(contimes_called_30_90_rate_new)))
                        # 最近180天订单金额求和
                    try:
                        orderfee_180d = np.array(sqldf(
                            "select sum(case when time>=datetime(order_time,'-180 days') and time<order_time then actual_fee else 0 end) from (select trade_text,time,actual_fee,order_time from data3 where trade_text='交易成功');"))
                    except Exception as e:
                        orderfee_180d = ''
                        logger.info('{0}最近180天订单金额求和 获取失败：'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},最近180天订单金额求和:{1}'.format(zw_order, str(orderfee_180d)))

                    # 一个星期内和三个月内30秒以内的被叫通话次数
                    try:

                        (
                            day7_called,
                            day90_called
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-07 days') and time<order_time and dial_type like '%被叫%' and duration<30 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and dial_type like '%被叫%' and duration<30 THEN 1 ELSE 0 END)  from data1;")),

                        )
                        contimes_called_30s_7_90_rate = float(day7_called) / float(day90_called) if float(
                            day90_called) != float(0) else ''
                    except Exception as e:
                        contimes_called_30s_7_90_rate = ''
                        logger.info('{0},一个星期内和三个月内30秒以内的被叫通话次数获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},一个星期内30s内被叫次数,day7_called:{1},3个月内30s内被叫次数,day90_called:{2},比值:{3}'
                                    .format(zw_order, str(float(day7_called)), str(float(day90_called)),
                                            str(contimes_called_30s_7_90_rate)))

                    # ----------  新新颜 ----------
                    # 一个星期内和三个月内30秒以内的被叫通话次数
                    try:

                        (
                            day7_called,
                            day90_called
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-07 days') and time<update_time and dial_type like '%被叫%' and duration<30 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-90 days') and time<update_time and dial_type like '%被叫%' and duration<30 THEN 1 ELSE 0 END)  from data1;")),

                        )
                        contimes_called_30s_7_90_rate_new_xinyan = float(day7_called) / float(day90_called) if float(
                            day90_called) != float(0) else ''
                    except Exception as e:
                        contimes_called_30s_7_90_rate_new_xinyan = ''
                        logger.info('{0},一个星期内和三个月内30秒以内的被叫通话次数获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},一个星期内30s内被叫次数,day7_called:{1},3个月内30s内被叫次数,day90_called:{2},比值:{3}'
                                    .format(zw_order, str(float(day7_called)), str(float(day90_called)),
                                            str(contimes_called_30s_7_90_rate_new_xinyan)))
                    # ----------  新新颜 ----------

                    # 一个星期内和三个月内20秒以内的被叫通话次数
                    try:

                        (
                            day7_called_20,
                            day90_called_20
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-07 days') and time<order_time and dial_type like '%被叫%' and duration<20 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and dial_type like '%被叫%' and duration<20 THEN 1 ELSE 0 END)  from data1;")),
                        )
                        contimes_called_20s_7_90_rate = float(day7_called_20) / float(day90_called_20) if float(
                            day90_called_20) != float(0) else ''
                    except Exception as e:
                        contimes_called_20s_7_90_rate = ''
                        logger.info('{0},一个星期内和三个月内20秒以内的被叫通话次数获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},一个星期内20s内被叫次数,day7_called_20:{1},3个月内20s内被叫次数,day90_called_20:{2},比值:{3}'
                                    .format(zw_order, str(float(day7_called_20)), str(float(day90_called_20)),
                                            str(contimes_called_20s_7_90_rate)))

                    try:
                        # 一个月内5秒以内的被叫通话次数,一个月内20秒以内的被叫通话次数,三个月内5秒以内的通话次数
                        (
                            day30_call_5s,
                            day30_call_20s,
                            day90_call_5s
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-30 days') and time<order_time and dial_type like '%被叫%' and duration<5 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-30 days') and time<order_time and dial_type like '%被叫%' and duration<20 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and duration<5 THEN 1 ELSE 0 END)  from data1;")),
                        )
                        (contimes_called_5s_30days, contimes_called_20s_30days, contimes_5s_90days) = (
                            float(day30_call_5s), float(day30_call_20s), float(day90_call_5s))
                    except Exception as e:
                        contimes_called_5s_30days = contimes_called_20s_30days = contimes_5s_90days = ''
                        logger.info('{0},一个月内5秒以内的被叫通话次数,一个月内20秒以内的被叫通话次数,三个月内5秒以内的通话次数获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},一个月内5秒被叫次数:{1},一个月内20秒被叫次数:{2},三个月内5秒以内的通话次数:{3}'.format(zw_order,
                                                                                                  contimes_called_5s_30days,
                                                                                                  contimes_called_20s_30days,
                                                                                                  contimes_5s_90days))

                    # ----   新新颜参数  ----
                    try:
                        # 一个月内5秒以内的被叫通话次数,一个月内20秒以内的被叫通话次数,三个月内5秒以内的通话次数
                        (
                            day30_call_5s,
                            day30_call_20s,
                            day90_call_5s
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-30 days') and time<update_time and dial_type like '%被叫%' and duration<5 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-30 days') and time<update_time and dial_type like '%被叫%' and duration<20 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-90 days') and time<update_time and duration<5 THEN 1 ELSE 0 END)  from data1;")),
                        )
                        (contimes_called_5s_30days, contimes_called_20s_30days_new_xinyan, contimes_5s_90days) = (
                            float(day30_call_5s), float(day30_call_20s), float(day90_call_5s))
                    except Exception as e:
                        contimes_called_5s_30days = contimes_called_20s_30days_new_xinyan = contimes_5s_90days = ''
                        logger.info('{0},一个月内5秒以内的被叫通话次数,一个月内20秒以内的被叫通话次数,三个月内5秒以内的通话次数获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},一个月内5秒被叫次数:{1},一个月内20秒被叫次数:{2},三个月内5秒以内的通话次数:{3}'.format(zw_order,
                                                                                                  contimes_called_5s_30days,
                                                                                                  contimes_called_20s_30days_new_xinyan,
                                                                                                  contimes_5s_90days))
                    # ----   新新颜参数  ----

                    try:
                        # 最近30天1点到8点通话个数计数
                        (
                            day30_time_1_8,
                            day30_time_8_12,
                            day7_time_22_1,
                            day30_time_22_1,
                            day7_time_8_12,
                            day30_call_cnt,
                            day180_call_cnt,
                            day30_number
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(order_time,'-30 days') and time<order_time and substr(time,12,2) <'08' and substr(time,12,2)>='01' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(order_time,'-30 days') and time<order_time and substr(time,12,2) <'12' and substr(time,12,2)>='08' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(order_time,'-7 days') and time<order_time and substr(time,12,2) <'01' or substr(time,12,2)>='22' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(update_time,'-30 days') and time<update_time and substr(time,12,2) <'01' or substr(time,12,2)>='22' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(update_time,'-7 days') and time<update_time and substr(time,12,2) <'12' and substr(time,12,2)>='08' THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(update_time,'-30 days') and time<update_time THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time >=datetime(update_time,'-180 days') and time<update_time THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select count(distinct CASE WHEN time >=datetime(update_time,'-30 days') and time<update_time THEN peer_number ELSE null END) from data1;"))

                        )
                        contimes_30days_1_to_8 = float(day30_time_1_8)
                        contimes_30days_8_to_12 = float(day30_time_8_12)
                        contimes_7days_22_to_1 = float(day7_time_22_1)
                        contimes_30days_22_to_1 = float(day30_time_22_1)
                        contimes_7days_8_to_12 = float(day7_time_8_12)
                        contimes_30_180_rate = float(day30_call_cnt) / float(day180_call_cnt) if float(
                            day180_call_cnt) != float(0) else ''
                        conode_30days = int(day30_number)
                    except Exception as e:
                        contimes_30days_1_to_8 = contimes_30days_8_to_12 = contimes_7days_22_to_1 = contimes_30days_22_to_1 = contimes_30_180_rate = conode_30days = ''
                        logger.info(
                            '{0},最近30天1点到8点通话个数计数获取失败, 最近30天22点到1点通话个数计数获取失败, 最近7天8点到12点通话个数计数,最近30天通话个数计数与最近180天通话个数计数比值, 最近30天通话联系人, 获取失败'.format(
                                zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info(
                            '{0},最近30天1点到8点通话个数:{1},最近30天8点到12点通话个数:{2},最近7天22点到1点通话个数计数:{3},最近30天22点到1点通话个数计数:{4},最近7天8点到12点通话个数计数:{5},最近30天通话个数计数与最近180天通话个数计数比值:{6},最近30天通话联系人:{7}'.format(
                                zw_order,
                                contimes_30days_1_to_8,
                                contimes_30days_8_to_12,
                                contimes_7days_22_to_1,
                                contimes_30days_22_to_1,
                                contimes_7days_8_to_12,
                                contimes_30_180_rate,
                                conode_30days
                            )
                        )

                    try:

                        # 最近30天1点到8点通话个数计数与最近30天通话个数计数比值
                        day30_call = np.array(sqldf(
                            "select SUM(CASE WHEN time>=datetime(order_time,'-30 days') and time<order_time THEN 1 ELSE 0 END)  from data1;"))
                        day30_call_number = float(day30_call)
                        contimes_1_to_8c_30days_rate = float(
                            contimes_30days_1_to_8 / day30_call_number) if day30_call_number != float(0) else ''
                    except Exception as e:
                        contimes_1_to_8c_30days_rate = ''
                        logger.info('{0},最近30天1点到8点通话个数计数与最近30天通话个数计数比值,获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info(
                            '{0},最近30天通话个数:{1},近30天1点到8点通话个数计数与最近30天通话个数计数比值:{2}'.format(zw_order, day30_call_number,
                                                                                         contimes_1_to_8c_30days_rate))

                    try:
                        # 通话1分钟以下的电话数
                        call_lt_min = np.array(sqldf(
                            "select count(distinct case when duration<60 then peer_number else null end) as num from data1;"))

                        call_lt_min = float(call_lt_min)
                    except Exception as e:
                        call_lt_min = ''
                        logger.info('{0},通话1分钟以下的电话数,获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},通话1分钟以下的电话数:{1}'.format(zw_order, call_lt_min))

                    try:
                        # 三个月内10秒以内的被叫通话次数,三个月内5秒以内的被叫通话次数,三个月内20秒以内的主叫通话次数,一个星期内和一个月内60秒以内的被叫通话次数,一个星期内10秒以内的被叫通话次数
                        (
                            day90_called_10s,
                            day90_called_5s,
                            day90_call_20s,
                            day7_called_60s,
                            day30_called_60s,
                            day7_called_10s
                        ) = (
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and dial_type like '%被叫%' and duration<10 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and dial_type like '%被叫%' and duration<5 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(order_time,'-90 days') and time<order_time and dial_type like '%主叫%' and duration<20 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-7 days') and time<update_time and dial_type like '%被叫%' and duration<60 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-30 days') and time<update_time and dial_type like '%被叫%' and duration<60 THEN 1 ELSE 0 END)  from data1;")),
                            np.array(sqldf(
                                "select SUM(CASE WHEN time>=datetime(update_time,'-7 days') and time<update_time and dial_type like '%被叫%' and duration<10 THEN 1 ELSE 0 END)  from data1;"))

                        )
                        (contimes_called_10s_90days, contimes_called_5s_90days, contimes_calls_20s_90days,) = (
                            float(day90_called_10s), float(day90_called_5s), float(day90_call_20s))
                        contimes_called_60s_7_30_rate = float(day7_called_60s) / float(day30_called_60s) if float(
                            day30_called_60s) != float(0) else ''
                        contimes_called_10s_7days = float(day7_called_10s)

                    except Exception as e:
                        contimes_called_10s_90days = contimes_called_5s_90days = contimes_calls_20s_90days = contimes_called_60s_7_30_rate = contimes_called_10s_7days = ''
                        logger.info(
                            '{0},三个月内10秒以内的被叫通话次数,三个月内5秒以内的被叫通话次数,三个月内20秒以内的主叫通话次数,一个星期内和一个月内60秒以内的被叫通话次数,一个星期内10秒以内的被叫通话次数, 获取失败:'.format(
                                zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info(
                            '{0},三个月内10秒以内的被叫通话次数:{1},三个月内5秒以内的被叫通话次数:{2},三个月内20秒以内的主叫通话次数:{3},一个星期内和一个月内60秒以内的被叫通话次数:{4},一个星期内10秒以内的被叫通话次数:{5}'.format(
                                zw_order,
                                contimes_called_10s_90days,
                                contimes_called_5s_90days,
                                contimes_calls_20s_90days,
                                contimes_called_60s_7_30_rate,
                                contimes_called_10s_7days
                            ))
                    # xinyan add param
                    contimes_called_5s_90days = np.array(sqldf(
                        "select SUM(CASE WHEN time>=datetime(update_time,'-90 days') and time<update_time and dial_type like '%被叫%' and duration<5 THEN 1 ELSE 0 END)  from data1;"))
                    contimes_called_5s_90days = list(map(lambda x: x[0], contimes_called_5s_90days))[
                        0] if contimes_called_5s_90days else ''

                    # xinyan add param
                    try:
                        # 通话一次的手机号数量
                        call_1 = np.array(sqldf(
                            "select sum(case when times = 1 then 1 else 0 end)as call_1 from (select peer_number,count(time) as times from data1 group by peer_number);"))
                        call_1 = float(call_1) if call_1 else ''

                    except Exception as e:
                        call_1 = ''
                        logger.info('{0},通话一次的手机号数量 获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},通话一次的手机号数量:{1}'.format(zw_order, str(call_1)))
                    try:
                        # 历史平均联系人通话时长
                        avg_time = np.array(sqldf(
                            "select case when count(peer_number) is not null and count(peer_number) != 0 then sum(time_span)/count(peer_number)  else 0 end as num from (select peer_number,sum(duration) as time_span from data1 group by peer_number);"))
                        avg_time = float(avg_time) if avg_time else ''
                    except Exception as e:
                        avg_time = ''
                        logger.info('{0},历史平均联系人通话时长 获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},历史平均联系人通话时长:{1}'.format(zw_order, avg_time))

                    try:
                        # nbr_call_30s 是中间变量 -- 总通话时间在30秒以上的联系人
                        # nbr_call_30s 是中间变量 -- 总通话时间在30秒以上的联系人
                        nbr_call_30s = float(np.array(sqldf(
                            "select count(distinct peer_number) from (select peer_number,sum(duration) as a from data1 group by peer_number) where a>30;")))
                        # nodes 是中间变量 -- 有通话的电话号码个数
                        nodes = float(np.array(sqldf("select count(distinct peer_number) from data1;")))
                        # nbr_cont_3m 是中间变量 -- 过去3个月有过通话的联系人
                        nbr_cont_3m = float(np.array(sqldf(
                            "select count(distinct case when julianday(update_time)-julianday(time)<91 and time<update_time then peer_number else null end) from data1;")))
                        # nbr_cont_early_morning 是中间变量 -- 在0:00 - 5:00这个时间段通过电话联系人
                        nbr_cont_early_morning = float(np.array(sqldf(
                            "select count(distinct case when substr(time,12,2) <'05' and substr(time,12,2)>='00' then peer_number else null end) from data1;")))
                        # nbr_cont_morning 是中间变量 -- 在[5:00 , 12:00)这个时间段通过电话联系人
                        nbr_cont_morning = float(np.array(sqldf(
                            "select count(distinct case when substr(time,12,2) <'12' and substr(time,12,2)>='05' then peer_number else null end) from data1;")))
                        # nbr_contact_1w 是中间变量 -- 过去7天通话联系人个数
                        nbr_contact_1w = float(np.array(sqldf(
                            "select count(distinct case when julianday(update_time)-julianday(time)<8 and time<update_time then peer_number else null end) from data1;")))
                        # 这里正式计算
                        if nodes > 0:
                            pct_nbr_call_30s = round(float(nbr_call_30s / nodes) * 100, 2)
                            pct_nbr_cont_3m = round(float(nbr_cont_3m / nodes) * 100, 2)
                            pct_nbr_cont_early_morning = round(float(nbr_cont_early_morning / nodes) * 100, 2)
                            pct_nbr_cont_morning = round(float(nbr_cont_morning / nodes) * 100, 2)
                        elif nodes == 0:  # 分母等于0
                            pct_nbr_call_30s = -9999976
                            pct_nbr_cont_3m = -9999976
                            pct_nbr_cont_early_morning = -9999976
                            pct_nbr_cont_morning = -9999976
                        else:  # 手机通话记录报告，若未取到报告，则取值99999999
                            pct_nbr_call_30s = 99999999
                            pct_nbr_cont_3m = 99999999
                            pct_nbr_cont_early_morning = 99999999
                            pct_nbr_cont_morning = 99999999

                        if nbr_cont_3m > 0:
                            pct_nbr_contact_1w_to_3m = round(float(nbr_contact_1w / nbr_cont_3m) * 100, 2)
                        elif nbr_cont_3m == 0:
                            pct_nbr_contact_1w_to_3m = -9999976
                        else:
                            pct_nbr_contact_1w_to_3m = 99999999

                    except Exception as e:
                        pct_nbr_call_30s = 99999999
                        pct_nbr_cont_3m = 99999999
                        pct_nbr_cont_early_morning = 99999999
                        pct_nbr_cont_morning = 99999999
                        pct_nbr_contact_1w_to_3m = 99999999
                        logger.info(
                            '{0},总通话时间在30秒以上的联系人数,过去3个月有过通话的联系人个数,在0-5时间段通话联系人,在[5:00 , 12:00)时间段通话联系人,过去7天过通话的联系人个数 获取失败:'.format(
                                zw_order))
                        logger.info(traceback.format_exc())

                    # 通讯录手机号码占总数的比值
                    try:
                        contact_nbr = np.array(
                            sqldf("select count(distinct contact_phone) from data4 WHERE length(contact_phone)>=7;"))
                        cell_nbr = np.array(sqldf(
                            "select sum(case when (length(contact_phone)=11 and substr(contact_phone,1,1) = '1') or (length(contact_phone)=13 and substr(contact_phone,1,2) = '86') then 1 else 0 end) from data4;"))
                        cell_rate = float(cell_nbr) / float(contact_nbr) if float(contact_nbr) != float(0) else ''

                    except Exception as e:
                        cell_rate = ''
                        logger.info('{0}, 通讯录手机号码占总数的比值获取失败:'.format(zw_order))
                        logger.info(traceback.format_exc())
                    finally:
                        logger.info('{0},通讯录手机号码占总数的比值:{1}'.format(zw_order, cell_rate))

                    # 黄定存 添加 衍生 变量
                    conspan_called_7_days = np.array(sqldf(
                        "select sum(case when time>=datetime(update_time,'-7 days') and time<update_time and dial_type like '%被叫%' then duration else 0 end) from data1;"))
                    conspan_called_7_days = list(map(lambda x: x[0], conspan_called_7_days))[0]
                    vip_count = ''  # !!!text['data']['moxieTaobao']['userinfo']['vip_count'] if text['data']['moxieTaobao'] else ''
                    # 黄定存 添加 衍生 变量

                    # 数据整理
                    model = {
                        'huabei_totalcreditamount': huabei_totalcreditamount,
                        'silent_ge_1': silent_ge_1,
                        'contimes_called_90_180_rate': contimes_called_90_180_rate,
                        'contimes_called_30_90_rate': contimes_called_30_90_rate,
                        'contimes_called_30s_7_90_rate': contimes_called_30s_7_90_rate,
                        'contimes_30days_1_to_8': contimes_30days_1_to_8,
                        'contimes_called_5s_30days': contimes_called_5s_30days,
                        'contimes_7days_22_to_1': contimes_7days_22_to_1,
                        'contimes_30days_8_to_12': contimes_30days_8_to_12,
                        'contimes_called_20s_30days': contimes_called_20s_30days,
                        'contimes_5s_90days': contimes_5s_90days,

                        'pct_nbr_call_30s': pct_nbr_call_30s,
                        'pct_nbr_cont_3m': pct_nbr_cont_3m,
                        'pct_nbr_cont_early_morning': pct_nbr_cont_early_morning,
                        'pct_nbr_cont_morning': pct_nbr_cont_morning,
                        'pct_nbr_contact_1w_to_3m': pct_nbr_contact_1w_to_3m,
                        'contimes_called_20s_7_90_rate': contimes_called_20s_7_90_rate,
                        "orderfee_180d": float((orderfee_180d[0][0])) if orderfee_180d[0][0] != None else float(
                            99999999),

                        "contimes_30days_22_to_1": contimes_30days_22_to_1,
                        "contimes_called_90_180_rate_new": contimes_called_90_180_rate_new,
                        "contimes_called_30_90_rate_new": contimes_called_30_90_rate_new,
                        "cell_rate": cell_rate,
                        "conode_30days": conode_30days,
                        "contimes_7days_8_to_12": contimes_7days_8_to_12,
                        "contimes_30_180_rate": contimes_30_180_rate,
                        "contimes_called_60s_7_30_rate": contimes_called_60s_7_30_rate,
                        "contimes_called_10s_7days": contimes_called_10s_7days,

                        # 黄定存新增变量
                        'vip_count': vip_count,
                        'contimes_called_30_90_rate_W': contimes_called_30_90_rate_new,
                        'contimes_called_30s_7_90_rate_W': contimes_called_30s_7_90_rate_new_xinyan,
                        'contimes_called_20s_30days_W': contimes_called_20s_30days_new_xinyan,
                        'conspan_called_7_days': conspan_called_7_days,  # 最近7天被叫通话时长
                        'silent_ge_1_w': silent_ge_1,
                        'conode_30days_w': conode_30days,
                        'contimes_called_5s_90days': contimes_called_5s_90days,
                        # 黄定存新增变量

                        # 董言 add
                        'contimes_called_90_180_rate_w': contimes_called_90_180_rate_new,
                        'contimes_called_30s_7_90_rate_w': contimes_called_30s_7_90_rate_new_xinyan,
                        'contimes_called_20s_30days_w': contimes_called_20s_30days_new_xinyan
                        # 董言 add

                    }

                    if int(model_type) == 0:
                        # 随机分配
                        pid = random.randint(0, 1)
                        logger.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                        if pid == 0:
                            comprehensive_score = score_card(model)
                            model_type = '03'  # 通用模型 V1
                            logger.info('{0},score_card Model result'.format(str(zw_order)))
                        else:
                            comprehensive_score = score_card_2(model)
                            model_type = '04'  # 通用模型 V2
                            logger.info('{0},score_card Model result'.format(str(zw_order)))
                    elif int(model_type) == 1:
                        # 新颜数据
                        xinyan_data = {}
                        if text['data']['xinyandata']:
                            for key, values in text['data']['xinyandata'].items(): xinyan_data[key] = float(
                                values) if values else float(0)
                        else:
                            xinyan_data = text['data']['xinyandata'] if text['data']['xinyandata'] != None else {}
                        logger.info(
                            '{0},xinyang_data:{1}'.format(str(zw_order), str(json.dumps(text['data']['xinyandata']))))
                        model.update(xinyan_data)
                        if text['data']['xinyandata']:
                            # if str(productCode)=='TSD02':
                            #     comprehensive_score = score_card_xmall(model)  # 商城模型
                            #     model_type = '01'
                            #     logger.info('{0},score_card_xmall Model result'.format(str(zw_order)))
                            # else:
                            comprehensive_score = score_card_recycle(model)
                            model_type = '02'  # 旧新颜模型
                            logger.info('{0},score_card_recycle Model result'.format(str(zw_order)))
                        else:
                            pid = random.randint(0, 1)
                            logger.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                            if pid == 0:
                                comprehensive_score = score_card(model)
                                model_type = '03'  # 通用模型 V1
                                logger.info('{0},score_card Model result'.format(str(zw_order)))
                            else:
                                comprehensive_score = score_card_2(model)
                                model_type = '04'  # 通用模型 V2
                                logger.info('{0},score_card Model result'.format(str(zw_order)))
                    elif int(model_type) == 2:
                        # 天创数据
                        model.update(text['data']['tcData'])
                        # 天创数据
                        if text['data']['tcData']:
                            comprehensive_score = score_card_tc(model)
                            model_type = '05'  # 天创模型
                            logger.info('{0},score_card Model result'.format(str(zw_order)))
                        else:
                            pid = random.randint(0, 1)
                            logger.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                            if pid == 0:
                                comprehensive_score = score_card(model)
                                model_type = '03'  # 通用模型 V1
                                logger.info('{0},score_card Model result'.format(str(zw_order)))
                            else:
                                comprehensive_score = score_card_2(model)
                                model_type = '04'  # 通用模型 V2
                                logger.info('{0},score_card Model result'.format(str(zw_order)))
                    elif int(model_type) == 3:
                        # 新 新颜模型
                        # xinyan_data = {}
                        # if text['data']['xinyandata']:
                        #     for key, values in text['data']['xinyandata'].items(): xinyan_data[key] = float(
                        #         values) if values else float(0)
                        #
                        # else:
                        #     xinyan_data = text['data']['xinyandata'] if text['data']['xinyandata'] != None else {}
                        # logger.info(
                        #     '{0},xinyang_data:{1}'.format(str(zw_order), str(json.dumps(text['data']['xinyandata']))))
                        xinyan_data = text['data']['xinyandata']
                        if text['data']['xinyandata']:
                            model.update(xinyan_data)
                            comprehensive_score = score_card_xinyan_nods(model)
                            model_type = '06'  # 新 新颜模型
                            logger.info('{0},score_card_recycle Model result'.format(str(zw_order)))
                        else:
                            pid = random.randint(0, 1)
                            logger.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                            if pid == 0:
                                comprehensive_score = score_card(model)
                                model_type = '03'  # 通用模型 V1
                                logger.info('{0},score_card Model result'.format(str(zw_order)))
                            else:
                                comprehensive_score = score_card_2(model)
                                model_type = '04'  # 通用模型 V2
                                logger.info('{0},score_card Model result'.format(str(zw_order)))

                    Model_Fraction = {
                        "appId": appId,
                        'merchantId': merchantId,
                        "desc": u"新户A卡评分",
                        "status": 'OK',
                        'userid': userid,
                        'loanOrderNo': str(zw_order),
                        'productCode': productCode,
                        'mode_type': model_type,
                        "comprehensive_score": str(int(comprehensive_score))
                    }
                    logger.info('{0},Get Model score:{1},产品类型:{2}'.format(zw_order, str(json.dumps(Model_Fraction)),
                                                                          str(productCode)))
                    # 模型参数入库
                    client = MongoClient('mongodb://localhost:27017/')
                    db = client['test']
                    collection = db['model_pramas']
                    model.update(text['data']['xinyandata'])
                    model['loanOrderNo'] = zw_order
                    model['userid'] = userid
                    model['order_time'] = order_time
                    model['model_type'] = model_type
                    model['add_mysql_time'] = str(datetime.datetime.now())
                    collection.insert(model)

                    return json.dumps(Model_Fraction, ensure_ascii=False)

                    # 模型参数入库

                    # config = {"host": "60.205.188.109", "port": "3306", "user": "root", "password": "Z2LD0cVBXG8ZkiPQ","db": "ModelDatabase", "table": "Acard_model_v3"}
                    # config = {"host": "rm-2zeuz81p5ltkju9ed.mysql.rds.aliyuncs.com", "port": "3306", "user": "model_root","password": "003Z7Q6Q4Ez4Nu2eL3nnYHD6", "db": "modeldatabase", "table": "Acard_model_v3"}
                    # model.update(text['data']['xinyandata'])
                    # model['loanOrderNo'] = zw_order
                    # model['userid'] = userid
                    # model['order_time'] = order_time
                    # model['model_type'] = model_type
                    # model['add_mysql_time'] = str(datetime.datetime.now())
                    # input_mysql_param = {}
                    #
                    # for key, values in model.items(): input_mysql_param[key] = str(values) if values else str(0)
                    # con = pymysql.connect(host=config['host'],
                    #                       port=int(config['port']),
                    #                       user=config['user'],
                    #                       password=config['password'],
                    #                       db=config['db'],
                    #                       charset="utf8",
                    #                       )
                    # cursor = con.cursor()
                    # sql_ml = "insert into {0}({1}) VALUES ({2})".format(config['table'],
                    #                                                     ",".join(list(input_mysql_param.keys())),
                    #                                                     ",".join(['"' + str(i) + '"' for i in
                    #                                                               list(input_mysql_param.values())])
                    #                                                     )
                    # m = cursor.execute(sql_ml)
                    # logger.info("{0} xinyan_param_data input mysql finish...".format(str(zw_order)))
                    # con.commit()
                    # con.close()
                    # return json.dumps(Model_Fraction,ensure_ascii=False)
                else:
                    logger.info('calls is empty')
                    logger.info('{0},Get Model score:{1}'.format(zw_order, str(json.dumps(error_data))))
                    error_data['error_msg'] = 'calls is empty'
                    return json.dumps(error_data, ensure_ascii=False)
            else:
                Model_Fraction = {
                    "merchantId": "HZRESK001",
                    "appId": "HZRESK001A20181122",
                    "desc": u"老用户评分",
                    "status": 'OK',
                    'userid': userid,
                    'loanOrderNo': str(zw_order),
                    'productCode': productCode,
                    'mode_type': model_type,
                    "comprehensive_score": str(600)
                }
                return json.dumps(Model_Fraction)

        else:
            logger.info('Input Model Data.data is empty')
            logger.info('{0},Get Model score:{1}'.format(zw_order, str(json.dumps(error_data))))
            error_data['error_msg':] = 'Input Model Data.data is empty'
            return json.dumps(error_data, ensure_ascii=False)

    except Exception as e:
        logger.info('param_generate:')
        logger.info(traceback.format_exc())
        logger.info('{0},Get Model score:{1}'.format(zw_order, str(json.dumps(error_data))))
        error_data['error_msg'] = str(traceback.format_exc()).replace('"', "'").replace('\n', '')
        return json.dumps(error_data, ensure_ascii=False)


def return_result_data():
    try:
        pass
    except Exception as e:
        logger.info('return')
        logger.info(traceback.format_exc())


if __name__ == '__main__':
    # data['data']['tianchang'] = {
    #     'tcp0066':'',
    #     'tcp0149':'',
    #     'tcp0164':'',
    #     'tcp0241':'',
    #     'tcp0319':'',
    #     'tcp0338':'',
    #     'tcp0348':'',
    # }
    with open('new.json', 'r', encoding='utf-8') as f:
        # f = open('dy_base.json', 'r').read()
        data = json.load(f)
        # data['data']['xinyandata']['min_alltime_allpro_pay_amt_m1'] = '0'
        # data['data']['xinyandata']['max_alltime_allpro_pay_amt_cnt5'] = '1853'
        # data['data']['xinyandata']['sum_alltime_noncdq_likeduepay_days_cnt3'] = '-99998'
        data['data']['productCode'] = 'TSD01'
        # model_type = '2'
        model_type = '3'  # xin xinyan
        print(param_generate(data, model_type))
