import time
from uuid import uuid4
from typing import Optional

from .base import BaseModel


class Message(BaseModel):

    class Kind:
        BASIC = 'basic'
        INFO = 'info'

    def __init__(self, text: str, chat: 'Chat', kind: str, author_id: Optional[str] = None):
        self.id = uuid4().hex
        self.text = text
        self.chat = chat
        self.kind = kind
        self.author_id = author_id
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        # self.read = False

    @classmethod
    def create(cls):
        ...
