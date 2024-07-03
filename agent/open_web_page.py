import requests
import json


def Call_Open_Web_Page_API(slot, scene_name, user_input, access_token):
    return query_data_with_keyword(user_input, access_token)


# 根据关键词查询数据
def query_data_with_keyword(keyword, access_token_str):
    url = 'https://mg.hc-yun.com/voice/api/voice/assistant-iflyos-test'
    # 定义请求头，包含 access_token
    headers = {
        'Cookie': access_token_str
    }

    # 定义查询参数
    params = {
        'keyword': keyword,
        'deviceId': 15668300705
    }

    # 发送 GET 请求，携带请求头和查询参数
    response = requests.get(url, headers=headers, params=params)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的数据，这里假设返回的是 JSON 格式
        data = response.json()
        print(data)
        return data['result']
    else:
        print('Failed to retrieve data:', response.status_code)
    return ''
