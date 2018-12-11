# encoding:utf-8
import traceback
import json
import pandas as pd
from pandasql import sqldf
import numpy as np
import time
from ASC20180512003001 import score_card  # tongyong V1
from ASC20180512003002 import score_card_2  # tongyong V2
from ASC20180522004001 import score_card_xmall  # shangcheng---------------------------模型被注释，没用上
from ASC20180522005001 import score_card_recycle  # huishou maibei
from ASC20180801_hdd import score_card_0801  # 长期表现--------------------------------该函数没用上
from ASC20181121_new_xinyan import score_card_xinyan_nods  # 新新颜评分卡
# from .ASC20180806_new_xinyan import score_card_xinyan_nods  # 新新颜评分卡
from Model_V4_2_ascore_20180803 import score_card_tc  # 天创数据
import datetime
import pymysql
import random

import logging
import logging.handlers


def get_logger(logger_name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)

    vlog = logging.getLogger(logger_name)
    vlog.setLevel(level)
    # logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        format='%(asctime)s-%(levelname)s-%(name)s-%(message)s'
    )
    filehandler = logging.handlers.TimedRotatingFileHandler(
        # '/home/Model/logs/model_server_logs/model_log',
        # 'D:/models_log',
        # "model_log",
        log_file,
        when='D',
        interval=10,  ##间隔此时长，原日志将被覆盖
        backupCount=3,  ##单个日志文件最多存放日志数量
    )
    fileHandler.suffix = "%Y-%m-%d.log"
    logFormatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    fileHandler.setFormatter(logFormatter)
    vlog.addHandler(fileHandler)
    return vlog



log_file1 = 'new_model_logs'
log_file2 = 'new_rule_logs'

logger1 = get_logger('model_log', log_file1)
logger = get_logger('rule_log', log_file2)


# logger1.info('>>> test1 log msg: %s', "111111111111111111111")
# logger2.info('>>> test2 log msg: %s', "222222222222222222222")

def param_generate(text, model_type):
    def get_value(var, key):
        try:
            return var[key]
        except:
            return None

    try:
        zw_order = str(text['data']['orderNo'])
        userid = str(text['data']['userid'])  # 用户中心
        productCode = str(text['data']['productCode'])
        order_time = str(text['data']['order_time'])
        if text['data']['isAgain'] == 0:

            error_data = {'mode_type': '00', "userid": str(userid), "comprehensive_score": '200', "desc": u"新户A卡评分",'isAgain':0,
                          "status": "失败", "loanOrderNo": str(zw_order), "productCode": str(productCode),'order_time': text['data']['order_time'],
                    'name': text['data']['name'],
                    'idCardNo': text['data']['idCardNo']}
            if text['data']:
                # 花呗额度
                huabei_base_data = text['data']['moxieTaobao']
                if huabei_base_data:
                    huabei_totalcreditamount = huabei_base_data['alipaywealth'][
                        'huabei_totalcreditamount'] if 'alipaywealth' in huabei_base_data.keys() else ''
                    # 判断 花呗值 单位
                    huabei_totalcreditamount = str(float(
                        huabei_totalcreditamount) / 1) if 'MB' in productCode and huabei_totalcreditamount != '' else str(
                        huabei_totalcreditamount)
                else:
                    huabei_totalcreditamount = ''
                logger1.info('{0},花呗额度，huabei_totalcreditamount:{1}'.format(zw_order, str(huabei_totalcreditamount)))

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
                        # call_base_param = text['data']['loanBondOrignalData']['message']
                        logger1.info('{0},calls:{1}'.format(str(zw_order), call_base_param))
                        # call_base_list = text['data']['loanBondOrignalData']['data'][0]['calls'] if '获取原始数据成功' else []
                        call_base_list = text['data']['loanBondOrignalData'][0]['calls'] if '获取原始数据成功' else []
                        if call_base_list:
                            logger1.info('{0},calls:{1}'.format(str(zw_order), json.dumps(call_base_list[0])))
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
                            logger1.info('{0},通话记录{1}个'.format(zw_order, str(len(call_list))))
                        else:
                            # 运营商数据 为空
                            call_list = []
                            logger1.info('{0},loanBondOrignalData.data.calls is empty'.format(str(zw_order)))
                except Exception as e:
                    call_list = []
                    logger1.info('{0},通话记录解析错误'.format(zw_order))
                    logger1.info(traceback.format_exc())
                finally:
                    columns_base = ['duration', 'location', 'time', 'dial_type', 'location_type', 'peer_number',
                                    'order_time', 'update_time']
                    data1 = pd.DataFrame(call_list, columns=columns_base)

                # 通讯录
                try:
                    mail_list = text['data']['mailList']
                    mail_data = {'contact_phone': list(map(lambda x: get_value(x, 'phone'), mail_list)),
                                 'name': list(map(lambda x: get_value(x, 'name'), mail_list))}
                    data4 = pd.DataFrame(mail_data)
                except Exception as e:
                    logger1.info(traceback.format_exc())

                # 电商 -- 20180523---------------------------------淘宝数据
                try:
                    order_time = int(text["data"]["order_time"])
                    time_local = time.localtime(order_time)
                    order_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    if text['data']['moxieTaobao']:
                        tb_base_list = text['data']['moxieTaobao']['tradedetails']['tradedetails']
                        tb_list = list(map(lambda x: {
                            'trade_text': x['trade_text'],
                            #                    'time':x['trade_createtime'].split('T')[0],
                            'time': x['trade_createtime'].replace('T', ' ').replace('.000+08',
                                                                                    '').strip() if 'trade_createtime' in list(
                                x.keys()) else None,
                            'actual_fee': float(x['actual_fee']) / 100 if 'MB' in productCode and x[
                                'actual_fee'] != '' else float(x['actual_fee']),
                            'order_time': order_time
                        }, tb_base_list))
                    else:
                        tb_list = []
                    logger1.info('{0},电商交易{1}个'.format(zw_order, str(len(tb_list))))
                except Exception as e:
                    tb_list = []
                    logger1.info('{0},电商记录解析错误'.format(zw_order))
                    logger1.info(traceback.format_exc())
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
                        logger1.info('{0},silent_ge_1 param Error...'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    logger1.info(
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
                        logger1.info('{0}最近1个月和3个月的比值，最近3个月和6个月的比值, 最近3个月和6个月的比值(新) 获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info(
                            '{0},最近3个月被叫个数,month3_called:{1},6个月的被叫个数,month6_called:{2},比值:{3}'.format(zw_order,
                                                                                                       str(float(
                                                                                                           month3_called)),
                                                                                                       str(float(
                                                                                                           month6_called)),
                                                                                                       str(
                                                                                                           contimes_called_90_180_rate)))
                        logger1.info(
                            '{0},最近1个月被叫个数,month1_called:{1},3个月的被叫个数,month3_called:{2},比值:{3}'.format(zw_order,
                                                                                                       str(float(
                                                                                                           month1_called)),
                                                                                                       str(float(
                                                                                                           month3_called)),
                                                                                                       str(
                                                                                                           contimes_called_30_90_rate)))
                        logger1.info(
                            '{0},最近3个月被叫个数,month3_called_update:{1},6个月的被叫个数,month6_called_update:{2},比值:{3}'.format(
                                zw_order, str(float(month3_called_update)), str(float(month6_called_update)),
                                str(contimes_called_90_180_rate_new)))
                        logger1.info(
                            '{0},最近1个月被叫个数,month1_called_update:{1},3个月的被叫个数,month3_called_update:{2},比值:{3}'.format(
                                zw_order, str(float(month1_called_update)), str(float(month3_called_update)),
                                str(contimes_called_30_90_rate_new)))
                        # 最近180天订单金额求和
                    try:
                        orderfee_180d = np.array(sqldf(
                            "select sum(case when time>=datetime(order_time,'-180 days') and time<order_time then actual_fee else 0 end) from (select trade_text,time,actual_fee,order_time from data3 where trade_text='交易成功');"))
                    except Exception as e:
                        orderfee_180d = ''
                        logger1.info('{0}最近180天订单金额求和 获取失败：'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},最近180天订单金额求和:{1}'.format(zw_order, str(orderfee_180d)))

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
                        logger1.info('{0},一个星期内和三个月内30秒以内的被叫通话次数获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},一个星期内30s内被叫次数,day7_called:{1},3个月内30s内被叫次数,day90_called:{2},比值:{3}'
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
                        logger1.info('{0},一个星期内和三个月内30秒以内的被叫通话次数获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},一个星期内30s内被叫次数,day7_called:{1},3个月内30s内被叫次数,day90_called:{2},比值:{3}'
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
                        logger1.info('{0},一个星期内和三个月内20秒以内的被叫通话次数获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},一个星期内20s内被叫次数,day7_called_20:{1},3个月内20s内被叫次数,day90_called_20:{2},比值:{3}'
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
                        logger1.info('{0},一个月内5秒以内的被叫通话次数,一个月内20秒以内的被叫通话次数,三个月内5秒以内的通话次数获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},一个月内5秒被叫次数:{1},一个月内20秒被叫次数:{2},三个月内5秒以内的通话次数:{3}'.format(zw_order,
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
                        logger1.info('{0},一个月内5秒以内的被叫通话次数,一个月内20秒以内的被叫通话次数,三个月内5秒以内的通话次数获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},一个月内5秒被叫次数:{1},一个月内20秒被叫次数:{2},三个月内5秒以内的通话次数:{3}'.format(zw_order,
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
                        logger1.info(
                            '{0},最近30天1点到8点通话个数计数获取失败, 最近30天22点到1点通话个数计数获取失败, 最近7天8点到12点通话个数计数,最近30天通话个数计数与最近180天通话个数计数比值, 最近30天通话联系人, 获取失败'.format(
                                zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info(
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
                        logger1.info('{0},最近30天1点到8点通话个数计数与最近30天通话个数计数比值,获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info(
                            '{0},最近30天通话个数:{1},近30天1点到8点通话个数计数与最近30天通话个数计数比值:{2}'.format(zw_order, day30_call_number,
                                                                                         contimes_1_to_8c_30days_rate))

                    try:
                        # 通话1分钟以下的电话数
                        call_lt_min = np.array(sqldf(
                            "select count(distinct case when duration<60 then peer_number else null end) as num from data1;"))

                        call_lt_min = float(call_lt_min)
                    except Exception as e:
                        call_lt_min = ''
                        logger1.info('{0},通话1分钟以下的电话数,获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},通话1分钟以下的电话数:{1}'.format(zw_order, call_lt_min))

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
                        logger1.info(
                            '{0},三个月内10秒以内的被叫通话次数,三个月内5秒以内的被叫通话次数,三个月内20秒以内的主叫通话次数,一个星期内和一个月内60秒以内的被叫通话次数,一个星期内10秒以内的被叫通话次数, 获取失败:'.format(
                                zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info(
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
                        logger1.info('{0},通话一次的手机号数量 获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},通话一次的手机号数量:{1}'.format(zw_order, str(call_1)))
                    try:
                        # 历史平均联系人通话时长
                        avg_time = np.array(sqldf(
                            "select case when count(peer_number) is not null and count(peer_number) != 0 then sum(time_span)/count(peer_number)  else 0 end as num from (select peer_number,sum(duration) as time_span from data1 group by peer_number);"))
                        avg_time = float(avg_time) if avg_time else ''
                    except Exception as e:
                        avg_time = ''
                        logger1.info('{0},历史平均联系人通话时长 获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},历史平均联系人通话时长:{1}'.format(zw_order, avg_time))

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
                        logger1.info(
                            '{0},总通话时间在30秒以上的联系人数,过去3个月有过通话的联系人个数,在0-5时间段通话联系人,在[5:00 , 12:00)时间段通话联系人,过去7天过通话的联系人个数 获取失败:'.format(
                                zw_order))
                        logger1.info(traceback.format_exc())

                    # 通讯录手机号码占总数的比值------------------------通讯录对应的指标cell_rate暂时没用上
                    try:
                        contact_nbr = np.array(
                            sqldf("select count(distinct contact_phone) from data4 WHERE length(contact_phone)>=7;"))
                        cell_nbr = np.array(sqldf(
                            "select sum(case when (length(contact_phone)=11 and substr(contact_phone,1,1) = '1') or (length(contact_phone)=13 and substr(contact_phone,1,2) = '86') then 1 else 0 end) from data4;"))
                        cell_rate = float(cell_nbr) / float(contact_nbr) if float(contact_nbr) != float(0) else ''

                    except Exception as e:
                        cell_rate = ''
                        logger1.info('{0}, 通讯录手机号码占总数的比值获取失败:'.format(zw_order))
                        logger1.info(traceback.format_exc())
                    finally:
                        logger1.info('{0},通讯录手机号码占总数的比值:{1}'.format(zw_order, cell_rate))

                    # 黄定存 添加 衍生 变量
                    conspan_called_7_days = np.array(sqldf(
                        "select sum(case when time>=datetime(update_time,'-7 days') and time<update_time and dial_type like '%被叫%' then duration else 0 end) from data1;"))
                    conspan_called_7_days = list(map(lambda x: x[0], conspan_called_7_days))[0]
                    vip_count = text['data']['moxieTaobao']['userinfo']['vip_count'] if text['data'][
                        'moxieTaobao'] else ''
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
                        logger1.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                        if pid == 0:
                            comprehensive_score = score_card(model)
                            model_type = '03'  # 通用模型 V1
                            logger1.info('{0},score_card Model result'.format(str(zw_order)))
                        else:
                            comprehensive_score = score_card_2(model)
                            model_type = '04'  # 通用模型 V2
                            logger1.info('{0},score_card Model result'.format(str(zw_order)))
                    elif int(model_type) == 1:
                        # 新颜数据
                        '''
                        xinyan_data = {}
                        if text['data']['xinyandata']:
                            for key, values in text['data']['xinyandata'].items(): xinyan_data[key] = float(
                                values) if values else float(0)
                        else:
                            xinyan_data = text['data']['xinyandata'] if text['data']['xinyandata'] != None else {}
                        logger1.info(
                            '{0},xinyang_data:{1}'.format(str(zw_order), str(json.dumps(text['data']['xinyandata']))))
                        model.update(xinyan_data)
                        '''
                        if text['data']['xinyandata']:
                            # if str(productCode)=='TSD02':
                            #     comprehensive_score = score_card_xmall(model)  # 商城模型
                            #     model_type = '01'
                            #     logger.info('{0},score_card_xmall Model result'.format(str(zw_order)))
                            # else:
                            xinyan_data = text['data']['xinyandata']
                            model.update(xinyan_data)
                            comprehensive_score = score_card_recycle(model)
                            model_type = '02'  # 旧新颜模型
                            logger1.info('{0},score_card_recycle Model result'.format(str(zw_order)))
                        else:
                            pid = random.randint(0, 1)
                            logger1.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                            if pid == 0:
                                comprehensive_score = score_card(model)
                                model_type = '03'  # 通用模型 V1
                                logger1.info('{0},score_card Model result'.format(str(zw_order)))
                            else:
                                comprehensive_score = score_card_2(model)
                                model_type = '04'  # 通用模型 V2
                                logger1.info('{0},score_card Model result'.format(str(zw_order)))
                    elif int(model_type) == 2:
                        # 天创数据
                        model.update(text['data']['tcData'])
                        # 天创数据
                        if text['data']['tcData']:
                            comprehensive_score = score_card_tc(model)
                            model_type = '05'  # 天创模型
                            logger1.info('{0},score_card Model result'.format(str(zw_order)))
                        else:
                            pid = random.randint(0, 1)
                            logger1.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                            if pid == 0:
                                comprehensive_score = score_card(model)
                                model_type = '03'  # 通用模型 V1
                                logger1.info('{0},score_card Model result'.format(str(zw_order)))
                            else:
                                comprehensive_score = score_card_2(model)
                                model_type = '04'  # 通用模型 V2
                                logger1.info('{0},score_card Model result'.format(str(zw_order)))
                    elif int(model_type) == 3:
                        # 新 新颜模型
                        '''
                        xinyan_data = {}
                        if text['data']['xinyandata']:
                            for key, values in text['data']['xinyandata'].items(): xinyan_data[key] = float(
                                values) if values else float(0)

                        else:
                            xinyan_data = text['data']['xinyandata'] if text['data']['xinyandata'] != None else {}
                        logger.info(
                            '{0},xinyang_data:{1}'.format(str(zw_order), str(json.dumps(text['data']['xinyandata']))))
                        '''
                        xinyan_data = text['data']['xinyandata']

                        if text['data']['xinyandata']:
                            model.update(xinyan_data)
                            comprehensive_score = score_card_xinyan_nods(model)
                            model_type = '06'  # 新 新颜模型
                            logger1.info('{0},score_card_recycle Model result'.format(str(zw_order)))
                        else:
                            pid = random.randint(0, 1)
                            logger1.info('{0},pid==={1}'.format(str(zw_order), str(pid)))
                            if pid == 0:
                                comprehensive_score = score_card(model)
                                model_type = '03'  # 通用模型 V1
                                logger1.info('{0},score_card Model result'.format(str(zw_order)))
                            else:
                                comprehensive_score = score_card_2(model)
                                model_type = '04'  # 通用模型 V2
                                logger1.info('{0},score_card Model result'.format(str(zw_order)))

                    Model_Fraction = {
                        "desc": u"新户A卡评分",
                        "status": '成功',
                        'userid': userid,
                        'loanOrderNo': str(zw_order),
                        'productCode': productCode,
                        'mode_type': model_type,
                        "comprehensive_score": str(int(comprehensive_score))
                    }
                    logger1.info('{0},Get Model score:{1},产品类型:{2}'.format(zw_order, str(json.dumps(Model_Fraction)),
                                                                           str(productCode)))
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
                    logger1.info('calls is empty')
                    logger1.info('{0},Get Model score:{1}'.format(zw_order, str(json.dumps(error_data))))
                    error_data['error_msg'] = 'calls is empty'
                    return json.dumps(error_data, ensure_ascii=False)
            else:
                logger1.info('Input Model Data.data is empty')
                logger1.info('{0},Get Model score:{1}'.format(zw_order, str(json.dumps(error_data))))
                error_data['error_msg':] = 'Input Model Data.data is empty'
                return json.dumps(error_data, ensure_ascii=False)
        else:
            error_data = {'mode_type': '00', "userid": str(userid), "comprehensive_score": '650.1', "desc": u"老户A卡评分",'isAgain':1,
                          "status": "成功", "loanOrderNo": str(zw_order), "productCode": str(productCode),'order_time': text['data']['order_time'],
                    'name': text['data']['name'],
                    'idCardNo': text['data']['idCardNo']}
            return json.dumps(error_data, ensure_ascii=False)
    except Exception as e:
        logger1.info('param_generate:')
        logger1.info(traceback.format_exc())
        logger1.info('{0},Get Model score:{1}'.format(zw_order, str(json.dumps(error_data))))
        error_data['error_msg'] = str(traceback.format_exc()).replace('"', "'").replace('\n', '')
        return json.dumps(error_data, ensure_ascii=False)


'''
def return_result_data():
    try:
        pass
    except Exception as e:
        logger1.info('return')
        logger1.info(traceback.format_exc())
'''
'''
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
    f = open('D:/data/testdata/model_test/hdc_new.json', 'rb').read()
    # f = open('dy_base.json', 'r').read()
    # for i in f:
    data = json.loads(f)
    data['data']['xinyandata']['min_alltime_allpro_pay_amt_m1'] = '0'  # 直接指定参数值，分数减14
    data['data']['xinyandata']['max_alltime_allpro_pay_amt_cnt5'] = '1853'  # -----------------似乎是无用参数
    data['data']['xinyandata']['sum_alltime_noncdq_likeduepay_days_cnt3'] = '12'  # 直接指定参数值，新新颜模型不改变分数，5001模型则是增加59分
    data['data']['productCode'] = 'TSD01'
    # model_type = '2'
    model_type = '3'  # xin xinyan
    print(param_generate(data, model_type))

'''


# encoding:utf-8

def checkIdcard(idcard):
    import re
    # Errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
    Errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
    area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北",
            "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    # 将小写X改为大写
    idcard = str(idcard)
    if idcard.find('x') > 0:
        idcard = idcard.replace('x', 'X')
    idcard = idcard.strip()
    idcard_list = list(idcard)

    # 地区校验
    if (not area[(idcard)[0:2]]):
        print(Errors[4])
    # 15位身份号码检测
    if (len(idcard) == 15):
        if ((int(idcard[6:8]) + 1900) % 4 == 0 or (
                (int(idcard[6:8]) + 1900) % 100 == 0 and (int(idcard[6:8]) + 1900) % 4 == 0)):
            erg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
        if (re.match(ereg, idcard)):
            return 0  # print(Errors[0])
        else:
            return 1  # print(Errors[2])
    # 18位身份号码检测
    elif (len(idcard) == 18):
        # 出生日期的合法性检查
        # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if (int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10]) % 4 == 0)):
            ereg = re.compile(
                '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        # //测试出生日期的合法性
        if (re.match(ereg, idcard)):
            # //计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 + (
                    int(idcard_list[2]) + int(idcard_list[12])) * 10 + (
                        int(idcard_list[3]) + int(idcard_list[13])) * 5 + (
                        int(idcard_list[4]) + int(idcard_list[14])) * 8 + (
                        int(idcard_list[5]) + int(idcard_list[15])) * 4 + (
                        int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(
                idcard_list[8]) * 6 + int(idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if (M == idcard_list[17]):  # 检测ID的校验位
                return 0  # print(Errors[0])
            else:
                return 1  # print(Errors[3])
        else:
            return 1  # print(Errors[2])
    else:
        return 1  # print(Errors[1])


def full_idacrd(idcard):  ##15位身份证号码补全18位

    x = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    d = {
        '0': '1',
        '1': '0',
        '2': 'X',
        '3': '9',
        '4': '8',
        '5': '7',
        '6': '6',
        '7': '5',
        '8': '4',
        '9': '3',
        '10': '2'}

    def check(code):
        sum = 0
        n = 0
        for i in code:
            sum += int(i) * x[n]
            n += 1
        # print(sum)
        result = sum % 11
        return d[str(result)]

    '''
    def full2half(code):
        code1 = code[:6] #行政码
        code2 = code[8:14] #生日
        code3 = code[14:17] #分配码
        return code1 + code2 + code3
    '''

    result = idcard[:6] + '19' + idcard[6:]
    return result + check(result)


# print(full_idacrd('510104821202379'))


def rule_data(modeldata):  ##假定传入的是json
    def get_value(var, key):
        try:
            return var[key]
        except:
            return None

    ###准入限制-----------优先不使用第三方数据（自身黑名单那然后贷后帮然后天创\新颜）
    limit_message = {"N1001": "accept", "S1001": "accept", "S1002": "accept", "S1003": "accept",
                     "S1004": "accept", "G3001": "accept", "M4001": "accept", "H1001": "accept", "H1002": "accept",
                     "H1003": "accept", "H1004": "accept", "H1005": "accept", "H1006": "accept", "H1007": "accept",
                     'H1009': 'accept', 'H1010': 'accept', 'H1011': 'accept', 'H1012': 'accept', 'H1013': 'accept',
                     "H1008": "accept", 'D1001': 'accept'}
    antifraud_message = {"Y1001": "accept", "Y2001": "accept", "Y2002": "accept", "Y2003": "accept",
                         "Y2004": "accept", "Y3001": "accept", "Y3002": "accept", "Y3003": "accept", "Y3004": "accept",
                         "Y3005": "accept", "Y3006": "accept", "Y3007": "accept", "Y3008": "accept", "Y3009": "accept",
                         "Y3010": "accept",
                         "Y3011": "accept", "Y3012": "accept", "Y3013": "accept", "Y3014": "accept", "Y3015": "accept",
                         "Y3016": "accept",
                         "Y3017": "accept", "Y3018": "accept", "Y3019": "accept", "Y3020": "accept", "Y3021": "accept",
                         'Y3023': "accept",
                         "T1001": "accept", "T1002": "accept", "T1003": "accept", "T1004": "accept", "T1005": "accept",
                         "T1006": "accept",
                         "T1007": "accept", "T1008": "accept", "T1009": "accept", "T1010": "accept", "S1001": "accept",
                         "S1002": "accept",
                         "S1003": "accept", "S1004": "accept", "S1005": "accept", "S1006": "accept", "I1001": "accept",
                         "I1002": "accept", "I1003": "accept", "I1004": "accept", "J1001": "accept", "J1002": "accept",
                         "J1003": "accept",
                         "J1004": "accept"}
    try:
        import time
        import datetime
        from collections import Counter
        import re
        from functools import reduce

        # from check_fun import checkIdcard  ##身份证校验函数
        # from check_fun import full_idacrd  ##15位身份证转18位

        warn_words = [u'借', u'贷', u'催收', u'口子', u'黑户', u'代还', u'套现', u'养卡']  ##中介不在其中
        relation_words = [u'父', u'母', u'娘', u'老婆', u'媳妇', u'爸', u'妈', u'姑', u'舅', u'姨', u'爹', u'叔', u'哥', u'姐', u'妹',
                          u'弟',
                          u'爷爷', u'奶奶', u'儿子', u'姥爷', u'姥姥', u'女儿', u'老公', u'丈夫', u'爱人']
        app_words = [u'007改机', u'008改机', u'变机宝', u'ROM大师', u'太极越狱', u'盘古越狱', u'变机精灵', u'ig改机', u'Xposed', u'应用变量',
                     u'深海',
                     u'机型更改软件']  ##app搜索验证

        if modeldata['data']['isAgain'] == 0:  ##初借客户

            ##身份证是否有效---目前仅做身份证是否有效，未做身份证姓名是否匹配
            if checkIdcard(modeldata['data']["idCardNo"]) != 0:
                limit_message['S1001'] = 'reject'
            else:
                ###年龄限制(最新的身份证有15位的)
                if len(modeldata['data']["idCardNo"]) == 15:
                    idcardno = full_idacrd(modeldata['data']["idCardNo"])
                else:
                    idcardno = modeldata['data']["idCardNo"]

                if str(datetime.datetime.today())[:4] + '-' + idcardno[10:12] + '-' + idcardno[12:14] > str(
                        datetime.datetime.today())[:10]:
                    age = int(str(datetime.datetime.today())[:4]) - int(idcardno[6:10]) - 1
                else:
                    age = int(str(datetime.datetime.today())[:4]) - int(idcardno[6:10])
                if age > 45 or age < 18:
                    limit_message['N1001'] = "reject"
            ##身份证前几位命中高危地区
            if modeldata['data']['idCardNo'][:6] in ["350524", "350525", "469003", "450126", "440923", "432522",
                                                     "361127",
                                                     "130826"] or \
                    modeldata['data']['idCardNo'][:4] in ["3723", "3303", "3503", "3509", "3522", "4452", "4405",
                                                          "3304",
                                                          "3209"] or \
                    modeldata['data']['idCardNo'][:2] in ["63", "65", "54"]:
                limit_message['G3001'] = 'reject'
            ##手机号码不是11位----有待商榷
            if len(modeldata['data']['mobile'].replace('+86', "").replace('+', '').replace(' ', '').replace('-',
                                                                                                            '')) != 11:
                limit_message['M4001'] = 'reject'

            ##运营商校验是否通过（状态正常、实名制、三要素与申请信息一致、入网时长不低于180天
            if modeldata['data']['scorpionAccessReport']:  ###是否有脱敏,----mobile 具体是什么
                if modeldata['data']['scorpionOriginalData']['state'] != 0 or modeldata['data']['scorpionOriginalData'][
                    'reliability'] != 1 or \
                        (not modeldata['data']['scorpionOriginalData']['open_time'] and int(
                            modeldata['data']['order_time']) - time.mktime(
                            time.strptime(modeldata['data']['scorpionOriginalData']['open_time'],
                                          '%Y-%m-%d %H:%M:%S'))) <= 180 * 24 * 60 * 60:
                    limit_message['S1002'] = 'reject'
                if modeldata['data']['scorpionOriginalData']['name'].find('*') < 0 and len(
                        modeldata['data']['scorpionOriginalData']['name'].replace(' ', '')) != 0 and \
                        modeldata['data']['scorpionOriginalData']['name'].replace(' ', '') != \
                        modeldata['data']['name']:
                    limit_message['S1002'] = 'reject'
            elif modeldata['data']['loanBondData']:  ###是否有脱敏----('状态有效且已经实名制且入网时长超过半年)  binding_time  不为入网时长！！！
                if modeldata['data']['loanBondData']['data_source'][0]['status'] != 'valid' or (
                        not modeldata['data']['loanBondData']['data_source'][0]['binding_time'] and
                        modeldata['data']['loanBondData']['data_source'][0]['reliability'] != u"实名认证" or \
                        int(modeldata['data']['order_time']) - time.mktime(
                    time.strptime(modeldata['data']['loanBondData']['data_source'][0]['binding_time'],
                                  '%Y-%m-%d %H:%M:%S')) <= 180 * 24 * 60 * 60):
                    limit_message['S1002'] = 'reject'
            elif modeldata['data']['loanBondOrignalData']:
                if modeldata['data']['loanBondOrignalData'][0]['basic']['real_name'].find('*') < 0 and len(
                        modeldata['data']['loanBondOrignalData'][0]['basic']['real_name'].replace(' ', '')) != 0 and \
                        modeldata['data']['loanBondOrignalData'][0]['basic']['real_name'].replace(' ', '') != \
                        modeldata['data']['name']:
                    limit_message['S1002'] = 'reject'

            '''
            elif modeldata['data']['loanBondOrignalData']:  ###是否有脱敏----手机号状态与是否实名制
                if (modeldata['data']['loanBondOrignalData'][0]['basic']['real_name'] != modeldata['data']['name'] and
                    modeldata['data']['loanBondOrignalData'][0]['basic']['name'].find('*') < 0) or \
                        (modeldata['data']['loanBondOrignalData'][0]['basic']['idcard'] != modeldata['data']['idCardNo'] and
                         modeldata['data']['loanBondOrignalData'][0]['basic']['idcard'].find('*') < 0 and
                         len(modeldata['data']['loanBondOrignalData'][0]['basic']['idcard'].replace(' ', '')) != 0) or \
                        (modeldata['data']['loanBondOrignalData'][0]['basic']['cell_phone'] != modeldata['data']['mobile'] and
                         modeldata['data']['loanBondOrignalData'][0]['basic']['mobile'].find('*') < 0) or \
                        (not modeldata['data']['loanBondOrignalData'][0]['basic']['reg_time'] and int(
                            modeldata['data']['order_time']) - time.mktime(
                            time.strptime(modeldata['data']['loanBondOrignalData'][0]['basic']['reg_time'],
                                          '%Y-%m-%d %H:%M:%S'))) <= 180 * 24 * 60 * 60:
                    limit_message['S1002'] = 'reject'
            '''

            ##索伦黑名单情况
            try:
                if modeldata['data']['loanBondSuolunData']:
                    if modeldata['data']['loanBondSuolunData']['risk_blacklist']['idcard_in_blacklist'] or \
                            modeldata['data']['loanBondSuolunData']['risk_blacklist']['phone_in_blacklist'] or \
                            modeldata['data']['loanBondSuolunData']['risk_blacklist']['in_court_blacklist'] or \
                            modeldata['data']['loanBondSuolunData']['risk_blacklist']['in_p2p_blacklist'] or \
                            modeldata['data']['loanBondSuolunData']['risk_blacklist']['in_bank_blacklist']:
                        limit_message['H1002'] = 'reject'


            except:
                logger.info('{0},索伦黑名单解析错误'.format(modeldata['orderNo']))
            ##索伦其他数据
            try:
                if modeldata['data']['loanBondSuolunData']:
                    if modeldata['data']['loanBondSuolunData']['risk_social_network'][
                        'sn_order1_blacklist_contacts_cnt'] != '' and int(
                        modeldata['data']['loanBondSuolunData']['risk_social_network'][
                            'sn_order1_blacklist_contacts_cnt']) >= 3:
                        limit_message['H1009'] = 'reject'
                    if modeldata['data']['loanBondSuolunData']['user_basic']['used_idcards_cnt'] != '' and \
                            int(modeldata['data']['loanBondSuolunData']['user_basic']['used_idcards_cnt']) >= 3:
                        limit_message['H1010'] = 'reject'
                    if modeldata['data']['loanBondSuolunData']['user_basic']['used_phones_cnt'] != '' and \
                            int(modeldata['data']['loanBondSuolunData']['user_basic']['used_phones_cnt']) >= 5:
                        limit_message['H1011'] = 'reject'
                    if modeldata['data']['loanBondSuolunData']['history_search'][
                        'search_cnt_recent_7_days'] != '' and int(
                        modeldata['data']['loanBondSuolunData']['history_search'][
                            'search_cnt_recent_7_days']) >= 5:
                        limit_message['H1012'] = 'reject'
                    if modeldata['data']['loanBondSuolunData']['history_search'][
                        'search_cnt_recent_14_days'] != '' and int(
                        modeldata['data']['loanBondSuolunData']['history_search'][
                            'search_cnt_recent_14_days']) >= 8:
                        limit_message['H1013'] = 'reject'

            except:
                logger.info('{0},索伦其他解析错误'.format(modeldata['orderNo']))

            ##天创黑名单-----------后续天创洗白使用
            try:
                if modeldata['data']['tcData2']:
                    if modeldata['data']['tcData2']['data']['black_level'] in ['A']:
                        limit_message['H1001'] = 'reject'
                    elif modeldata['data']['tcData2']['data']['black_level'] in ['B', 'C', 'D']:
                        limit_message['H1001'] = 'review'
            except:
                logger.info('{0},天创黑名单解析错误'.format(modeldata['orderNo']))
            '''    
            ##相关分数过低---xiugai
            if not modeldata['data']['score'][1]['score'] and modeldata['data']['score'][2]['score']<=2:###跟刘磊沟通修改阈值
                limit_message['H1004']='reject'
            if not modeldata['data']['score'][1]['score'] and modeldata['data']['score'][1]['score']<=550:###芝麻分过低
                limit_message['H1006']='reject'
            if not modeldata['data']['score'][3]['score'] and modeldata['data']['score'][3]['score']<=470:###新颜贷款行为分过低 !!!!具体分数待定
                limit_message['H1005']='reject'
            '''
            ##相关分数过低
            try:
                if modeldata['data']['score']['hulu_score']:
                    if int(modeldata['data']['score']['hulu_score']) <= 2:  ###葫芦分格式是string
                        limit_message['H1004'] = 'reject'
            except:
                logger.info('{0},葫芦分解析错误'.format(modeldata['orderNo']))

            try:
                if modeldata['data']['score']['zhima']:
                    if int(modeldata['data']['score']['zhima']) <= 550:  ###芝麻分过低  ()
                        limit_message['H1006'] = 'reject'
            except:
                logger.info('{0},芝麻分解析错误'.format(modeldata['orderNo']))

            try:
                if modeldata['data']['score']['xinyan_score1']:
                    if int(modeldata['data']['score']['xinyan_score1']) <= 470:  ###新颜贷款行为分过低 !!!!具体分数待定
                        limit_message['H1005'] = 'reject'
            except:
                logger.info('{0},新颜贷款行为分解析错误'.format(modeldata['orderNo']))

            ###申请反欺诈

            ##运营商数据-----数据完全为空情形

            ##通话记录相关（暂时仅区分是魔蝎还是贷后邦，后续区分是本地还是运营商）
            try:  ###刘磊
                jjlxr_json_phone = [phone for phone in
                                    [modeldata['data']['contacts'][0].get('phone1'),
                                     modeldata['data']['contacts'][1].get('phone1')]
                                    if phone]
            except:
                jjlxr_json_phone = []
                logger.info('{0},紧急联系人解析错误'.format(modeldata['orderNo']))

            if modeldata['data']['scorpionOriginalData']:
                ##入网时长
                try:
                    if modeldata['data']['scorpionOriginalData']['open_time'] and \
                            modeldata['data']['scorpionOriginalData'][
                                'open_time'] != '':
                        if not modeldata['data']['scorpionOriginalData']['open_time'] and int(
                                modeldata['data']['order_time']) - time.mktime(
                            time.strptime(modeldata['data']['scorpionOriginalData']['open_time'],
                                          '%Y-%m-%d %H:%M:%S')) <= 180 * 24 * 60 * 60:
                            antifraud_message['Y1001'] = 'reject'
                except:
                    logger.info('{0},魔蝎运营商入网时长解析错误'.format(modeldata['orderNo']))
                ##短信相关
                try:
                    if modeldata['data']['scorpionOriginalData']['smses']:
                        scorpionOriginalData_smses_list = list(
                            map(lambda x: x['items'], modeldata['data']['scorpionOriginalData']['smses']))
                        scorpionOriginalData_smses_list = list(
                            reduce(lambda x, y: x + y, scorpionOriginalData_smses_list))

                        if len(scorpionOriginalData_smses_list) == 0:  ##没有短信记录
                            antifraud_message['Y2001'] = 'reject'

                        if len(scorpionOriginalData_smses_list) != 0 and len(
                                scorpionOriginalData_smses_list) < 30:  # 短信条数少于30条
                            antifraud_message['Y2003'] = 'reject'
                except:
                    logger.info('{0},魔蝎葫芦分解析错误'.format(modeldata['orderNo']))

                # 将魔蝎数据整理成贷后邦相同格式(数据格式与字段名称)
                try:
                    if modeldata['data']['scorpionOriginalData']['calls']:
                        scorpionOriginalData_call_list = list(
                            map(lambda x: x['items'], modeldata['data']['scorpionOriginalData']['calls']))
                        scorpionOriginalData_call_list = list(
                            reduce(lambda x, y: x + y, scorpionOriginalData_call_list))
                        scorpionOriginalData_call_list2 = []
                        if len(scorpionOriginalData_call_list) == 0:  # 通话记录缺失（魔蝎通话记录为空时call对应的items是一个空数据）
                            antifraud_message['Y3001'] = 'reject'
                        else:
                            scorpionOriginalData_call_list2 = scorpionOriginalData_call_list

                            if max(list(map(lambda x: time.mktime(time.strptime(x['time'], '%Y-%m-%d %H:%M:%S')),
                                            scorpionOriginalData_call_list2))) - min(
                                list(map(lambda x: time.mktime(time.strptime(x['time'], '%Y-%m-%d %H:%M:%S')),
                                         scorpionOriginalData_call_list2))) < 90 * 24 * 60 * 60:  # 通话时间跨度小于90天
                                antifraud_message['Y3002'] = 'reject'
                            if len([phone for phone in list(
                                    map(lambda x: x.replace('+86', "").replace('+', '').replace(' ', '').replace('-',
                                                                                                                 ''),
                                        jjlxr_json_phone)) if \
                                    phone in list(set(list(map(lambda x: x['peer_number'],
                                                               [i for i in scorpionOriginalData_call_list2 if
                                                                int(modeldata['data']['order_time']) - time.mktime(
                                                                    time.strptime(i['time'],
                                                                                  '%Y-%m-%d %H:%M:%S')) <= 180 * 24 * 60 * 60])))) and phone.find(
                                        '*') < 0]) == 0:  # 2个紧急联系人不在近180天通话记录中()
                                antifraud_message['Y3003'] = 'reject'

                            if len(set([scorpionOriginalData_call_list2[i]['time'][:10] for i in
                                        list(range(len(scorpionOriginalData_call_list2))) if \
                                        int(modeldata['data']['order_time']) - time.mktime(
                                            time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                          '%Y-%m-%d %H:%M:%S')) <= 7 * 24 * 60 * 60])) <= 1:  # 最近7天无通话记录天数不低于6天
                                antifraud_message['Y3004'] = 'reject'
                            if len(set([scorpionOriginalData_call_list2[i]['time'][:10] for i in
                                        list(range(len(scorpionOriginalData_call_list2))) if \
                                        int(modeldata['data']['order_time']) - time.mktime(
                                            time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                          '%Y-%m-%d %H:%M:%S')) <= 15 * 24 * 60 * 60])) <= 3:  # 最近15天无通话记录天数不低于12天
                                antifraud_message['Y3005'] = 'reject'
                            if len(set([scorpionOriginalData_call_list2[i]['time'][:10] for i in
                                        list(range(len(scorpionOriginalData_call_list2))) if \
                                        int(modeldata['data']['order_time']) - time.mktime(
                                            time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                          '%Y-%m-%d %H:%M:%S')) <= 30 * 24 * 60 * 60])) <= 9:  # 最近30天无通话记录天数不低于21天
                                antifraud_message['Y3006'] = 'reject'
                            if len(set([scorpionOriginalData_call_list2[i]['time'][:10] for i in
                                        list(range(len(scorpionOriginalData_call_list2))) if \
                                        int(modeldata['data']['order_time']) - time.mktime(
                                            time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                          '%Y-%m-%d %H:%M:%S')) <= 90 * 24 * 60 * 60])) <= 20:  # 最近90天无通话记录天数不低于70天
                                antifraud_message['Y3007'] = 'reject'

                            ##短时通话占比较高
                            duration30_5 = [scorpionOriginalData_call_list2[i]['duration'] for i in
                                            list(range(len(scorpionOriginalData_call_list2))) if \
                                            int(modeldata['data']['order_time']) - time.mktime(
                                                time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                              '%Y-%m-%d %H:%M:%S')) <= 30 * 24 * 60 * 60]
                            duration90_6 = [scorpionOriginalData_call_list2[i]['duration'] for i in
                                            list(range(len(scorpionOriginalData_call_list2))) if \
                                            int(modeldata['data']['order_time']) - time.mktime(
                                                time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                              '%Y-%m-%d %H:%M:%S')) <= 90 * 24 * 60 * 60]

                            if len([i for i in duration30_5 if i <= 5]) / len(
                                    duration30_5) >= 0.5:  # 近30天通话时长小于等于5s通话占占总通话比
                                antifraud_message['Y3010'] = 'reject'
                            if len([i for i in duration90_6 if i <= 6]) / len(
                                    duration90_6) >= 0.5:  # 近90天通话时长小于等于6s通话占占总通话比
                                antifraud_message['Y3011'] = 'reject'

                            ##主叫次数较低
                            dail90 = [scorpionOriginalData_call_list2[i]['dial_type'] for i in
                                      list(range(len(scorpionOriginalData_call_list2))) if \
                                      int(modeldata['data']['order_time']) - time.mktime(
                                          time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                        '%Y-%m-%d %H:%M:%S')) <= 90 * 24 * 60 * 60]
                            if len([i for i in dail90 if
                                    i.find('DIAL') >= 0 and i.find('DIALED') < 0]) <= 3:  # 近90天月均主叫次数不超过1次
                                antifraud_message['Y3012'] = 'reject'

                            # 最近一次通话与订单时间间隔超过15天
                            if int(modeldata['data']['order_time']) - max(
                                    list(map(lambda x: time.mktime(time.strptime(x['time'],
                                                                                 '%Y-%m-%d %H:%M:%S')),
                                             scorpionOriginalData_call_list2))) > 15 * 24 * 60 * 60:
                                antifraud_message['Y3020'] = 'reject'
                        # print(list(map(lambda x:x['b'],[])).index('1'))  ##此办法找key，避免数据有误
                except:
                    logger.info('{0},魔蝎通话记录解析错误'.format(modeldata['orderNo']))

                ####以下是魔蝎特有标签----确认字典
                try:
                    if modeldata['data']['scorpionAccessReport']:
                        behavior_check = modeldata['data']['scorpionAccessReport']['behavior_check']
                        if int(re.sub("\D", "", behavior_check[
                            list(map(lambda x: x['check_point'], behavior_check)).index('phone_power_off')][
                            'result'])) > 15:  # 关机次数超过15天--沟通时间限制-(默认静默与关机相同)---字典格式有哪些
                            antifraud_message['Y3014'] = 'review'
                        if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index('contact_110')][
                            'result'] == u'多次通话':  # 110通话情况
                            antifraud_message['Y3021'] = 'reject'
                        if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index('contact_court')][
                            'result'] == u'多次通话':  # 法院号码通话情况
                            antifraud_message['Y3016'] = 'reject'
                        if \
                                behavior_check[
                                    list(map(lambda x: x['check_point'], behavior_check)).index('contact_lawyer')][
                                    'result'] == u'多次通话':  # 律师号码通话情况
                            antifraud_message['Y3017'] = 'reject'
                        if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index('contact_night')][
                            'result'] == u'频繁夜间活动':  # 夜间活动情况
                            antifraud_message['Y3015'] = 'review'
                        if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index('contact_loan')][
                            'result'] == u"经常被联系":  # 贷款类号码联系情况
                            antifraud_message['Y3018'] = 'reject'
                        if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index('phone_call')][
                            'result'] == u"数量稀少" or \
                                behavior_check[
                                    list(map(lambda x: x['check_point'], behavior_check)).index('phone_call')][
                                    'result'] == u"数量众多":  # 互通过电话号码数量
                            antifraud_message['Y3019'] = 'review'
                        if \
                                behavior_check[
                                    list(map(lambda x: x['check_point'], behavior_check)).index('contact_collection')][
                                    'result'] == u"经常被联系":  # 魔蝎有催收类号码联系情况
                            antifraud_message['Y3023'] = 'reject'
                except:
                    logger.info('{0},魔蝎运营商报告解析错误'.format(modeldata['orderNo']))


            elif modeldata['data']['loanBondOrignalData']:

                ##入网时长  数据缺失是null还是‘’？
                try:
                    if modeldata['data']['loanBondOrignalData'][0]['basic']['reg_time']:  ###注意与之前结构变化
                        if modeldata['data']['loanBondOrignalData'][0]['basic']['reg_time'].replace(" ",
                                                                                                    "") == "" or \
                                int(modeldata['data']['order_time']) - time.mktime(
                            time.strptime(modeldata['data']['loanBondOrignalData'][0]['basic']['reg_time'],
                                          '%Y-%m-%d %H:%M:%S')) < 180 * 24 * 60 * 60 or \
                                modeldata['data']['loanBondOrignalData'][0]['basic']['reg_time'].replace(' ',
                                                                                                         '') == '':
                            antifraud_message['Y1001'] = 'reject'
                except:
                    logger.info('{0},贷后邦入网时长解析错误'.format(modeldata['orderNo']))

                ##短信相关
                try:
                    if modeldata['data']['loanBondOrignalData'][0]['smses']:
                        if len(modeldata['data']['loanBondOrignalData'][0]['smses']) == 0:  ##无短信内容
                            antifraud_message['Y2001'] = 'reject'
                        if len(modeldata['data']['loanBondOrignalData'][0]['smses']) != 0 and len(  ##短信记录过少
                                modeldata['data']['loanBondOrignalData'][0]['smses']) < 30:
                            antifraud_message['Y2003'] = 'reject'
                except:
                    logger.info('{0},贷后邦运营商短信解析错误'.format(modeldata['orderNo']))

                ##通话记录相关
                try:
                    loanBondOrignalData_call_list = modeldata['data']['loanBondOrignalData'][0]['calls']
                    if len(loanBondOrignalData_call_list) == 0:  # 通话记录缺失（实际贷后邦数据不会存在此情形）
                        antifraud_message['Y3001'] = 'reject'
                    else:
                        if max(list(map(lambda x: time.mktime(time.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S')),
                                        loanBondOrignalData_call_list))) - \
                                min(list(map(lambda x: time.mktime(time.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S')),
                                             loanBondOrignalData_call_list))) < 90 * 24 * 60 * 60:  # 通话时间跨度小于90天
                            antifraud_message['Y3002'] = 'reject'
                        if len([phone for phone in
                                list(map(
                                    lambda x: x.replace('+86', "").replace('+', '').replace(' ', '').replace('-', ''),
                                    jjlxr_json_phone)) \
                                if phone in list(
                                set(list(map(lambda x: x['other_cell_phone'],
                                             loanBondOrignalData_call_list)))) and phone.find(
                                '*') < 0]) == 0:  # 2紧急联系人均不在通话记录中
                            antifraud_message['Y3003'] = 'reject'

                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in
                                    list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(
                                        time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                      '%Y-%m-%d %H:%M:%S')) <= 7 * 24 * 60 * 60])) <= 1:  # 最近7天无通话记录天数不低于6天
                            antifraud_message['Y3004'] = 'reject'
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in
                                    list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(
                                        time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                      '%Y-%m-%d %H:%M:%S')) <= 15 * 24 * 60 * 60])) <= 3:  # 最近15天无通话记录天数不低于12天
                            antifraud_message['Y3005'] = 'reject'
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in
                                    list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(
                                        time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                      '%Y-%m-%d %H:%M:%S')) <= 30 * 24 * 60 * 60])) <= 9:  # 最近30天无通话记录天数不低于21天
                            antifraud_message['Y3006'] = 'reject'
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in
                                    list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(
                                        time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                      '%Y-%m-%d %H:%M:%S')) <= 90 * 24 * 60 * 60])) <= 20:  # 最近90天无通话记录天数不低于70天
                            antifraud_message['Y3007'] = 'reject'

                        ##被叫接通次数较少------本地通话记录才能实现（注意双卡双待的手机）
                        '''
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(time.strptime(loanBondOrignalData_call_list[i]['start_time'],'%Y-%m-%d %H:%M:%S')) <=90*24 * 60 * 60]))<=20:# 最近90天无通话记录天数不低于70天
                                antifraud_message['Y3007']='reject'
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(time.strptime(loanBondOrignalData_call_list[i]['start_time'],'%Y-%m-%d %H:%M:%S')) <=90*24 * 60 * 60]))<=20:# 最近90天无通话记录天数不低于70天
                                antifraud_message['Y3007']='reject'
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(time.strptime(loanBondOrignalData_call_list[i]['start_time'],'%Y-%m-%d %H:%M:%S')) <=90*24 * 60 * 60]))<=20:# 最近90天无通话记录天数不低于70天
                                antifraud_message['Y3007']='reject'
                        if len(set([loanBondOrignalData_call_list[i]['start_time'][:10] for i in list(range(len(loanBondOrignalData_call_list))) if \
                                    int(modeldata['data']['order_time']) - time.mktime(time.strptime(loanBondOrignalData_call_list[i]['start_time'],'%Y-%m-%d %H:%M:%S')) <=90*24 * 60 * 60]))<=20:# 最近90天无通话记录天数不低于70天
                                antifraud_message['Y3007']='reject'

                        '''

                        ##短时通话占比较高
                        duration30_5 = [loanBondOrignalData_call_list[i]['use_time'] for i in
                                        list(range(len(loanBondOrignalData_call_list))) if \
                                        int(modeldata['data']['order_time']) - time.mktime(
                                            time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                          '%Y-%m-%d %H:%M:%S')) <= 30 * 24 * 60 * 60]
                        duration90_6 = [loanBondOrignalData_call_list[i]['use_time'] for i in
                                        list(range(len(loanBondOrignalData_call_list))) if \
                                        int(modeldata['data']['order_time']) - time.mktime(
                                            time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                          '%Y-%m-%d %H:%M:%S')) <= 90 * 24 * 60 * 60]
                        if duration30_5:
                            if len([i for i in duration30_5 if i <= 5]) / len(
                                    duration30_5) >= 0.5:  # 近30天通话时长小于等于5s通话占占总通话比
                                antifraud_message['Y3010'] = 'reject'
                        if duration90_6:
                            if len([i for i in duration90_6 if i <= 6]) / len(
                                    duration90_6) >= 0.5:  # 近90天通话时长小于等于6s通话占占总通话比
                                antifraud_message['Y3011'] = 'reject'

                        ##主叫次数较低

                        dail90 = [loanBondOrignalData_call_list[i]['init_type'] for i in
                                  list(range(len(loanBondOrignalData_call_list))) if \
                                  int(modeldata['data']['order_time']) - time.mktime(
                                      time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                    '%Y-%m-%d %H:%M:%S')) <= 90 * 24 * 60 * 60]
                        if len([i for i in dail90 if i and i.find(u'主叫') >= 0]) <= 3:  # 近90天月均主叫次数不超过1次
                            antifraud_message['Y3012'] = 'reject'
                        # 最近一次通话与订单时间间隔超过15天
                        if int(modeldata['data']['order_time']) - max(list(
                                map(lambda x: time.mktime(time.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S')),
                                    loanBondOrignalData_call_list))) > 15 * 24 * 60 * 60:
                            antifraud_message['Y3020'] = 'reject'
                except:
                    logger.info('{0},贷后邦通话记录解析错误'.format(modeldata['orderNo']))
                ####以下是贷后邦特有标签
                try:
                    behavior_check = modeldata['data']['loanBondData']['behavior_check']
                    if int(re.sub("\D", "",
                                  behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'关机情况')][
                                      'result'])) > 15:  # 关机次数超过15天--沟通时间限制-(默认静默与关机相同)---字典格式有哪些
                        antifraud_message['Y3014'] = 'review'
                    if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'110话通话情况')][
                        'result'] == u'多次通话':  # 110通话情况
                        antifraud_message['Y3021'] = 'reject'
                    if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'法院号码通话情况')][
                        'result'] == u'多次通话':  # 法院号码通话情况
                        antifraud_message['Y3016'] = 'reject'
                    if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'律师号码通话情况')][
                        'result'] == u'多次通话':  # 律师号码通话情况
                        antifraud_message['Y3017'] = 'reject'
                    if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'夜间活动情况')][
                        'result'] == u'频繁夜间活动':  # 夜间活动情况
                        antifraud_message['Y3015'] = 'review'
                    if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'贷款类号码联系情况')][
                        'result'] == u"经常被联系":  # 贷款类号码联系情况
                        antifraud_message['Y3018'] = 'reject'
                    if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'互通过电话的号码数量')][
                        'result'] == u"数量稀少" or \
                            behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index(u'互通过电话的号码数量')][
                                'result'] == u"数量众多":  # 互通过电话号码数量
                        antifraud_message['Y3019'] = 'review'
                    # if behavior_check[list(map(lambda x: x['check_point'], behavior_check)).index('contact_collection')][
                    # 'result'] == u"经常被联系":  # 贷后邦催收类号码联系情况
                    # antifraud_message['Y3023'] = 'reject'
                except:
                    logger.info('{0},贷后邦运营商报告解析错误'.format(modeldata['orderNo']))

            ###通讯录相关（只能本地爬取） 苹果与安卓均能爬取----匿名规则暂时未加(技术端---通讯录为空的客户前置会拒绝)
            try:
                if modeldata['data']['mailList']:
                    txl_json_name = [name for name in
                                     list(set(list(map(lambda x: get_value(x, 'name'), modeldata['data']['mailList']))))
                                     if name]  ##手机通讯录对应的名字
                    txl_json_phone = [i for i in list(
                        set(list(map(lambda x: get_value(x, 'phone'), modeldata['data']['mailList']))))
                                      if i and i.replace('+86', "").replace('+', '').replace(' ', '').replace('-',
                                                                                                              '')]  ##手机通讯录对应的手机号码
                    if not txl_json_name or not txl_json_phone:
                        antifraud_message['T1001'] = 'reject'
                    else:
                        if not modeldata['data']['scorpionOriginalData'] and not modeldata['data'][
                            'loanBondOrignalData']:
                            antifraud_message['Y3001'] = 'reject'
                        else:
                            ##运营商通话记录近3个月通话top20客户（区分魔蝎还是贷后邦）
                            if modeldata['data']['scorpionOriginalData']:
                                if len(scorpionOriginalData_call_list2) > 0:
                                    peer_number_last90days = [
                                        phone.replace('+86', "").replace('+', '').replace(' ', '').replace('-', '')
                                        for
                                        phone in
                                        [scorpionOriginalData_call_list2[i].get('peer_number') for i in
                                         list(range(len(scorpionOriginalData_call_list2))) if \
                                         int(modeldata['data']['order_time']) - time.mktime(
                                             time.strptime(scorpionOriginalData_call_list2[i]['time'],
                                                           '%Y-%m-%d %H:%M:%S')) < 90 * 24 * 60 * 60]]
                                    peer_number_last90daystop20 = list(
                                        map(lambda x: x[0], sorted(dict(Counter(peer_number_last90days)).items(),
                                                                   key=lambda x: x[1], reverse=True)))[:20]
                            else:  ###后续考虑删除短号后进行计算
                                peer_number_last90days = [
                                    phone.replace('+86', "").replace('+', '').replace(' ', '').replace('-', '')
                                    for
                                    phone in [loanBondOrignalData_call_list[i].get('other_cell_phone') for i in
                                              list(range(len(loanBondOrignalData_call_list))) if \
                                              int(modeldata['data']['order_time']) - time.mktime(
                                                  time.strptime(loanBondOrignalData_call_list[i]['start_time'],
                                                                '%Y-%m-%d %H:%M:%S')) < 90 * 24 * 60 * 60]]
                                peer_number_last90daystop20 = list(
                                    map(lambda x: x[0], sorted(dict(Counter(peer_number_last90days)).items(),
                                                               key=lambda x: x[1], reverse=True)))[:20]

                            if len(list(set(list(
                                    map(lambda x: x.get('phone'), modeldata['data']['mailList']))))) < 30:  # 通讯录手机号个数
                                antifraud_message['T1004'] = 'reject'
                            if len(list(map(lambda x: len(x), txl_json_phone))) / len(
                                    txl_json_phone) <= 0.5:  ###11位手机号占比过少
                                antifraud_message['T1005'] = 'reject'
                            if len([phone for phone in
                                    list(map(
                                        lambda x: x.replace('+86', "").replace('+', '').replace(' ', '').replace('-',
                                                                                                                 ''),
                                        jjlxr_json_phone)) if phone in txl_json_phone]) == 0:  ###2个紧急联系人号码不在通讯录中!!!!
                                antifraud_message['T1003'] = 'reject'
                            if len([warn for warn in
                                    [max(list(
                                        map(lambda x: x[i],
                                            [list(map(lambda x: x.find(i), txl_json_name)) for i in warn_words])))
                                        for
                                        i in list(range(len(txl_json_name)))] if warn >= 0]) > 5:  ##联系人中带敏感词超过5人
                                antifraud_message['T1008'] = 'reject'
                            if len([warn for warn in
                                    [max(list(
                                        map(lambda x: x[i],
                                            [list(map(lambda x: x.find(i), txl_json_name)) for i in warn_words])))
                                        for
                                        i in list(range(len(txl_json_name)))] if warn >= 0]) / len(
                                txl_json_name) > 0.1:  ##:##联系人中带敏感词比例超过10%， bug  姓名为null
                                antifraud_message['T1007'] = 'reject'
                            if len([relation for relation in
                                    [max(list(
                                        map(lambda x: x[i],
                                            [list(map(lambda x: x.find(i), txl_json_name)) for i in relation_words])))
                                        for i in list(range(len(txl_json_name)))] if
                                    relation >= 0]) < 1:  ##通讯录不带有亲属类称谓联系人
                                antifraud_message['T1002'] = 'reject'

                            if [i for i in list(map(lambda x: len(x), txl_json_phone)) if i <= 6]:
                                if len([i for i in list(map(lambda x: len(x), txl_json_phone)) if i <= 6]) / len(
                                        txl_json_phone) >= 0.3:  ##短号比例较高
                                    antifraud_message['T1009'] = 'reject'
                            if len([phone for phone in peer_number_last90daystop20 if
                                    phone.find('*') >= 0]) == 0:  ##通讯录真实性，首先判断号码是否脱敏----默认前提 联系人数量超过20人
                                if len([phone for phone in txl_json_phone if
                                        phone in peer_number_last90daystop20]) < 3:  ##通讯录真实性
                                    antifraud_message['T1006'] = 'reject'
                            # elif len([phone for phone in peer_number_last90daystop20 if phone.find('*')>=0])==20:
                            # print('根据脱敏类型判断与第三方沟通')
                            elif len([phone for phone in peer_number_last90daystop20 if phone.find('*') >= 0]) < 20:
                                real_phone = [phone for phone in peer_number_last90daystop20 if phone.find('*') < 0]
                                ano_phone = [phone for phone in peer_number_last90daystop20 if phone.find('*') >= 0]
                                if len(real_phone) > 3 and len(
                                        [phone for phone in txl_json_phone if phone in real_phone]) < 3:  ##通讯录真实性
                                    antifraud_message['T1006'] = 'review'
                                    # print('根据脱敏类型判断与第三方沟通')
                else:
                    # if not modeldata['data']['mailList']:  ##安卓手机通讯录为空----需要实际数据观察待调优是none还是空字符串
                    antifraud_message['T1001'] = 'reject'
            except:

                logger.info('{0},通讯录数据解析错误'.format(modeldata['orderNo']))
            ##紧急联系人相关---紧急联系人关联生产库回溯30天关联的userid 以及对应最新的时间（注意后续userid命名规则变化）
            try:
                if modeldata['data']['contacts_his']:  ##此处时间是时间戳格式
                    if len([modeldata['data']['contacts_his'][i] for i in
                            list(range(len(modeldata['data']['contacts_his']))) if \
                            int(modeldata['data']['order_time']) - int(modeldata['data']['contacts_his'][i][
                                                                           'order_time']) < 3 * 60 * 60]) >= 1:  ##紧急联系人近3小时关联联系人过多(确认当前数据未落入是生产库)
                        antifraud_message['J1001'] = 'reject'
                    if len([modeldata['data']['contacts_his'][i] for i in
                            list(range(len(modeldata['data']['contacts_his']))) if \
                            int(modeldata['data']['order_time']) - int(modeldata['data']['contacts_his'][i][
                                                                           'order_time']) < 72 * 60 * 60]) >= 2:  ##紧急联系人近72小时关联联系人过多(确认当前数据未落入是生产库)
                        antifraud_message['J1002'] = 'reject'
                    if len([modeldata['data']['contacts_his'][i] for i in
                            list(range(len(modeldata['data']['contacts_his']))) if \
                            int(modeldata['data']['order_time']) - int(modeldata['data']['contacts_his'][i][
                                                                           'order_time']) < 30 * 24 * 60 * 60]) >= 3:  ##紧急联系人近1个月关联联系人过多(确认当前数据未落入是生产库)
                        antifraud_message['J1003'] = 'reject'
            except:
                logger.info('{0},紧急联系人关联他人紧急联系人订单解析错误'.format(modeldata['orderNo']))
            try:
                if modeldata['data']['contacts_order']:  ##此处刘磊是时间戳
                    if len([modeldata['data']['contacts_order'][i] for i in
                            list(range(len(modeldata['data']['contacts_order']))) if \
                            int(modeldata['data']['order_time']) - int(
                                modeldata['data']['contacts_order'][i]['order_time'])
                            < 3 * 24 * 60 * 60]) >= 1:  ##紧急联系人近3小时关联联系人过多(确认当前数据未落入是生产库)
                        antifraud_message['J1004'] = 'reject'
            except:
                logger.info('{0},紧急联系人本人订单解析错误'.format(modeldata['orderNo']))

            ##设备相关---紧急联系人关联生产库回溯30天关联的userid 以及对应最新的时间（注意后续userid命名规则变化）--------该规则目前不可用
            try:
                if modeldata['data']['deviceId_his']:
                    if len([modeldata['data']['deviceId_his'][i] for i in
                            list(range(len(modeldata['data']['deviceId_his']))) if \
                            int(modeldata['data']['order_time']) - int(modeldata['data']['deviceId_his'][i][
                                                                           'order_time']) < 3 * 60 * 60]) >= 1:  ##紧急联系人近3小时关联联系人过多(确认当前数据未落入是生产库)
                        antifraud_message['S1006'] = 'reject'
                    if len([modeldata['data']['deviceId_his'][i] for i in
                            list(range(len(modeldata['data']['deviceId_his']))) if \
                            int(modeldata['data']['order_time']) - int(modeldata['data']['deviceId_his'][i][
                                                                           'order_time']) < 72 * 60 * 60]) >= 3:  ##紧急联系人近72小时关联联系人过多(确认当前数据未落入是生产库)
                        antifraud_message['S1005'] = 'reject'
            except:
                logger.info('{0},设备历史订单解析错误'.format(modeldata['orderNo']))

            ##applist命中敏感软件------目前仅安卓手机可用
            # app_words = []
            try:
                if modeldata['data']['app_list']:
                    if modeldata['data']['app_list'] != 'null':
                        if max(list(reduce(lambda x, y: x + y,
                                           [list(map(lambda t: t['appName'].find(i),
                                                     json.loads(modeldata['data']['app_list'])))
                                            for i
                                            in app_words]))) >= 0:
                            antifraud_message['S1003'] = 'review'
            except:
                logger.info('{0},applist解析错误'.format(modeldata['orderNo']))

            return {'orderNo': modeldata['data']['orderNo'], 'limit_message': limit_message,'isAgain':0,
                    'order_time': modeldata['data']['order_time'],
                    'name': modeldata['data']['name'],
                    'idCardNo': modeldata['data']['idCardNo'],
                    'antifraud_message': antifraud_message}

        else:  ###老客户
            return {'orderNo': modeldata['data']['orderNo'], 'limit_message': limit_message,'isAgain':1,
                    'order_time':modeldata['data']['order_time'],
                    'name': modeldata['data']['name'],
                    'idCardNo': modeldata['data']['idCardNo'],
                    'antifraud_message': antifraud_message}
    except:  ###特殊异常 检查数据
        limit_message['D1001'] = 'reject'
        return {'orderNo': modeldata['data']['orderNo'], 'limit_message': limit_message,'isAgain':3,
                'antifraud_message': antifraud_message}


def final_score(model_result, rule_result):
    new_dict = {'limit_message': {}, 'antifraud_message': {}}
    # ori_dict = rule_data(modeldata)
    for k, v in rule_result['limit_message'].items():
        if v == 'reject':
            new_dict['limit_message'][k] = v
    for k, v in rule_result['antifraud_message'].items():
        if v == 'reject':
            new_dict['antifraud_message'][k] = v
    if len(new_dict['limit_message']) + len(new_dict['antifraud_message']) != 0:
        final_score = {'orderNo': rule_result['orderNo'], 'rule_score': 200.1,
                       'model_score': json.loads(model_result)['comprehensive_score'],
                       'model_score_type': json.loads(model_result)['mode_type'],
                       'status': json.loads(model_result)['status'],
                       'desc': json.loads(model_result)['desc'],
                       'order_time': rule_result['order_time'],
                       'name': rule_result['name'],
                       'idCardNo': rule_result['idCardNo'],
                       'isAgain': rule_result['isAgain'],
                       'comprehensive_score': 200.1}
    else:
        final_score = {'orderNo': rule_result['orderNo'], 'rule_score': 650.1,
                       'model_score': json.loads(model_result)['comprehensive_score'],
                       'model_score_type': json.loads(model_result)['mode_type'],
                       'status': json.loads(model_result)['status'],
                       'desc': json.loads(model_result)['desc'],
                       'order_time': rule_result['order_time'],
                       'name': rule_result['name'],
                       'idCardNo': rule_result['idCardNo'],
                       'isAgain': rule_result['isAgain'],
                       'comprehensive_score': json.loads(model_result)['comprehensive_score']}

    return json.dumps(final_score)
