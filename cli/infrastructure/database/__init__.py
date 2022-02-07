import os

import psycopg2


def read_config(dbname=None):
    host = os.environ["CLI_DATABASE_HOST"]
    dbname = os.environ["CLI_DATABASE_NAME"] if dbname is None else dbname
    user = os.environ["CLI_DATABASE_USERNAME"]
    password = os.environ["CLI_DATABASE_PASSWORD"]
    return {
        "host": host,
        "dbname": dbname,
        "user": user,
        "password": password,
    }


def generate_connection(dbname=None):
    config = read_config(dbname=dbname)
    return psycopg2.connect(**config)
