from typing import List


class IChat:

    def __init__(self, chatters: List['IPerson'] = None):
        ...

    def add_message(self, msg: 'IMessage') -> None:
        ...

    def to_dict(self, mode: str = 'response') -> dict:
        ...