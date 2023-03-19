from ..models.conversation import Conversation
from ..models.message import Message
from ..chatgpt.openai.chatgpt_client import ChatGPTClient
from ..config.config import OPENAI_API_KEY_FILE
from ...tools.utils import utils

import logging

FAKE_ANSWER_MSG = "Fake Answer."

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ConversationInteractor:
    conversation_interactor = None

    def __init__(self):
        self.conversation = None
        self.chatgpt_client = None
        self.__class__.conversation_interactor = self

        self._get_chatgpt_client()

    def _get_chatgpt_client(self):
        logger.info("Get ChatGPT client")
        try:
            self.chatgpt_client = ChatGPTClient(api_key=utils.read_file_as_string(OPENAI_API_KEY_FILE))
        except Exception as e:
            logger.error(f"Error getting ChatGPT client: {e}")

    @property
    def conversation(self):
        return self._conversation

    @conversation.setter
    def conversation(self, value):
        self._conversation = value
        self.__class__.conversation_interactor = self

    def create_conversation(self, title):
        self.conversation = Conversation(title)

    def set_conversation(self, conversation):
        self.conversation = conversation

    def get_last_conversation(self):
        if not self.conversation.__class__.conversations:
            return None
        return self.conversation.__class__.conversations[-1]

    def get_conversations(self):
        return self.conversation.__class__.conversations

    def get_messages(self):
        return self.conversation.messages

    def add_message(self, author, text):
        self.conversation.messages.update({
                Message.next_num_id: Message(author, text)
                })

    def change_message(self, id_, text):
        self.conversation.messages[id_].text = text

    def get_conversation_formatted(self):
        return [ChatGPTClient.format_message(msg.author, msg.text) for msg in self.conversation.messages.values()]

    def get_chatgpt_answer_fake(self, text):
        self.add_message('user', text)
        self.add_message('assistant', FAKE_ANSWER_MSG)
        return FAKE_ANSWER_MSG

    def get_chatgpt_answer(self, text):
        logger.info("Get ChatGPT answer")
        try:
            self.add_message('user', text)
            answer = self.chatgpt_client.get_answer(self.get_conversation_formatted())
            self.add_message('assistant', answer)
            return answer
        except Exception as e:
            logger.error(f"Error getting ChatGPT answer: {e}")
            answer = "Error getting ChatGPT answer! <br>" \
                     "Please, check if your API Key file contains a valid private Key. <br>" \
                     "Although, it could be that ChatGPT is not available at this moment."
            self.add_message('assistant', answer)
            return answer

    def __str__(self):
        return f"conversation: {self.conversation}"

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @classmethod
    def reset(cls):
        cls.conversation_interactor.conversation.reset()
        Message.reset()
        cls.conversation_interactor = None

    @staticmethod
    def reuse_or_create_conversation():
        conversation_int = ConversationInteractor.conversation_interactor

        if not conversation_int:
            conversation_int = ConversationInteractor()
            conversation_int.create_conversation(title='conversation_1')
            return conversation_int

        return conversation_int
