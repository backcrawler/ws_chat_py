from typing import Optional


class IPerson:

    class Status:
        FREE = 'free'
        IN_CHAT = 'in_chat'
        UNREACHABLE = 'unreachable'

    def __init__(self, token: str, name: Optional[str] = None, chat: Optional['IChat'] = None):
        ...

    @property
    def status(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    def to_dict(self, mode: str = 'response') -> dict:
        ...