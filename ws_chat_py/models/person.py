import time
from uuid import uuid4
from typing import Optional

from .base import BaseModel


class Person(BaseModel):

    class Status:
        FREE = 'free'
        IN_CHAT = 'in_chat'
        UNREACHABLE = 'unreachable'

    def __init__(self, token: str, name: str, chat: Optional['Chat'] = None):
        self.id = token
        self.name = name
        self.chat = chat
        self.status = self.Status.FREE
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        self.engine = None
