# -*- coding: utf-8 -*-
"""
Created on Tuesday May  22 21:00:00 2018

@author: 

SCORECARD FOR TMALL

"""

def score_card_xmall(model):

    score = 0.0
    if model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == 99999999:
        score += 82.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == -99998:
        score += 92.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == -999976:
        score += 67.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"] == -999977:
        score += 52.0
    elif model["per_alltime_xfjrdivallpro_pay_amt_cnt3"]:
        score += 95.0
    else:
        score += 82.0;

    if model["per_weekdivalltime_allpro_pay_amt_m3"] == 99999999:
        score += 63.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -99998:
        score += 72.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -999976:
        score += 52.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -999977:
        score += 52.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] == -999978:
        score += 52.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] and model["per_weekdivalltime_allpro_pay_amt_m3"] < 0.347:
        score += 63.0
    elif model["per_weekdivalltime_allpro_pay_amt_m3"] >= 0.347:
        score += 76.0
    else:
        score += 63.0

    if model["pct_nbr_cont_3m"] == 99999999:
        score += 69.0
    elif model["pct_nbr_cont_3m"] and model["pct_nbr_cont_3m"] < 38.5:
        score += 52.0
    elif model["pct_nbr_cont_3m"] >= 38.5 and model["pct_nbr_cont_3m"] < 45.4:
        score += 63.0
    elif model["pct_nbr_cont_3m"] >= 45.4 and model["pct_nbr_cont_3m"] < 74.8:
        score += 73.0
    elif model["pct_nbr_cont_3m"] >= 74.8 and model["pct_nbr_cont_3m"] < 83.4:
        score += 63.0
    elif model["pct_nbr_cont_3m"] >= 83.4:
        score += 59.0
    else:
        score = score + 69.0

    if model["pct_nbr_cont_morning"] == 99999999:
        score += 59.0
    elif model["pct_nbr_cont_morning"] and model["pct_nbr_cont_morning"] < 37.3:
        score += 52.0
    elif model["pct_nbr_cont_morning"] >= 37.3:
        score += 65.0
    else:
        score += 59.0

    if model["pct_nbr_cont_early_morning"] == 99999999:
        score += 61.0
    elif model["pct_nbr_cont_early_morning"] and model["pct_nbr_cont_early_morning"] < 2.8:
        score += 69.0
    elif model["pct_nbr_cont_early_morning"] >= 2.8 and model["pct_nbr_cont_early_morning"] < 4.9:
        score += 62.0
    elif model["pct_nbr_cont_early_morning"] >= 4.9 and model["pct_nbr_cont_early_morning"] < 11.3:
        score += 58.0
    elif model["pct_nbr_cont_early_morning"] >= 11.3:
        score += 52.0
    else:
        score += 61.0

    if model["pct_nbr_call_30s"] == 99999999:
        score += 74.0
    elif model["pct_nbr_call_30s"] and model["pct_nbr_call_30s"] < 53.4:
        score += 94.0
    elif model["pct_nbr_call_30s"] >= 53.4 and model["pct_nbr_call_30s"] < 61.1:
        score += 86.0
    elif model["pct_nbr_call_30s"] >= 61.1 and model["pct_nbr_call_30s"] < 69.4:
        score += 75.0
    elif model["pct_nbr_call_30s"] >= 69.4 and model["pct_nbr_call_30s"] < 78.6:
        score += 64.0
    elif model["pct_nbr_call_30s"] >= 78.6:
        score += 51.0
    else:
        score = score + 74.0

    if model["pct_nbr_contact_1w_to_3m"] == 99999999:
        score += 70.0
    elif model["pct_nbr_contact_1w_to_3m"] and model["pct_nbr_contact_1w_to_3m"] < 6.9:
        score += 51.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 6.9 and model["pct_nbr_contact_1w_to_3m"] < 26.3:
        score += 74.0
    elif model["pct_nbr_contact_1w_to_3m"] >= 26.3:
        score += 61.0
    else:
        score += 70.0

    if model["orderfee_180d"] == 99999999:
        score += 60.0
    elif model["orderfee_180d"] and model["orderfee_180d"] < 763.32:
        score += 51.0
    elif model["orderfee_180d"] >= 763.32 and model["orderfee_180d"] < 1913.48:
        score += 57.0
    elif model["orderfee_180d"] >= 1913.48 and model["orderfee_180d"] < 5341.349:
        score += 65.0
    elif model["orderfee_180d"] >= 5341.349:
        score += 72.0
    else:
        score += 60.0

    if(score<0):
        score=0
    elif(score>1000):
        score=1000
    return score

if __name__ == "__main__":
    model = {
        'per_alltime_xfjrdivallpro_pay_amt_cnt3': '',
        'per_weekdivalltime_allpro_pay_amt_m3': 11,
        'pct_nbr_cont_3m': 0.628686327,
        'pct_nbr_cont_morning': 0.365750529,
        'pct_nbr_cont_early_morning': 0.055045872,
        'pct_nbr_call_30s': 1,
        'pct_nbr_contact_1w_to_3m': 37,
        'orderfee_180d': 73,
    }
    print (score_card_xmall(model))
