# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 21:07:08 2021

@author: SESA553573
"""

import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time

apple = yf.Ticker("ibm")
apple_history = apple.history(period='5d',interval='5m' )

indicators = [{'kind':'ema', 'length': 5}, {'kind':'sma', 'length': 50}]
my_strategy = ta.Strategy(name='Test', ta=indicators)
time.sleep(30)
apple_history.ta.mp = False
apple_history.ta.cores = 0
apple_history.ta.strategy(my_strategy)