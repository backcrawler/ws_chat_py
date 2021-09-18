import time
from typing import List, Optional
from uuid import uuid4

from .base import BaseModel
from ws_chat_py.models.person import Person


class Chat(BaseModel):

    class State:
        PENDING = 'pending'
        CHATTING = 'chatting'
        PAUSED = 'paused'
        CLOSED = 'closed'
        DELETED = 'deleted'

    def __init__(self, chatters: List[Person] = None):
        self.id = uuid4().hex
        self.chatters = chatters or []
        self.state = self.State.PENDING
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        self.history_records = []
        self.messages: List['Message'] = []
        self.engine = None

    def add_message(self, msg: 'Message') -> None:
        self.messages.append(msg)
