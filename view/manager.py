# coding:utf-8
import operator
import requests
import json
import time
import asyncio
import aiohttp
from create_app import app
from flask import render_template
from model.contract_okex import ContractOkEx


sema = asyncio.Semaphore(3)
event_loop = asyncio.get_event_loop()


async def get_data(url):
    async with aiohttp.request('GET', url) as r:
        data = await r.json()
    return data


# async def main():
#     # 获取instrument_id
#     time1 = time.time()
#     url1 = "https://www.okex.me/api/futures/v3/instruments"
#     r1 = requests.get(url1)
#     data1 = json.loads(r1.content.decode())
#     print(time.time() - time1)
#     instrument_id_list = [d["instrument_id"] for d in data1]
#
#     url = []
#     for instrument_id in instrument_id_list:
#         url2 = f"https://www.okex.me/api/futures/v3/instruments/{instrument_id}/mark_price"
#         url.append(url2)
#     # print(url)
#     start = time.time()
#
#
#     tasks = [get_data(u) for u in url]
#
#     results = event_loop.run_until_complete(asyncio.gather(*tasks))
#     end = time.time()
#     print(end - start)
#     return results


@app.route("/123")
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
        time1 = time.time()
        url2 = f"https://www.okex.me/api/futures/v3/instruments/{instrument_id}/mark_price"
        r2 = requests.get(url2)
        data2 = json.loads(r2.content.decode())
        time2 = time.time()
        print(time2 - time1)
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
    
    return render_template("index.html", show_list=show_list)


@app.route("/")
def index2(*args, **kwargs):
    # 获取instrument_id
    time1 = time.time()
    url1 = "https://www.okex.me/api/futures/v3/instruments"
    r1 = requests.get(url1)
    data1 = json.loads(r1.content.decode())
    print(time.time() - time1)
    instrument_id_list = [d["instrument_id"] for d in data1]
    
    url = []
    for instrument_id in instrument_id_list:
        url2 = f"https://www.okex.me/api/futures/v3/instruments/{instrument_id}/mark_price"
        url.append(url2)
    # print(url)
    start = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [get_data(u) for u in url]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    print(results)
    end = time.time()
    print(end - start)
    show_list = []
    for i in range(int(len(results) / 3)):
        contract = ContractOkEx(None, None, None, None, None, None, None, None, None)
        contract.this_week_name = results[3 * i]["instrument_id"]
        contract.this_week_price = results[3 * i]["mark_price"]
        contract.next_week_name = results[3 * i + 1]["instrument_id"]
        contract.next_week_price = results[3 * i + 1]["mark_price"]
        contract.this_quarter_name = results[3 * i + 2]["instrument_id"]
        contract.this_quarter_price = results[3 * i + 2]["mark_price"]
        contract.this_week_vs_next_week = round((contract.this_week_price/contract.next_week_price)*100-100, 2)
        contract.this_week_vs_quarter = round((contract.this_week_price/contract.this_quarter_price)*100-100, 2)
        contract.next_week_vs_quarter = round((contract.next_week_price/contract.this_quarter_price)*100-100, 2)
        show_list.append(contract)
    
    cmp_ful = operator.attrgetter('this_week_vs_quarter')
    show_list.sort(key=cmp_ful, reverse=True)
    show_list = [contract.__dict__ for contract in show_list]
    return render_template("index_async.html", show_list=show_list)



