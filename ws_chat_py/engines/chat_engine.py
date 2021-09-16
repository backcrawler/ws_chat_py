from ws_chat_py.models.chat import Chat

from ws_chat_py.managers.chat_manager import chat_manager


class ChatEngine:

    manager = chat_manager

    def __init__(self, chat: Chat):
        self.chat = chat
        chat.engine = self

    @classmethod
    def create_chat(cls, state, chatters) -> Chat:
        chat = Chat(state=state, chatters=chatters)
        engine = cls(chat)
        cls.manager.add_chat(chat)
        return chat
