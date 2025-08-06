# azampay/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the client's current working directory
env_path = Path.cwd() / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    @property
    def ENVIRONMENT(self):
        return os.getenv("AZAMPAY_ENVIRONMENT", "sandbox")

    @property
    def APP_NAME(self):
        return os.getenv("AZAMPAY_APP_NAME")

    @property
    def CLIENT_ID(self):
        return os.getenv("AZAMPAY_CLIENT_ID")

    @property
    def CLIENT_SECRET(self):
        return os.getenv("AZAMPAY_CLIENT_SECRET")
