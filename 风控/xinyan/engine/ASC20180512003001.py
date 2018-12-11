# -*- coding: utf-8 -*-
"""
Created on Sat May  12 16:00:00 2018

@author: 
"""

import json
import pandas as pd
from pandasql import sqldf
import time
import datetime
import numpy as np
import math
import traceback

def score_card(model):
    PDO=50
    BASE=500
    ODD_RATE=2
    factor = PDO / math.log(ODD_RATE)
    offset = BASE - (PDO / math.log(ODD_RATE)) * math.log(ODD_RATE)

    #  contimes_5s_90days_w
    if model['contimes_5s_90days']:
        if model['contimes_5s_90days'] >= 41:
            contimes_5s_90days_w = -0.6427
        elif model['contimes_5s_90days'] >= 26:
            contimes_5s_90days_w = -0.2142
        elif model['contimes_5s_90days'] >= 16.22:
            contimes_5s_90days_w = -0.111
        elif model['contimes_5s_90days'] >= 2.89:
            contimes_5s_90days_w = 0.1953
        else:
            contimes_5s_90days_w = -0.1768
    else:
        contimes_5s_90days_w = -0.1896
        
    #  contimes_7days_22_to_1_w
    if model["contimes_7days_22_to_1"]:
        if model["contimes_7days_22_to_1"] >= 168.78:
            contimes_7days_22_to_1_w = -0.4584
        elif model["contimes_7days_22_to_1"] >= 92.95:
            contimes_7days_22_to_1_w = -0.206
        elif model["contimes_7days_22_to_1"] >= 50.45:
            contimes_7days_22_to_1_w = -0.0256
        elif model["contimes_7days_22_to_1"] >= 14.15:
            contimes_7days_22_to_1_w = 0.1622
        else:
            contimes_7days_22_to_1_w = 0.3596
    else:
        contimes_7days_22_to_1_w = -0.1896

    #  contimes_30days_1_to_8_w
    if model["contimes_30days_1_to_8"]:
        if model["contimes_30days_1_to_8"] >= 26.2:
            contimes_30days_1_to_8_w = -0.4181
        elif model["contimes_30days_1_to_8"] >= 16.5:
            contimes_30days_1_to_8_w = -0.1969
        elif model["contimes_30days_1_to_8"] >= 10.35:
            contimes_30days_1_to_8_w = -0.0202
        elif model["contimes_30days_1_to_8"] >= 3.55:
            contimes_30days_1_to_8_w = 0.1055
        else:
            contimes_30days_1_to_8_w = 0.0969
    else:
        contimes_30days_1_to_8_w = -0.1896
        
    #  contimes_30days_8_to_12_w
    if model["contimes_30days_8_to_12"]:
        if model["contimes_30days_8_to_12"] >= 138.73:
            contimes_30days_8_to_12_w = 0.2828
        elif model["contimes_30days_8_to_12"] >= 73.55:
            contimes_30days_8_to_12_w = 0.2284
        elif model["contimes_30days_8_to_12"] >= 35.1:
            contimes_30days_8_to_12_w = 0.0548
        elif model["contimes_30days_8_to_12"] >= 12.65:
            contimes_30days_8_to_12_w = -0.1032
        else:
            contimes_30days_8_to_12_w = -0.4819
    else:
        contimes_30days_8_to_12_w = -0.1896

    #  contimes_called_5s_30days_w
    if model["contimes_called_5s_30days"]:
        if model["contimes_called_5s_30days"] >= 12.59:
            contimes_called_5s_30days_w = -0.7286
        elif model["contimes_called_5s_30days"] >= 6.77:
            contimes_called_5s_30days_w = -0.155
        elif model["contimes_called_5s_30days"] >= 1.14:
            contimes_called_5s_30days_w = 0.1129
        else:
            contimes_called_5s_30days_w = 0.0225
    else:
        contimes_called_5s_30days_w = -0.1896
        
    #  contimes_called_20s_30days_w
    if model["contimes_called_20s_30days"]:
        if model["contimes_called_20s_30days"] >= 92.5:
            contimes_called_20s_30days_w = 0.1668
        elif model["contimes_called_20s_30days"] >= 55.35:
            contimes_called_20s_30days_w = 0.265
        elif model["contimes_called_20s_30days"] >= 29.15:
            contimes_called_20s_30days_w = 0.1564
        elif model["contimes_called_20s_30days"] >= 10.85:
            contimes_called_20s_30days_w = -0.1142
        else:
            contimes_called_20s_30days_w = -0.5483
    else:
        contimes_called_20s_30days_w = -0.1896
        
    #  contimes_called_30_90_rate_w
    if model["contimes_called_30_90_rate"]:
        if model["contimes_called_30_90_rate"] >= 0.51843:
            contimes_called_30_90_rate_w = -0.4539
        elif model["contimes_called_30_90_rate"] >= 0.39474:
            contimes_called_30_90_rate_w = 0.1361
        elif model["contimes_called_30_90_rate"] >= 0.28955:
            contimes_called_30_90_rate_w = 0.2952
        elif model["contimes_called_30_90_rate"] >= 0.21502:
            contimes_called_30_90_rate_w = 0.0132
        else:
            contimes_called_30_90_rate_w = -0.5094
    else:
        contimes_called_30_90_rate_w = -0.1503

    #  contimes_called_30s_7_90_rate_w
    if model["contimes_called_30s_7_90_rate"]:
        if model["contimes_called_30s_7_90_rate"] >= 0.16074582:
            contimes_called_30s_7_90_rate_w = -0.4216
        elif model["contimes_called_30s_7_90_rate"] >= 0.09623215:
            contimes_called_30s_7_90_rate_w = 0.324
        elif model["contimes_called_30s_7_90_rate"] >= 0.05745795:
            contimes_called_30s_7_90_rate_w = 0.3488
        elif model["contimes_called_30s_7_90_rate"] >= 0.03340699:
            contimes_called_30s_7_90_rate_w = -0.0114
        else:
            contimes_called_30s_7_90_rate_w = -0.3554
    else:
        contimes_called_30s_7_90_rate_w = -0.2235

    #  contimes_called_90_180_rate_w
    if model["contimes_called_90_180_rate"]:
        if model["contimes_called_90_180_rate"] >= 0.703281:
            contimes_called_90_180_rate_w = -0.4092
        elif model["contimes_called_90_180_rate"] >= 0.600291:
            contimes_called_90_180_rate_w = 0.0402
        elif model["contimes_called_90_180_rate"] >= 0.493102:
            contimes_called_90_180_rate_w = 0.3326
        elif model["contimes_called_90_180_rate"] >= 0.340678:
            contimes_called_90_180_rate_w = -0.0918
        else:
            contimes_called_90_180_rate_w = -0.6835
    else:
        contimes_called_90_180_rate_w = -0.1136

    #  huabei_totalcreditamount_w
    if model["huabei_totalcreditamount"]:
        if float(model["huabei_totalcreditamount"]) >= 3783.38:
            huabei_totalcreditamount_w = 0.6122
        elif float(model["huabei_totalcreditamount"]) >= 1742.5:
            huabei_totalcreditamount_w = 0.4718
        elif float(model["huabei_totalcreditamount"]) >= 831.25:
            huabei_totalcreditamount_w = 0.1495
        elif float(model["huabei_totalcreditamount"]) >= 286.5:
            huabei_totalcreditamount_w = -0.3253
        else:
            huabei_totalcreditamount_w = -0.7713
    else:
        huabei_totalcreditamount_w = -0.57

    #  silent_ge_1_w
    if model["silent_ge_1"]:
        if model["silent_ge_1"] >= 17.95:
            silent_ge_1_w = -0.202
        elif model["silent_ge_1"] >= 7.8:
            silent_ge_1_w = -0.1828
        elif model["silent_ge_1"] >= 2.55:
            silent_ge_1_w = 0.047
        else:
            silent_ge_1_w = 0.2717
    else:
        silent_ge_1_w = -0.3281
    score1 = 1.30993 + 0.65874 * huabei_totalcreditamount_w + 1.0728 * silent_ge_1_w \
    + 0.78285 * contimes_called_90_180_rate_w + 0.55543 * contimes_called_30_90_rate_w \
    + 0.69733 * contimes_called_30s_7_90_rate_w + 0.62627 * contimes_30days_1_to_8_w \
    + 0.79572 * contimes_called_5s_30days_w + 1.25951 * contimes_7days_22_to_1_w \
    + 0.70059 * contimes_30days_8_to_12_w + 1.06909 * contimes_called_20s_30days_w \
    + 0.8083 * contimes_5s_90days_w
    score = round(offset + factor * score1)
    # print(
    #     "huabei_totalcreditamount_w:" + str(huabei_totalcreditamount_w) + '\n'
    #                                                                       "silent_ge_1_w:" + str(silent_ge_1_w) + '\n'
    #                                                                                                               "contimes_called_90_180_rate_w:" + str(
    #         contimes_called_90_180_rate_w) + '\n'
    #                                          "contimes_called_30_90_rate_w:" + str(contimes_called_30_90_rate_w) + '\n'
    #                                                                                                                "contimes_called_30s_7_90_rate_w:" + str(
    #         contimes_called_30s_7_90_rate_w) + '\n'
    #                                            "contimes_30days_1_to_8_w:" + str(contimes_30days_1_to_8_w) + '\n'
    #                                                                                                          "contimes_called_5s_30days_w:" + str(
    #         contimes_called_5s_30days_w) + '\n'
    #                                        "contimes_7days_22_to_1_w:" + str(contimes_7days_22_to_1_w) + '\n'
    #                                                                                                      "contimes_30days_8_to_12_w:" + str(
    #         contimes_30days_8_to_12_w) + '\n'
    #                                      "contimes_called_20s_30days_w:" + str(contimes_called_20s_30days_w) + '\n'
    #                                                                                                            "contimes_5s_90days_w:" + str(
    #         contimes_5s_90days_w) + '\n'
    #         'score:'+str(score)+'\n'
    #         'score1:'+str(score1)+'\n'
    # )
    if(score<0):
        score=0
    elif(score>1000):
        score=1000
    return score

if __name__ == "__main__":
    # pass
#    import config
#    data = config.data
    model = {
        'huabei_totalcreditamount': '',
        'silent_ge_1': 11,
        'contimes_called_90_180_rate': 0.628686327,
        'contimes_called_30_90_rate': 0.365750529,
        'contimes_called_30s_7_90_rate': 0.055045872,
        'contimes_30days_1_to_8': 1,
        'contimes_called_5s_30days': 37,
        'contimes_7days_22_to_1': 73,
        'contimes_30days_8_to_12': 35,
        'contimes_called_20s_30days': 81,
        'contimes_5s_90days': 45
    }
    print (score_card(model))
    # if model['huabei_totalcreditamount']:
    #     print ('no')
    # else:
    #     print ('aa')

