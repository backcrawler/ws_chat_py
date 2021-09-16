from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .configs import PROJECT_NAME, DEBUG, VERSION, ALLOWED_HOSTS, STATIC_DIR
from .handlers.router import router
from .errors.error_handlers import http422_error_handler, http_error_handler, server_error_handler


def get_app() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(Exception, server_error_handler)

    application.include_router(router)
    application.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    return application


# create app and serve forever with uvicorn
app = get_app()
