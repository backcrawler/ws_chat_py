from typing import Optional, Dict

from ws_chat_py.models.person import Person
from ws_chat_py.utils.util import Singleton


class PersonManager(metaclass=Singleton):

    def __init__(self):
        self.__id_to_person: Dict[str, Person] = {}

    def add_person(self, p: Person) -> None:
        self.__id_to_person[p.id] = p

    def remove_person(self, p: Person) -> None:  # does not raise any errors
        try:
            del self.__id_to_person[p.id]
        except KeyError:
            pass

    def has_person(self, p: Person) -> bool:
        return p.id in self.__id_to_person

    def get_person_by_id(self, p_id: str) -> Optional[Person]:
        return self.__id_to_person.get(p_id)

    def get_any_pending_person(self, p_id: Optional[str] = None) -> Optional[Person]:
        for person in self.__id_to_person.values():
            if person.status == Person.Status.FREE:
                if not p_id and person.id == p_id:
                    continue
                return person


person_manager = PersonManager()
