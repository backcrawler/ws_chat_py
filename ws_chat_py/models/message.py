import time
from uuid import uuid4

from .base import BaseModel


class Message(BaseModel):

    def __init__(self, text: str, chat: 'Chat', author_id: str):
        self.id = uuid4().hex
        self.text = text
        self.chat = chat
        self.author_id = author_id
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        # self.read = False
