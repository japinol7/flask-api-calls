class Message:
    next_num_id = 1

    def __init__(self, author, text):
        self.id = self.__class__.next_num_id
        self.author = author
        self.text = text

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1

    def __str__(self):
        return f"id: {self.id}, author: {self.author}, text: {self.text}"

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"'{self.author}', " \
               f'"{self.text}")'

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
