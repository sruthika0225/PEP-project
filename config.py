from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    DATABASE_PATH = BASE_DIR / "database" / "tasks.db"
    SECRET_KEY = "change-this-secret-key"
