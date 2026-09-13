import requests
import json
def send_to_wechat(token,title,content):
    url = "https://www.pushplus.plus/send"
    payload = json.dumps({
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, data=payload, headers=headers,timeout=10)
    try:
        if response.status_code != 200:
            return {"code":-1,"msg":f"请求失败,状态码为{response.status_code}"}
        result_json=response.json()
        return result_json
    except Exception as e:
        return {"code": -999, "msg": f"网络连接异常: {e}"}