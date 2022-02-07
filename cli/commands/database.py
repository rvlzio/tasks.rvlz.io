import os

import click

from cli.services import database


@click.group(name="database")
def cli():
    pass


@cli.command("create-database")
@click.argument("database_name")
def create_database(database_name):
    database.create_database(database_name)


@cli.command("drop-database")
@click.argument("database_name")
def drop_database(database_name):
    database.drop_database(database_name)


@cli.command("list-databases")
def list_databases():
    database.list_databases()


@cli.command("create-database-user")
@click.argument("username")
@click.argument("password")
def create_database_user(username, password):
    database.create_database_user(username, password)


@cli.command("drop-database-user")
@click.argument("username")
def drop_database_user(username):
    database.drop_database_user(username)


@cli.command("list-users")
def list_users():
    database.list_users()
