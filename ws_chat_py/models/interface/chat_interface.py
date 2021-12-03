from typing import List


class IChat:

    def __init__(self, chatters: List['IPerson'] = None):
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def chatters(self) -> List['IPerson']:
        ...

    @chatters.setter
    def chatters(self, value: List['IPerson']) -> None:
        ...

    @property
    def state(self) -> str:
        ...

    @state.setter
    def state(self, value: str) -> None:
        ...

    @property
    def created_ts(self) -> float:
        ...

    @property
    def modified_ts(self) -> float:
        ...

    @modified_ts.setter
    def modified_ts(self, value: float) -> None:
        ...

    @property
    def history_records(self) -> list:
        ...

    @history_records.setter
    def history_records(self, value: list) -> None:
        ...

    @property
    def messages(self) -> List['IMessage']:
        ...

    @messages.setter
    def messages(self, value: List['IMessage']) -> None:
        ...

    def add_message(self, msg: 'IMessage') -> None:
        ...

    def to_dict(self, mode: str = 'response') -> dict:
        ...
