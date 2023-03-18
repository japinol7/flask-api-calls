class Conversation:
    next_num_id = 1
    conversations = []

    def __init__(self, title):
        self.id = self.__class__.next_num_id
        self.title = title
        self.messages = {}

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1
        self.__class__.conversations.append(self)

    def __str__(self):
        return f"id: {self.id}, title: {self.title}, # messages: {len(self.messages)}"

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f'"{self.title}")'

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        for conversation in cls.conversations:
            conversation.messages = {}
        cls.conversations = []
