from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_USER: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_TIME: int

    @property
    def database_url(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings() # type: ignore