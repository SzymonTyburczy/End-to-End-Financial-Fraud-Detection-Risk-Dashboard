from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_NAME: str = "fraud_detection"

    MLFLOW_TRACKING_URI: str = "http://localhost:5000"

    @property
    def db_url(self):
        safe_user = quote_plus(self.DB_USER)
        safe_password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{safe_user}:{safe_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()