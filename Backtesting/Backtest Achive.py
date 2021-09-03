# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 18:21:20 2021

@author: SESA553573
"""
#%%
import pandas as pd
from matplotlib import pyplot as plt
import getminutedata as gd
import pandas_ta as ta

symbol = "gld"
ema5 = []
delta_ema5 = []
have_position = False
position_type = "none"
position_type_list = []
buys = []
sells = []
shorts = []
covers = []
trades = []
profit = []
capital = []
smoothing = 2

class trade():
    def __init__(self, order_type=None):
        self.order_type = order_type
        
    def open_position(self, open_price):
        self.open_price = open_price
        self.status = "open"
    def close_position(self, close_price):
        self.close_price = close_price
        self.status = "closed"

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
        
# def buy(price):
#     global buys
#     global have_position
#     global position_type
#     buys.append(price)
#     have_position = True
#     position_type = "long"
#     print("Buy")
#     print("Time: {}".format(df.index[item]))
#     print("Current close: {}".format(df.close[item]))
#     print("Next open: {}".format(df.open[item+1]))
#     print("")
    
# def sell(price):
#     global sells
#     global have_position
#     global position_type
#     sells.append(price)
#     have_position = False
#     position_type = "none"
#     print("Sell")
#     print("Time: {}".format(df.index[item]))
#     print("Current close: {}".format(df.close[item]))
#     print("Next open: {}".format(df.open[item+1]))
#     print("")
    
# def short(price):
#     global shorts
#     global have_position
#     global position_type
#     shorts.append(price)
#     have_position = True
#     position_type = "short"
#     print("Short")
#     print("Time: {}".format(df.index[item]))
#     print("Current close: {}".format(df.close[item]))
#     print("Next open: {}".format(df.open[item+1]))
#     print("")
    
# def cover(price):
#     global covers
#     global have_position
#     global position_type
#     covers.append(price)
#     have_position = False
#     position_type = "none"
#     print("Cover")
#     print("Time: {}".format(df.index[item]))
#     print("Current close: {}".format(df.close[item]))
#     print("Next open: {}".format(df.open[item+1]))
#     print("")
                    
    
#%%
df = gd.get_minute_data(symbol)
df = df.apply(pd.to_numeric, errors='coerce')
#df.index = df.index.values[::-1]
df = df.iloc[::-1]


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


#%%
for item in range(len(df.index)):
    if item == 0:
        periods = 1
        daily_average_volume = df.volume[item]
        capital.append(df.open[item])
    else:
        if(df.index[item-1].split("-")[1] == df.index[item].split("-")[1]):
            periods = periods + 1
            daily_average_volume = ((daily_average_volume * (periods - 1)) + (df.volume[item]))/periods
        else:
            periods = 1
            daily_average_volume = df.volume[item]
            
#%% Trading strategy
        #Open position
        if ((trades == []) or (trades[-1].status == 'closed')):
            capital.append(capital[item-1])
            #Buy filter
            if((df.RSI_14[item] < 29) and (df.RSI_14[item] > df.RSI_14[item-1])
            or (df.close[item] < df.BBL_100[item])):
                if(df.volume[item] > daily_average_volume/1.5):
                    if df.EMA_5[item] > df.EMA_5[item-1]:
                        #Buy the open of the next tick
                        try:
                            #buy(df.open[item + 1])
                            new_trade = trade("long")
                            new_trade.open_position(df.open[item + 1])
                            trades.append(new_trade)
                        except:
                            break
                        entry_price = df.open[item + 1]
                        entry_capital = capital[item]
                        
            #Short filter
            elif((df.RSI_14[item] > 71) and (df.RSI_14[item] < df.RSI_14[item-1])
            or (df.close[item] < df.BBU_100[item])):
                if(df.volume[item] > daily_average_volume/1.5):
                    if df.EMA_5[item] < df.EMA_5[item-1]:
                        #Short the open of the next tick
                        try:
                            #short(df.open[item + 1])
                            new_trade = trade("short")
                            new_trade.open_position(df.open[item + 1])
                            trades.append(new_trade)
                        except:
                            break
                        entry_price = df.open[item + 1]
                        entry_capital = capital[item]
                
        #sell filter
        elif(trades[-1].status == "open") and (trades != []) and (item < df.shape[0]-1):
            if trades[-1].order_type == "long":
                #Sell filter
                capital.append(entry_capital * (df.open[item+1]/entry_price))
                if (((df.RSI_14[item] > 71) and (df.RSI_14[item] < df.RSI_14[item-1]))
                or (df.close[item] < entry_price * 0.99)
                or (df.close[item] > df.BBU_100[item])):
    
                    try:
                        #Sell the open of the next tick
                        #sell(df.open[item + 1])
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
                        #cover(df.open[item + 1])
                        trades[-1].close_position(df.open[item + 1])
                    except:
                        break
        else:
            capital.append(capital[item-1])
                    
    #position_type_list.append(position_type)
            
#%%           
dfc = pd.DataFrame(capital, columns=["capital"],dtype=float,index=df.index)
df = pd.concat([df,dfc],axis=1)
#%%    
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

#%%
# for buy in range(len(buys)):
#     if sells[buy] != None:
#         profit.append((sells[buy]-buys[buy])/buys[buy])
# for short in range(len(shorts)):
#     if shorts[short] != None:
#         profit.append((shorts[short]-covers[short])/shorts[short])
        
total_return = 1
for transaction in range(len(trades)):
    total_return = total_return * (trades[transaction].calculate_profit())
    
benchmark_return = 1 + (df.open[len(df.open)-1] - df.open[0])/df.open[0]

alpha = (total_return - benchmark_return)*100

print("Total Return: {}".format(total_return))
print("Benchmark Return: {}".format(benchmark_return))
print("Alpha: {}".format(alpha))
print("Start Capital: {}".format(df.capital[0]))
print("End Capital: {}".format(df.capital[-1]))
print("Return on Capital: {}".format(1+((df.capital[-1]-df.capital[0])/df.capital[0])))
#plot_trades(df)
