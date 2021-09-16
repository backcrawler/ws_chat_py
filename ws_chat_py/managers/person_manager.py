from typing import Optional

from ws_chat_py.models.person import Person


class PersonManager:

    def __init__(self):
        self.__id_to_person = {}  # Dict[str, Chat]

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


person_manager = PersonManager()
