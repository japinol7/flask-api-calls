from ..models.conversation import Conversation
from ..models.message import Message

from ...tools.utils import utils

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ConversationInteractor:
    conversation_interactor = None

    def __init__(self):
        self.conversation = None
        self.__class__.conversation_interactor = self

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
        self.conversation.messages += [Message(author, text)]

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
