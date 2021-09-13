from fastapi import Request, APIRouter


root_router = APIRouter()


@root_router.get("/")
async def root_handler():
    return {"message": "Hello World"}
