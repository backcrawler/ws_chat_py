from ws_chat_py.models.person import Person
from ws_chat_py.managers.person_manager import person_manager


class PersonEngine:

    manager = person_manager

    def __init__(self, person: Person):
        self.person = person
        person.engine = self

    @classmethod
    def create_person(cls, name: str) -> Person:
        person = Person(name)
        engine = cls(person)
        cls.manager.add_person(person)
        return person
