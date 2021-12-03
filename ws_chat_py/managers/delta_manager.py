import asyncio
from collections import defaultdict
from functools import partial
from typing import Dict, List, Optional

from ws_chat_py.utils.util import Singleton, a_partial
from ws_chat_py.utils.a_list_demux import AListDemux
from ws_chat_py.configs import DELTA_WAIT_TIME
from ..models.interface import IChat
from ..schemas.delta import Delta


class DeltaManager(metaclass=Singleton):

    def __init__(self):
        self.max_wait_time = DELTA_WAIT_TIME
        self._demux = AListDemux[List[Delta]]()

    def add_delta(self, delta: dict, p_id: str) -> None:
        loop = asyncio.get_running_loop()
        loop.call_soon(lambda: asyncio.ensure_future(self._demux.set(p_id, delta)))

    def add_delta_for_chat(self, delta: dict, chat: IChat) -> None:
        loop = asyncio.get_running_loop()
        for person in chat.chatters:
            loop.call_soon(partial(asyncio.ensure_future, self._demux.set(person.id, delta)))

    async def get_deltas_for_person(self, p_id: str) -> Optional[List]:
        try:
            deltas = await self._demux.get(p_id, self.max_wait_time)
        except asyncio.TimeoutError:
            print(self._demux)
            return None
        else:
            deltas = deltas.copy()
            self._demux.delete(p_id)
            print(self._demux)
            return deltas


delta_manager = DeltaManager()
