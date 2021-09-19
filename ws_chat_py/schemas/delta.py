from typing import Dict, Any

from pydantic import BaseModel


class Delta(BaseModel):
    name: str
    ch_id: str
    type: str
    data: Dict[str, Any]
