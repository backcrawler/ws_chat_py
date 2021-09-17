import asyncio
import weakref
from typing import Optional, Dict, List

from ws_chat_py.models.chat import Chat
from ws_chat_py.utils.util import Singleton


class ChatManager(metaclass=Singleton):

    def __init__(self):
        self.__id_to_chat: Dict[str, Chat] = {}

    def add_chat(self, ch: Chat) -> None:
        self.__id_to_chat[ch.id] = ch

    def remove_chat(self, ch: Chat) -> None:  # does not raise any errors
        try:
            del self.__id_to_chat[ch.id]
        except KeyError:
            pass

    def has_chat(self, ch: Chat) -> bool:
        return ch.id in self.__id_to_chat

    def get_chat_by_id(self, ch_id: str) -> Optional[Chat]:
        return self.__id_to_chat.get(ch_id)

    def get_all_chats_in_system(self) -> List[Chat]:
        return list(self.__id_to_chat.values())


chat_manager = ChatManager()
