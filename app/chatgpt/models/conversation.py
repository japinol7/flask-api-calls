class Conversation:
    next_num_id = 1
    conversations = []

    def __init__(self, id_, author, title):
        self.id = id_
        self.title = title
        self.author = author
        self.messages = []

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1
        self.__class__.conversations.append(self)

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.conversations = []
