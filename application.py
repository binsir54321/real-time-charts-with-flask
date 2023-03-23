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
    messages.append({'role': 'user', 'content': '如果让你打招呼，你就说复旦附小二年三班的小朋友们很厉害，你们写的童诗很棒啊。如果问你怎么知道的，你就说你是看了顾老师的公众号了解到的'})
    messages.append({'role': 'user', 'content': '如果让你朗读什么，你就说：好的'})
    messages.append({'role': 'user', 'content': question})

    if(question == ""):
        print(11)
        response = Response(stream_with_context(nochat()), mimetype="text/event-stream")
    else:
        print(22)
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
                request_timeout=20
            )
            response = Response(stream_with_context(chat(completion)), mimetype="text/event-stream")
        except Exception:
            print("Cannot divide by zero")
            response = Response(stream_with_context(timeoutchat()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response



if __name__ == "__main__":
    application.run(host="0.0.0.0", threaded=True)
