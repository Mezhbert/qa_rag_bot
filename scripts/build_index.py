import logging
import os
import requests
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.constants import CONFIG, CPP_STANDARD, CHROMA_DIR

logging.basicConfig(level=logging.INFO)

def download_pdf(url, out_path):
    if os.path.exists(out_path):
        logging.info(f"[download_pdf] Файл уже существует: {out_path}")
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    logging.info(f"[download_pdf] Скачиваем PDF с {url} ...")
    resp = requests.get(url)
    resp.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(resp.content)
    logging.info(f"[download_pdf] Скачивание завершено, файл сохранен: {out_path}")

def pdf_to_text(pdf_path):
    logging.info(f"[pdf_to_text] Извлечение текста из {pdf_path}...")
    text_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_chunks.append(text)
    return "\n".join(text_chunks)


def build_index():
    if os.path.exists(CHROMA_DIR):
        logging.info(f"[build_index] Каталог базы {CHROMA_DIR} уже существует — удалите для пересборки.")
        return

    if CONFIG.get("cache_pdf", True):
        download_pdf(CPP_STANDARD["pdf_url"], CPP_STANDARD["local_pdf_path"])
    else:
        if not os.path.exists(CPP_STANDARD["local_pdf_path"]):
            raise FileNotFoundError(f"PDF файл стандарта не найден: {CPP_STANDARD['local_pdf_path']}")

    text = pdf_to_text(CPP_STANDARD["local_pdf_path"])

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = text_splitter.create_documents([text])

    logging.info(f"[build_index] Создано чанков: {len(docs)}")

    embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")
    _ = Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_DIR)

    logging.info("[build_index] Индекс построен и сохранён в %s", CHROMA_DIR)


if __name__ == "__main__":
    build_index()
