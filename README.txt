Crypto Trader
===========

This app allows the user to trade cryptocurrencies in a simulated portfolio at prices from the https://bittrex.com/ cryptocurrency exchange.  Prices are retrieved using Bittrex’s REST API.  The user begins with 100 million in USD and is free to trade any currency on the market.  The user can view price statistics and a 100-day price history chart of any given currency before making trade decisions, allowing them to practice their analysis skills.  

Requirements
============
Python 3.x with pandas, numpy, pymongo, plotly, and Flask.  Because this is a web app, the user must be able to access the IP address of the machine running the app from a web browser.

Setup
=====

Once the requirements are met, the user should clone the repository, and execute the flask_app.py file.

Alternative option:
Dockerhub link: https://hub.docker.com/r/pgoodridge/data602-assignment2/

Usage
=====

This is a web app, so it must be run from a browser.  The landing page links to three screens, the trading menu, blotter, and P/L.  The trading menu is the only screen of these three that requires user input.  The user must choose proper options for their trade before the trade can be executed.  Trade quantities must be in denominations greater than 1/100,000,000.  It should also be noted that the user cannot hold simultaneous short and long positions in a given security.
The landing page gives the user two options that affect their experience:
1.	Resetting their portfolio using the “Wipe Account” button.  The portfolio will persist between sessions, so the user may choose to do this if their positions are performing badly and they would like to attempt a new strategy.
2.	Choosing a different base currency for display in the P/L and blotter.  All transactions will still be recorded in USD behind the scenes

**Definitions**

Value Weight: This is calculated each time the user views their P/L.  It is equal to:
(Market Value of position/Total market value invested) *100
(note: the total market value does not include holdings in USD)

Share Weight: Short positions are counted as positive for this calc.  This is equal to:
Total shares in position/Total shares in portfolio
WAP (Weighted Average Price): This is recalculated with every buy or short sale.  It is equal to:
(Shares Owned * Previous WAP + Shares Purchased * Price)/Total Shares

RPL (Realized Profit or Loss): This is calculated with every sell or cover transaction.  It is equal to:
Previous RPL + Gain/Loss on transaction

UPL (Unrealized Profit or Loss): This is calculated each time the P/L is viewed.  It is equal to:
Market value * position - WAP * Position

Total PL: This is calculated each time the P/L is viewed.  It is equal to:
UPL + RPL
