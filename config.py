import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABSE_PORT = os.getenv("DATABSE_PORT")
SECRET = os.getenv("SECRET")
DISPLAY = os.getenv("DISPLAY")
JWT_SECRET = os.getenv("JWT_SECRET")
