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
    conf = TomlConf(Path("test-conf.toml"))
    for k, v in env.data.items():
        fields = conf._doc.get("fields", {})
        log.info(f"Doing: {k=}")
        if k not in fields:
            conf.add_field(k, type="string", location=k, default=v)
            conf._doc.add(tk.nl())
    conf.dump()


@cli.command()
def sync():
    click.echo("sync")


cli.add_command(create)
cli.add_command(sync)

"""
- read .toml if it exists
- Doesn't exist,
- read the target .env file

"""
