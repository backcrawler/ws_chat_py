from typing import Optional, List

from ws_chat_py.models import Chat, Message
from ws_chat_py.managers import chat_manager, delta_manager
from ws_chat_py.schemas.request_schemas import ActionCommand
from ws_chat_py.schemas.delta import Delta


class ChatEngine:

    manager = chat_manager

    def __init__(self, chat: Chat):
        self.chat = chat
        chat.engine = self

    @classmethod
    def create_chat(cls, chatters: List['Person']) -> Chat:
        chat = Chat(chatters=chatters)
        engine = cls(chat)
        cls.manager.add_chat(chat)
        delta = Delta(name='CHAT', ch_id=chat.id, type='add', data=chat.to_dict())
        for person in chatters:
            delta_manager.add_delta(delta, person.id)  # todo: revise with listener
        return chat

    def create_basic_message(self, text: str, ch_id: str, author_id: Optional[str] = None) -> Message:
        chat = self.manager.get_chat_by_id(ch_id)
        message = Message.create(
            text=text,
            chat=chat,
            kind=Message.Kind.BASIC,
            author_id=author_id
        )
        return message

    def process_action(self, action_cmd: ActionCommand, **params) -> None:  # todo: state-machine
        action = action_cmd.action
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

    def send_info_msg_to_chatters(self, msg: str) -> Message:
        message = Message.create(
            text=msg,
            chat=self.chat,
            kind=Message.Kind.INFO,
            author_id=None
        )
        return message

    def check_auth_for_members(self, token: str) -> bool:
        for member in self.chat.chatters:
            if member.id == token:
                return True
        return False
