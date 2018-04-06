# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 13:21:03 2018

@author: pgood
"""

from flask import Flask, render_template, request, jsonify, make_response, send_file, Markup

from user_accountv2 import User, Blotter, PL, UserDB
my_db = UserDB()
account = User(my_db)
my_pl = PL(account, my_db)
my_blotter = Blotter(account, my_db)

app = Flask(__name__)
 
@app.route("/")
def index():
    currency = request.args.get('cur')
    wipe = request.args.get('wipe')
    if currency != None:
        account.change_currency(currency)
    if wipe == 'yes':
        account.wipe_account(my_db, my_blotter, my_pl)
    return render_template('landing.html')

@app.route("/blotter")
def blotter():
    my_blotter.showBlotter(account)
    if my_blotter.blotter_rows < 1:
        html = "You haven't made any transactions yet!"
    else:
        html = my_blotter.blotter_view.to_html(index = False)
    return render_template('blotter.html', table = html)
    

@app.route("/pl")
def pl():
    my_pl.showPL(account)
    return render_template('pl.html', table = my_pl.pl_view.to_html(index = False))

@app.route("/trade")
def trade():
    return render_template('trade.html')

@app.route('/stats', methods = ['POST'])
def show_stats():
    from get_currency_info import get_24, find_actives
    ticker =  request.form['ticker']
    if ticker.upper() in find_actives():
        stdev, min, max, mean = get_24(ticker)
        return jsonify(stdev=stdev, mean=mean, min=min, max=max)
    else:
        return jsonify(stdev = 'Ticker not found', mean = '', min = '', max = '')

@app.route('/graph')
def show_graph():
    from plotly.offline import plot
    from get_currency_info import make_chart, find_actives
    ticker = request.args.get('ticker')
    if ticker != None:
        if ticker.upper() in find_actives():
            data = make_chart(ticker)
            my_plot = plot(data, output_type="div", show_link=False)
        else:
            my_plot = 'Ticker not found'
    else:
        my_plot = 'Ticker not found'
    return render_template('graph.html', my_plot = my_plot)


@app.route ('/preview', methods = ['POST'])
def preview_trade():
    from get_currency_info import get_current, find_actives
    ticker = request.form['ticker']
    trade_type = request.form['type']
    shares = request.form['shares']
    if ticker.upper() in find_actives():
        cur = get_current(ticker, trade_type)
        cur_format = "${:,.2f}".format(cur)
        tot = cur * float(shares)
        tot_format = "${:,.2f}".format(tot)
        return (jsonify(current = cur_format, total = tot_format))
    else:
        return jsonify(current = 'Ticker not found', total = '')

@app.route('/execute', methods = ['POST'])
def executeTrade():
    from get_currency_info import get_current, find_actives
    ticker = request.form['ticker'].upper()
    trade_type = request.form['type']
    shares = float(request.form['shares'])
    if ticker in find_actives():
        price = get_current(ticker, trade_type)
        account.evalTransaction(trade_type, shares, price, ticker, my_db, my_pl, my_blotter)
        if account.message == 'Success':
            return(jsonify(message = 'Order Success! {}@${:,.2f}'.format(ticker, price)))
        else: 
            return(jsonify(message = account.message))
    else:
        return(jsonify(message = 'Ticker not found'))
        

        
if __name__ == "__main__":
    app.run(host = '0.0.0.0')
    
