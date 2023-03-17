import markdown
import requests
import json


class ChatgptError(Exception):
    pass


class ChatGPTResponse:
    def __init__(self):
        self.id = None
        self.object = None
        self.created = None
        self.model = None
        self.usage = {}
        self.choices = []
        self.finish_reason = None
        self.index = None
        self.answer_raw = None
        self.answer = None

    def clear(self):
        self.id = None
        self.object = None
        self.created = None
        self.model = None
        self.usage = {}
        self.choices = []
        self.finish_reason = None
        self.index = None
        self.answer_raw = None
        self.answer = None

    def set_state(self, response):
        self.id = response.get('id')
        self.object = response.get('object')
        self.created = response.get('created')
        self.model = response.get('model')
        self.usage = response.get('usage')
        self.choices = response.get('choices')
        self.finish_reason = response.get('finish_reason')
        self.index = response.get('index')
        self.answer_raw = response.get('choices')[0].get('message')['content']
        self.answer = markdown.markdown(self.answer_raw)

    def __str__(self):
        return (f"Id: {self.id}\n"
                f"object: {self.object}\n"
                f"created: {self.created}\n"
                f"model: {self.model}\n"
                f"usage: {self.usage}\n"
                f"choices: {self.choices}\n"
                f"finish_reason: {self.finish_reason}\n"
                f"index: {self.index}\n")


class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = None
        self.headers = None
        self.data = None
        self.response = ChatGPTResponse()

        self._init()

    def _init(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
            }

    @staticmethod
    def format_message(role_name, message):
        return {'role': role_name, 'content': message}

    def get_answer(self, messages):
        self.response.clear()
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages
            }

        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
            response_json = response.json()
            self.response.set_state(response_json)
            return self.response.answer
        except Exception as e:
            raise ChatgptError(f"Error processing chatgpt answer! Msg: {e}")


if __name__ == '__main__':
    from app.chatgpt.config.config import OPENAI_API_KEY_FILE
    from app.tools.utils import utils

    messages_ = []
    messages_ += [ChatGPTClient.format_message(
        'user',
        "Hi, I am Joan. You are a game master in a RPG board game based in the Middle Earth. "
        "You should create a fantasy context for 1 player and give them a list of 5 from 10 options. "
        "Then the player will choose a numbered option. This will allow you to continue the story and give "
        "another list of options to choose from. You can introduce NPCs whenever you think necessary. "
        "Can you play this game with me?"
        )]
    messages_ += [ChatGPTClient.format_message(
        'assistant',
        "Sure. I will play this game with you."
        )]
    messages_ += [ChatGPTClient.format_message(
        'user',
        "We can start in a forest where two female elves are surrounded by four giant spiders."
        )]

    client = ChatGPTClient(api_key=utils.read_file_as_string(OPENAI_API_KEY_FILE))
    answer = ChatGPTClient.format_message('assistant', client.get_answer(messages_))
    messages_ += [answer]

    print(client.response)
    for message in messages_:
        print(message)
