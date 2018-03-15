# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 20:10:09 2018

@author: pgood
"""

def exit_app():
    import sys
    print("Thank you for trading!")
    sys.exit()

#These seemed to be the 3 logical components of the user interface, and therefore have a function for each.
#A case could be made for splitting the trading menu up into one function for each parameter: (stock,shares,
#(stock,transaction type, shares)

def main_menu():
    print("Main Menu\n")
    print("\t1. Trade\n")
    print("\t2. Show Blotter\n")
    print("\t3. Show P/L\n")
    print("\t9. Quit\n")
    menu1 = input("Make your selection: ")
    return menu1

def trading_menu():
    import os
    import time
    from get_currency_info import get_charts, get_current
    answer = ''
    while True:
        os.system('clear')
        print("Trading Menu\n")
        print('Enter "cancel" at any time to return to main menun\n')
        print('Enter "quit" to leave the app\n\n')
        security = input("Enter the ticker of the security you would like to trade: ")
        security = security.lower()
        if security == "cancel":
            return
        elif security == "quit":
            exit_app()
        try:
            get_charts(security)
        except ValueError:
            print("Currency {} not found.\n Please choose a valid ticker".format(security))
            continue
        trade_map = dict(zip([str(num) for num in range(1,5)], ["buy", "sell", "short", "cover"]))
        while True:
            os.system("clear")
            print("**{0} Trade**".format(security.upper()))
            print("Choose the trade type\n")
            print("1. Buy\n")
            print("2. Sell\n")
            print("3. Short Sell\n")
            print("4. Cover Short\n")
            answer = input("Enter the trade type: ")
            answer = answer.lower()
            if answer == "cancel":
                return
            elif answer == "quit":
                exit_app()
            if answer not in [str(num) for num in range(1,5)]:
                print("Please choose a valid entry(1-4)")
                time.sleep(4)
                continue
            trade_type = trade_map[answer]
            break
        
        
        while True:
            os.system("clear")
            #print("**{0} Trade**\n".format(security.upper()))
            answer = input("How many shares would you like to trade? ")
            if answer == "cancel":
                return
            elif answer == "quit":
                exit_app()
            try:#The answer could be a float, character, or negative number (well as a string)
                #Each type must be accounted for.
                quant = int(answer)
                if int(quant) == float(quant) and int(quant) > 0:
                    return (security, trade_type, quant)
                else:
                    print("Please choose an whole number greater than 0")
                    time.sleep(4)
                    continue                    
            except ValueError:
                print("Please choose an whole number greater than 0")
                time.sleep(4)
                continue
        os.system('clear')
            
        

def execute_trade(security, trade_type, quant, user_transactions):
    import os
    import time
    from get_currency_info import get_current
    os.system('clear')
    price = get_current(security, trade_type)
    print("**{0} Trade**".format(security.upper()))
    print("\nThe current price of {} is ${:,.2f}".format(security.upper(), price))
    choice = input("Confirm trade (Y/N): ")#No room for abuse here.  The user can enter whatever
                                            #they want to cancel the trade
    if choice.lower() == "y":
        user_transactions.evalTransaction(trade_type, quant, get_current(security, trade_type), security)
        return
    else:
        print("Trade cancelled")
        time.sleep(4)
        return
    


