import requests
import os
import json
import uuid

from flask import Flask, request


app = Flask(__name__)


CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

URL_CHAT = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
URL_GET_TOKEN = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


def generate_uuid():
    return str(uuid.uuid4())


def get_bearer_token():
    payload='scope=GIGACHAT_API_PERS'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': generate_uuid(),
        'Authorization': f'Basic {CLIENT_SECRET}'
    }

    response = requests.request("POST", URL_GET_TOKEN, headers=headers, data=payload, verify=False)
    
    print(response)

    return response.json()["access_token"]


def get_prompt(lang):
    if lang == "ru_RU":
        return "Ответь на вопросы rак можно более кратко и с минимальным числом слов."
    elif lang == "en_EN":
        return "Answer questions as briefly as possible and with as few words as possible."
    else:
        return ""


def get_chat_answer(user_text, prompt, bearer_token):
    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        "temperature": 0,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("POST", URL_CHAT, headers=headers, data=payload, verify=False)
    
    print(response)

    return response.json()["choices"][0]["message"]["content"]


# bearer_token = get_bearer_token()
# prompt = get_prompt('ru_RU')
# answer = get_chat_answer("Как дела?", prompt, bearer_token)
# print(answer)


@app.route('/update', methods=['POST'])
def update_data():
    body = request.get_json()
    print(body)
    
    # Check if required fields are present in the request body
    required_fields = ['text', 'lang']
    
    for field in required_fields:
        if field not in body:
            return {
                'statusCode': 400,
                'body': f'Missing required field: {field}',
            }
    
    text = body['text']
    lang = body['lang']
    
    bearer_token = get_bearer_token()
    prompt = get_prompt(lang)
    answer = get_chat_answer(text, prompt, bearer_token)
    
    return {
        'statusCode': 200,
        'body': answer,
    }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
