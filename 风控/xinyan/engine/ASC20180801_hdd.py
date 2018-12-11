# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:00:22 2018

@author: 联想

长表现期评分卡
"""


import json
import pandas as pd
from pandasql import sqldf
import time
import datetime
import numpy as np
import math
import traceback

def score_card_0801(model):
    PDO=50
    BASE=600
    ODD_RATE=2
    factor = PDO / math.log(ODD_RATE)
    offset = BASE - (PDO / math.log(ODD_RATE)) * math.log(ODD_RATE)

    #contimes_called_30_90_rate
    if model["contimes_called_30_90_rate"]:
        if model["contimes_called_30_90_rate"] >= 0.50347:
            contimes_called_30_90_rate_w = -0.6142
        elif model["contimes_called_30_90_rate"] >= 0.41502:
            contimes_called_30_90_rate_w = 0.0377
        elif model["contimes_called_30_90_rate"] >= 0.3006:
            contimes_called_30_90_rate_w = 0.2604
        elif model["contimes_called_30_90_rate"] >= 0.23595:
            contimes_called_30_90_rate_w = -0.1221
        else:
            contimes_called_30_90_rate_w = -0.6771
    else:
        contimes_called_30_90_rate_w = -0.0356
    
    #contimes_called_60s_7_30_rate
    if model["contimes_called_60s_7_30_rate"]:
        if model["contimes_called_60s_7_30_rate"] >= 0.3628246:
            contimes_called_60s_7_30_rate_w = -0.3709 
        elif model["contimes_called_60s_7_30_rate"] >= 0.2682268:
            contimes_called_60s_7_30_rate_w = 0.0589
        elif model["contimes_called_60s_7_30_rate"] >= 0.1821357:
            contimes_called_60s_7_30_rate_w = 0.233 
        elif model["contimes_called_60s_7_30_rate"] >= 0.1262512:
            contimes_called_60s_7_30_rate_w = -0.0611
        else:
            contimes_called_60s_7_30_rate_w = -0.7522
    else:
        contimes_called_60s_7_30_rate_w = -0.2174
    
    #contimes_called_90_180_rate
    if model["contimes_called_90_180_rate"]:
        if model["contimes_called_90_180_rate"] >= 0.716534:
            contimes_called_90_180_rate_w = -0.7342
        elif model["contimes_called_90_180_rate"] >= 0.632095:
            contimes_called_90_180_rate_w = -0.1941
        elif model["contimes_called_90_180_rate"] >= 0.535089:
            contimes_called_90_180_rate_w = 0.2466
        elif model["contimes_called_90_180_rate"] >= 0.40453:
            contimes_called_90_180_rate_w = 0.21
        else:
            contimes_called_90_180_rate_w = -0.5147
    else:
        contimes_called_90_180_rate_w = -0.0284

    #contimes_7days_8_to_12
    if model["contimes_7days_8_to_12"]:
        if model["contimes_7days_8_to_12"] >= 39.04:
            contimes_7days_8_to_12_w = 0.1607
        elif model["contimes_7days_8_to_12"] >= 22.46:
            contimes_7days_8_to_12_w = 0.1177
        elif model["contimes_7days_8_to_12"] >= 11.38:
            contimes_7days_8_to_12_w = 0.133
        elif model["contimes_7days_8_to_12"] >= 2.78:
            contimes_7days_8_to_12_w = -0.0766
        else:
            contimes_7days_8_to_12_w = -0.6538
    else:
        contimes_7days_8_to_12_w = -0.0581

    #contimes_30_180_rate
    if model["contimes_30_180_rate"]:
        if model["contimes_30_180_rate"] >= 0.304506:
            contimes_30_180_rate_w = -0.6671
        elif model["contimes_30_180_rate"] >= 0.233561:
            contimes_30_180_rate_w = -0.0324
        elif model["contimes_30_180_rate"] >= 0.157732:
            contimes_30_180_rate_w = 0.2464
        elif model["contimes_30_180_rate"] >= 0.110248:
            contimes_30_180_rate_w = -0.0216                  
        else:
            contimes_30_180_rate_w = -0.5579
    else:
        contimes_30_180_rate_w = -0.0581          

    #contimes_30days_22_to_1
    if model["contimes_30days_22_to_1"]:
        if model["contimes_30days_22_to_1"] >= 163.97:
            contimes_30days_22_to_1_w = -0.5616
        elif model["contimes_30days_22_to_1"] >= 93.16:
            contimes_30days_22_to_1_w = -0.2792
        elif model["contimes_30days_22_to_1"] >= 50.46:
            contimes_30days_22_to_1_w = -0.032
        elif model["contimes_30days_22_to_1"] >= 16.54:
            contimes_30days_22_to_1_w = 0.1263
        else:
            contimes_30days_22_to_1_w = 0.3149
    else:
        contimes_30days_22_to_1_w = -0.0581

    #contimes_called_20s_30days
    if model["contimes_called_10s_7days"]:
        if model["contimes_called_10s_7days"] >= 75.42:
            contimes_called_10s_7days_w = 0.0279
        elif model["contimes_called_10s_7days"] >= 39:
            contimes_called_10s_7days_w = 0.2966
        elif model["contimes_called_10s_7days"] >= 16.46:
            contimes_called_10s_7days_w = 0.2054
        elif model["contimes_called_10s_7days"] >= 3.08:
            contimes_called_10s_7days_w = 0.0001
        else:
            contimes_called_10s_7days_w = -0.4777
    else:
        contimes_called_10s_7days_w = -0.0581

    #cell_rate
    if model["cell_rate"] >= 0.9868:
        cell_rate_w = -0.2881
    elif model["cell_rate"] >= 0.961:
        cell_rate_w = -0.043
    elif model["cell_rate"] >= 0.9213:
        cell_rate_w = 0.1185
    elif model["cell_rate"] >= 0.8545:
        cell_rate_w = 0.223
    else:
        cell_rate_w = 0.1219

    #conode_30days       
    if model['conode_30days']:
        if model['conode_30days'] >= 225.72:
            conode_30days_w = -0.3063
        elif model['conode_30days'] >= 135.38:
            conode_30days_w = 0.1964
        elif model['conode_30days'] >= 75.86:
            conode_30days_w = 0.1731
        elif model['conode_30days'] >= 39.5:
            conode_30days_w = -0.0752
        else:
            conode_30days_w = -0.5761
    else:
        conode_30days_w = -0.0581


    score1 = 0.43385 + 0.97494*contimes_30days_22_to_1_w \
                 + 0.6553*contimes_called_90_180_rate_w\
                 + 0.54949*contimes_called_30_90_rate_w \
                 + 0.53802*cell_rate_w \
                 + 0.49055*conode_30days_w \
                 + 0.51561*contimes_7days_8_to_12_w \
                 + 0.30757*contimes_30_180_rate_w \
                 + 0.53671*contimes_called_60s_7_30_rate_w \
                 + 0.69663*contimes_called_10s_7days_w

    score = round(offset + factor * score1)

    if(score<0):
        score=0
    elif(score>1000):
        score=1000
    return score


if __name__ == "__main__":
    model={"contimes_30days_22_to_1":154,
           "contimes_called_90_180_rate":0.600964113551151,
           "contimes_called_30_90_rate":0.443850267379679,
           "cell_rate":0, 
           "conode_30days":389,
           "contimes_7days_8_to_12":100,
           "contimes_30_180_rate":0.225232511120097,
           "contimes_called_60s_7_30_rate":0.345381526104417,
           "contimes_called_10s_7days":344}
    
    print (score_card(model))












