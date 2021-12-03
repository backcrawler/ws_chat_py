from collections import defaultdict
from typing import List, TypeVar, Dict, Optional, Generic

from .a_demux import ADemux

T = TypeVar('T')


class AListDemux(ADemux, Generic[T]):

    def __init__(self):
        super().__init__()
        self._key_to_data: Dict[str, List[T]] = defaultdict(list)

    def _process_value(self, key: str, value: T) -> None:
        self._key_to_data[key].append(value)

    async def get(self, key: str, timeout: Optional[float] = None) -> List[T]:
        return await super().get(key, timeout)

    async def _retrieve(self, key: str) -> List[T]:
        return await super()._retrieve(key)
