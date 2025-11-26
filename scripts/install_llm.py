import requests
import json
import logging
from app.constants import CONFIG
import os

logging.basicConfig(level=logging.INFO)

def install_llm():
    model_name = CONFIG["llm"]["model_name"]
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    url = f"{ollama_host}/api/pull"

    headers = {"Content-Type": "application/json"}
    data = {"name": model_name}

    logging.info(f"Проверка и загрузка модели '{model_name}' через Ollama...")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                message = json.loads(line.decode('utf-8'))
                if "status" in message:
                    logging.info(f"Ollama: {message['status']}")
                if "error" in message:
                    logging.error(f"Ошибка Ollama: {message['error']}")
                    return False

        logging.info(f"Модель '{model_name}' успешно установлена.")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Не удалось подключиться к Ollama на {ollama_host}. Проверьте, запущен ли сервис.")
        logging.error(f"Подробности: {e}")
        return False


if __name__ == "__main__":
    install_llm()
