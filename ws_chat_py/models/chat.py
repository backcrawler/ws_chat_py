import time
from typing import List, Optional
from uuid import uuid4

from .base import BaseModel
from .message import Message
from ws_chat_py.models.person import Person
from ..managers.delta_manager import delta_manager
from ..schemas.delta import Delta


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
        self.history_records = []  # todo: make history
        self.messages: List[Message] = []
        self.engine = None

    def add_message(self, msg: Message) -> None:  # todo: make listener
        self.messages.append(msg)
        delta = Delta(name='CHAT_MESSAGE', ch_id=self.id, type='add', data=msg.to_dict())
        delta_manager.add_delta_for_chat(delta, self)

    def to_dict(self, mode='response') -> dict:
        if mode == 'response':
            result = {
                'chatId': self.id,
                'createdTs': self.created_ts,
                'modifiedTs': self.modified_ts,
                'messages': [msg.to_dict() for msg in self.messages],
                'state': self.state,
            }

        elif mode == 'db':
            result = {
                'chatId': self.id,
                'createdTs': self.created_ts,
                'modifiedTs': self.modified_ts,
                'messages': [msg.id for msg in self.messages],
                'state': self.state,
            }

        else:
            raise ValueError('Incorrect mode given')

        return result
