from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    DATABASE_URL: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str  
    DATABASE_PASSWORD: str