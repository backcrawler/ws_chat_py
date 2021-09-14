import time
from typing import List
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

    def __init__(self, state: str = None, chatters: List[Person] = None):
        self.id = uuid4().hex
        self.chatters = chatters or []
        self.state = state or self.State.PENDING
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        self.history_records = []
        self.messages = []
        self.engine = None

