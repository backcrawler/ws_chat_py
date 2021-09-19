import asyncio
from collections import defaultdict
from typing import Dict, List, Optional

from ws_chat_py.utils.util import Singleton
from ws_chat_py.configs import DELTA_WAIT_TIME


class DeltaManager(metaclass=Singleton):

    def __init__(self):
        self.__person_id_to_deltas: Dict[str, List] = defaultdict(list)
        self.max_wait_time = DELTA_WAIT_TIME
        self.period_check = 0.2  # seconds

    def add_delta(self, delta: dict, p_id: str) -> None:
        self.__person_id_to_deltas[p_id].append(delta)

    async def get_deltas_for_person(self, p_id: str) -> Optional[List]:  # todo: make AsyncMap
        i = 0
        while True:
            if i * self.period_check >= self.max_wait_time:
                break

            deltas = self.__person_id_to_deltas.get(p_id)
            if deltas:
                del self.__person_id_to_deltas[p_id]
                return deltas

            i += 1
            await asyncio.sleep(self.period_check)

        return None


delta_manager = DeltaManager()
