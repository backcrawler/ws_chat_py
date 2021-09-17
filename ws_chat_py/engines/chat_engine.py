from ws_chat_py.models.chat import Chat

from ws_chat_py.managers.chat_manager import chat_manager


class ChatEngine:

    manager = chat_manager

    def __init__(self, chat: Chat):
        self.chat = chat
        chat.engine = self

    @classmethod
    def create_chat(cls, chatters) -> Chat:
        chat = Chat(chatters=chatters)
        engine = cls(chat)
        cls.manager.add_chat(chat)
        return chat

    def process_action(self, action: str, **params) -> None:  # todo: state-machine
        if self.chat.state == self.chat.State.PENDING:
            if action == 'start_chat':
                self.chat.state = self.chat.State.CHATTING
                self.send_info_msg_to_chatters('Chat started')

        elif self.chat.state == self.chat.State.CHATTING:
            if action == 'pause_chat':
                self.chat.state = self.chat.State.PAUSED
                self.send_info_msg_to_chatters('Chat paused')
            elif action == 'close_chat':
                self.chat.state = self.chat.State.CLOSED
                self.send_info_msg_to_chatters('Chat closed')

        elif self.chat.state == self.chat.State.PAUSED:
            if action == 'resume_chat':
                self.chat.state = self.chat.State.CHATTING
                self.send_info_msg_to_chatters('Chat resumed')

        elif self.chat.state == self.chat.State.CLOSED:
            ...

    def send_info_msg_to_chatters(self, msg: str) -> None:
        ...

    def check_auth_for_members(self, token: str) -> bool:
        for member in self.chat.chatters:
            if member.id == token:
                return True
        return False
