import requests
import json


class ChatgptError(Exception):
    pass


class ChatGPTClient:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = None
        self.headers = None
        self.data = None

        self._init()

    def _init(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
            }

    def get_answer(self, message):
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': message}
                ]
            }

        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
            response_json = response.json()
            answer = response_json['choices'][0]['message']['content']
        except Exception as e:
            raise ChatgptError(f"Error processing chatgpt answer! Msg: {e}")

        return answer


if __name__ == '__main__':
    from app.chatgpt.config.config import OPENAI_API_KEY_FILE
    from app.tools.utils import utils

    client = ChatGPTClient(api_key=utils.read_file_as_string(OPENAI_API_KEY_FILE))
    res = client.get_answer("Please, print the first twelve prime numbers "
                            "and a Python program that generates them.")
    print(res)
