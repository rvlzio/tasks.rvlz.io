import functools

import click

from cli.infrastructure import database, token_store


def database_connection(func):
    @functools.wraps(func)
    def connection_wrapper(*args, **kwargs):
        dbname = kwargs.pop("database_name", None)
        conn = None
        try:
            conn = database.generate_connection(dbname=dbname)
            func(conn, *args, **kwargs)
        except Exception as err:
            click.echo(f"Database operation failed.")
            click.echo(f"exception: '{str(err).strip()}'")
        finally:
            if conn is not None:
                conn.close()

    return connection_wrapper


def token_store_connection(func):
    @functools.wraps(func)
    def connection_wrapper(*args, **kwargs):
        conn = None
        try:
            conn = token_store.generate_connection()
            func(conn, *args, *kwargs)
        except Exception as err:
            click.echo(f"Tokenstore operation failed.")
            click.echo(f"exception: '{str(err).strip()}'")
        finally:
            if conn is not None:
                conn.close()

    return connection_wrapper
