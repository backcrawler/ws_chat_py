from typing import Union, List, Dict, Any

from pydantic import BaseModel


class SimpleResponse(BaseModel):
    response: str


class _SingleDelta(BaseModel):
    ch_id: str
    type: str
    data: Dict[str, Any]


class DeltaResponse(BaseModel):
    response: Union[str, List[_SingleDelta]]
