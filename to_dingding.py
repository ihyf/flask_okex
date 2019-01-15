# coding:utf-8
import time
import requests
import json
import asyncio
import time
from model.contract_okex import ContractOkEx
from view.manager import get_data
from utils.tools import auto_send_dingding


def get_more_than_five():
    # 获取instrument_id
    url1 = "https://www.okex.me/api/futures/v3/instruments"
    r1 = requests.get(url1)
    data1 = json.loads(r1.content.decode())
    instrument_id_list = [d["instrument_id"] for d in data1]
    
    url = []
    for instrument_id in instrument_id_list:
        url2 = f"https://www.okex.me/api/futures/v3/instruments/{instrument_id}/mark_price"
        url.append(url2)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [get_data(u) for u in url]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    show_list = []
    num = 5.5
    for i in range(int(len(results) / 3)):
        contract = ContractOkEx(None, None, None, None, None, None, None, None, None)
        contract.this_week_name = results[3 * i]["instrument_id"]
        contract.this_week_price = results[3 * i]["mark_price"]
        contract.next_week_name = results[3 * i + 1]["instrument_id"]
        contract.next_week_price = results[3 * i + 1]["mark_price"]
        contract.this_quarter_name = results[3 * i + 2]["instrument_id"]
        contract.this_quarter_price = results[3 * i + 2]["mark_price"]
        contract.this_week_vs_next_week = round((contract.this_week_price / contract.next_week_price) * 100 - 100, 2)
        contract.this_week_vs_quarter = round((contract.this_week_price / contract.this_quarter_price) * 100 - 100, 2)
        
        contract.next_week_vs_quarter = round((contract.next_week_price / contract.this_quarter_price) * 100 - 100, 2)
        if contract.this_week_vs_quarter > num or contract.next_week_vs_quarter > 5.5:
            # to_dingding
            robot_id = "f2ab17f31719b093d80754a95524a5b37d38eec507d36ef4b51e708206ea4feb"
            send_content = (str(contract.this_week_name) + " 当周 VS 季度 现为:" + str(contract.this_week_vs_quarter) + "%")
            auto_send_dingding(send_content=send_content, robot_id=robot_id)
        show_list.append(contract)
    return


if __name__ == "__main__":
    while True:
        get_more_than_five()
        time.sleep(5)
