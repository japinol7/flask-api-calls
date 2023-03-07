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

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.roles = []
