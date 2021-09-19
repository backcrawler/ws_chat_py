import asyncio

from ws_chat_py.models.person import Person
from ws_chat_py.managers.person_manager import person_manager
from ..engines.chat_engine import ChatEngine


class PersonEngine:

    manager = person_manager

    def __init__(self, person: Person):
        self.person = person
        person.engine = self

    @classmethod
    def create_person(cls, token: str, name: str, chat=None) -> Person:
        person = Person(token, name, chat)
        engine = cls(person)
        cls.manager.add_person(person)
        return person

    @classmethod
    async def set_new_chat_for_person(cls, token: str) -> 'Chat':
        person_b = await cls.manager.get_any_free_person(token)
        person_a = cls.manager.get_person_by_id(token)
        new_chat = ChatEngine.create_chat([person_a, person_b])
        return new_chat
