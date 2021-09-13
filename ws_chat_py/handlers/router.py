from fastapi import APIRouter

from .root_handlers import root_router
from .ws_handlers import ws_router


router = APIRouter()
router.include_router(root_router, tags=['root'])
router.include_router(ws_router, tags=['ws'])
