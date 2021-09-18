from typing import Optional, Dict, Any

from pydantic import BaseModel


class IncomingMessage(BaseModel):
    text: str
    ch_id: str


class InitRequest(BaseModel):
    name: str


class ActionCommand(BaseModel):
    ch_id: str
    action: str
    data: Optional[Dict[str, Any]]
