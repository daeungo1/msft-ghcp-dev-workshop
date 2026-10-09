from fastapi import HTTPException, status


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


def unauthenticated(message: str = "Authentication required.") -> AppError:
    return AppError(status.HTTP_401_UNAUTHORIZED, "UNAUTHENTICATED", message)


def forbidden(message: str = "Admin access is required.") -> AppError:
    return AppError(status.HTTP_403_FORBIDDEN, "FORBIDDEN", message)


def http_exception(status_code: int, detail: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=detail)
