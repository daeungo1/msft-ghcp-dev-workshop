from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db import Base, default_database_url, import_models, make_engine
from app.errors import AppError
from app.follows.routes import router as follows_router
from app.members.routes import router as members_router
from app.posts.routes import router as posts_router


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": {"code": code, "message": message}})


def _http_error_code(status_code: int) -> str:
    return {
        400: "BAD_REQUEST",
        401: "UNAUTHENTICATED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
    }.get(status_code, "HTTP_ERROR")


def create_app(database_url: str | None = None) -> FastAPI:
    engine = make_engine(database_url or default_database_url())
    session_factory = sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        import_models()
        Base.metadata.create_all(engine)
        yield

    app = FastAPI(title="TeamFeed", lifespan=lifespan)
    app.state.engine = engine
    app.state.sessionmaker = session_factory

    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return _error_response(exc.status_code, exc.code, exc.message)

    @app.exception_handler(HTTPException)
    async def handle_http_error(_: Request, exc: HTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
        return _error_response(exc.status_code, _http_error_code(exc.status_code), message)

    @app.exception_handler(StarletteHTTPException)
    async def handle_starlette_http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
        return _error_response(exc.status_code, _http_error_code(exc.status_code), message)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        message = "; ".join(error["msg"] for error in exc.errors())
        return _error_response(422, "VALIDATION_ERROR", message)

    app.include_router(members_router)
    app.include_router(posts_router)
    app.include_router(follows_router)
    return app


app = create_app()
