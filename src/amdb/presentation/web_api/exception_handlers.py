from fastapi import FastAPI
from fastapi.responses import JSONResponse

from amdb.application.common.exception import ApplicationError
from amdb.infrastructure.exception import InfrastructureError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, _application_error_handler)
    app.add_exception_handler(InfrastructureError, _infrastructure_error_handler)


def _application_error_handler(_, error: ApplicationError) -> JSONResponse:
    return JSONResponse(content={"message": error.message}, status_code=400)


def _infrastructure_error_handler(_, error: InfrastructureError) -> JSONResponse:
    return JSONResponse(content=None, status_code=500)
