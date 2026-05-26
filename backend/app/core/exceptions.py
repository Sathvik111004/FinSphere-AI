from fastapi import HTTPException, status

class FinSphereException(Exception):
    """Base exception class for FinSphere system."""
    pass

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionDeniedError(HTTPException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class IngestionError(HTTPException):
    def __init__(self, detail: str = "Error ingesting document"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "An error occurred with database operations. Diagnostics logged."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
