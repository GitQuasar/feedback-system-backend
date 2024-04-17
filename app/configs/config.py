from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Берём информацию из файла .env
    DATABASE: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str 
    DB_NAME: str

    @property
    def DATABASE_URL_async(self):
        # DSN
        return f"{self.DATABASE}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

# Класс, откуда берем ссылку для подключения к БД
settings = Settings()