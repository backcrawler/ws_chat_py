from fastapi import FastAPI

from .configs import PROJECT_NAME, API_PREFIX, DEBUG, VERSION
from .handlers.router import router


def get_app() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    # application.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=ALLOWED_HOSTS or ["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    # application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))
    #
    # application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(router, prefix=API_PREFIX)

    return application


# create app and serve forever with uvicorn
app = get_app()
