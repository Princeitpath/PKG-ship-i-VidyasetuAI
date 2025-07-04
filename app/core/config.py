
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()
