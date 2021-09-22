from typing import Optional, List


class IMessage:

    class Kind:
        BASIC = 'basic'
        INFO = 'info'

    def __init__(self, chatters: List['IPerson'] = None):
        ...

    @classmethod
    def create(cls, text: str, chat: 'IChat', kind: str, author_id: Optional[str] = None):
        ...

    def to_dict(self, mode: str = 'response') -> dict:
        ...
