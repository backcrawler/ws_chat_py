from ws_chat_py.models.chat import Chat


class ChatEngine:

    def __init__(self, chat: Chat):
        self.chat = chat
        chat.engine = self

    @classmethod
    def create_chat(cls, state, chatters) -> Chat:
        chat = Chat(state=state, chatters=chatters)
        engine = cls(chat)
        return chat
