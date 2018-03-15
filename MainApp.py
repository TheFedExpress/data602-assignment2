# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:33:32 2018

@author: pgood
"""


import menu
import sys
import os
import time
from user_account import UserAccount
from flask import Flask

my_account = UserAccount()

#The different parts of the app were split into files to keep the main logic readable

while True:
    os.system('clear')
    choice = menu.main_menu()
    if choice == "1":
        try:
            security, trade_type, quant = menu.trading_menu()
        except TypeError:
            #Start the main menu again if the user cancels transaction
            continue
        else:
            menu.execute_trade(security, trade_type, quant, my_account)   
    elif choice == "2":
        my_account.showBlotter()
    elif choice == "3":
        my_account.showPL()
    elif choice.lower() in ["9", "quit"]:
        print("Thank you for trading!")
        sys.exit()
    else:
        print("Please make a valid selection (1,2,3, or 9)")
        time.sleep(4)
        continue
    