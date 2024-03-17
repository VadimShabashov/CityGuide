import requests
import os
import json

MAX_TOKENS= os.environ.get('MAX_TOKENS')
IDENTIFIER = os.environ.get('IDENTIFIER')
API_KEY = os.environ.get('API_KEY')
URL="https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

class YandexGPT:
    def __init__(self, url=URL, api_key=API_KEY, max_tokens=MAX_TOKENS):
        self.url = url
        self.api_key = api_key
        self.max_tokens = max_tokens

    @staticmethod
    def system_prompt(lang):
        prompt_info = f"""
        Пожалуйста сожми ответ до одного предложения, отвечай кратко и лаконично, оставляя только самую важную информацию
        """
        
        if lang == 'en_EN':
            prompt_info = f"""
            Answer questions as briefly as possible and with as few words as possible.
            """

        prompts = []
        prompts.append({'role': 'system', 'text': prompt_info})
        

        return prompts

    def get_prompt_message(self, user_text, lang):
        """
        Подготовка промпта
        """
        prompts = self.system_prompt(lang)
        prompts.append({'role': 'user', 'text': user_text})
        return prompts

    def get_prompt(self, user_text, lang, temperature=0):
        prompt_messages = self.get_prompt_message(user_text, lang)
        prompt = {
            "modelUri": f"gpt://{IDENTIFIER}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": self.max_tokens
            },
            "messages": prompt_messages
        }

        return prompt

    def send_prompt(self, prompt):
        """
        Отправка запроса по api
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        try:
            response = requests.post(self.url, headers=headers, json=prompt)
            return response.json()

        except Exception as e:
            print(e)

    def get_answer(self, prompt):
        """
        Получение ответа
        """
        result = self.send_prompt(prompt)['result']['alternatives'][0]['message']['text']
        if result is None:
            return 'Error: No answer. Try more'

        return result


def handler(event, context):
    try:
        # Check if request method is POST
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'body': 'Only a POST request with `Content-Type: application/json` is supported',
            }
        
        # Parse JSON from request body
        body = json.loads(event['body'])
        
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
        yandex_gpt = YandexGPT(URL, API_KEY, MAX_TOKENS)

        prompt = yandex_gpt.get_prompt(text, lang)
        answer = yandex_gpt.get_answer(prompt)
        
        return {
            'statusCode': 200,
            'body': answer,
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e),
        }

