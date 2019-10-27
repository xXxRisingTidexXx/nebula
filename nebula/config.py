from pathlib import Path
from typing import Dict, Any
from yaml import safe_load
from nebula.trafarets import config_trafaret

PROJECT_PATH = Path(__file__).parent.parent

CONFIG_PATH = PROJECT_PATH / 'config/dev.yaml'


def _get_config() -> Dict[str, Any]:
    with open(str(CONFIG_PATH)) as stream:
        config = safe_load(stream.read())
        config_trafaret.check(config)
        return config


CONFIG = _get_config()

DSN = (
    f'postgresql+psycopg2://'
    f'{CONFIG["database"]["user"]}:'
    f'{CONFIG["database"]["password"]}@'
    f'{CONFIG["database"]["host"]}:'
    f'{CONFIG["database"]["port"]}/'
    f'{CONFIG["database"]["database"]}'
)
