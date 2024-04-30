from datetime import datetime, timedelta
from time import time
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.configs.config import settings

SECRET_KEY = settings.SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# JWT_TOKEN_PREFIX = "Bearer"

class Token:
    acces_token: str = None
    token_type: str = None

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
После проверки пользователя мы генерируем JWT токен для управления сеансом.
Этот токен отправляется обратно пользователю и используется в последующих запросах.
"""

def create_access_token(data: dict) -> str:
    """
    Аргументы:
    data: dict (набор данных, которые нужно зашифровать)
    """

    # Указываем время, после которого токен будет неактивен
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)   
    data.update({"exp": expire})

    # Шифруем токен, используя SECRET_KEY
    # Подписываем токен, используя ALGORITHM
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

"""
Декодирование JWT-токена.
Возвращает декодированные данные, если срок действия токена еще не истек.
В противном случае возвращает None.

Веб-приложение будет запрашивать декодированный токен при каждом запросе, чтобы идентифицировать запрос как авторизованный.
Если запрос авторизованный, то веб-приложение позволяет клиенту получить доступ к защищенному маршруту.
"""

def decode_and_verify_token(token: str):
    """
    Аргументы:
    token: str (строка-токен)
    """
    try:
        payload: dict = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if payload['exp'] >= time():
        return payload
    else:
        return None