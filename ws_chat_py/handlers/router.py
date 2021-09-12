from fastapi import APIRouter

from .handlers import root_handler


router = APIRouter()
router.include_router(root_handler, tags=['root'])