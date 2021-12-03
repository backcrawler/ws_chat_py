from typing import Optional, List


class IMessage:

    class Kind:
        BASIC = 'basic'
        INFO = 'info'

    def __init__(self, chatters: List['IPerson'] = None):
        ...

    @property
    def id(self) -> str:
        ...

    @property
    def text(self) -> str:
        ...

    @text.setter
    def text(self, value: str) -> None:
        ...

    @property
    def chat(self) -> 'IChat':
        ...

    @property
    def kind(self) -> str:
        ...

    @kind.setter
    def kind(self, value: str) -> None:
        ...

    @property
    def author_id(self) -> Optional[str]:
        ...

    @property
    def created_ts(self) -> float:
        ...

    @property
    def modified_ts(self) -> float:
        ...

    @classmethod
    def create(cls, text: str, chat: 'IChat', kind: str, author_id: Optional[str] = None):
        ...

    def to_dict(self, mode: str = 'response') -> dict:
        ...
