from enum import Enum


class UserRoleType(Enum):
    NONE = 0
    USER = 1
    ASSISTANT = 2


class UserRole:
    next_num_id = 1
    roles = []

    def __init__(self, id_, name, role_type):
        self.id = id_
        self.name = name
        self.type = role_type

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1
        self.__class__.roles.append(self)

    def __str__(self):
        return f"id: {self.id}, name: {self.name}, type: {self.type}"

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"'{self.name}', " \
               f"'{self.type}')"

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.roles = []
