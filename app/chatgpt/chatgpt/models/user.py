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

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.users = []
