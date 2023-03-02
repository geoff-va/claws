import logging
from pathlib import Path

from dotenv import dotenv_values

log = logging.getLogger(__name__)


class EnvReader:
    def __init__(self, env_path: Path) -> None:
        self.data = dotenv_values(env_path)
        log.info("Loaded %s", env_path)
