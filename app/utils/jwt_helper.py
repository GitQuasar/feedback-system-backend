from jose import jwt
from datetime import datetime, timedelta, timezone

from app.configs.config import settings

"""
JWT-токен - строка зашифрованных данных, состоящая из трех частей, которые разделены точкой:
Header.Payload.Signature

- Header (заголовок) - информация о токене.
    Выглядит примерно так:
        {
            "typ": "JWT", (тип токена)
            "alg": "HS256" (алгоритм подписи токена)
        }

- Payload (нагрузка, т.е. полезные данные) — собственно, данные, которые мы хотим передать в токене.
    Выглядит примерно так:
        {
            "dataname1": "some_data",
            "dataname2": "some_data",
            "dataname3": "some_data",
            "iat": xxxxxxxxxx (дата создания токена) (опционально)
            "exp": xxxxxxxxxx (время жизни токена, по истечению которого токен не будет приниматься)
        }

- Signature (подпись) — подпись токена.
Подпись позволяет определить, не был ли изменен токен при передаче.
Каждое веб-приложение имеет собственную подпись.

Данные изначально представлены в виде JSON-объекта.
Для передачи в виде JWT эти данные преобразуются в строку и шифруются.

Простейший сценарий использования JWT-токенов следующий:

1. Пользователь Регистрируется/Входит в систему, ему выдается токен;

2. Токен сохраняется на стороне клиента;

3. Каждый следующий свой запрос клиент делает с заголовком:
Authorization: Bearer <token>

4. Сервер, получая запрос с таким заголовком, проверяет его валидность. И в случае успеха отправляет запрашиваемый контент.
"""

"""
Создание JWT-токена.
После проверки пользователя мы генерируем JWT токен для управления сеансом.
Этот токен отправляется обратно пользователю и используется в последующих запросах.
"""

"""
Декодирование JWT-токена.
Возвращает декодированные данные, если срок действия токена еще не истек.
В противном случае возвращает None.

Веб-приложение будет запрашивать декодированный токен при каждом запросе, чтобы идентифицировать запрос как авторизованный.
Если запрос авторизованный, то веб-приложение позволяет клиенту получить доступ к защищенному маршруту.
"""

ACCESS_TOKEN_TYPE: str = "Access"
REFRESH_TOKEN_TYPE: str = "Refresh"

# Кодирование набора данных в виде JWT
def encode_jwt(payload: dict):
    token: str = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

# Декодирование JWT в набор данных
def decode_jwt(token: str):
    payload: dict = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return payload

# Создание acces_token-а на основе переданного набора данных
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload.update(
        # Тип токена
        token_type=ACCESS_TOKEN_TYPE,
        # Время создания токена
        iat=now,
        # Время жизни токена
        exp=expire
    )
    access_token: str = encode_jwt(payload)
    return access_token

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload.update(
        # Тип токена
        token_type=REFRESH_TOKEN_TYPE,
        # Время создания токена
        iat=now,
        # Время жизни токена
        exp=expire
    )
    access_token: str = encode_jwt(payload)
    return access_token

# def verify_refresh_token(token:str):
#     # credential_exception = HTTPException(
#     #     status_code=status.HTTP_401_UNAUTHORIZED,
#     #     detail="Could not validate credentials",
#     #     headers={"WWW-Authenticate": "Bearer"}        
#     # )
#     try:
#         payload = decode_jwt(token)
#         id: str = payload.get("id")
#         if id is None:
#             raise http_exceptions
#         token_data = TokenData(id=id)
#     except JWTError:
#         raise credential_exception

#     return token_data

# def get_new_access_token(token:str):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate refresh credentials",
#         headers={"WWW-Authenticate": "Bearer"}        
#     )
#     token_data = verify_refresh_token(token, credentials_exception)
#     return create_access_token(token_data)