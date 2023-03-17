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
    yield f"data:[DONE]\n\n"
    return jsonify({'success': True})

@application.route("/chart-data")
def chart_data() -> Response:
    question = request.args.get('question')
    print(question)
    messages = []
    messages.append({'role': 'user', 'content': question})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

    response = Response(stream_with_context(chat(completion)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response



if __name__ == "__main__":
    application.run(host="0.0.0.0", threaded=True)
