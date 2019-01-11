# coding:utf-8
from create_app import app
from flask import render_template,jsonify
import requests
import json


@app.route("/")
def index():
    # 获取instrument_id
    url1 = "https://www.okex.me/api/futures/v3/instruments"
    r1 = requests.get(url1)
    data1 = json.loads(r1.content.decode())
    instrument_id_list = [d["instrument_id"]for d in data1]
    # 获取价格
    data_list = []
    for instrument_id in instrument_id_list:
        data = {}
        url2 = f"https://www.okex.me/api/futures/v3/instruments/{instrument_id}/mark_price"
        r2 = requests.get(url2)
        data2 = json.loads(r2.content.decode())
        data["instrument_id"] = data2["instrument_id"]
        data["mark_price"] = data2["mark_price"]
        data_list.append(data)
        
    show_list = []
    for i in range(int(len(data_list)/3)):
        l = []
        l.append(data_list[3*i]["instrument_id"])
        l.append(data_list[3*i]["mark_price"])
        l.append(data_list[3*i+1]["instrument_id"])
        l.append(data_list[3*i+1]["mark_price"])
        l.append(data_list[3*i+2]["instrument_id"])
        l.append(data_list[3*i+2]["mark_price"])
        l.append("当周 vs 次周")
        l.append(round((data_list[3*i]["mark_price"]/data_list[3*i+1]["mark_price"])*100-100, 2))
        l.append("当周 vs 季度")
        l.append(round((data_list[3*i]["mark_price"] / data_list[3 * i + 2]["mark_price"]) * 100 - 100, 2))
        l.append("次周 vs 季度")
        l.append(round((data_list[3 * i+1]["mark_price"] / data_list[3 * i + 2]["mark_price"]) * 100 - 100, 2))
        
        show_list.append(l)
    print(show_list)
    
    return render_template("index.html", show_list=show_list)

