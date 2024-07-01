# encoding=utf-8
import json
from models.chatbot_model import ChatbotModel
from utils.helpers import load_all_scene_configs
from flask import Flask, request, jsonify, send_file
from utils import logger

import os
import sys

app = Flask(__name__)

# 创建一个可变长度的数组 用来存放字符串
response_array = []
# 实例化ChatbotModel
chatbot_model = ChatbotModel(load_all_scene_configs('9527'))

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')


@app.route('/function', methods=['POST'])
def function():
    json_data = request.get_data()
    data = json.loads(json_data)

    chatId = data.get('chatId')

    data = data["data"]
    question = data.get('question')
    AI_history = data.get('history')

    # 实例化ChatbotModel
    #chatbot_model = ChatbotModel(load_all_scene_configs(chatId))

    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question, AI_history[-1]['value'] if AI_history else "", chatId)

    if response == question:
        return jsonify({"no_function": True, "question": question})
    else:
        return jsonify({"use_function": True, "answer": response})


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
