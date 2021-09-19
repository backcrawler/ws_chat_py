from typing import Union, List, Dict, Any

from pydantic import BaseModel

from .delta import Delta


class SimpleResponse(BaseModel):
    response: str


class DeltaResponse(BaseModel):
    response: Union[str, List[Delta]]
