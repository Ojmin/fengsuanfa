# -*- coding: utf-8 -*-
"""
Created on Tuesday May  22 21:00:00 2018

@author: zhanghaiyang

SCORECARD FOR TMALL

"""
#contimes_called_90_180_rate_w------------float(month3_called_update)/float(month6_called_update) if float(month6_called_update) !=float(0) else ''


def score_card_xinyan_nods(model):
    score = 628.0

    if model["contimes_called_90_180_rate_w"] == '':
        score += 0.0
    elif  model["contimes_called_90_180_rate_w"] < 0.407:
        score += -14.0
    elif model["contimes_called_90_180_rate_w"] >= 0.407 and model["contimes_called_90_180_rate_w"] < 0.454:
        score += 9.0
    elif model["contimes_called_90_180_rate_w"] >= 0.454 and model["contimes_called_90_180_rate_w"] < 0.594:
        score += 12.0
    elif model["contimes_called_90_180_rate_w"] >= 0.594 and model["contimes_called_90_180_rate_w"] < 0.651:
        score += 1.0
    elif model["contimes_called_90_180_rate_w"] >= 0.651 and model["contimes_called_90_180_rate_w"] < 0.67:
        score += -10.0
    elif model["contimes_called_90_180_rate_w"] >= 0.67 and model["contimes_called_90_180_rate_w"] < 0.811:
        score += -21.0
    elif model["contimes_called_90_180_rate_w"] >= 0.811:
        score += -27.0
    else:
        score += 0.0
    #contimes_called_30_90_rate_W--------float(month1_called_update)/float(month3_called_update) if float(month3_called_update) !=float(0) else ''

    if model["contimes_called_30_90_rate_W"] == '':
        score += 0.0
    elif  model["contimes_called_30_90_rate_W"] < 0.235:
        score += -26.0
    elif model["contimes_called_30_90_rate_W"] >= 0.235 and model["contimes_called_30_90_rate_W"] < 0.289:
        score += -4.0
    elif model["contimes_called_30_90_rate_W"] >= 0.289 and model["contimes_called_30_90_rate_W"] < 0.338:
        score += 12.0
    elif model["contimes_called_30_90_rate_W"] >= 0.338 and model["contimes_called_30_90_rate_W"] < 0.378:
        score += 18.0
    elif model["contimes_called_30_90_rate_W"] >= 0.378 and model["contimes_called_30_90_rate_W"] < 0.447:
        score += 4.0
    elif model["contimes_called_30_90_rate_W"] >= 0.447 and model["contimes_called_30_90_rate_W"] < 0.507:
        score += -16.0
    elif model["contimes_called_30_90_rate_W"] >= 0.507:
        score += -36.0
    else:
        score = score + 0.0

    #conode_30days----------np.array(sqldf("select count(distinct CASE WHEN time >=datetime(update_time,'-30 days') and time<update_time THEN peer_number ELSE null END) from data1;"))
    #data1 = pd.DataFrame(call_list, columns=columns_base)
    #
    if model["conode_30days"] == '':
        score += 0.0
    elif  model["conode_30days"] < 37.0:
        score += -13.0
    elif model["conode_30days"] >= 37.0 and model["conode_30days"] < 58.0:
        score += 0.0
    elif model["conode_30days"] >= 58.0 and model["conode_30days"] < 112.0:
        score += 8.0
    elif model["conode_30days"] >= 112.0 and model["conode_30days"] < 188.0:
        score += 3.0
    elif model["conode_30days"] >= 188.0 and model["conode_30days"] < 259.0:
        score += -14.0
    elif model["conode_30days"] >= 259.0:
        score += -28.0
    else:
        score += 0.0

     #contimes_called_10s_7days----np.array(sqldf("select SUM(CASE WHEN time>=datetime(update_time,'-7 days') and time<update_time and dial_type like '%被叫%' and duration<10 THEN 1 ELSE 0 END)  from data1;"))
     ##data1 = pd.DataFrame(call_list, columns=columns_base)

    if model["contimes_called_10s_7days"] == '':
        score += 0.0
    elif  model["contimes_called_10s_7days"] < 1.0:
        score += -29.0
    elif model["contimes_called_10s_7days"] >= 1.0 and model["contimes_called_10s_7days"] < 3.0:
        score += -19.0
    elif model["contimes_called_10s_7days"] >= 3.0 and model["contimes_called_10s_7days"] < 5.0:
        score += -2.0
    elif model["contimes_called_10s_7days"] >= 5.0 and model["contimes_called_10s_7days"] < 10.0:
        score += 17.0
    elif model["contimes_called_10s_7days"] >= 10.0 and model["contimes_called_10s_7days"] < 16.0:
        score += 40.0
    elif model["contimes_called_10s_7days"] >= 16.0:
        score += 33.0
    else:
        score = score + 0.0

    #
    if model["contimes_called_5s_90days"] == '':
        score += 0.0
    elif  model["contimes_called_5s_90days"] < 3.0:
        score += 9.0
    elif model["contimes_called_5s_90days"] >= 3.0 and model["contimes_called_5s_90days"] < 6.0:
        score += 8.0
    elif model["contimes_called_5s_90days"] >= 6.0 and model["contimes_called_5s_90days"] < 21.0:
        score += -2.0
    elif model["contimes_called_5s_90days"] >= 21.0:
        score += -41.0
    else:
        score = score + 0.0


    if model["contimes_called_60s_7_30_rate"] == '':
        score += 0.0
    elif  model["contimes_called_60s_7_30_rate"] < 0.129:
        score += -30.0
    elif model["contimes_called_60s_7_30_rate"] >= 0.129 and model["contimes_called_60s_7_30_rate"] < 0.18:
        score += -3.0
    elif model["contimes_called_60s_7_30_rate"] >= 0.18 and model["contimes_called_60s_7_30_rate"] < 0.316:
        score += 12.0
    elif model["contimes_called_60s_7_30_rate"] >= 0.316 and model["contimes_called_60s_7_30_rate"] < 0.411:
        score += -14.0
    elif model["contimes_called_60s_7_30_rate"] >= 0.411:
        score += -38.0
    else:
        score = score + 0.0

    '''
    if model["dis_alltime_allpro_succpay_maxdis_cnt5"] == '':
        score += 0.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] == -99998:
        score += 0.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] < 8.0:
        score += 42.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] >= 8.0 and model["dis_alltime_allpro_succpay_maxdis_cnt5"] < 31.0:
        score += 19.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] >= 31.0 and model["dis_alltime_allpro_succpay_maxdis_cnt5"] < 80.0:
        score += 16.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] >= 80.0 and model["dis_alltime_allpro_succpay_maxdis_cnt5"] < 152.0:
        score += 4.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] >= 152.0 and model["dis_alltime_allpro_succpay_maxdis_cnt5"] < 219.0:
        score += -12.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] >= 219.0:
        score += -42.0
    else:
        score = score + 0.0
     '''

    if model["dis_alltime_allpro_succpay_maxdis_cnt5"] =="-99998":
        score += 0.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"]=="[0,8)":
        score += 42.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] =="[8,15)" or model["dis_alltime_allpro_succpay_maxdis_cnt5"]=="[15,31)":
        score += 19.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] =="[31,80)" :
        score += 16.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"] =="[80,152)":
        score += 4.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"]=="[152,219)":
        score += -12.0
    elif model["dis_alltime_allpro_succpay_maxdis_cnt5"]=="[219,+inf)":
        score += -42.0
    else:
        score = score + 0.0

    '''
    if model["sum_work_allpro_pay_amt_cnt10"] == "":
        score += 0.0
    elif model["sum_work_allpro_pay_amt_cnt10"] =="-99998":
        score += 0.0
    elif  model["sum_work_allpro_pay_amt_cnt10"] < 553.11:
        score += -56.0
    elif model["sum_work_allpro_pay_amt_cnt10"] >= 553.11 and model["sum_work_allpro_pay_amt_cnt10"] < 2740.26:
        score += -9.0
    elif model["sum_work_allpro_pay_amt_cnt10"] >= 2740.26 and model["sum_work_allpro_pay_amt_cnt10"] < 4077.2:
        score += -2.0
    elif model["sum_work_allpro_pay_amt_cnt10"] >= 4077.2 and model["sum_work_allpro_pay_amt_cnt10"] < 9061.47:
        score += 5.0
    elif model["sum_work_allpro_pay_amt_cnt10"] >= 9061.47 and model["sum_work_allpro_pay_amt_cnt10"] < 12453.74:
        score += 13.0
    elif model["sum_work_allpro_pay_amt_cnt10"] >= 12453.74:
        score += 20.0
    else:
        score = score + 0.0
     '''


    if model["sum_work_allpro_pay_amt_cnt10"] == "-99998":
        score += 0.0
    elif  model["sum_work_allpro_pay_amt_cnt10"]=="[0,553.11)":
        score += -56.0
    elif model["sum_work_allpro_pay_amt_cnt10"] =="[553.11,1100.11)" or model["sum_work_allpro_pay_amt_cnt10"]=="[1100.11,2740.26)":
        score += -9.0
    elif model["sum_work_allpro_pay_amt_cnt10"]=="[2740.26,4077.2)":
        score += -2.0
    elif model["sum_work_allpro_pay_amt_cnt10"]=="[4077.2,9061.47)":
        score += 5.0
    elif model["sum_work_allpro_pay_amt_cnt10"]=="[9061.47,12453.74)":
        score += 13.0
    elif model["sum_work_allpro_pay_amt_cnt10"]=="[12453.74,+inf)":
        score += 20.0
    else:
        score = score + 0.0

    '''
    if model["sum_alltime_noncdq_likeduepay_days_cnt3"] == '':
        score += 0.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"] == -99998:
        score += 0.0
    elif  model["sum_alltime_noncdq_likeduepay_days_cnt3"] < 3.0:
        score += 1.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"] >= 3.0 and model["sum_alltime_noncdq_likeduepay_days_cnt3"] < 4.0:
        score += 25.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"] >= 4.0 and model["sum_alltime_noncdq_likeduepay_days_cnt3"] < 82.0:
        score += -8.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"] >= 82.0:
        score += -33.0
    else:
        score = score + 0.0
    '''


    if model["sum_alltime_noncdq_likeduepay_days_cnt3"] == '-99998':
        score += 0.0
    elif  model["sum_alltime_noncdq_likeduepay_days_cnt3"] =="[0,3)":
        score += 1.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"]=="[3,4)":
        score += 25.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"]=="[4,5)" or model["sum_alltime_noncdq_likeduepay_days_cnt3"]=="[5,7)" or \
            model["sum_alltime_noncdq_likeduepay_days_cnt3"]=="[7,10)" or  model["sum_alltime_noncdq_likeduepay_days_cnt3"]=="[10,82)":
        score += -8.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"]=="[82,+inf)":
        score += -33.0
    else:
        score = score + 0.0

    '''
    if model["min_alltime_allpro_pay_amt_m1"] == '':
        score += 0.0
    elif model["min_alltime_allpro_pay_amt_m1"] == -99998:
        score += 0.0
    elif  model["min_alltime_allpro_pay_amt_m1"] < 10.08:
        score += -14.0
    elif model["min_alltime_allpro_pay_amt_m1"] >= 10.08 and model["min_alltime_allpro_pay_amt_m1"] < 204.38:
        score += 30.0
    elif model["min_alltime_allpro_pay_amt_m1"] >= 204.38 and model["min_alltime_allpro_pay_amt_m1"] < 642.15:
        score += 17.0
    elif model["min_alltime_allpro_pay_amt_m1"] >= 642.15:
        score += 6.0
    else:
        score = score + 0.0
    '''
    if model["min_alltime_allpro_pay_amt_m1"] == '-99998':
        score += 0.0
    elif  model["min_alltime_allpro_pay_amt_m1"]=="[0,5)" or model["min_alltime_allpro_pay_amt_m1"]=="[5,10.08)":
        score += -14.0
    elif model["min_alltime_allpro_pay_amt_m1"]== "[10.08,98)" or model["min_alltime_allpro_pay_amt_m1"]=="[98,204.38)":
        score += 30.0
    elif model["min_alltime_allpro_pay_amt_m1"]=="[204.38,360)" or model["min_alltime_allpro_pay_amt_m1"]=="[360,642.15)":
        score += 17.0
    elif model["min_alltime_allpro_pay_amt_m1"]=="[642.15,+inf)":
        score += 6.0
    else:
        score = score + 0.0

    if (score < 0):
        score = 0
    elif (score > 1000):
        score = 1000
    return score

#score_card_xinyan_nods(model)



if __name__ == "__main__":
    # pass
    # import config
    # data = config.data
    model = {
        'contimes_called_90_180_rate_w': 0,
        'contimes_called_30_90_rate_W': 11,
        'conode_30days': 12,
        'contimes_called_10s_7days': 0.365750529,
        'contimes_called_5s_90days': 0.255045872,
        'contimes_called_60s_7_30_rate': 1,
        'dis_alltime_allpro_succpay_maxdis_cnt5': "[15,31)",#最近5次全部时间全部产品距离非逾期还款第一次距今天数
        'sum_work_allpro_pay_amt_cnt10': "[2740.26,4077.2)",#最近10次工作日全部产品累计还款金额
        'sum_alltime_noncdq_likeduepay_days_cnt3': "[10,82)",#最近3次全部时间非超短期现金贷累计还款疑似逾期天数
        'min_alltime_allpro_pay_amt_m1': "[204.38,360)"#最近1个月全部时间全部产品最小还款金额
    }
    print (score_card_xinyan_nods(model))
    # if model['huabei_totalcreditamount']:
    #     print ('no')
    # else:
    #     print ('aa')