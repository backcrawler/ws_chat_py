import time
from uuid import uuid4
from typing import Optional

from .base import BaseModel
from .interface import IChat
from ..schemas.delta import Delta
from .interface import IPerson


class Person(BaseModel, IPerson):

    class Status:
        IDLE = 'idle'
        FREE = 'free'
        IN_CHAT = 'in_chat'
        UNREACHABLE = 'unreachable'

    def __init__(self, token: str, name: Optional[str] = None, chat: Optional[IChat] = None):
        ts = time.time()
        field_name_to_value = {
            'id': token,
            'name': name,
            'chat': chat,
            'status': self.Status.IDLE,
            'created_ts': ts,
            'modified_ts': ts,
            'client_side_id': uuid4().hex,
        }
        super().__init__(field_name_to_value)
        self.engine = None

    @property
    def id(self) -> str:
        return self._get_field('id')

    @property
    def name(self) -> Optional[str]:
        return self._get_field('name')

    @name.setter
    def name(self, value: Optional[str]) -> None:
        from ..managers import delta_manager  # todo: make listeners
        self._set_field('name', value)
        delta = Delta(
            name='PERSON_NAME',  # todo: remove STUB
            ch_id=self.chat and self.chat.id,
            type='upd',
            data={'name': self.name}
        )
        if self.chat:
            delta_manager.add_delta_for_chat(delta, self.chat)
        else:
            delta_manager.add_delta(delta, self.id)

    @property
    def chat(self) -> Optional[IChat]:
        return self._get_field('chat')

    @chat.setter
    def chat(self, value: Optional[IChat]) -> None:
        self._set_field('chat', value)

    @property
    def status(self) -> str:
        return self._get_field('status')

    @status.setter
    def status(self, value: str):
        if value != self.status:
            if value == self.Status.FREE:
                self.engine.manager.add_to_free_persons(self)
            elif self.status == self.Status.FREE and value != self.Status.FREE:
                self.engine.manager.remove_from_free_persons(self)
            self._set_field('status', value)

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
    def client_side_id(self) -> str:
        return self._get_field('client_side_id')

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
