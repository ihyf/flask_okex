import json
import requests


# 钉钉自动发送
def auto_send_dingding(send_content, profit_ratio="", robot_id=""):
    try:
        msg = {
            "msgtype": "text",
            "text": {
                "content": send_content
            }
        }
        Headers = {"Content-Type": "application/json; charset=utf-8"}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id
        body = json.dumps(msg)
        requests.post(url, data=body, headers=Headers)
    except Exception as err:
        pass
