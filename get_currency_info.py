# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 00:14:23 2018

@author: pgood
"""
"""
def get_current(ticker, trade_type):
    import requests
    url = 'https://bittrex.com/api/v1.1/public/getticker?market={}'.format(ticker)
    response = requests.get(url)
    json_text = response.json()
    result = json_text['result']
    bid = float(result['Bid'])
    ask = float(result['Ask'])
    last = float(result['Last'])
    if trade_type in ('buy', 'cover'):
        return ask
    elif trade_type in ('sell', 'short'):
        return bid
    elif trade_type == 'check':
        return(bid, ask, last)
"""        
def get_current(ticker, trade_type):
    import requests
    url = 'https://bittrex.com/api/v1.1/public/getticker?market=USDT-{}'.format(ticker.upper())
    response = requests.get(url)
    json_text = response.json()['result']

    bid = float(json_text['Bid'])
    ask = float(json_text['Ask'])
    last = float(json_text['Last'])
    if trade_type in ('buy', 'cover'):
        return ask
    elif trade_type in ('sell', 'short'):
        return bid
    elif trade_type == 'check':
        return(bid, ask, last)

print(get_current('ath', 'buy'))
   
def get_charts(ticker):
    import requests
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    import pandas as pd
    start = datetime.now() - timedelta(days = 120)
    end = datetime.now()
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USDT&limit=120&aggregate=1'.format(ticker.upper())
    response = requests.get(url)
    json_text = response.json()['Data']
    df = pd.DataFrame(json_text, columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
    df.sort_values(by = ['time'], inplace = True)
    dates = df['time'].map(datetime.fromtimestamp)
    df['time'] = dates
    plot = plt.plot('time', 'close', data = df.iloc[19:119, :])
    plt.title('{} to USD (last 100 days)'.format(ticker))
    plt.ylabel('{} Price (USD)'.format(ticker.upper()))
    plt.xlabel('Date')
    labels = dates.map('{:%Y-%m-%d}'.format)[19:119:5].values
    plt.xticks(labels, labels, rotation = 45)
    df['moving'] = df['close'].rolling(window = 20).mean()
    plt.plot('time', 'moving', data = df)
    plt.title('{} Price History'.format(ticker.upper()))
    plt.legend()


