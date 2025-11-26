import yaml
import logging

def load_config(path="config.yaml"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Ошибка: файл конфигурации '{path}' не найден.")
        return None