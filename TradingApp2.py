# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 14:22:35 2018

@author: pgood
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont 

class TradingApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.main_choice = tk.StringVar()
        self.main_choice.set('StartPage')
        
        self.container = tk.Frame(self)
        self.container.grid(column = 0, row = 0, sticky=(N, W, E, S))
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self._frame = StartPage(parent=self.container, controller=self)
        
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.main_choice.set(page_name)
        frames = {}
        for F in (StartPage, Trade, PLPage, BlotterPage):
            page_name = F.__name__
            frames[page_name] = F
        new_frame = frames[self.main_choice.get()](parent=self.container, controller=self)
        self._frame.destroy()
        self._frame = new_frame

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.grid(column=0, row=0)
        
        label = ttk.Label(self, text="Main Menu", font=controller.title_font).grid(
                column = 4, row = 1)
        choice = StringVar()
        
        trade = ttk.Radiobutton(self, text = 'Trade', variable = choice, value = 'Trade')
        trade.grid(column = 2, row = 2, sticky = (W,E))
        blotter = ttk.Radiobutton(self, text = 'Show Blotter', variable = choice, value = 'BlotterPage')
        blotter.grid(column = 2, row = 3, sticky = (W,E))
        pl = ttk.Radiobutton(self, text = 'Show P/L', variable = choice, value = 'PLPage')
        pl.grid(column = 2, row = 4, sticky = (W,E))
        quit_app = ttk.Radiobutton(self, text = 'Quit', variable = choice, value = 'Quit')
        quit_app.grid(column = 2, row = 5, sticky = (W,E))


        button = tk.Button(self, text="Go",
                            command=lambda: controller.show_frame(choice.get()))
        
        button.grid(column = 10, row = 6, sticky= (W,E))


class Trade(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.ticker = StringVar()
        self.final_ticker = StringVar()
        self.final_shares = StringVar()
        price = StringVar()
        trade_type = StringVar(None, 'buy')
        trade_type.set("buy")
        shares = StringVar()
        
        self.lfdata = ttk.Labelframe(self, padding=(6, 6, 12, 12),
                text='Trade Options')
        self.lfdata.grid(column=1, columnspan=1,rowspan = 13, row=2, sticky='nsew') 
        
        #labels
        
        label = tk.Label(self, text="Trading Menu", font=controller.title_font)
        label.grid(column = 2, row = 1, sticky = (W,E))
        labelshares = tk.Label(self, text = "Enter Quantity:")
        labelshares.grid(column = 1, row = 12, sticky = (W,E), pady=10, in_=self.lfdata) 
        tk.Label(self, text="Enter Ticker:").grid(column = 1, row = 4, 
                sticky = (W,E), in_=self.lfdata)
        tk.Label(self, text="Choose Trade Type:").grid(column = 1, row = 6, 
                sticky = (W,E))
        tk.Label(self, text = "Current Price (USD):").grid(column = 2, row = 6)
        tk.Label(self, textvariable = price).grid(column = 3, row = 6, padx=5, pady=5)


        #text boxes
                
        entershares = ttk.Entry(self, textvariable = shares)
        entershares.grid(column = 1, row = 13, in_=self.lfdata)
        enterticker = ttk.Entry(self, textvariable = self.ticker, in_=self.lfdata)
        enterticker.grid(column = 1, row = 5,  sticky = 'we', padx=5, pady=5, in_=self.lfdata) 
        lookup = tk.Button(self, text = 'Show Chart', 
                           command = lambda: self.showChart())
        lookup.grid(column = 2, row = 4,  sticky = 'we')
        
        #buttons
        
        back_button = tk.Button(self, text="Go to the main menu",
                           command=lambda: controller.show_frame("StartPage"))
        back_button.grid(column = 4, row = 14, sticky = 'we')
        
        price_button = tk.Button(self, text = 'Check Price', 
                                 command = lambda: self.getCurrent(price,self.ticker.get(), self.trade_type.get()))
        price_button.grid(column = 2, row = 5, padx=5, pady=5)
        trade_button = tk.Button(self, text = 'Make Trade', state=DISABLED,
                                 command = lambda: self.getCurrent(price,ticker.get(), trade_type.get()))
        trade_button.grid(column = 1, row = 15)
       
        #radiobuttons
        
        buy = ttk.Radiobutton(self, text = 'Buy', variable = trade_type, value = 'buy',)
        buy.grid(column = 1, row = 7, sticky = 'we', in_=self.lfdata)
        sell = ttk.Radiobutton(self, text = 'Sell', variable = trade_type, value = 'sell')
        sell.grid(column = 1, row = 8, sticky = 'we', in_=self.lfdata)
        short = ttk.Radiobutton(self, text = 'Short', variable = trade_type, value = 'short')
        short.grid(column = 1, row = 9, sticky = 'we', in_=self.lfdata)
        cover = ttk.Radiobutton(self, text = 'Cover Short', 
                                variable = trade_type, value = 'cover')
        cover.grid(column = 1, row = 10, sticky = 'we', in_=self.lfdata)
        
        
        

    def showChart(self):
        import requests
        from datetime import datetime, timedelta
        import matplotlib.pyplot as plt
        import pandas as pd
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        start = datetime.now() - timedelta(days = 120)
        end = datetime.now()
        ticker = self.ticker.get().upper()
        url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USDT&limit=120&aggregate=1'.format(ticker)
        response = requests.get(url)
        json_text = response.json()['Data']
        df = pd.DataFrame(json_text, columns = ['time', 'low', 'high', 'open', 'close', 'volume'])
        df.sort_values(by = ['time'], inplace = True)
        dates = df['time'].map(datetime.fromtimestamp)
        df['time'] = dates
        f = Figure(figsize=(6, 6), dpi=100)
        a = f.add_subplot(111)     
        a.plot('time', 'close', data = df.iloc[19:119, :])
        a.set_title('{} to USD (last 100 days)'.format(ticker))
        a.set_ylabel('{} Price (USD)'.format(ticker.upper()))
        a.set_xlabel('Date')
        labels = dates.map('{:%Y-%m-%d}'.format)[19:119:5].values
        a.set_xticklabels(labels)
        for tick in a.get_xticklabels():
            tick.set_rotation(45)
        df['moving'] = df['close'].rolling(window = 20).mean()
        a.plot('time', 'moving', data = df)
        a.set_title('{} Price History'.format(ticker.upper()))
        a.legend()     

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(column = 5, row = 1, rowspan = 35, columnspan = 30)
        
    def getCurrent(self, price, ticker, trade_type):
        import requests
        url = 'https://bittrex.com/api/v1.1/public/getticker?market=USDT-{}'.format(ticker.upper())
        response = requests.get(url)
        try:    
            json_text = response.json()['result']    
            bid = json_text['Bid']
            ask = json_text['Ask']
            last = json_text['Last']
        except TypeError:
            bid = "Ticker not found"
            ask = "Ticker not found"
            last = "Ticker not found"
            
        if trade_type in ('buy', 'cover'):
            price.set(last)
        elif trade_type in ('sell', 'short'):
            price.set(bid)
        elif trade_type == 'check':
            return(bid, ask, last)
    
    def previewTrade():
        

class BlotterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label = tk.Label(self, text="Blotter", font=controller.title_font)
        label.grid(row = 1, column = 1)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row = 5, column = 1)


class PLPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label = tk.Label(self, text="P&L", font=controller.title_font)
        label.grid(row = 1, column = 1)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row = 5, column = 1)


if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()