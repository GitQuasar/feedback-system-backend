from os import access
from app.configs.config import settings

SECRET_KEY = settings.SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# JWT_TOKEN_PREFIX = "Bearer"

class Token:
    acces_token: str = None
    token_type: str = None