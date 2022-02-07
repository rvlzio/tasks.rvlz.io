import click

from .decorators import token_store_connection


@token_store_connection
def create_user(conn, username, password):
    passwords = ["+" + password]
    commands = [
        "+hget",
        "+hmget",
        "+hset",
        "+del",
        "+select",
        "+del",
        "+ping",
    ]
    keys = ["tk_id:*"]
    conn.acl_setuser(
        username,
        enabled=True,
        passwords=["+" + password],
        commands=commands,
        keys=keys,
    )
    click.echo(f'user "{username}" created')


@token_store_connection
def delete_user(conn, username):
    conn.acl_deluser(username)
    click.echo(f'user "{username}" deleted')


@token_store_connection
def list_users(conn):
    users = conn.acl_users()
    click.echo("\n".join(users))
