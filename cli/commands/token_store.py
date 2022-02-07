import os

import click

from cli.services import token_store


@click.group("token-store")
def cli():
    pass


@cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user(username, password):
    token_store.create_user(username, password)


@cli.command("delete-user")
@click.argument("username")
def delete_user(username):
    token_store.delete_user(username)


@cli.command("list-users")
def list_users():
    token_store.list_users()
