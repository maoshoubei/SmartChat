# encoding=utf-8
import json
import random
import time

from models.chatbot_model import ChatbotModel
from utils.helpers import load_all_scene_configs
from flask import Flask, request, jsonify, send_file
from utils import logger

import os
import sys
import certifi
import requests

from fastapi import FastAPI

app = Flask(__name__)

# 创建一个可变长度的数组 用来存放字符串
response_array = []
# 实例化ChatbotModel
#chatbot_model = ChatbotModel(load_all_scene_configs('9527'))
#
#os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

# 创建一个 根据chatId 映射 ChatbotModel对象的映射表
chatbot_model_map = {}

#print(certifi.where())


def getRandom(randomlength=12):
    """
    生成一个指定长度的随机字符串
    """
    digits = '0123456789'
    ascii_letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


@app.route('/function', methods=['POST'])
def function():
    global chatbot_model
    json_data = request.get_data()
    data = json.loads(json_data)

    chatId = data.get('chatId')

    data = data["data"]
    question = data.get('question')
    AI_history = data.get('history')
    access_token = request.headers.get('Cookie')
    # 如果chatId 为空则表示是第一次对话 需要新建一个chatId
    if not chatId:
        chatId = getRandom()
        chatbot_model = ChatbotModel(load_all_scene_configs(chatId))
        chatbot_model_map[chatId] = chatbot_model
    else:
        chatbot_model = chatbot_model_map[chatId]
    # 实例化ChatbotModel
    #chatbot_model = ChatbotModel(load_all_scene_configs(chatId))

    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question, AI_history[-1]['value'] if AI_history else "", chatId, access_token)

    if response == question:
        return jsonify({"no_function": True, "question": question, "chatId": chatId})
    else:
        return jsonify({"use_function": True, "answer": response, "chatId": chatId})


if __name__ == '__main__':
    app.run(host='192.168.10.105', port=7000)


def user_input():
    while True:
        question = input("请输入您的问题：")

        if not question:
            print(jsonify({"error": "No question provided"}))
            break

        # 判断response_array 是否为空 ，不为空则取出response_array[0] 否则取一个空字符串
        if len(response_array) == 0:
            responseHistory = ''
        else:
            responseHistory = response_array[0]

        response = chatbot_model.process_multi_question(question, responseHistory, '9527')
        response_array.append(response)
        print(response)

# user_input()
