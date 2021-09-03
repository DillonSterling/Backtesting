# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 18:21:20 2021

@author: SESA553573
"""
#%% Declare variables
import pandas as pd
from matplotlib import pyplot as plt
import getminutedata as gd
import pandas_ta as ta
from datetime import datetime

symbol = "cost"
trades = []
profit = []
capital = []
smoothing = 2

#%% Declare classes
class trade():
    def __init__(self, order_type=None):
        self.order_type = order_type
        
    def open_position(self, open_price):
        self.open_price = open_price
        self.status = "open"
        self.open_date = df.index[item]
        
    def close_position(self, close_price):
        self.close_price = close_price
        self.status = "closed"
        self.close_date = df.index[item]
            
        print("Order type: {}".format(self.order_type))
        print("Open Time: {} Price: {}".format(self.open_date, self.open_price))
        print("Close Time: {} Price: {}".format(self.close_date, self.close_price))
        print("Profit: {}".format(self.calculate_profit()))
        print("")

    def calculate_profit(self):
        if self.status == "closed":
            if self.order_type == 'long':
                self.profit = 1 + (self.close_price-self.open_price)/self.open_price
                return self.profit
            elif self.order_type == 'short':
                self.profit = 1 + (self.open_price-self.close_price)/self.open_price
                return self.profit
        else:
            self.profit = 1
            print("Order is not closed")
            return self.profit
    
#%% Get data
df = gd.get_minute_data(symbol)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.iloc[::-1]
data_loaded = True
df.ta.ema(length=5, append=True)
df.ta.sma(length=10, append=True)
df.ta.sma(length=20, append=True)
df.ta.sma(length=50, append=True)
df.ta.sma(length=100, append=True)
df.ta.sma(length=200, append=True)
df.ta.rsi(append=True)
df.ta.rsi(length=100, append=True)
df.ta.macd(fast=8,slow=21,append=True)
df.ta.bbands(length=20,append=True,col_names=('BBL_20','BBM_20','BBU_20','BBB_20','BBP_20'))
df.ta.bbands(length=100,append=True,col_names=('BBL_100','BBM_100','BBU_100','BBB_100','BBP_100'))

#%% Main loop
for item in range(len(df.index)):
    if item == 0:
        periods = 1
        daily_average_volume = df.volume[item]
        capital.append(df.open[item])
    else:
        if(datetime.fromisoformat(df.index[item-1]).hour == datetime.fromisoformat(df.index[item]).hour):
            periods = periods + 1
            daily_average_volume = ((daily_average_volume * (periods - 1)) + (df.volume[item]))/periods
        else:
            periods = 1
            daily_average_volume = df.volume[item]
            
#%% Trading strategy
        #Open position
        if ((datetime.fromisoformat(df.index[item]).minute <= 58) and (datetime.fromisoformat(df.index[item]).hour <= 15)):
            if ((trades == []) or (trades[-1].status == 'closed')):
                capital.append(capital[item-1])
                
                #Buy filter
                if((df.RSI_14[item] < 29) and (df.RSI_14[item] > df.RSI_14[item-1])
                or (df.low[item] < df.BBL_100[item])):
                    if(df.volume[item] > daily_average_volume/1.5):
                        if df.EMA_5[item] > df.EMA_5[item-1]:
                            if df.SMA_100[item] > df.SMA_100[item-1]:
                            #if df.SMA_20[item] > df.SMA_50[item]:
                                #Buy the open of the next tick
                                try:
                                    new_trade = trade("long")
                                    new_trade.open_position(df.open[item + 1])
                                    trades.append(new_trade)
                                except:
                                    break
                                entry_price = df.open[item + 1]
                                entry_capital = capital[item]
                            
                #Short filter
                elif((df.RSI_14[item] > 71) and (df.RSI_14[item] < df.RSI_14[item-1])
                or (df.high[item] > df.BBU_100[item])):
                    if(df.volume[item] > daily_average_volume/1.5):
                        #if df.EMA_5[item] < df.EMA_5[item-1]:
                        if df.SMA_100[item] < df.SMA_100[item-1]:
                            if df.SMA_20[item] < df.SMA_50[item]:
                                #Short the open of the next tick
                                try:
                                    new_trade = trade("short")
                                    new_trade.open_position(df.open[item + 1])
                                    trades.append(new_trade)
                                except:
                                    break
                                entry_price = df.open[item + 1]
                                entry_capital = capital[item]
                        
            #sell filter
            elif(trades[-1].status == "open") and (trades != []) and (item < df.shape[0]-1):
                try:
                    if trades[-1].order_type == "long":
                        #Sell filter
                        capital.append(entry_capital * (df.open[item+1]/entry_price))
                        if (((df.RSI_14[item] > 71) and (df.RSI_14[item] < df.RSI_14[item-1]))
                        or (df.close[item] < entry_price * 0.99)
                        or (df.close[item] > df.BBU_100[item])):
                            try:
                                #Sell the open of the next tick
                                trades[-1].close_position(df.open[item + 1])
                            except:
                                break
                            
                    elif trades[-1].order_type == "short":
                        #Cover filter
                        capital.append(entry_capital * (entry_price/df.open[item+1]))
                        if (((df.RSI_14[item] < 29) and (df.RSI_14[item] > df.RSI_14[item-1]))
                        or (df.close[item] > entry_price * 1.01)
                        or (df.close[item] < df.BBL_100[item])):
                            try:
                                #Sell the open of the next tick
                                trades[-1].close_position(df.open[item + 1])
                            except:
                                break
                except:
                    break
            else:
                capital.append(capital[item-1])
        else:
            if ((trades == []) or (trades[-1].status == 'closed')):
                capital.append(capital[item-1])
            elif(trades[-1].status == "open") and (trades != []) and (item < df.shape[0]-1):
                if trades[-1].order_type == "long":
                    capital.append(entry_capital * (df.open[item+1]/entry_price))
                    trades[-1].close_position(df.open[item + 1])
                elif trades[-1].order_type == "short":
                    capital.append(entry_capital * (entry_price/df.open[item+1]))
                    trades[-1].close_position(df.open[item + 1])

#%% Plot definition
def plot_trades(df):       
    plt.title("Closing Price") 
    plt.xlabel("Period") 
    plt.ylabel("Price")
    plt.figure(dpi=2400)
    plt.plot(df.close) 
    plt.plot(df.capital)
    #plt.plot(df.SMA_200)
    plt.plot(df.BBL_100)
    plt.plot(df.BBM_100)
    plt.plot(df.BBU_100)
    plt.show()
    #plt.savefig("chart.png", dpi=1200)
    # plt.plot(df.RSI_14)
    # plt.plot(df.RSI_100)
    # plt.show()

#%% Create metrics

dfc = pd.DataFrame(capital, columns=["capital"],dtype=float,index=df.index)
df = pd.concat([df,dfc],axis=1)

total_return = 1
for transaction in range(len(trades)):
    total_return = total_return * (trades[transaction].calculate_profit())
    
benchmark_return = 1 + (df.open[len(df.open)-1] - df.open[0])/df.open[0]

alpha = (total_return - benchmark_return)*100

strategy_drawdown = ta.drawdown(df.capital)
strategy_max_drawdown = max(strategy_drawdown["DD_PCT"])*100

security_drawdown = ta.drawdown(df.close)
security_max_drawdown = max(security_drawdown["DD_PCT"])*100

#%% Print metrics
print("Total Return: {:.3f}".format(total_return))
print("Benchmark Return: {:.3f}".format(benchmark_return))
print("Alpha: {:.3f}%".format(alpha))
print("Start Capital: {:.3f}".format(df.capital[0]))
print("End Capital: {:.3f}".format(df.capital[-1]))
print("Return on Capital: {:.3f}".format(1+((df.capital[-1]-df.capital[0])/df.capital[0])))
print("Strategy max drawdown: {:.3f}%".format(strategy_max_drawdown))
print("Security max drawdown: {:.3f}%".format(security_max_drawdown))

#%% Function calls
#plot_trades(df)

