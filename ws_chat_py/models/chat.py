import time
from typing import List, Optional
from uuid import uuid4

from .interface import IChat, IPerson, IMessage
from .base import BaseModel  # todo: make listeners
from ..managers.delta_manager import delta_manager
from ..schemas.delta import Delta


class Chat(BaseModel, IChat):

    class State:
        PENDING = 'pending'
        CHATTING = 'chatting'
        PAUSED = 'paused'
        CLOSED = 'closed'
        DELETED = 'deleted'

    def __init__(self, chatters: List[IPerson] = None):
        ts = time.time()
        field_name_to_value = {
            'id': uuid4().hex,
            'chatters': chatters or [],
            'state': self.State.PENDING,
            'created_ts': ts,
            'modified_ts': ts,
            'history_records': [],  # todo: make history
            'messages': [],
        }
        super().__init__(field_name_to_value)
        self.engine = None

    @property
    def id(self) -> str:
        return self._get_field('id')

    @property
    def chatters(self) -> List['IPerson']:
        return self._get_field('chatters')

    @chatters.setter
    def chatters(self, value: List[IPerson]) -> None:
        self._set_field('chatters', value)

    @property
    def state(self) -> str:
        return self._get_field('state')

    @state.setter
    def state(self, value: str) -> None:
        self._set_field('state', value)

    @property
    def created_ts(self) -> float:
        return self._get_field('created_ts')

    @property
    def modified_ts(self) -> float:
        return self._get_field('modified_ts')

    @modified_ts.setter
    def modified_ts(self, value: float) -> None:
        self._set_field('modified_ts', value)

    @property
    def history_records(self) -> list:
        return self._get_field('history_records')

    @history_records.setter
    def history_records(self, value: list) -> None:
        self._set_field('history_records', value)

    @property
    def messages(self) -> List[IMessage]:
        return self._get_field('messages')

    @messages.setter
    def messages(self, value: List[IMessage]) -> None:
        self._set_field('messages', value)

    def add_message(self, msg: IMessage) -> None:  # todo: make listener
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
