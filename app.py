import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# =========================
# Production Configuration
# =========================

app.config.update(

    # Secret Key from .env
    SECRET_KEY=os.getenv("SECRET_KEY"),

    # Database URL from .env
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),

    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    # Secure Session Settings (Production Safe)
    SESSION_COOKIE_SECURE=True,      # Only send cookies over HTTPS
    SESSION_COOKIE_HTTPONLY=True,    # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE="Lax"    # CSRF protection layer
)
