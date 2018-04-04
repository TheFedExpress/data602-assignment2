# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 13:21:03 2018

@author: pgood
"""

from flask import Flask, render_template, request, jsonify, make_response, send_file, Markup

from user_account import UserAccount
from user_account import UserDB

db = UserDB()
account = UserAccount(db)

app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('test.html')

@app.route("/blotter")
def blotter():
    account.showBlotter()
    if account.blotter_rows < 1:
        html = "You haven't made any transactions yet!"
    else:
        html = account.blotter_view.to_html(index = False)
    return render_template('blotter.html', table = html)
    

@app.route("/pl")
def pl():
    account.showPL()
    return render_template('pl.html', table = account.pl_view.to_html(index = False))

@app.route("/trade")
def trade():
    return render_template('trade.html')

@app.route('/stats', methods = ['POST'])
def show_stats():
    from get_currency_info import get_24 
    ticker =  request.form['ticker']
    mean, min, max, stdev = get_24(ticker)
    return jsonify(mean=mean, min=min, max=max, stdev=stdev)

@app.route('/graph', methods = ['POST'])
def show_graph():
    from plotly.offline import plot
    from get_currency_info import make_chart
    ticker = request.form['ticker'] 
    data = make_chart(ticker)
    plot(data, filename='file.html')
    return ''


@app.route ('/preview', methods = ['POST'])
def preview_trade():
    from get_currency_info import get_current
    ticker = request.form['ticker']
    trade_type = request.form['type']
    shares = request.form['shares']
    
    cur = get_current(ticker, trade_type)
    cur_format = "${:,.2f}".format(cur)
            
    try:
        tot = cur * float(shares)
        tot_format = "${:,.2f}".format(tot)
        return (jsonify(current = cur_format, total = tot_format))
    except ValueError:
        pass

@app.route('/execute', methods = ['POST'])
def executeTrade():
    from get_currency_info import get_current
    ticker = request.form['ticker'].upper()
    trade_type = request.form['type']
    shares = float(request.form['shares'])
    price = get_current(ticker, trade_type)
    account.evalTransaction(trade_type, shares, price, ticker, db)
    if account.message == 'Success':
        return(jsonify(message = 'Order Success! {}@${:,.2f}'.format(ticker, price)))
    else: 
        return(jsonify(message = account.message))
        

        
if __name__ == "__main__":
    app.run(host = '0.0.0.0')
    
