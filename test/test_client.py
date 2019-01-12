import requests
import json
import aiohttp
import asyncio


url = "http://127.0.0.1:8888/api"
headers = {"content-type": "application/json"}
p = {
    "method": "index2",
    "params": {
        "appid": 1
    },
    "jsonrpc": "2.0",
    "id": 0
}


async def get_data():
    async with aiohttp.request("POST", url=url, data=json.dumps(p), headers=headers) as r:
        data = await r.json()
        return data

event_loop = asyncio.get_event_loop()
tasks = [get_data()]
results = event_loop.run_until_complete(asyncio.gather(*tasks))
print(results)

