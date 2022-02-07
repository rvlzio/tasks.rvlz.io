import os

import redis


def read_config():
    host = os.environ.get("CLI_TOKEN_STORE_HOST")
    db = os.environ.get("CLI_TOKEN_STORE_NAME")
    username = os.environ.get("CLI_TOKEN_STORE_USERNAME")
    password = os.environ.get("CLI_TOKEN_STORE_PASSWORD")
    return {
        "username": username,
        "password": password,
        "host": host,
        "db": db,
    }


def generate_connection():
    config = read_config()
    return redis.Redis(**config, decode_responses=True)
