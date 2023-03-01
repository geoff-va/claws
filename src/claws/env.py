from pathlib import Path

from dotenv import dotenv_values


class EnvReader:
    def __init__(self, env_path: Path) -> None:
        self.data = dotenv_values(env_path)
