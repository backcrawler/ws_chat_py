import time
from uuid import uuid4
from typing import Optional

from .base import BaseModel
from .interface import IChat
from ..schemas.delta import Delta


class Person(BaseModel):

    class Status:
        FREE = 'free'
        IN_CHAT = 'in_chat'
        UNREACHABLE = 'unreachable'

    def __init__(self, token: str, name: Optional[str] = None, chat: Optional[IChat] = None):
        self.id = token
        self._name = name
        self.chat = chat
        self._status = self.Status.FREE
        self.created_ts = time.time()
        self.modified_ts = self.created_ts
        self.client_side_id = uuid4()
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

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        from ..managers import delta_manager  # todo: make listeners
        self._name = value
        delta = Delta(
            name='PERSON_NAME',
            ch_id=self.chat and self.chat.id,
            type='upd',
            data={'name': self.name}
        )
        if self.chat:
            delta_manager.add_delta_for_chat(delta, self.chat)
        else:
            delta_manager.add_delta(delta, self.id)

    def to_dict(self, mode='response') -> dict:
        result = {
            'name': self.name,
            'createdTs': self.created_ts,
            'modifiedTs': self.modified_ts,
            'chatId': self.chat and self.chat.id,
            'clientSideId': self.client_side_id,
        }
        if mode == 'response':
            pass
        elif mode == 'db':
            result['id'] = self.id
        else:
            raise ValueError('Incorrect mode given')

        return result
