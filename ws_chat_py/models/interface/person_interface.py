from typing import Optional


class IPerson:

    class Status:
        FREE = 'free'
        IN_CHAT = 'in_chat'
        UNREACHABLE = 'unreachable'

    def __init__(self, token: str, name: Optional[str] = None, chat: Optional['IChat'] = None):
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def name(self) -> Optional[str]:
        ...

    @name.setter
    def name(self, value: Optional[str]) -> None:
        ...

    @property
    def chat(self) -> Optional['IChat']:
        ...

    @chat.setter
    def chat(self, value: Optional['IChat']) -> None:
        ...

    @property
    def status(self) -> str:
        ...

    @status.setter
    def status(self, value: str):
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
    def client_side_id(self) -> str:
        ...

    def to_dict(self, mode: str = 'response') -> dict:
        ...