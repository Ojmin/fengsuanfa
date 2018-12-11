# -*- coding: utf-8 -*-
"""
Created on Tuesday May  22 21:00:00 2018

@author: zhanghaiyang

SCORECARD FOR TMALL

"""
def score_card_tc(model):
   score = 629.0
   if model["tcp0066"]=='':
      score+= 0.0
   elif model["tcp0066"] <  1.0:
      score+=   12.0
   elif model["tcp0066"] >= 1.0 and model["tcp0066"] <  2.0 :  
      score+=   2.0
   elif model["tcp0066"] >= 2.0 and model["tcp0066"] <  3.0 :  
      score+=   -9.0
   elif model["tcp0066"] >= 3.0 :  
      score+=   -30.0
   else:
        score += 0.0


   if model["tcp0215"]=='':
      score+= 0
   elif model["tcp0215"] <  1.0 :  
       score+=   -21.0
   elif model["tcp0215"] >= 1.0 and model["tcp0215"] <  2.0 :  
       score+=   -4.0
   elif model["tcp0215"] >= 2.0 and model["tcp0215"] <  3.0 :  
       score+=   19.0
   elif model["tcp0215"] >= 3.0 :  score+=   26.0
   else:
        score += 0.0

   if model["tcp0242"]=='':
       score+= 0
   elif model["tcp0242"] <  2.0 :  
    score+=   -31.0
   elif model["tcp0242"] >= 2.0 and model["tcp0242"] <  12.0 :  
    score+=   -5.0
   elif model["tcp0242"] >= 12.0 and model["tcp0242"] <  205.0 :  
    score+=   4.0
   elif model["tcp0242"] >= 205.0 :  
    score+=   13.0
   else:
        score += 0.0

   if model["tcp0268"]=='':
       score+= 0
   elif model["tcp0268"] <  0.01 :  
    score+=   -13.0
   elif model["tcp0268"] >= 0.01 and model["tcp0268"] <  1.14 :  
    score+=   12.0
   elif model["tcp0268"] >= 1.14 and model["tcp0268"] <  1.41 :  
    score+=   7.0
   elif model["tcp0268"] >= 1.41 and model["tcp0268"] <  1.74 :  
    score+=   1.0
   elif model["tcp0268"] >= 1.74 and model["tcp0268"] <  2.009 :  
    score+=   -5.0
   elif model["tcp0268"] >= 2.009 :  
    score+=   -15.0
   else:
        score += 0.0

   if model["tcp0279"]=='':
       score+= 0
   elif model["tcp0279"] <  1.0 :  
    score+=   8.0
   elif model["tcp0279"] >= 1.0 and model["tcp0279"] <  10.0 :  
    score+=   -3.0
   elif model["tcp0279"] >= 10.0 :  
    score+=   -23.0
   else:
        score += 0.0

   if model["tcp0319"]=='':
       score+= 0
   elif model["tcp0319"] <  2.0 :  
    score+=   -8.0
   elif model["tcp0319"] >= 2.0 and model["tcp0319"] <  4.0 :  
    score+=   -14.0
   elif model["tcp0319"] >= 4.0 and model["tcp0319"] <  8.0 :  
    score+=   -5.0
   elif model["tcp0319"] >= 8.0 and model["tcp0319"] <  10.0 :  
    score+=   8.0
   elif model["tcp0319"] >= 10.0 and model["tcp0319"] <  13.0 :  
    score+=   12.0
   elif model["tcp0319"] >= 13.0 :  
    score+=   26.0
   else:
        score += 0.0
   if model["tcp0336"]=='':
       score+= 0
   elif model["tcp0336"] <  288.0 :  
    score+=   5.0
   elif model["tcp0336"] >= 288.0 and model["tcp0336"] <  603.0 :  
    score+=   -0.0
   elif model["tcp0336"] >= 603.0 :  
    score+=   -21.0
   else:
        score += 0.0

   if model["tcp0347"]=='':
       score+= 0
   elif model["tcp0347"] <  0.32 :  
    score+=   10.0
   elif model["tcp0347"] >= 0.32 and model["tcp0347"] <  0.47 :  
    score+=   3.0
   elif model["tcp0347"] >= 0.47 and model["tcp0347"] <  0.61 :  
    score+=   -1.0
   elif model["tcp0347"] >= 0.61 :
    score+=   -16.0
   else:
        score += 0.0

   if model["contimes_called_90_180_rate_w"]=='':
       score+= 0
   elif model["contimes_called_90_180_rate_w"] <  0.406 :  
    score+=   -15.0
   elif model["contimes_called_90_180_rate_w"] >= 0.406 and model["contimes_called_90_180_rate_w"] <  0.453 :  
    score+=   7.0
   elif model["contimes_called_90_180_rate_w"] >= 0.453 and model["contimes_called_90_180_rate_w"] <  0.59 :  
    score+=   12.0
   elif model["contimes_called_90_180_rate_w"] >= 0.59 and model["contimes_called_90_180_rate_w"] <  0.668 :  
    score+=   -1.0
   elif model["contimes_called_90_180_rate_w"] >= 0.668 and model["contimes_called_90_180_rate_w"] <  0.693 :  
    score+=   -16.0
   elif model["contimes_called_90_180_rate_w"] >= 0.693 and model["contimes_called_90_180_rate_w"] <  0.731 :  
    score+=   -27.0
   elif model["contimes_called_90_180_rate_w"] >= 0.731 :
       score+=   -32.0
   else:
        score += 0.0 

   if model["contimes_called_30s_7_90_rate_w"]=='':
       score+= 0
   elif model["contimes_called_30s_7_90_rate_w"] <  0.033 :  
        score+=   -45.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.033 and model["contimes_called_30s_7_90_rate_w"] <  0.047 :  
    score+=   -18.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.047 and model["contimes_called_30s_7_90_rate_w"] <  0.056 :  
    score+=   -2.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.056 and model["contimes_called_30s_7_90_rate_w"] <  0.069 :  
    score+=   6.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.069 and model["contimes_called_30s_7_90_rate_w"] <  0.113 :  
    score+=   16.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.113 and model["contimes_called_30s_7_90_rate_w"] <  0.144 :  
    score+=   5.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.144 and model["contimes_called_30s_7_90_rate_w"] <  0.166 :  
    score+=   -8.0
   elif model["contimes_called_30s_7_90_rate_w"] >= 0.166 :
       score+=   -33.0
   else:
        score += 0.0

   if model["contimes_called_20s_30days_w"]=='':
       score+= 0
   elif model["contimes_called_20s_30days_w"] <  15.0 :  
    score+=   -46.0
   elif model["contimes_called_20s_30days_w"] >= 15.0 and model["contimes_called_20s_30days_w"] <  22.0 :  
    score+=   -20.0
   elif model["contimes_called_20s_30days_w"] >= 22.0 and model["contimes_called_20s_30days_w"] <  28.0 :  
    score+=   -13.0
   elif model["contimes_called_20s_30days_w"] >= 28.0 and model["contimes_called_20s_30days_w"] <  33.0 :  
    score+=   -9.0
   elif model["contimes_called_20s_30days_w"] >= 33.0 and model["contimes_called_20s_30days_w"] <  53.0 :  
    score+=   3.0
   elif model["contimes_called_20s_30days_w"] >= 53.0 and model["contimes_called_20s_30days_w"] <  149.0 :  
    score+=   14.0
   elif model["contimes_called_20s_30days_w"] >= 149.0 :  
    score+=   -2.0
   else:
        score += 0.0 

   if(score<0):
        score=0
   elif(score>1000):
        score=1000
   return score