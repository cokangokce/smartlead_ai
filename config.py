import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-key")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    DATABASE_PATH = os.getenv(
        "DATABASE_PATH", str(Path(__file__).resolve().parent / "smartlead.db")
    )
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"