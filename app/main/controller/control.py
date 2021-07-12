import os
from flask import Flask, send_file, render_template
import pymongo
from app import app
from datetime import date
import csv
import re
'''
Đầu vào: Dữ liệu các mã cổ phiếu.
Đầu ra: Các file excell được download trực tiếp từ website ứng với từng mã"
'''
myclient = pymongo.MongoClient("mongodb+srv://ducthangbnn:Oivung1215@cluster0.1rpru.mongodb.net/test", connect=False)
mydb = myclient["stocks"]
mycol = mydb["price_9h_30"]


@app.route('/', methods=['GET', 'POST'])
def table():
    price_stocks = mycol.find().sort("date", -1)
    text_all = re.compile('.*?')
    if os.path.exists(r'app\\EMA20_B30_{0}.csv'.format(text_all)):
        os.remove(r'app\\EMA20_B30_{0}.csv'.format(text_all))

    rows = [['symbol','date','time', 'price','holding','change']]


    for price_stock in price_stocks:
        row = [price_stock['code'], price_stock['date'], price_stock['time'], price_stock['price'], price_stock['volume'], price_stock['up_or_down']]
        rows.append(row)

    with open(r'app\\EMA20_B30_{0}.csv'.format(str(date.today()).replace('-',"")), 'a', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerows(rows)
    price_stocks = mycol.find().sort("date", -1)
    return render_template('index.html', cache_timeout=0,
                          price_stocks = price_stocks)

@app.route('/download_file', methods = ['GET', 'POST'])
def download_file():
    path = r'EMA20_B30_{0}.csv'.format(str(date.today()).replace('-',""))
    return send_file(path, as_attachment=True, cache_timeout=0)
