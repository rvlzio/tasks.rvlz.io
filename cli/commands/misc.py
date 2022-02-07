import subprocess

import click


@click.group(name="misc")
def cli():
    pass


@cli.command("format")
def format_code():
    command = ["black", "--line-length", "80", "./cli", "./services/api/src"]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout, stderr = process.communicate()
    click.echo(stdout)
