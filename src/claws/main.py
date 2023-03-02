import logging
import sys
from pathlib import Path

import click

from .conf import TomlConf
from .conf_readers import conf_reader_factory
from .env import EnvReader

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

log = logging.getLogger(__name__)


@click.group()
def cli():
    """CLAWS"""


@cli.command()
@click.argument("path")
def sync(path):
    """Syncrhonize or create a new claws-conf file with its config file"""
    path = Path(path)
    reader = conf_reader_factory(path.suffix)
    conf_data = reader(path)
    conf = TomlConf(Path("test_confs/test-conf.toml"))
    conf.create(conf_data)


@cli.command()
@click.argument("path")
def validate(path):
    env = EnvReader(Path(path))
    conf = TomlConf(Path("test_confs/test-conf.toml"))
    conf.validate(env.data)


cli.add_command(sync)
cli.add_command(validate)
