class User:
    next_num_id = 1
    users = []

    def __init__(self, id_, name, role):
        self.id = id_
        self.name = name
        self.role = role

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1
        self.__class__.users.append(self)

    def __str__(self):
        return f"id: {self.id}, name: {self.name}, role: {self.role}"

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"'{self.name}', " \
               f"'{self.role}')"

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.users = []
