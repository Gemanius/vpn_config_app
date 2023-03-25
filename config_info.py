import requests
from math import floor
import json
import base64
from datetime import datetime

server_urls = [
    {"url": "https://46.246.96.86:13713/xui/inbound/list", "cookie": "MTY3NzMxNzA1MHxEdi1CQkFFQ180SUFBUkFCRUFBQVpmLUNBQUVHYzNSeWFXNW5EQXdBQ2t4UFIwbE9YMVZUUlZJWWVDMTFhUzlrWVhSaFltRnpaUzl0YjJSbGJDNVZjMlZ5XzRNREFRRUVWWE5sY2dIX2hBQUJBd0VDU1dRQkJBQUJDRlZ6WlhKdVlXMWxBUXdBQVFoUVlYTnpkMjl5WkFFTUFBQUFHZi1FRmdFQ0FRWnRhRzUyY0c0QkNXMW9iblp3YmpFeU13QT189nzDBo6ZUT8XQNK4z6fk36ocLFmNSljQ5gnsGsaCkog="},
    {"url": "https://193.200.16.10:13813/xui/inbound/list", "cookie": "MTY3ODU3MjUxM3xEdi1CQkFFQ180SUFBUkFCRUFBQVpmLUNBQUVHYzNSeWFXNW5EQXdBQ2t4UFIwbE9YMVZUUlZJWWVDMTFhUzlrWVhSaFltRnpaUzl0YjJSbGJDNVZjMlZ5XzRNREFRRUVWWE5sY2dIX2hBQUJBd0VDU1dRQkJBQUJDRlZ6WlhKdVlXMWxBUXdBQVFoUVlYTnpkMjl5WkFFTUFBQUFFXy1FRUFFQ0FRTnRhRzRCQm0xb2JqZzRPQUE9fOEwsjLVJ-ClieTYAibUIiTFl6mCsCZy-e2Bjw5IaZ3R"}
]
iran_server_mapping = [
    {
        "out_url": "https://46.246.96.86:13713/xui/inbound/list",
        "in_url": "general-stk.darkube.app"
    },
    {
        "out_url": "https://193.200.16.10:13813/xui/inbound/list",
        "in_url": "general-pld.darkube.app"
    }
]

sharing_json = {"add": "general-stk.darkube.app", "aid": "0", "alpn": "", "fp": "", "host": "", "id": "fd9482a3-4c24-4bd3-9275-fbbc13a9cef4",
                "net": "ws", "path": "/amir-eb", "port": "80", "ps": "amir ebrahimi", "scy": "auto", "sni": "", "tls": "", "type": "", "v": "2"}


def set_cookie(session):
    return {
        'session': session
    }


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


def request_to_server(server_data):
    response = requests.post(server_data["url"], cookies=set_cookie(server_data["cookie"]),
                             headers=headers, verify=False)
    return response.json()["obj"]


def find_config(name):
    selected_config = 0
    for server_data in server_urls:
        response = request_to_server(server_data)
        for config in response:
            if config["remark"] == name:
                selected_config = config, server_data["url"]
                break
        if selected_config != 0:
            break
    return selected_config


def create_response(name):
    try:
        res = find_config(name)
        if res == 0:
            return f'<h1>config is not found</h1>'
        config, server_urls = res
        expiry_time = datetime.utcfromtimestamp(
            int(config["expiryTime"]/1000)).strftime('%Y-%m-%d') if config["expiryTime"] != 0 else "unlimited"
        remained_capcity = floor(
            (config["total"]-(config["up"]+config["down"]))/1000000000)
        new_config = sharing_json
        new_config["ps"] = config["remark"]
        new_config["id"] = json.loads(config["settings"])["clients"][0]['id']
        config = json.loads(config["streamSettings"])["wsSettings"]
        new_config["path"] = config["path"]
        new_config["add"] = next(
            (data["in_url"] for data in iran_server_mapping if data["out_url"] == server_urls), None)
        encoded_config = "vmess://"+str(base64.b64encode(
            str.encode(json.dumps(new_config))))[2:-1]
        return f'<h2> config</h2><textarea style="width:250px;height:300px;">{encoded_config}</textarea><p> حجم باقی مانده </p> <p>{remained_capcity}</p><p>تا تاریخ </p><p>{expiry_time}</p>'
    except Exception as error:
        pass
