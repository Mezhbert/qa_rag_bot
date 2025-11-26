from dotenv import load_dotenv
import logging
import os
from utlis import load_config
logging.basicConfig(level=logging.INFO)

CONFIG = load_config()
if CONFIG is None:
    exit(1)

ROOT = "../"

load_dotenv()
START_MSG = "Hello! I answer questions about the C11 standard. Please ask your question in English."
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHROMA_DIR=os.join.path(ROOT, "data/chroma_db")
STANDARD_DIR = os.getenv("STANDARD_DIR", "data/standard")
CPP_STANDARD = CONFIG.get("c_standard", {
    "name": "C_11",
    "pdf_url": "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1548.pdf",
    "local_pdf_path": os.path.join(STANDARD_DIR, "n1548.pdf")
})
