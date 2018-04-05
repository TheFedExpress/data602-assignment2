# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:53:12 2018

@author: pgood
"""

class User:
    
    def __init__(self, db):
        self.currency = 'USDT'
    
    #For fungible shares, it doesn't make sense to allow for simultaneous short and long positions
    #This would also require two lines on the P/L, causing confusion
    def evalTransaction(self, tran_type, shares, price, ticker, db, pl, blotter):
       from datetime import datetime
       cash = pl.pl.loc['cash', 'market']
       total = shares * price
       cash = pl.pl.loc['cash', 'market']
       try:
            prev_shares = pl.pl.loc[ticker, "position"]
            new = 0
       except KeyError:
            new = 1
            prev_shares = 0

       if tran_type in ["buy", "cover"]:
            #User abuse/misuse prevention
            margin = pl.check_margin()

            if tran_type == "cover" and prev_shares >= 0:
                self.message = "You do not have any short sales with this security"
            elif tran_type == "cover" and shares + prev_shares > 0:
                self.message = "\nYou have attempted to cover {} shares.  Please cover {} shares or less"
                self.message.format(shares, -prev_shares)
                
            elif tran_type == "buy" and cash <= margin * 2 + shares * price:
                self.message = "\nThis transaction requires ${:,.2f} in your account.  You have ${:,.2f}."
                self.message.format(margin * 2 + shares * price, cash)
                
            elif tran_type == "buy" and prev_shares < 0:
                self.message = "\nYou currently have {} shares of {} shorted.  Please cover those before buying.".format(shares, ticker)
                
            else:#Process transaction
                date = datetime.now ()
                trans = (cash,  ticker, -total, price, shares, tran_type)
                pl.eval_pl(tran_type, shares, price, ticker, total, db, new, prev_shares)
                blotter.eval_blotter(db, date, trans)
                self.message = "Success"
                
       else:#sell/short      
            #simplified margin system only based on cash
            #no margin calls either
            #I could have used the dataframe calcs from the showPL method to calculate total equity, but
            #that requires getting the market price from the whole portfolio, and that would slow down
            #the app
            if tran_type == "short":
                margin = pl.check_margin()
                                 
            if tran_type == "sell" and prev_shares < 0:
                self.message = "You have a short position in {0} of {1} shares".format(ticker, prev_shares*-1)
                
            elif tran_type == "sell" and prev_shares < shares:
                self.message= "You have {0} shares of {1} in you account.  Please choose a different quantity to sell".format(prev_shares, ticker)
                
                
            elif tran_type == "short" and prev_shares > 0:
                self.message = "You have a long position in {} of {} shares.  Please sell before shorting"
                
            elif tran_type == "short" and cash <= (margin * 2 + shares * price):
                self.message = "This transaction requires ${:,.2f} in your account.  You have ${:,.2f}."
            else:
               date = datetime.now ()
               trans = (cash,  ticker, total, price, shares, tran_type)
               pl.eval_pl(tran_type, shares, price, ticker, total, db, new, prev_shares)
               blotter.eval_blotter(db, date, trans)
               self.message = "Success"

class Blotter:
    
    def __init__(self, user, db):
        import pandas as pd
        from datetime import datetime
        if db.new_account == 1:
            self.blotter_rows = 0
            self.blotter = pd.DataFrame(columns = [ "cash_balance", "currency", "net", "price",
                                 "shares", "tran_type"])
        else:
            self.blotter_rows = db.db.blotter.count()
            if self.blotter_rows > 0:
                blotter_list = []
                blotter_recs = db.db.blotter.find({})
                for rec in blotter_recs:
                    record_dict = {}
                    for key in rec.keys():
                        if key != '_id':
                            if key == 'date':
                                record_dict[key] = datetime.fromtimestamp(rec[key])
                            else:
                                record_dict[key] = rec[key]
                    blotter_list.append(record_dict)
                            
                self.blotter = pd.DataFrame(blotter_list)
                self.blotter.set_index('date', inplace=True)

            else:
                self.blotter = pd.DataFrame(columns = [ "cash_balance", "currency", "net", "price",
                                 "shares", "tran_type"])
                
    def showBlotter(self):
        if self.blotter_rows > 0:
            df = self.blotter.copy()
            df["price"] = df["price"].map('${:,.2f}'.format)
            df["net"] = df["net"].map('${:,.2f}'.format)
            df["cash_balance"] = df["cash_balance"].map('${:,.2f}'.format)
            dates = df.index
            df['Transaction Date'] = dates
            
            df = df[['Transaction Date', "currency", "price", "shares", "tran_type", "net", "cash_balance"]]
            labels = ["Transaction Date", "Currency", "Price", "Shares Traded", "Transaction Type",
                      "Net Cash Flow", "Cash Balance"]
            df.columns = labels
            self.blotter_view = df
    def eval_blotter(self, db, date, trans):
           self.blotter.loc[date] = trans
           db.blotter_insert(date, trans)
           self.blotter_rows += 1

            
class PL:
    
    def __init__(self, user, db, starting = 100000000.0):
        import pandas as pd
        if db.new_account == 1:
            start = {"cash": {"position": 0, "market": starting, "wap" : 0.0, "rpl": 0.0, "upl": 0.0, "total_pl": 0.0,
                                           "allocation_by_shares": 0.0, "allocation_by_dollars": 100.0}}
            self.pl = pd.DataFrame.from_dict(start, orient = 'index')
            db.pl_insert(self.pl, 'cash')
        else:
            pl_recs = db.db.pl.find({})
            pl_dict = {}
            for rec in pl_recs:
                for key in rec.keys():
                    if key != '_id':
                        pl_dict[key] = rec[key]
            self.pl = pd.DataFrame.from_dict(pl_dict, orient = 'index')        
    
    def check_margin(self):
        from get_currency_info import get_current
        margin = 0
        for currency in self.pl.index:
            if self.pl.loc[currency, "position"] < 0:
                margin += self.pl.loc[currency, "position"] * get_current(currency, "buy") * -1
        return margin
    
    def eval_pl(self, tran_type, shares, price, ticker, total, db, new, prev_shares):
        if tran_type in ('buy', 'cover'):
            self.pl.loc['cash', 'market'] -= total
            if new == 0:
                new_shares = prev_shares + shares
                if tran_type == "buy":
                    if self.pl.loc[ticker, "position"] == 0:
                        self.pl.loc[ticker, "wap"] = price
            
                    else:
                        prev_value = prev_shares * self.pl.loc[ticker, "wap"]
                        self.pl.loc[ticker, "wap"] = (prev_value + shares * price)/new_shares
                        
                else:#Cover
                    gain = self.pl.loc[ticker, "wap"] * shares - total
                    self.pl.loc[ticker, "rpl"]  = self.pl.loc[ticker, "rpl"] + gain
                self.pl.loc[ticker, "position"] = new_shares
                
                if new_shares == 0:#for aesthetics in the P&L
                    self.pl.loc[ticker, "wap"] = 0
                db.pl_update(self.pl, ticker)
                db.pl_update(self.pl, 'cash')
            else:
                self.pl.loc[ticker, ['position', 'market', 'wap', 'rpl', 'upl', 'total_pl', 
                     'allocation_by_dollars', 'allocation_by_shares']] = (shares, 0, price, 0, 0, shares*price, 0, 0)

                db.pl_insert(self.pl, ticker)
                db.pl_update(self.pl, 'cash')
        else:
           self.pl.loc['cash', 'market'] += total
           if new == 0:
           #process transaction
               new_shares = self.pl.loc[ticker,'position'] - shares
               
               if tran_type == "sell":
                   
                   gain = total -  self.pl.loc[ticker, 'wap'] * shares
                   self.pl.loc[ticker, 'rpl']  = self.pl.loc[ticker, "rpl"] + gain
                   
               else:#short
                   if self.pl.loc[ticker, 'position'] == 0:
                       self.pl.loc[ticker, "wap"] = price
                       
                   else:
                       prev_value = prev_shares * self.pl.loc[ticker, "wap"]*-1
                       self.pl.loc[ticker, "wap"] = (prev_value + shares * price)/new_shares*-1
                       
               self.pl.loc[ticker, "position"] = new_shares
               if new_shares == 0:
                   self.pl.loc[ticker, "wap"] = 0               
               db.pl_update(self.pl, ticker)
               db.pl_update(self.pl, 'cash')
           else:
               self.pl.loc[ticker, ['position', 'market', 'wap', 'rpl', 'upl', 'total_pl', 
                 'allocation_by_dollars', 'allocation_by_shares']] = (-shares, 0, price, 0, 0, -shares*price, 0, 0)
               db.pl_insert(self.pl, ticker)
               db.pl_update(self.pl, 'cash')



           
    def showPL(self):
        import numpy as np
        from get_currency_info import get_current
        
        df = self.pl.copy()[self.pl.index != 'cash']
        #create a datafram from positions for easy calculated columns
        markets = []
        for position in df.index.values:
            bid, ask, market = get_current(position, 'check')
            markets.append(market)
        df["market"] = markets
        cash = self.pl.loc['cash', 'market']
        
        df["total_value"] = df.position * df.market
        df['share_weight'] =  abs(df.position)/np.sum(abs(df.position))
        df['value_weight'] = abs(df['total_value'])/np.sum(abs(df['total_value']))
        upl = df.position * df.market - df.position * df.wap
        df["upl"] = upl
        
        df.fillna(0)
        df.replace(np.nan, 0, inplace=True)
        
        final_df = df
        currencies = final_df.index
        final_df['currency'] = currencies
        final_df = df[['currency', "position", "market", "total_value", 'value_weight', 'share_weight', "wap", "upl", 
                       "rpl"]]
        
        
                    
        #total row
        val = cash + np.sum(final_df["total_value"])
        totals = ['Total', '', '',  val,'', '', '', np.sum(final_df["upl"]), np.sum(final_df["rpl"])]
        for item in range(len(totals)):
            if type(totals[item]) is not str:
                totals[item] = "${:,.2f}".format(totals[item]) 
                
        totals = tuple(totals)
        cash_row = ("Cash", '', '', "${:,.2f}".format(cash),'', '',  '', '','')
        space_row = tuple(['' for i in range(9)])
        
        for item in ["market", "total_value", "wap", "upl", "rpl"]:
            final_df[item] = final_df[item].map('${:,.2f}'.format)
        for item in ['value_weight', 'share_weight']:
            final_df[item] = (final_df[item]*100).map('{:,.0f}%'.format)
            
        rows = len(final_df)
        
        final_df.loc[rows] = cash_row
        final_df.loc[rows + 1] = space_row
        final_df.loc[rows + 2] = totals
            
        cols = ['Currency', "Position", "Market Price", "Total Value", 'Value Weight', 'Share Weight',
                "WAP", "UPL", "RPL"]
        
        
        final_df.columns = cols
        self.pl_view = final_df

class UserDB:
    def __init__(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://cuny:data@ds153958.mlab.com:53958/currency-app', connectTimeoutMS = 50000)
        self.db = client.get_database('currency-app')
        if self.db.pl.count() > 0:
            self.new_account = 0
        else:
            self.new_account = 1
        
        
    def pl_insert(self, df, ticker):
        item = df.loc[ticker].to_dict()
        self.db.pl.insert_one({ticker: item})
        
    def pl_update(self, df, ticker):
        item = df.loc[ticker].to_dict()
        self.db.pl.update_one({ticker : {'$exists' : True}}, {'$set': {ticker : item}})

    def blotter_insert(self, date, row):
         from datetime import datetime
         keys = [ "cash_balance", "currency", "net", "price",
                                 "shares", "tran_type", 'date']
         vals = list(row)
         since_date = datetime(1970, 1, 1, 0, 0, 0)
         seconds = (date - since_date).total_seconds()
         vals.append(seconds)
         doc = dict(zip(keys, vals))
         self.db.blotter.insert_one(doc)
        