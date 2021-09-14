import time
from uuid import uuid4

from .base import BaseModel


class Person(BaseModel):

    def __init__(self, name: str, chat: 'Chat' = None, fields: dict = None):
        self.id = uuid4().hex
        self.name = name
        self.chat = chat
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        self.fields = fields or {}
        self.engine = None

