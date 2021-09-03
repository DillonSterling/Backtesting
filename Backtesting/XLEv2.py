# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 18:03:00 2021

@author: SESA553573
"""

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
capital = []
start_index = 1200
smoothing = 2

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

file_name = 'IBM.csv'
df = pd.read_csv(file_name)
df.columns = ["Date","Open","High","Low","Close","Volume","SMA20","SMA50","SMA100"
              ,"SMA200","RSI","MACD","UP","Down"]
df.index = df.index.values[::-1]
df = df.iloc[::-1]
Ndf = df.apply(pd.to_numeric, errors='coerce')

#%%
for item in range(len(Ndf.index)):
    if item == 0:
        periods = 1
        daily_average_volume = Ndf.Volume[item]
        ema5.append(Ndf.Close[item])
        delta_ema5.append(0)
        print(Ndf.Open[item])
        capital.append(Ndf.Open[item])
    else:
        if(df.Date[item-1].split("/")[1] == df.Date[item].split("/")[1]):
            periods = periods + 1
            daily_average_volume = ((daily_average_volume * (periods - 1)) + (Ndf.Volume[item]))/periods
        else:
            periods = 1
            daily_average_volume = Ndf.Volume[item]
        ema5.append(Ndf.Close[item]*(smoothing/6) + ema5[item-1]*(1-(smoothing/6))) 
        #ema5.append(ema5[item-1] + alpha * (Ndf.Close[item] - ema5[item-1]))
        delta_ema5.append(ema5[item]-ema5[item-1])
        
#%%
        if have_position == False:
            capital.append(capital[item-1])
            if(Ndf.Volume[item] > daily_average_volume/1.5):
                if(Ndf.Close[item-1] <= max(Ndf.SMA20[item-1], Ndf.SMA50[item-1], Ndf.SMA100[item-1], Ndf.SMA200[item-1])
                and Ndf.Close[item] > max(Ndf.SMA20[item], Ndf.SMA50[item], Ndf.SMA100[item], Ndf.SMA200[item])):
                    if delta_ema5[item] > 0:
                        
                            #Buy the open of the next tick
                            try:
                                buy(Ndf.Open[item + 1])
                            except:
                                break
                            buy_price = Ndf.Open[item + 1]
                            buy_capital = capital[item]
                            print("Buy")
                            print(df.iloc[item])
                            print("")
        else:
            capital.append(buy_capital * (Ndf.Open[item+1]/buy_price))
            #if (ema5[item-1] > ema5[item]):
            if (Ndf.Close[item] <= max(Ndf.SMA20[item], Ndf.SMA50[item], Ndf.SMA100[item], Ndf.SMA200[item])):

                    try:
                        #Sell the open of the next tick
                        sell(Ndf.Open[item + 1])
                    except:
                        break
                    print("Sell")
                    print(df.iloc[item])
                    print("")
                        
#%%               
plt.title("Closing Price") 
plt.xlabel("Period") 
plt.ylabel("Price")
plt.figure(dpi=1200)
plt.plot(Ndf.Close) 
#plt.plot(ema5)
plt.plot(capital)
plt.show()
plt.savefig("chart.png", dpi=1200)

#%%
for buy in range(len(buys)):
    if sells[buy] != None:
        profit.append(((sells[buy]-buys[buy])/buys[buy]))
        
total_return = 1
for trade in range(len(profit)):
    total_return = total_return * (1 + profit[trade])
    
benmchmark_return = 1 + (Ndf.Open[len(Ndf.Open)-1] - Ndf.Open[0])/Ndf.Open[0]
