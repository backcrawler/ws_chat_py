import asyncio
from typing import Dict, TypeVar, Generic, Optional, Callable

T = TypeVar('T')


class ADemux(Generic[T]):

    def __init__(self):
        self._futures: Dict[str, asyncio.Future[Callable]] = {}
        self._key_to_data: Dict[str, T] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str, timeout: Optional[float] = None) -> T:
        if timeout is None:
            result = await self._retrieve(key)
        else:
            result = await self._retrieve(key)
            # result = await asyncio.wait_for(self._retrieve(key), timeout)
        return result

    async def _retrieve(self, key: str) -> T:
        if key in self._futures:
            f = self._futures[key]
            if f.done():
                async with self._lock:
                    callback = await self._futures[key]
            else:
                callback = await self._futures[key]
        else:
            self._futures[key] = asyncio.Future()
            callback = await self._futures[key]

        return callback()

    async def set(self, key: str, value: T) -> None:
        async with self._lock:
            if key in self._futures:
                f = self._futures[key]
            else:
                f = asyncio.Future()
                self._futures[key] = f

            if not f.done():
                f.set_result(lambda: self._key_to_data[key])

            self._process_value(key, value)

    def delete(self, key: str) -> None:
        f = self._futures[key]
        if f.done():
            del self._futures[key]
            del self._key_to_data[key]
        else:
            raise RuntimeError('Task is not finished yet')

    def _process_value(self, key: str, value: T) -> None:
        self._key_to_data[key] = value

    def __str__(self):
        return f'ADict({self._futures} | {self._key_to_data})'
