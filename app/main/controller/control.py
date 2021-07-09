
from flask import Flask, flash, request, redirect, url_for, render_template, current_app
import pymongo
from app import app

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
    return render_template('index.html', cache_timeout=0,
                          price_stocks = price_stocks)
