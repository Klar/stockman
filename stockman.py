#!/usr/bin/python
# -*- coding: utf-8 -*-

# wget https://bootstrap.pypa.io/get-pip.py
# sudo python2.7 get-pip.py

# pip install yahoo-finance

import urllib
from yahoo_finance import Share
import sqlite3
import sys
import os
import traceback

# variables
db_name = "stockman.db"

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'


#=======================
# generate and insert ##
#=======================
def generate_db():
    #remove file if exists
    if os.path.isfile(db_name):
        os.remove(db_name)

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    #create stockprices table
    cur.execute("CREATE TABLE stockprices(id INTEGER PRIMARY KEY AUTOINCREMENT, fk_stock_id INTEGER, price_date INTEGER, price REAL);")

    #create stocks table
    cur.execute("CREATE TABLE stocks(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, buying_price REAL, should_sellPrice INTEGER);")

    #stock insert with buying / selling price
    cur.execute('INSERT INTO stocks (name, buying_price, should_sellPrice) VALUES ("NKE",30,60);')
    cur.execute('INSERT INTO stocks (name, buying_price, should_sellPrice) VALUES ("TSLA",150,250);')
    cur.execute('INSERT INTO stocks (name, buying_price, should_sellPrice) VALUES ("YHOO",25,50);')
    cur.execute('INSERT INTO stocks (name, buying_price, should_sellPrice) VALUES ("NOK",5,10);')

    con.commit()

    con.close()
    print "Tables + Records created successfully";

    if not os.path.exists("stocks"):
        os.makedirs("stocks")


def read_stocks():
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("SELECT id, name, buying_price, should_sellPrice FROM stocks;")

    stocks = cur.fetchall()

    con.commit()
    con.close()

    return stocks


def insert_stockprices(stockprices):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.executemany("INSERT INTO stockprices(fk_stock_id, price_date, price) VALUES (?, ?, ?)", stockprices)

    con.commit()
    con.close()


def read(stocks):

    stockprices = []

    print "Grabbing Stock information + Graphs"

    for fk_stock_id, name, buying_price, should_sellPrice in stocks:

        stocktuple = ()
        #grabs graph image
        stock_png = "http://stockcharts.com/c-sc/sc?s=%s&p=D&yr=1&mn=0&dy=0&i=p40921996910&r=1462822387848.png" % name
        urllib.urlretrieve(stock_png,"stocks/" + name + ".png")

        current_price = float(Share(name).get_price())	# current buy price
        price_date = Share(name).get_trade_datetime()
        if current_price >= should_sellPrice:
            print "We should sell / buy: %s for %f" % (name, current_price)

        stocktuple = (fk_stock_id,price_date,current_price)
        stockprices.append(stocktuple)

    # print stockprices
    print "Inserting current Price into DB"

    insert_stockprices(stockprices)

    print "Successful"

try:
  generate_db()
  stocks_name = read_stocks()
  read(stocks_name)

except Exception, e:
    print e
    print "\n\n"+traceback.format_exc()+"\n"

# info
    # get_price()
    # get_change()
    # get_volume()
    # get_prev_close()
    # get_open()
    # get_avg_daily_volume()
    # get_stock_exchange()
    # get_market_cap()
    # get_book_value()
    # get_ebitda()
    # get_dividend_share()
    # get_dividend_yield()
    # get_earnings_share()
    # get_days_high()
    # get_days_low()
    # get_year_high()
    # get_year_low()
    # get_50day_moving_avg()
    # get_200day_moving_avg()
    # get_price_earnings_ratio()
    # get_price_earnings_growth_ratio()
    # get_price_sales()
    # get_price_book()
    # get_short_ratio()
    # get_trade_datetime()
    # get_historical(start_date, end_date)
    # get_info()
    # refresh()