from fastapi import status, HTTPException

InvalidUserTypeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid user type",
    headers={"WWW-Authenticate": "Bearer"})

InactiveUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User is not active")

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid user credentials",
    headers={"WWW-Authenticate": "Bearer"})

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"})

UnauthorizedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden")

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User with such credentials not found",
    headers={"WWW-Authenticate": "Bearer"})

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
    headers={"WWW-Authenticate": "Bearer"})