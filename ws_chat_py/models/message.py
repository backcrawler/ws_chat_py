import time
from uuid import uuid4
from typing import Optional

from .interface import IChat, IMessage
from .base import BaseModel


class Message(BaseModel, IMessage):

    class Kind:
        BASIC = 'basic'
        INFO = 'info'

    def __init__(self, text: str, chat: IChat, kind: str, author_id: Optional[str] = None):
        ts = time.time()
        field_name_to_value = {
            'id': uuid4().hex,
            'text': text,
            'chat': chat,
            'kind': kind,
            'author_id': author_id,
            'created_ts': ts,
            'modified_ts': ts,
        }
        super().__init__(field_name_to_value)

    @property
    def id(self) -> str:
        return self._get_field('id')

    @property
    def text(self) -> str:
        return self._get_field('text')

    @text.setter
    def text(self, value: str) -> None:
        self._set_field('text', value)

    @property
    def chat(self) -> IChat:
        return self._get_field('chat')

    @property
    def kind(self) -> str:
        return self._get_field('kind')

    @kind.setter
    def kind(self, value: str) -> None:
        self._set_field('kind', value)

    @property
    def author_id(self) -> Optional[str]:
        return self._get_field('author_id')

    @property
    def created_ts(self) -> float:
        return self._get_field('created_ts')

    @property
    def modified_ts(self) -> float:
        return self._get_field('modified_ts')

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
