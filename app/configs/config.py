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
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REVIEWS_ON_PAGE_LIMIT: int
    STAFF_ON_PAGE_LIMIT: int
    MAXIMUM_UPLOAD_FILE_SIZE_BYTES: int
    WEB_APP_URL: str
    FRONTEND_PORT: str
    BACKEND_PORT: str

    @property
    def DATABASE_URL_ASYNC(self):
        return f"{self.DATABASE}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SECRET_KEY(self):
        return self.SECRET_KEY
    
    @property
    def ALGORITHM(self):
        return self.ALGORITHM
    
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def REVIEWS_ON_PAGE_LIMIT(self):
        return self.REVIEWS_ON_PAGE_LIMIT
    
    @property
    def STAFF_ON_PAGE_LIMIT(self):
        return self.STAFF_ON_PAGE_LIMIT
    
    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self):
        return self.REFRESH_TOKEN_EXPIRE_DAYS

    @property
    def MAXIMUM_UPLOAD_FILE_SIZE_BYTES(self):
        return self.MAXIMUM_UPLOAD_FILE_SIZE_BYTES
    
    @property
    def WEB_APP_URL(self):
        return self.WEB_APP_URL

    @property
    def FRONTEND_PORT(self):
        return self.FRONTEND_PORT
    
    @property
    def BACKEND_PORT(self):
        return self.BACKEND_PORT
    
    model_config = SettingsConfigDict(env_file=".env")

# Экземпляр кофигурационного класса
settings = Settings()