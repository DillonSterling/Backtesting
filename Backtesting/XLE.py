# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 10:58:49 2021

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
import datetime
ema5 = []
delta_ema5 = []
have_position = False
buys = []
sells = []
profit = []
alpha = .5

def buy(price):
    global buys
    global have_position
    buys.append(price)
    have_position = True
    
def sell(price):
    global sells
    global have_position
    sells.append(price)
    have_position = False
    
#%%
df = pd.read_csv('XLE.csv')
df.columns = ["Date","Open","High","Low","Close","Volume","SMA20","SMA50","SMA100"
              ,"SMA200","RSI","MACD","UP","Down"]
df.index = df.index.values[::-1]
df = df.iloc[::-1]
Ndf = df.apply(pd.to_numeric, errors='coerce')

for item in range(len(Ndf.index)):
    if item == 0:
        periods = 1
        daily_average_volume = Ndf.Volume[item]
        ema5.append(Ndf.Close[item])
        delta_ema5.append(0)
    else:
        if(df.Date[item-1].split("/")[1] == df.Date[item].split("/")[1]):
            periods = periods + 1
            daily_average_volume = ((daily_average_volume * (periods - 1)) + (Ndf.Volume[item]))/periods
        else:
            periods = 1
            daily_average_volume = Ndf.Volume[item]
        ema5.append(ema5[item-1] + alpha * (Ndf.Close[item] - ema5[item-1])) 
        delta_ema5.append(ema5[item]-ema5[item-1])
        
    if(Ndf.SMA50[item] >= Ndf.SMA100[item]):
        if(Ndf.Volume[item] > daily_average_volume):
            if(Ndf.Close[item-1] <= Ndf.SMA50[item-1] and Ndf.Close[item] > Ndf.SMA50[item]):
                if delta_ema5[item] > 0:
                    if have_position == False:
                        #Buy the open of the next tick
                        buy(Ndf.Open[item + 1])
                        print("Buy")
                        print("Index: " + str(item))
                        print(df.iloc[item])
                        print("Next Open Price: " + str(Ndf.Open[item + 1]))
                        print("Daily Average Volume: " + str(daily_average_volume))
                        print("ema5: " + str(ema5[item]))
                        print("previous delta_ema5: " + str(delta_ema5[item-1]))
                        print("delta_ema5: " + str(delta_ema5[item]))
                        print("")
    if item != 0:
        if delta_ema5[item-1] > 0:
            if delta_ema5[item] < 0:
                if have_position == True:
                    sell(Ndf.Open[item + 1])
                    print("Sell")
                    print("Index: " + str(item))
                    print(df.iloc[item])
                    print("Next Open Price: " + str(Ndf.Open[item + 1]))
                    print("Daily Average Volume: " + str(daily_average_volume))
                    print("ema5: " + str(ema5[item]))
                    print("previous delta_ema5: " + str(delta_ema5[item-1]))
                    print("delta_ema5: " + str(delta_ema5[item]))
                    print("")
#%%               
plt.title("Closing Price") 
plt.xlabel("Period") 
plt.ylabel("Price") 
plt.plot(Ndf.Close) 
plt.plot(ema5)
plt.show()
        
plt.plot(delta_ema5)
plt.show()

#%%
for buy in range(len(buys)):
    if sells[buy] != None:
        profit.append(((sells[buy]-buys[buy])/buys[buy])*100)
