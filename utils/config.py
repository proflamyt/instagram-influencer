from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    SECRET_KEY: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'
        


settings = Settings()

