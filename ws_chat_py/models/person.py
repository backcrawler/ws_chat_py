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
        self._status = self.Status.FREE
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        self.engine = None

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value != self._status:
            if value == self.Status.FREE:
                self.engine.manager.add_to_free_persons(self)
            elif self._status == self.Status.FREE and value != self.Status.FREE:
                self.engine.manager.remove_from_free_persons(self)
            self._status = value
