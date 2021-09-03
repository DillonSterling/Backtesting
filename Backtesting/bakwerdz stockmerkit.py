# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 15:18:39 2020

@author: Dillon
"""
#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import scipy as sp
from scipy import stats
import statistics
import csv
import zipline as zp
import pyfolio


#%%
column_names = ["Date","Price","Open","High","Low","Vol.","Change %"]
df = pd.read_csv('SPY Historical Data.csv', names=column_names)
df.index = df.index.values[::-1]
df = df.iloc[::-1]
Ndf = df.apply(pd.to_numeric, errors='coerce')

Open = Ndf.Open
Date = df.Date
Price = Ndf.Price



#%%
OCchange = []
Pchange = []
OpenLen = len(Open)
for x in range(1,OpenLen):
    change = Price[x]-Open[x]
    pchange = ((Price[x]/Open[x])-1)*100
    OCchange.append(change)
    Pchange.append(pchange)
    
#%%
def NextDay(Data,low,high):
    Changelow_high = []
    Output = []
    DataLen = len(Data)
    for x in range(0,DataLen-2):
        if (Data[x] > low):
            if (Data[x] < high):
                changelow_high = Data [x+1]
                Changelow_high.append(changelow_high)
    #plt.hist(Changelow_high,bins=500)
    #plt.show()
    if (len(Changelow_high)== 0):
        return "NaN"
    Mean = statistics.mean(Changelow_high)
    if (len(Changelow_high)> 1):
        StDev = statistics.stdev(Changelow_high,Mean)
    else:
        StDev = "NaN"
    StratReturn = (1+(Mean/100))**len(Changelow_high)
    
    
    Output.append(low)
    Output.append(high)
    Output.append(Mean)
    Output.append(StDev)
    Output.append(len(Changelow_high))
    Output.append(StratReturn)
    
    #print(Output)
    return Output
    
# #%%
# Open_Roll_20 = Open.rolling(20).mean()
# Open_Roll_50 = Open.rolling(50).mean()
# Open_Roll_100 = Open.rolling(100).mean()
# Open_Roll_200 = Open.rolling(200).mean()
# #%%
#  #plt.plot(range(len(Open)), Open)
#  plt.plot(range(len(Open_Roll_50)), Open_Roll_50)
#  plt.plot(range(len(Open_Roll_100)), Open_Roll_100)
#  plt.plot(range(len(Open_Roll_200)), Open_Roll_200)
#  plt.plot(range(len(Pchange)), Pchange)
#  plt.axis([5000, 0, -10, 400])
#  plt.hist(Pchange,bins=1000)
#  pyfolio.axes_style
#  plt.show()

 #%%
 #plt.plot(range(len(Change1_2)), Change1_2)
#     plt.hist(Change1_2,bins=500)
#     pyfolio.axes_style
#     plt.show()
#%%
def PlotNDMatrix(Data,low,high):
    NDMatrix = []
    for l in range(low,high):
        if (NextDay(Data,l,l+1) != "NaN"):   
            NDMatrix.append(NextDay(Data,l,l+1))
    NDColNames = ["Low", "High", "Avg next day return", "Standard deviation", "Occurances", "Strategy return"]
    
    with open('Next day matrix '+str(min)+' to '+str(max)+'.csv', 'w') as f: 
          
        # using csv.writer method from CSV package 
        write = csv.writer(f) 
          
        write.writerow(NDColNames) 
        write.writerows(NDMatrix) 
    
#%%
def NextDayR(Data,low,high):
    Changelow_highR = []
    DataLen = len(Data)
    for x in range(0,DataLen-2):
        if (Data[x] > low):
            if (Data[x] < high):
                changelow_high = Data [x+1]
                Changelow_highR.append(changelow_high)

    #print(Changelow_highR)
    return Changelow_highR

#%%
def NextDay2(Data,low,high,low2,high2):
    Changelow_high = []
    Changelow_high2 = []
    Output = []
    DataLen = len(Data)
    for x in range(0,DataLen-2):
        if (Data[x] > low):
            if (Data[x] < high):
                changelow_high = Data[x+1]
                Changelow_high.append(changelow_high)
    for y in range(0,len(Changelow_high)-2):
        if (Changelow_high[y] > low2):
            if (Changelow_high[y] < high2):
                changelow_high2 = Changelow_high[y+2]
                Changelow_high2.append(changelow_high2)

    if (len(Changelow_high2)== 0):
        return "NaN"
    Mean = statistics.mean(Changelow_high2)
    if (len(Changelow_high2)> 1):
        StDev = statistics.stdev(Changelow_high2,Mean)
    else:
        StDev = "NaN"
    StratReturn = (1+(Mean/100))**len(Changelow_high2)
    
    
    Output.append(low)
    Output.append(high)
    Output.append(low2)
    Output.append(high2)
    Output.append(Mean)
    Output.append(StDev)
    Output.append(len(Changelow_high2))
    Output.append(StratReturn)
    
    #print(Output)
    return Output
#%%
def PlotNDMatrix2(Data,min1,max1,min2,max2):
    NDMatrix = []
    for l in range(min1-1,max1+1):
        for h in range(min2-1,max2+1): 
            if (NextDay2(Data,l,l+1,h,h+1) != "NaN"):   
                NDMatrix.append(NextDay2(Data,l,l+1,h,h+1))
    NDColNames = ["Low1", "High1","Low2", "High2", "Avg next day return", "Standard deviation", "Occurances", "Strategy return"]
    
    with open('Next day matrix.csv', 'w') as f: 
        print(NDMatrix)
        # using csv.writer method from CSV package 
        write = csv.writer(f) 
          
        write.writerow(NDColNames) 
        write.writerows(NDMatrix)
        
#%%
zp
