from typing import Annotated
from fastapi import status, HTTPException

InvalidUserTypeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid user type")

InactiveUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User is not active")

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid user credentials",
    headers={"WWW-Authenticate": "Bearer"})

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is either expired or invalid",
    headers={"WWW-Authenticate": "Bearer"})

UnauthorizedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden")

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found")

ReviewNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Review not found")

NoStaffInTheDatabaseException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="How did that happen?")

CannotDeleteCurrentUserException = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Cannot delete current user")

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with such email address already exists")

UnsupportedMediaType = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Unsupported file type",
    )

def FileSizeCapOverflowException(
    filename: str,
    max_size: Annotated[int, "Maximum size (in BYTES) allowed"]
    ) -> HTTPException:
    """
    args:
        filename: str
        max_size: int (number of bytes)
    """
    return HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail=f"Size of {filename} is bigger than maximum allowed ({max_size} bytes)"
    )