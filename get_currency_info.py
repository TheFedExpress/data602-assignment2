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
        

def get_24(ticker):
    import requests
    import pandas as pd
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USDT'.format(ticker.upper())
    response = requests.get(url)
    obj = response.json()['Data']
    df = pd.DataFrame(obj, columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
    raw = df['close'].values
    stats = [raw.std(), raw.mean(), raw.min(), raw.max()]
    formated = tuple(['${:,.2f}'.format(item) for item in stats])
    return formated
    

def make_chart(ticker):
    from plotly.graph_objs import Scatter, Data, Line
    from plotly.offline import plot    
    import requests
    from datetime import datetime, timedelta
    import pandas as pd
    
    ticker = ticker.upper()
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USDT&limit=119&aggregate=1'.format(ticker)
    response = requests.get(url)
    json_text = response.json()['Data']
    df = pd.DataFrame(json_text, columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
    df.sort_values(by = ['time'], inplace = True)
    dates = df['time'].map(datetime.fromtimestamp)
    df['time'] = dates
    labels = dates.map('{:%Y-%m-%d}'.format)[19:].values
    df['moving'] = df['close'].rolling(window = 20).mean()
    price = Scatter(x= labels, y = df.loc[19:, 'close'], line = Line(width = 2, color = 'blue'), name = ticker)
    moving = Scatter(x= labels, y = df.loc[19:, 'moving'], line = Line(width = 2, color = 'orange'), name = 'Moving Avg')
    data = Data([price, moving])
    return data

def find_actives():
    import requests
    import pandas as pd
    url = 'https://bittrex.com/api/v1.1/public/getcurrencies'
    response = requests.get(url)
    obj = response.json()['result']
    df = pd.DataFrame(obj)
    actives = df[df.IsActive == True]['Currency'].values
    return actives