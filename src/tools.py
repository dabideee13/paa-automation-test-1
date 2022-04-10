import json
import time
import random
from typing import Optional
from pathlib import Path


def wait(low: Optional[float] = None, high: Optional[float] = None) -> None:
    if low is None:
        low = 0.4

    if high is None:
        high = 5

    if low > high:
        high = low + 1

    time.sleep(random.uniform(low, high))


def get_config() -> dict[str, str]:

    def format_download_path(path: str) -> Path:
        return Path.joinpath(Path.cwd(), path)

    with open('config.json', 'r') as f:
        config_data = json.load(f)

    config_data['download_path'] = format_download_path(config_data['download_path'])
    return config_data


def get_credentials() -> dict[str, str]:
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials


if __name__ == '__main__':
    print(get_config(), '\n')
    print(get_credentials(), '\n')
