from starlette.requests import Request
from starlette.responses import JSONResponse


async def server_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({'error': 'server_error'}, status_code=500)
