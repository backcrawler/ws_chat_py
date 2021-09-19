import asyncio
import random
from typing import Optional, Dict, Set

from ws_chat_py.models.person import Person
from ws_chat_py.configs import PERSON_WAIT_TIME
from ws_chat_py.utils.util import Singleton


class PersonManager(metaclass=Singleton):

    def __init__(self):
        self.__id_to_person: Dict[str, Person] = {}
        self.__free_persons: Set[str] = set()
        self.max_wait_time = PERSON_WAIT_TIME
        self.period_check = 0.3  # seconds

    def add_person(self, p: Person) -> None:
        self.__id_to_person[p.id] = p
        if p.status == Person.Status.FREE:
            self.add_to_free_persons(p)

    def add_to_free_persons(self, p: Person) -> None:
        self.__free_persons.add(p.id)

    def remove_from_free_persons(self, p: Person) -> None:
        self.__free_persons.remove(p.id)

    def remove_person(self, p: Person) -> None:  # does not raise any errors
        try:
            if p.id in self.__free_persons:
                self.__free_persons.remove(p.id)
            del self.__id_to_person[p.id]
        except KeyError:
            pass

    def has_person(self, p: Person) -> bool:
        return p.id in self.__id_to_person

    def get_person_by_id(self, p_id: str) -> Optional[Person]:
        return self.__id_to_person.get(p_id)

    async def get_any_free_person(self, p_id: Optional[str] = None) -> Optional[Person]:
        i = 0
        extra_set = {p_id}  # deduct this of each iteration to prevent from self-fetching
        while True:
            if i * self.period_check >= self.max_wait_time:
                break

            person_list = list(self.__free_persons - extra_set)
            if person_list:
                p_id_to_fetch = random.choice(person_list)
                return self.get_person_by_id(p_id_to_fetch)

            i += 1
            await asyncio.sleep(self.period_check)


person_manager = PersonManager()
