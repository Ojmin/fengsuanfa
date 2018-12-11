# -*- coding: utf-8 -*-
"""
Created on Sat May  12 16:00:00 2018
# 更新日期 2018-07-09 共9个变量 
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

def score_card_2(model):
    PDO=50
    BASE=500
    ODD_RATE=2
    factor = PDO / math.log(ODD_RATE)
    offset = BASE - (PDO / math.log(ODD_RATE)) * math.log(ODD_RATE)

        
    #  contimes_7days_22_to_1_w
    if model["contimes_7days_22_to_1"]:
        if model["contimes_7days_22_to_1"] >= 14.04:
            contimes_7days_22_to_1_w = -0.63
        elif model["contimes_7days_22_to_1"] >= 7.99:
            contimes_7days_22_to_1_w = -0.2298
        elif model["contimes_7days_22_to_1"] >= 4.25:
            contimes_7days_22_to_1_w = -0.0273
        elif model["contimes_7days_22_to_1"] >= 1.39:
            contimes_7days_22_to_1_w = 0.0775
        else:
            contimes_7days_22_to_1_w = 0.0811
    else:
        contimes_7days_22_to_1_w = -0.0094

    #  contimes_30days_1_to_8_w
    if model["contimes_30days_1_to_8"]:
        if model["contimes_30days_1_to_8"] >= 42.71:
            contimes_30days_1_to_8_w = -0.5422
        elif model["contimes_30days_1_to_8"] >= 22.98:
            contimes_30days_1_to_8_w = -0.2279
        elif model["contimes_30days_1_to_8"] >= 12.08:
            contimes_30days_1_to_8_w = -0.0761
        elif model["contimes_30days_1_to_8"] >= 4.45:
            contimes_30days_1_to_8_w = 0.0597
        else:
            contimes_30days_1_to_8_w = 0.1546
    else:
        contimes_30days_1_to_8_w = -0.0094
        
    #  contimes_30days_8_to_12_w
    if model["contimes_30days_8_to_12"]:
        if model["contimes_30days_8_to_12"] >= 176.45:
            contimes_30days_8_to_12_w = 0.2136
        elif model["contimes_30days_8_to_12"] >= 93.97:
            contimes_30days_8_to_12_w = 0.1996
        elif model["contimes_30days_8_to_12"] >= 43.32:
            contimes_30days_8_to_12_w = 0.1107
        elif model["contimes_30days_8_to_12"] >= 16.25:
            contimes_30days_8_to_12_w = -0.1336
        else:
            contimes_30days_8_to_12_w = -0.6179
    else:
        contimes_30days_8_to_12_w = -0.0094

        
    #  contimes_called_20s_30days_w
    if model["contimes_called_20s_30days"]:
        if model["contimes_called_20s_30days"] >= 288.78:
            contimes_called_20s_30days_w = 0.1826
        elif model["contimes_called_20s_30days"] >= 145.58:
            contimes_called_20s_30days_w = 0.272
        elif model["contimes_called_20s_30days"] >= 60.93:
            contimes_called_20s_30days_w = 0.1495
        elif model["contimes_called_20s_30days"] >= 25.85:
            contimes_called_20s_30days_w = -0.2507
        else:
            contimes_called_20s_30days_w = -0.7592
    else:
        contimes_called_20s_30days_w = -0.0094
        
    #  contimes_called_30_90_rate_w
    if model["contimes_called_30_90_rate"]:
        if model["contimes_called_30_90_rate"] >= 0.5184:
            contimes_called_30_90_rate_w = -0.6494
        elif model["contimes_called_30_90_rate"] >= 0.416114:
            contimes_called_30_90_rate_w = 0.0659
        elif model["contimes_called_30_90_rate"] >= 0.301566:
            contimes_called_30_90_rate_w = 0.3314
        elif model["contimes_called_30_90_rate"] >= 0.216512:
            contimes_called_30_90_rate_w = -0.0779
        else:
            contimes_called_30_90_rate_w = -0.6163
    else:
        contimes_called_30_90_rate_w = 0.1662

    #  contimes_called_30s_7_90_rate_w
    if model["contimes_called_30s_7_90_rate"]:
        if model["contimes_called_30s_7_90_rate"] >= 0.1570243:
            contimes_called_30s_7_90_rate_w =  -0.4699
        elif model["contimes_called_30s_7_90_rate"] >= 0.0969768:
            contimes_called_30s_7_90_rate_w = 0.27
        elif model["contimes_called_30s_7_90_rate"] >= 0.0600797:
            contimes_called_30s_7_90_rate_w = 0.3301
        elif model["contimes_called_30s_7_90_rate"] >= 0.0287221:
            contimes_called_30s_7_90_rate_w = -0.0697
        else:
            contimes_called_30s_7_90_rate_w = -0.3588
    else:
        contimes_called_30s_7_90_rate_w = 0.1635

    #  contimes_called_90_180_rate_w
    if model["contimes_called_90_180_rate"]:
        if model["contimes_called_90_180_rate"] >= 0.722313:
            contimes_called_90_180_rate_w = -0.8636
        elif model["contimes_called_90_180_rate"] >= 0.621539:
            contimes_called_90_180_rate_w = -0.1491
        elif model["contimes_called_90_180_rate"] >= 0.462099:
            contimes_called_90_180_rate_w = 0.2951
        elif model["contimes_called_90_180_rate"] >= 0.340168:
            contimes_called_90_180_rate_w = -0.0193
        else:
            contimes_called_90_180_rate_w = -0.7975
    else:
        contimes_called_90_180_rate_w = 0.1841

    #  huabei_totalcreditamount_w
    if model["huabei_totalcreditamount"]:
        if float(model["huabei_totalcreditamount"]) >= 789:
            huabei_totalcreditamount_w = 0.3852 
        else:
            huabei_totalcreditamount_w = -0.6646
    else:
        huabei_totalcreditamount_w = -1.6961

    #  silent_ge_1_w
    if model["silent_ge_1"]:
        if model["silent_ge_1"] >= 26.04:
            silent_ge_1_w = -0.1973
        elif model["silent_ge_1"] >= 13.92:
            silent_ge_1_w = -0.2394
        elif model["silent_ge_1"] >= 6.12:
            silent_ge_1_w = -0.1251
        elif model["silent_ge_1"] >= 2.08:
            silent_ge_1_w = 0.0987                      
        else:
            silent_ge_1_w = 0.3765
    else:
        silent_ge_1_w =  -0.0094
    
    score1 = 1.12413 + 0.86976 * huabei_totalcreditamount_w + 0.94854 * silent_ge_1_w \
    + 0.60312 * contimes_called_90_180_rate_w + 0.54085 * contimes_called_30_90_rate_w \
    + 0.68007 * contimes_called_30s_7_90_rate_w + 1.50472 * contimes_30days_1_to_8_w \
    + 1.14005 * contimes_7days_22_to_1_w \
    + 0.24297 * contimes_30days_8_to_12_w + 0.46688 * contimes_called_20s_30days_w
    
    
    score = round(offset + factor * score1)
    score += 10 # 为了与上一版模型保持分数一致 
    

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

