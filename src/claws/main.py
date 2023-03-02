import logging
import sys
from pathlib import Path

import click
import tomlkit as tk

from .conf import TomlConf
from .env import EnvReader

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

log = logging.getLogger(__name__)


@click.group()
def cli():
    """CLAWS"""


@cli.command()
@click.argument("path")
def create(path):
    """Create a new toml conf file from existing config file"""
    # TODO: factory to get correct reader type based on file path
    env = EnvReader(Path(path))
    conf = TomlConf(Path("test_confs/test-conf.toml"))
    conf.create(env)


@cli.command()
def sync():
    click.echo("sync")


@cli.command()
@click.argument("path")
def validate(path):
    env = EnvReader(Path(path))
    conf = TomlConf(Path("test_confs/test-conf.toml"))
    conf.validate(env.data)


cli.add_command(create)
cli.add_command(sync)
