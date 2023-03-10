class Message:
    next_num_id = 1
    messages = []

    def __init__(self, author, text):
        self.id = self.__class__.next_num_id
        self.author = author
        self.text = text

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1
        self.__class__.messages.append(self)

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.messages = []
