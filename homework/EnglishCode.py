# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 13:30:49 2019

@author: pkwin
"""

import pandas as pd
import math
import datetime
from random import randint

pd.options.mode.chained_assignment = None

Today = pd.to_datetime(datetime.datetime.today().date())

Thirty_day = datetime.timedelta(days = 30)

TotalTestWord = 50


DF = pd.read_excel('C:/Users/genio/Desktop/English/English.xlsx')
#DF = pd.read_excel('C:/Users/pkwin/Desktop/English/English.xlsx')

DF.loc[DF["LatestTestDate"] != Today,"TodayTestCounts"] = 0

DF["ErrorRate"] = DF['ErrorCounts'] / DF["QuestionCounts"]

NewWordDF = DF.loc[DF["ErrorRate"].isnull()]

NewWordCounts = NewWordDF.shape[0]

if NewWordCounts > 0:
    
    TestResultDF = NewWordDF.sample(frac = 1).reset_index(drop = True)
else:
    
    TestResultDF = NewWordDF.copy()

##Rate

TotalTestWord = TotalTestWord - NewWordCounts


#DF = pd.read_excel('C:/Users/pkwin/Desktop/English/English.xlsx')

DF1 = DF.loc[DF["TodayTestCounts"] <= 10]

HighErrorDF = DF1.loc[DF1["ErrorRate"] >= 0.5]

LowErrorDF = DF1.loc[DF1["ErrorRate"] < 0.5]

if HighErrorDF.shape[0] > 0:
    
    HighErrorDF = HighErrorDF.sample(frac = 1).reset_index(drop = True)

else:
    
    pass

if LowErrorDF.shape[0] >0:
    
    LowErrorDF = LowErrorDF.sample(frac = 1).reset_index(drop = True)

else:
    pass

NewHighErrorDF = HighErrorDF.loc[HighErrorDF['LatestTestDate'] >= Today - Thirty_day ]

OldHighErrorDF = HighErrorDF.loc[HighErrorDF['LatestTestDate'] < Today - Thirty_day ]

NewLowErrorDF = LowErrorDF.loc[LowErrorDF['LatestTestDate'] >= Today - Thirty_day ]

OldLowErrorDF = LowErrorDF.loc[LowErrorDF['LatestTestDate'] < Today - Thirty_day ]




NewHighErrorRate = 0.5
OldHighErrorRate = 0.25
NewLowErrorRate = 0.15
OldLowErrorRate = 0.1

NewHighErrorTestCounts = math.ceil(TotalTestWord * NewHighErrorRate)
OldHighErrorTestCounts = math.ceil(TotalTestWord * OldHighErrorRate)
NewLowErrorTestCounts = math.ceil(TotalTestWord * NewLowErrorRate)
OldLowErrorTestCounts = math.ceil(TotalTestWord * OldLowErrorRate)



if NewHighErrorDF.shape[0] < NewHighErrorTestCounts:
    
    NewHighErrorTestCounts = NewHighErrorDF.shape[0]



if OldHighErrorDF.shape[0] == 0:
    
    NewHighErrorTestCounts += OldHighErrorTestCounts
    
    OldHighErrorTestCounts = 0
    
elif OldHighErrorDF.shape[0] < OldHighErrorTestCounts:
    
    OldHighErrorTestCounts = OldHighErrorDF.shape[0]

 
if NewLowErrorDF.shape[0] < NewLowErrorTestCounts:
    
    NewLowErrorTestCounts = NewLowErrorDF.shape[0]
    
    
if OldLowErrorDF.shape[0] == 0:
    
    NewLowErrorTestCounts += OldLowErrorTestCounts
    
    OldLowErrorTestCounts = 0
    
elif OldLowErrorDF.shape[0] < OldLowErrorTestCounts:
    
    OldLowErrorTestCounts = OldLowErrorDF.shape[0]

#################################################################
    
if NewHighErrorTestCounts > 0:
    
    NewHighErrorDF = NewHighErrorDF.sample(n = NewHighErrorTestCounts)

else:
    NewHighErrorDF.drop(NewHighErrorDF.index, inplace = True)

if OldHighErrorTestCounts > 0:
    
    OldHighErrorDF = OldHighErrorDF.sample(n = OldHighErrorTestCounts)

else:
    OldHighErrorDF.drop(OldHighErrorDF.index, inplace = True)

if NewLowErrorTestCounts > 0:
    
    NewLowErrorDF = NewLowErrorDF.sample(n = NewLowErrorTestCounts)

else:
    NewLowErrorDF.drop(NewLowErrorDF.index, inplace = True)

if OldLowErrorTestCounts > 0:
    
    OldLowErrorDF = OldLowErrorDF.sample(n = OldLowErrorTestCounts)

else:
    OldLowErrorDF.drop(OldLowErrorDF.index, inplace = True)
##Result
TestResultDF = pd.concat([TestResultDF,NewHighErrorDF], axis = 0)

TestResultDF = pd.concat([TestResultDF,OldHighErrorDF], axis = 0)

TestResultDF = pd.concat([TestResultDF,NewLowErrorDF], axis = 0)

TestResultDF = pd.concat([TestResultDF,OldLowErrorDF], axis = 0)

TestResultDF.reset_index(drop = True, inplace = True)

print("Start test")

for i in range(0,TestResultDF.shape[0]):
    
#    i = 1
    IsEnglish = randint(0,1)
    TestWord = TestResultDF.loc[i,"Word"]
    MeanNumber = TestResultDF.loc[i,"MeanNumber"]
    PartOfSpeech = TestResultDF.loc[i,"PartOfSpeech"]
    TestChineseWord = TestResultDF.loc[i,"ChineseWord"]
    
    ALLChineseWord = list(DF.loc[(DF["Word"] == TestWord), "ChineseWord"])
         
    CheckChineseWord = TestChineseWord.split(';')
    
    ALLEnglishWord = []
    
    for check in CheckChineseWord:
        
        ALLEnglishWord = ALLEnglishWord + list(DF.loc[DF["ChineseWord"].str.contains(check),"Word"])
    
    ALLEnglishWord = list(set(ALLEnglishWord))
    
    DF.loc[(DF["Word"] == TestWord) & (DF["MeanNumber"] == MeanNumber),"QuestionCounts"] += 1 
    DF.loc[(DF["Word"] == TestWord) & (DF["MeanNumber"] == MeanNumber),"TodayTestCounts"] += 1
    DF.loc[(DF["Word"] == TestWord) & (DF["MeanNumber"] == MeanNumber),"LatestTestDate"] = Today 
    
    Answer = ""
    
    if IsEnglish == 1:
        
        print(" ")
        print(str(i + 1)+". "+TestWord + " " + str(MeanNumber) + " " + PartOfSpeech)
        print("Please input your answer:")
        
        while Answer != TestChineseWord:
            
            Answer = input()
            
    #        name = "陷入…某種情感之中"
            
            if Answer == TestChineseWord:
                
                break
            
            elif Answer in ALLChineseWord:
                
                print("Please input other mean:")
                
                continue
            
            else:
                print(" ")
                print(DF.loc[(DF["Word"] == TestWord), ["Word","MeanNumber","PartOfSpeech","ChineseWord"]])
                print(" ")
                DF.loc[(DF["Word"] == TestWord) & (DF["MeanNumber"] == MeanNumber),"ErrorCounts"] += 1
                
                break
            
    else:
        
        print(" ")
        print(str(i + 1)+". "+TestChineseWord + " " + str(MeanNumber) + " " + PartOfSpeech)
        print("Please input your answer:")
        
        while Answer != TestWord:
            
            Answer = input()
            
    #        name = "陷入…某種情感之中"
            
            if Answer == TestWord:
                
                break
            
            elif Answer in ALLEnglishWord:
                
                print("Please input other mean:")
                
                continue
            
            else:
                print(" ")
                print(DF.loc[(DF["Word"] == TestWord), ["Word","MeanNumber","PartOfSpeech","ChineseWord"]])
                print(" ")
                DF.loc[(DF["Word"] == TestWord) & (DF["MeanNumber"] == MeanNumber),"ErrorCounts"] += 1
                
                break
        
print("Test Stop")

DF["ErrorRate"] = DF['ErrorCounts'] / DF["QuestionCounts"]

DF.to_excel("C:/Users/genio/Desktop/English/English.xlsx", index = False)
#DF.to_excel("C:/Users/pkwin/Desktop/English/English.xlsx", index = False)

        
        
        
        
        
    
    
    
    
    
    

