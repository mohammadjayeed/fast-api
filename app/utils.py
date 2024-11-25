import os
from dotenv import load_dotenv
def load_env_variables():
    load_dotenv(override=True)  # Reloads the .env file and overrides existing values

    host = os.getenv("HOST")
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    return host, database, user, password