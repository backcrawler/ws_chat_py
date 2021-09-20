from typing import Dict, Any, Optional

from pydantic import BaseModel


class Delta(BaseModel):
    name: str
    ch_id: Optional[str]
    type: str
    data: Dict[str, Any]
