#coding:utf8
import requests
import openai
from collections.abc import Iterable
import json

openai.api_key = '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'
messages = []
messages.append({'role': 'user', 'content': '说一个50个字的关于西游记的介绍'})
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=True
)
# ai_response = completion.choices[0].message['content']
# # print(ai_response)
# messages.append({'role': 'assistant', 'content': ai_response})
# print(messages)
# question = ''
# headers = {'Authorization': 'Bearer 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'}
# payload = {
#     'prompt': question,
#     'max_tokens': 100,
#     'temperature': 0.7,
#     'stream': True
# }
# response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', json=payload, headers=headers, stream=True)
# print("???")

# for chunk in completion.iter_content(chunk_size=1024):
#     if chunk:
#             # yield f"{chunk.decode('utf-8')}\n\n"
#         print(chunk)
# print(completion.iter_content())
print(isinstance(completion, Iterable))
for each in completion:
    # print(isinstance(each, Iterable))
    if("content" in each.choices[0].delta):
        print(each.choices[0])
    # print(json.loads(each.choices[0]).decode('utf-8'))