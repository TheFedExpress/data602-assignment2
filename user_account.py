# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:53:12 2018

@author: pgood
"""

class UserAccount:
    
    def __init__(self, starting = 100000000):
        import pandas as pd
        start = {"cash": {"position": 0, "market": 100000000.0, "wap" : 0.0, "rpl": 0.0, "upl": 0.0, "total_pl": 0.0,
                                       "allocation_by_shares": 0.0, "allocation_by_dollars": 100.0}}
        self.pl = pd.DataFrame.from_dict(start, orient = 'index')        
        self.transaction_log = []
    
    def __len__(self):
        return len(self.transaction_log)
    
    def __getitem__(self, position):
        return self.transaction_log[position]
    
    #For fungible shares, it doesn't make sense to allow for simultaneous short and long positions
    #This would also require two lines on the P/L, causing confusion
    def evalTransaction(self, tran_type, shares, price, ticker):
       from datetime import datetime
       from get_currency_info import get_current
       import pandas as pd
       import time
       cash = self.pl.loc['cash', 'market']
       try:
            prev_shares = self.pl.loc[ticker, "shares"]
            new = 0
       except KeyError:
            new = 1
            prev_shares = 0
       total = shares * price     
       if tran_type in ["buy", "cover"]:
            #User abuse/misuse prevention
            if tran_type == "buy":
                margin = 0
                for security in self.pl.index:
                    if self.pl.loc[security, "position"] < 0:
                        margin += self.pl.loc[security, "position"] * get_current(security, "buy") * -1

            if tran_type == "cover" and prev_shares >= 0:
                    print("\nYou do not have any short sales with this security")
                    time.sleep(4)#This will allow the user to see the Error reason before the
                                #screen is cleared
            elif tran_type == "cover" and shares + prev_shares > 0:
                message = "\nYou have attempted to cover {} shares.  Please cover {} shares or less"
                print(message.format(shares, -prev_shares))
                time.sleep(4)
                
            elif tran_type == "buy" and cash <= margin * 2 + shares * price:
                message = "\nThis transaction requires ${:,.2f} in your account.  You have ${:,.2f}."
                print(message.format(margin * 2 + shares * price, cash))
                time.sleep(4)
                
            elif tran_type == "buy" and prev_shares < 0:
                message = "\nYou currently have {} shares of {} shorted.  Please cover those before buying."
                print(message.format(prev_shares*-1, ticker))
                time.sleep(4)
                
            else:#Process transaction
                if new == 0:
                    self.pl.loc['cash', 'market'] -= total
                    new_shares = prev_shares + shares
                    if tran_type == "buy":
                        if self.pl.loc[ticker, "position"] == 0:
                            self.pl.loc[ticker, "wap"] = price#running totals much easier
                
                        else:
                            prev_value = prev_shares * self.pl.loc[ticker, "wap"]
                            self.pl.loc[ticker, "wap"] = (prev_value + shares * price)/new_shares
                            
                    else:#Cover
                        gain = self.pl.loc[ticker, "wap"] * shares - total
                        self.pl.loc[ticker, "rpl"]  = self.pl.loc[ticker, "rpl"] + gain
                    self.pl.loc[ticker, "position"] = new_shares
                    
                    if new_shares == 0:#for aesthetics in the P&L
                        self.pl.loc[ticker, "wap"] = 0
                        
                    date = datetime.now ()
                    trans = {"tran_type" : tran_type, "stock": ticker, "shares": shares, "price": price,
                             "net": -total, "timestamp" : date}
                    self.transaction_log.append(trans)
                    message = "\nYou have made a {} of {} shares of {} at {:,.2f}"
                    print(message.format(tran_type, shares, ticker.upper(), price))
                    time.sleep(4)
                else:
                    self.pl.loc['cash', 'market'] -= total
                    self.pl.loc[ticker, ['position', 'market', 'wap', 'rpl', 'upl', 'total_pl', 
                                         'allocation_by_dollars', 'allocation_by_shares']] = (shares, 0, price, 0, 0, shares*price, 0, 0)
                
       else:#sell/short      
            #simplified margin system only based on cash
            #no margin calls either
            #I could have used the dataframe calcs from the showPL method to calculate total equity, but
            #that requires getting the market price from the whole portfolio, and that would slow down
            #the app
            if tran_type == "short":
                margin = 0
                for security in self.pl.index:
                    if self.pl.loc[security, "position"] < 0:
                        margin += self.pl.loc[security, "position"] * get_current(security, "buy") * -1
                                 
            if tran_type == "sell" and prev_shares < 0:
                print("\nInvalid transaction")
                print("You have a short position in {} of {} shares".format(ticker, prev_shares*-1))
                time.sleep(4)
                
            elif tran_type == "sell" and prev_shares < shares:
                print("\nYou have {} shares of {} in you account".format(prev_shares, ticker))
                print("Please choose a different quantity to sell")
                time.sleep(4)
                
            elif tran_type == "short" and prev_shares > 0:
                print("\nInvalid transaction")
                message = "You have a long position in {} of {} shares.  Please sell before shorting"
                print(message.format(ticker, prev_shares))
                time.sleep(4)
                
            elif tran_type == "short" and cash <= (margin * 2 + shares * price):
                print("\nYou must meet the margin requirement of 200%")
                message = "This transaction requires ${:,.2f} in your account.  You have ${:,.2f}."
                print(message.format((margin * 2 + shares * price), cash))
                time.sleep(4)
            else:
               self.pl.loc['cash', 'market'] = total + cash
               if new == 0:
               #process transaction
                   new_shares = self.positions.loc[security,'shares'] - shares
                   total = shares * price
                   
                   if tran_type == "sell":
                       
                       gain = total -  self.pl.loc[ticker, 'wap'] * shares
                       self.pl.loc[ticker, 'rpl']  = self.positions[ticker]["rpl"] + gain
                       
                   else:#short
                       self.pl.loc['cash', 'market'] = total + cash
                       if self.pl.loc[ticker, 'shares'] == 0:
                           self.pl.loc[ticker, "wap"] = price
                           
                       else:
                           prev_value = prev_shares * self.pl.loc[ticker, "wap"]*-1
                           self.pl.loc[ticker, "wap"] = (prev_value + shares * price)/new_shares*-1
                           
                   self.pl.loc[ticker, "shares"] = new_shares
                   if new_shares == 0:
                       self.pl.loc[ticker, "wap"] = 0
     
                   

                   date = datetime.now ()
                   trans = {"tran_type" : tran_type, "stock": ticker, "shares": shares, "price": price,
                            "net": total,  "timestamp" : date}
                   self.transaction_log.append(trans)
                   
                   message = "You have made a {} of {} shares of {} at {:,.2f}"
                   print(message.format(tran_type, shares, ticker.upper(), price))
                   time.sleep(4)
               else:
                   self.pl.loc['cash', 'market'] = total + cash
                   self.pl.loc[ticker, ['position', 'market', 'wap', 'rpl', 'upl', 'total_pl', 
                     'allocation_by_dollars', 'allocation_by_shares']] = (-shares, 0, price, 0, 0, -shares*price, 0, 0)
    


                
    def showBlotter(self):
        import pandas as pd
        from prettytable import PrettyTable
        import time
        import os
        from menu import exit_app
        
        os.system('clear')
        
        if len(self.transaction_log) == 0:
            print("You haven't made any transactions with us.")
            time.sleep(4)
        else:
            df = pd.DataFrame(self.transaction_log)
            df["price"] = df["price"].map('${:,.2f}'.format)
            df["net"] = df["net"].map('${:,.2f}'.format)
            df["timestamp"] = df["timestamp"].map('{:%Y-%m-%d %H:%M}'.format)
            
            final_df = df[["stock", "price", "shares", "tran_type", "net", "timestamp"]]
            labels = ["Stock", "Price", "Shares Traded", "Transaction Type",
                      "Net Cash Flow", "Timestamp"]
            
            table = PrettyTable()
            
            table.field_names = (labels)
            for row in final_df.itertuples():
                table.add_row(row[1:])

            
            print(table)
            while True:
                answer = input("Enter 9 to return to main menu: ")
                if answer == "9":
                    break
                elif answer.lower() == "quit":
                    exit_app()

           
    def showPL(self):
        import pandas as pd
        import numpy as np
        from get_currency_info import get_current
        from menu import exit_app
        from prettytable import PrettyTable
        import os
        
        os.system('clear')
        
        df = self.pl[self.pl.index != 'cash']
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
        
        final_df = df[["position", "market", "total_value", 'value_weight', 'share_weight', "wap", "upl", 
                       "rpl"]]
        
        #total row
        val = cash + np.sum(final_df["total_value"])
        totals = ['Total', '', '',  val,'', '', '', np.sum(final_df["upl"]), np.sum(final_df["rpl"])]
        for item in range(len(totals)):
            if type(totals[item]) is not str:
                totals[item] = "${:,.2f}".format(totals[item]) 
                
        totals = tuple(totals)
        
        for item in ["market", "total_value", "wap", "upl", "rpl"]:
            final_df[item] = final_df[item].map('${:,.2f}'.format)
            
        #Final printing table
        table = PrettyTable()
        
        cols = ["Currency", "Position", "Market Price","Total Value",'Value Weight', 'Share Weight',
                "WAP", "UPL", "RPL"]       
        
        table.field_names = (cols)
        for row in final_df.itertuples():
            table.add_row(row)
            
        table.add_row(('', '', '', '', '','', '', '', ''))
        table.add_row(("Cash", '', '', "${:,.2f}".format(cash),'', '',  '', '',''))
        table.add_row(('', '', '', '', '','', '', '', ''))
        table.add_row((totals))
        print(table)
        
        while True:
            answer = input("Enter 9 to return to main menu: ")
            if answer == "9":
                break
            elif answer.lower() == "quit":
                exit_app()

        
