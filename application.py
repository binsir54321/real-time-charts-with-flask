import json
import logging
import random
import sys
import time
from datetime import datetime
from typing import Iterator
import requests
import openai

from flask import Flask, Response, render_template, request, stream_with_context, jsonify
from flask_cors import CORS

openai.api_key = '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'

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

application = Flask(__name__)

CORS(application)
random.seed()  # Initialize the random number generator


@application.route("/")
def index() -> str:
    return render_template("index.html")


def generate_random_data() -> Iterator[str]:
    """
    Generates random value between 0 and 100

    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        while True:
            json_data = "111"
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)

def chat(completion):
    # data = request.get_json()
    
    for each in completion:
        if("content" in each.choices[0].delta):
            yield f"data:{each.choices[0].delta.content}\n\n"
            print(each.choices[0].delta.content)
    yield f"data:。\n\n"
    yield f"data:[DONE]\n\n"
    return jsonify({'success': True})

def nochat():
    # data = request.get_json()
    
    yield f"data:抱歉，我没有听到您说什么。\n\n"
    yield f"data:。\n\n"
    yield f"data:[DONE]\n\n"
    return jsonify({'success': True})

def zhaohu():
    # data = request.get_json()
    
    yield f"data:小朋友们好呀，很高兴见到你们，我看了你们写的童诗，你们真的好棒呀。\n\n"
    yield f"data:。\n\n"
    yield f"data:[DONE]\n\n"
    return jsonify({'success': True})

def zhidao():
    # data = request.get_json()
    
    yield f"data:我是从顾老师的公众号上了解到的，如果你不知道的话，我可以为你朗读一下。\n\n"
    yield f"data:。\n\n"
    yield f"data:[DONE]\n\n"
    return jsonify({'success': True})

def timeoutchat():
    # data = request.get_json()
    
    yield f"data:抱歉，我现在意识有点不清醒。\n\n"
    yield f"data:。\n\n"
    yield f"data:[DONE]\n\n"
    return jsonify({'success': True})

@application.route("/chart-data")
def chart_data() -> Response:
    question = request.args.get('question')
    print("question",question)

    messages = []
    
    
    messages.append({'role': 'user', 'content': '你只会说中文,你的回答中不会出现英文字母和英文单词，你的名字叫小幻'})
    messages.append({'role': 'user', 'content': question})

    if(question == ""):
        print(11)
        response = Response(stream_with_context(nochat()), mimetype="text/event-stream")
    elif("招呼" in question):
        print(111)
        response = Response(stream_with_context(zhaohu()), mimetype="text/event-stream")
    elif("哪里看到的" in question):
        print(111)
        response = Response(stream_with_context(zhidao()), mimetype="text/event-stream")
    else:
        print(22)
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
                request_timeout=10
            )
            response = Response(stream_with_context(chat(completion)), mimetype="text/event-stream")
        except Exception as e:
            print(e)
            response = Response(stream_with_context(timeoutchat()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@application.route('/api/getdraw',methods=['POST'])
def askchatgpt():
    data =request.get_data()
    datajson = json.loads(data)
    question = datajson['question']
    print("question",question)
    if(question == ""):
        print(11)
        response = {"code":200,"url":f"http://127.0.0.1:5000/static/{question}.png","text":f"我没听到要画什么"}
    response = openai.Image.create(
        prompt=question,
        n=1,
        size="512x512")
    print(response)
    r = requests.get(response['data'][0]['url'])
    with open(f'./static/{question}.png','wb') as f:
        f.write(r.content)
        f.close()
    return {"code":200,"url":f"http://127.0.0.1:5000/static/{question}.png","text":f"请看我画的：{question}"}


if __name__ == "__main__":
    application.run(host="0.0.0.0", threaded=True)
