import click
import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .decorators import database_connection


@database_connection
def create_database(conn, database_name):
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {database_name};")
    click.echo(f'database "{database_name}" created')


@database_connection
def drop_database(conn, database_name):
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE {database_name};")
    click.echo(f'database "{database_name}" dropped')


@database_connection
def list_databases(conn):
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    databases = "\n".join([row[0] for row in cur.fetchall()])
    click.echo(databases)


@database_connection
def create_database_user(conn, username, password):
    cur = conn.cursor()
    cur.execute(f"CREATE ROLE {username} WITH LOGIN PASSWORD '{password}';")
    conn.commit()
    click.echo(f'user/role "{username}" created')


@database_connection
def drop_database_user(conn, username):
    cur = conn.cursor()
    cur.execute(f"DROP ROLE {username};")
    conn.commit()
    click.echo(f'user/role "{username}" dropped')


@database_connection
def list_users(conn):
    query = """
    SELECT usename,
    CASE
     WHEN usesuper AND usecreatedb THEN 
	   CAST('superuser, create database' AS pg_catalog.text)
     WHEN usesuper THEN 
	    CAST('superuser' AS pg_catalog.text)
     WHEN usecreatedb THEN 
	    CAST('create database' AS pg_catalog.text)
     ELSE 
	    CAST('' AS pg_catalog.text)
    END
    FROM pg_catalog.pg_user
    ORDER BY usename desc;
    """
    cur = conn.cursor()
    cur.execute(query)
    users = "\n".join(
        [
            row[0] + ("" if row[1] == "" else " > " + row[1])
            for row in cur.fetchall()
        ]
    )
    click.echo(users)
