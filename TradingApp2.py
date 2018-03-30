# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 14:22:35 2018

@author: pgood
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont 
from user_account import UserAccount
from user_account import UserDB

db = UserDB()
account = UserAccount(db)


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

        self._frame = StartPage(parent=self.container, controller=self, account = account)
        
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.main_choice.set(page_name)
        frames = {}
        for F in (StartPage, Trade, PLPage, BlotterPage):
            page_name = F.__name__
            frames[page_name] = F
            
        new_frame = frames[self.main_choice.get()](parent=self.container, controller=self, account = account)
        self._frame.destroy()
        self._frame = new_frame

class StartPage(tk.Frame):

    def __init__(self, parent, controller, account):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.grid(column=0, row=0)
        
        label = ttk.Label(self, text="Currecny Trader", font=controller.title_font).grid(
                column = 1, row = 1, columnspan = 12, sticky = 'we', padx = 30, pady = 30)
        choice = StringVar()
        self.radiodata = ttk.LabelFrame(self, text = 'Menu Choice',padding=(6, 6, 12, 12))
        self.radiodata.grid(column = 2, row = 3, rowspan = 6)
        trade = ttk.Radiobutton(self, text = 'Trade', variable = choice, value = 'Trade')
        trade.grid(column = 2, row = 4, sticky = 'we', in_ = self.radiodata)
        blotter = ttk.Radiobutton(self, text = 'Show Blotter', variable = choice, value = 'BlotterPage')
        blotter.grid(column = 2, row = 5, sticky = (W,E), in_ = self.radiodata)
        pl = ttk.Radiobutton(self, text = 'Show P/L', variable = choice, value = 'PLPage')
        pl.grid(column = 2, row = 6, sticky = 'we', in_ = self.radiodata)
        quit_app = ttk.Radiobutton(self, text = 'Quit', variable = choice, value = 'Quit')
        quit_app.grid(column = 2, row = 7, sticky = 'we', in_ = self.radiodata)


        button = tk.Button(self, text="Go",
                            command=lambda: controller.show_frame(choice.get()))
        
        button.grid(column = 2, row = 10, sticky= 'we', pady = 10)


class Trade(tk.Frame):

    def __init__(self, parent, controller, account):
        tk.Frame.__init__(self, parent)
        
        self.grid(column=0, row=0, sticky='nwes')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.ticker = StringVar()
        self.final_ticker = StringVar()
        self.final_shares = StringVar()
        self.final_type = StringVar()
        self.total_order = StringVar()
        self.price = StringVar()
        self.trade_type = StringVar(None, 'buy')
        self.trade_type.set("buy")
        self.shares = StringVar()
        self.state = StringVar()
        self.std = StringVar()
        self.mean = StringVar()
        self.min = StringVar()
        self.max = StringVar()
        
        self.lfdata = ttk.Labelframe(self, padding=(6, 6, 12, 12),
                text='Trade Options')
        self.lfdata.grid(column=1,row = 2, columnspan=1,rowspan = 13, sticky='nsew') 
        
        self.statdata = ttk.Labelframe(self, padding=(12, 12, 12, 12),
                text='Price Statistics(last 24 Hours)')
        self.statdata.grid(column=3, columnspan=2, rowspan = 9, row=6, sticky='nsew') 
        
        #labels
        
        label = tk.Label(self, text="Trading Menu", font=controller.title_font)
        label.grid(column = 1, row = 1, sticky = 'we', columnspan = 5)
        labelshares = tk.Label(self, text = "Enter Quantity:")
        labelshares.grid(column = 1, row = 12, sticky = (W,E), pady=10, in_=self.lfdata) 
        tk.Label(self, text="Enter Ticker:").grid(column = 1, row = 4, 
                sticky = 'we', in_=self.lfdata)
        
        tk.Label(self, text = "Mean:").grid(column = 3, row = 8, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, text = "Min:").grid(column = 3, row = 9, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, text = "Max:").grid(column = 3, row = 10, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, text = "Standard Deviation:").grid(column = 3, row = 11, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, textvariable = self.mean).grid(column = 4, row = 8, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, textvariable = self.min).grid(column = 4, row = 9, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, textvariable = self.max).grid(column = 4, row = 10, padx=5, pady=5, in_ = self.statdata)
        tk.Label(self, textvariable = self.std).grid(column = 4, row = 11, padx=5, pady=5, in_ = self.statdata)

        tk.Label(self, text = "Current Price (USD):").grid(column = 1, row = 16,padx=5, pady = 10)
        tk.Label(self, text = "Total Order Value:").grid(column = 1, row = 17)
        tk.Label(self, textvariable = self.price).grid(column = 2, row = 16, padx=5, pady=5)
        tk.Label(self, textvariable = self.total_order).grid(column = 2, row = 17, padx=5, pady=5)
        tk.Label(self, textvariable = self.state).grid(column = 2, row = 19, padx=5, pady=5)


        #text boxes
                
        entershares = ttk.Entry(self, textvariable = self.shares)
        entershares.grid(column = 1, row = 13, in_=self.lfdata)
        enterticker = ttk.Entry(self, textvariable = self.ticker, in_=self.lfdata)
        enterticker.grid(column = 1, row = 5,  sticky = 'we', padx=5, pady=5, in_=self.lfdata) 
        
        #buttons
        
        back_button = tk.Button(self, text="Go to the main menu",
                           command=lambda: controller.show_frame("StartPage"))
        back_button.grid(column = 5, row = 19, sticky = 'we')
        
        price_button = tk.Button(self, text = 'Preview Trade', 
                                 command = lambda: self.getCurrent())
        price_button.grid(column = 1, row = 15, padx=5, pady=5, in_=self.lfdata)
        self.trade_button = tk.Button(self, text = 'Make Trade', state=DISABLED,
                                 command = lambda: self.executeTrade(account))
        self.trade_button.grid(column = 1, row = 19)
       
        self.lookup = tk.Button(self, text = 'Show Chart/Stats', 
                           command = lambda: self.showChart())
        self.lookup.grid(column = 3, row = 4,  sticky = 'we')
        
        #radiobuttons
        
        buy = ttk.Radiobutton(self, text = 'Buy', variable = self.trade_type, value = 'buy',)
        buy.grid(column = 1, row = 7, sticky = 'we', in_=self.lfdata)
        sell = ttk.Radiobutton(self, text = 'Sell', variable = self.trade_type, value = 'sell')
        sell.grid(column = 1, row = 8, sticky = 'we', in_=self.lfdata)
        short = ttk.Radiobutton(self, text = 'Short', variable = self.trade_type, value = 'short')
        short.grid(column = 1, row = 9, sticky = 'we', in_=self.lfdata)
        cover = ttk.Radiobutton(self, text = 'Cover Short', 
                                variable = self.trade_type, value = 'cover')
        cover.grid(column = 1, row = 10, sticky = 'we', in_=self.lfdata)
        
        
        

    def showChart(self):
        import requests
        from datetime import datetime, timedelta
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        from get_currency_info import get_24

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
        f = Figure(figsize=(8, 6), dpi=100)
        a = f.add_subplot(111)

        a.plot('time', 'close', data = df.iloc[19:119, :])
        start, end = a.get_xlim()
        ticks = np.arange(start, end, (end - start)/10)
        a.xaxis.set_ticks(ticks)
        a.set_title('{} to USD (last 100 days)'.format(ticker))
        a.set_ylabel('{} Price (USD)'.format(ticker.upper()))
        a.set_xlabel('Date')
        a.get_xticks()
        print(dates)
        labels = dates.map('{:%Y-%m-%d}'.format)[19:119:10]
        print(labels)
        a.set_xticklabels(labels)
        for tick in a.get_xticklabels():
            tick.set_rotation(45)
        df['moving'] = df['close'].rolling(window = 20).mean()
        a.plot('time', 'moving', data = df)
        a.set_title('{} Price History'.format(ticker.upper()))
        a.legend()     

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(column = 6, row = 1, rowspan = 35, columnspan = 30)
        ticker = self.ticker.get().upper()
        stats = get_24(ticker)
        self.std.set(stats[0])
        self.mean.set(stats[1])
        self.min.set(stats[2])
        self.max.set(stats[3])
        
    def getCurrent(self):
        from get_currency_info import get_current
        ticker =  self.ticker.get().upper()
        trade_type = self.trade_type.get()
        price = get_current(ticker, trade_type)
        price_format = "${:,.2f}".format(price)
            
        try:
            total_price = price * float(self.shares.get())
            self.total_order.set("${:,.2f}".format(total_price))
            self.price.set(price_format)
            self.final_shares.set(self.shares.get())
            self.final_ticker.set(ticker)
            self.final_type.set(trade_type)
            self.trade_button['state'] = 'normal'
        except ValueError:
            self.total_order.set("Invalid Entry") 

    def executeTrade(self, account):
        from get_currency_info import get_current
        ticker = self.final_ticker.get()
        trade_type = self.final_type.get()
        shares = float(self.final_shares.get())
        price = get_current(ticker, trade_type)
        response = account.evalTransaction(trade_type, shares, price, ticker, db)
        self.final_ticker.set('')
        self.final_shares.set('')
        self.final_type.set('')
        self.price.set('')
        self.shares.set('')
        self.ticker.set('')
        self.total_order.set('')
        self.trade_button['state'] = 'disabled'
        if account.message == 'success':
            self.state.set('Order Success! {}@${:,.2f}'.format(ticker, price))
        else: 
            self.state.set(account.message)
        

          

class BlotterPage(tk.Frame):

    def __init__(self, parent, controller, account):
        tk.Frame.__init__(self, parent)

        self.grid(column=0, row=0, sticky='nwes')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 1, row = 12)
        account.showBlotter()
        if account.blotter_rows < 1:
            label = tk.Label(self, text="Blotter", font=controller.title_font)
            label.grid(row = 1, column = 1, columnspan = 2)
            tk.Label(self,text = "You haven't made any transactions").grid(column = 1, row = 2)
        else:

            rows = len(account.blotter_view)
            cols = len(account.blotter_view.columns)
            tk.Label(self, text = 'Blotter', font = controller.title_font).grid(
                column = 1, row = 1, columnspan = cols)
            for i in range(rows + 1):
    
                for j in range(cols):
                    if i == 0:
                       tk.Label(self, text = account.blotter_view.columns[j]).grid(column = j, row = i + 2,
                               padx=5, pady=5)
                       ttk.Separator(self, orient = HORIZONTAL).grid(column = j, row = i + 3,
                         sticky = 'ew')                
                    else:
                        tk.Label(self, text = account.blotter_view.iloc[i-1,j]).grid(column = j, row = i*2 + 2,
                                padx=5, pady=5)
                        
                        ttk.Separator(self, orient = HORIZONTAL).grid(column = j, row = i*2 + 3,
                         sticky = 'ew')


class PLPage(tk.Frame):
    
    def __init__(self, parent, controller, account):
        tk.Frame.__init__(self, parent)
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        account.showPL()
        rows = len(account.pl_view)
        cols = len(account.pl_view.columns)
        tk.Label(self, text = 'P/L', font = controller.title_font).grid(
            column = 1, row = 1, columnspan = cols)

        for i in range(rows + 1):

            for j in range(cols):
                if i == 0:
                   tk.Label(self, text = account.pl_view.columns[j]).grid(column = j, row = i + 2,
                           padx=5, pady=5)
                   ttk.Separator(self, orient = HORIZONTAL).grid(column = j, row = i + 3,
                     sticky = 'ew')                
                else:
                    tk.Label(self, text = account.pl_view.iloc[i-1,j]).grid(column = j, row = i*2 + 2,
                            padx=5, pady=5)
                    
                    ttk.Separator(self, orient = HORIZONTAL).grid(column = j, row = i*2 + 3,
                     sticky = 'ew')


        '''

        self.table = Table(self, dataframe= account.pl_view,
                                showtoolbar=False, showstatusbar=False, width = 1000, height = 600)
        
        self.table.show()
        self.table.adjustColumnWidths()
        '''        
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 1, row = rows*2 + 4, pady=15)
        

if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()