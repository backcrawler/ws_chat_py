from typing import Optional, Dict, List

from ws_chat_py.utils.util import Singleton
from ..models.interface import IChat


class ChatManager(metaclass=Singleton):

    def __init__(self):
        self.__id_to_chat: Dict[str, IChat] = {}

    def add_chat(self, ch: IChat) -> None:
        self.__id_to_chat[ch.id] = ch

    def remove_chat(self, ch: IChat) -> None:  # does not raise any errors
        try:
            del self.__id_to_chat[ch.id]
        except KeyError:
            pass

    def has_chat(self, ch: IChat) -> bool:
        return ch.id in self.__id_to_chat

    def get_chat_by_id(self, ch_id: str) -> Optional[IChat]:
        return self.__id_to_chat.get(ch_id)

    def get_all_chats_in_system(self) -> List[IChat]:
        return list(self.__id_to_chat.values())


chat_manager = ChatManager()
