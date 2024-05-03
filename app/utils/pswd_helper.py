import bcrypt

# Хэширование пароля с использванием bcrypt
def hash_password(password: str):
    hash: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash

# Проверка переданного пароля и сохранённой хэш-строки на совпадение
def verify_password(plain_password: str, hashed_password: bytes):
    return bcrypt.checkpw(password=plain_password.encode('utf-8') , hashed_password=hashed_password)