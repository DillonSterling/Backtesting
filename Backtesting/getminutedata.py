# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 23:25:14 2021

@author: SESA553573
"""
import csv
import requests
import pandas as pd

def get_minute_data(symbol="IBM"):
    function = "TIME_SERIES_INTRADAY_EXTENDED"
    interval = "1min"
    year = "1"
    month = "1"
    slicee = f"year{year}month{month}"
    apikey = "0NJC5WJDXT3NCAV5"
    
    
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&slice={slicee}&apikey={apikey}" 

    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        print("got data")
    
    df = pd.DataFrame(my_list[1:], columns=my_list[0])
    df = df.set_index('time')
    print("processed into dataframe")
    return df