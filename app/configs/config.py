from pydantic_settings import BaseSettings, SettingsConfigDict

# Класс, предоставляющий конфигурационную информацию
class Settings(BaseSettings):
    # Берём информацию из файла .env
    DATABASE: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET: str

    @property
    def DATABASE_URL_ASYNC(self):
        # DSN
        return f"{self.DATABASE}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SECRET(self):
        return self.SECRET
    
    model_config = SettingsConfigDict(env_file=".env")

# Экземпляр кофигурационного класса
settings = Settings()