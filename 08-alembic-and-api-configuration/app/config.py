from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
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

    model_config = SettingsConfigDict(env_file = env_path)

settings = Settings() # type: ignore