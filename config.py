import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = secrets.token_hex(32)
DATABASE_PATH = os.path.join(BASE_DIR, "app.db")
