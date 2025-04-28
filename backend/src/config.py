import os

APP_ENV = os.environ.get("APP_ENV", "development")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME","postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD","p@ssword")
DATABASE_HOST = os.environ.get("DATABASE_HOST","localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT","5432")
DATABASE_NAME = os.environ.get("DATABASE_NAME","chat-app-db")

