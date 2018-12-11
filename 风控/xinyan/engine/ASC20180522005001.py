# -*- coding: utf-8 -*-
"""
Created on Tuesday May  22 21:00:00 2018

@author: 

SCORECARD FOR RECYCLE AND MAIBEI

"""

def score_card_recycle(model):
    
    score = 0.0
    if model["pct_nbr_cont_3m"] == 99999999:
        score += 64.0
    elif model["pct_nbr_cont_3m"] and model["pct_nbr_cont_3m"] < 40.8:
        score += 57.0
    elif model["pct_nbr_cont_3m"] >= 40.8 and model["pct_nbr_cont_3m"] < 71.4:
        score += 69.0
    elif model["pct_nbr_cont_3m"] >= 71.4 and model["pct_nbr_cont_3m"] < 79.2:
        score += 58.0
    elif model["pct_nbr_cont_3m"] >= 79.2:
        score += 48.0
    else:
        score += 64.0

    if model["pct_nbr_cont_morning"] == 99999999:
        score += 59.0
    elif model["pct_nbr_cont_morning"] and model["pct_nbr_cont_morning"] < 35.8:
        score += 48.0
    elif model["pct_nbr_cont_morning"] >= 35.8 and model["pct_nbr_cont_morning"] < 38.4:
        score += 58.0
    elif model["pct_nbr_cont_morning"] >= 38.4 and model["pct_nbr_cont_morning"] < 48.4:
        score += 63.0
    elif model["pct_nbr_cont_morning"] >= 48.4:
        score += 77.0
    else:
        score += 59.0

    if model["pct_nbr_call_30s"] == 99999999:
        score += 64.0
    elif model["pct_nbr_call_30s"] and model["pct_nbr_call_30s"] < 50.1:
        score += 80.0
    elif model["pct_nbr_call_30s"] >= 50.1 and model["pct_nbr_call_30s"] < 58.9:
        score += 72.0
    elif model["pct_nbr_call_30s"] >= 58.9 and model["pct_nbr_call_30s"] < 71.5:
        score += 63.0
    elif model["pct_nbr_call_30s"] >= 71.5 and model["pct_nbr_call_30s"] < 82.5:
        score += 56.0
    elif model["pct_nbr_call_30s"] >= 82.5:
        score += 48.0
    else:
        score += 64.0;

    if model["pct_nbr_contact_1w_to_3m"] == 99999999:
        score += 63.0
    elif model["pct_nbr_contact_1w_to_3m"] == -9999976:
        score += 63.0
    elif model["pct_nbr_contact_1w_to_3m"] and model["pct_nbr_contact_1w_to_3m"] < 7.3:
        score += 48.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 7.3 and model["pct_nbr_contact_1w_to_3m"] < 10.2:
        score += 60.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 10.2 and model["pct_nbr_contact_1w_to_3m"] < 22.4:
        score += 70.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 22.4 and model["pct_nbr_contact_1w_to_3m"] < 24.5:
        score += 62.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 24.5 and model["pct_nbr_contact_1w_to_3m"] < 27.9:
        score += 56.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 27.9:
        score += 48.0
    else:
        score += 63.0;

    if model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == -99998:
        score += 67.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == -999976:
        score += 48.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == -999977:
        score += 48.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] and model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] < 17.136:
        score += 62.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] >= 17.136 and model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] < 212.889:
        score += 79.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] >= 212.889:
        score += 83.0
    else:
        score += 67.0

    if model["per_weekdivalltime_allpro_pay_amt_m3"] == -99998:
        score += 69.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -999976:
        score += 48.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -999977:
        score += 48.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -999978:
        score += 48.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] and model["per_weekdivalltime_allpro_pay_amt_m3"] < 0.246:
        score += 61.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] >= 0.246:
        score += 74.0
    else:
        score += 62.0

    if model["sum_alltime_noncdq_likeduepay_days_cnt3"] == -99998:
        score += 59.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"] and model["sum_alltime_noncdq_likeduepay_days_cnt3"] < 34.0:
        score += 66.0
    elif model["sum_alltime_noncdq_likeduepay_days_cnt3"] >= 34.0:
        score += 48.0
    else:
        score += 59.0

    if model["contimes_called_20s_7_90_rate"] == 99999999:
        score += 65.0
    elif model["contimes_called_20s_7_90_rate"] and model["contimes_called_20s_7_90_rate"] < 0.039:
        score += 48.0
    elif model["contimes_called_20s_7_90_rate"] >= 0.039 and model["contimes_called_20s_7_90_rate"] < 0.063:
        score += 59.0
    elif model["contimes_called_20s_7_90_rate"] >= 0.063 and model["contimes_called_20s_7_90_rate"] < 0.118:
        score += 66.0
    elif model["contimes_called_20s_7_90_rate"] >= 0.118:
        score += 60.0
    else:
        score += 57.0

    if model["orderfee_180d"] == 99999999:
        score += 50.0
    elif model["orderfee_180d"] and model["orderfee_180d"] < 289.21:
        score += 47.0
    elif model["orderfee_180d"] >= 289.21 and model["orderfee_180d"] < 3056.31:
        score += 59.0
    elif model["orderfee_180d"] >= 3056.31:
        score += 69.0
    else:
        score += 60.0

    if(score<0):
        score=0
    elif(score>1000):
        score=1000
    return score

if __name__ == "__main__":
    model = {
        'per_alltime_xfjrdivallpro_pay_amt_cnt3': 2,
        'per_weekdivalltime_allpro_pay_amt_m3': 11,
        'pct_nbr_cont_3m': 0.628686327,
        'pct_nbr_cont_morning': 0.365750529,
        'pct_nbr_call_30s':0.3,
        'pct_nbr_contact_1w_to_3m': 0.055045872,
        'sum_alltime_noncdq_likeduepay_days_cnt3': 1,
        'contimes_called_20s_7_90_rate': 37,
        'orderfee_180d': 73,
    }
    print (score_card_recycle(model))
