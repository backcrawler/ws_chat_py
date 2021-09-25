import time
from uuid import uuid4
from typing import Optional

from .interface import IChat, IMessage


class Message(IMessage):

    class Kind:
        BASIC = 'basic'
        INFO = 'info'

    def __init__(self, text: str, chat: IChat, kind: str, author_id: Optional[str] = None):
        self.id = uuid4().hex
        self.text = text
        self.chat = chat
        self.kind = kind
        self.author_id = author_id
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        # self.read = False

    @classmethod
    def create(cls, text: str, chat: IChat, kind: str, author_id: Optional[str] = None):
        msg = cls(text, chat, kind, author_id)
        chat.add_message(msg)
        return msg

    def to_dict(self, mode='response') -> dict:
        if mode in ('response', 'db'):
            result = {
                'id': self.id,
                'text': self.text,
                'createdTs': self.created_ts,
                'modifiedTs': self.modified_ts,
                'chatId': self.chat.id,
                'kind': self.kind,
            }
        else:
            raise ValueError('Incorrect mode given')

        return result
