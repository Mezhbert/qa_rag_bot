from typing import Any
import logging
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.constants import CHROMA_DIR, CONFIG
from langchain_ollama import OllamaLLM
from langchain.schema import BaseRetriever

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helper bot for the C11 standard.\n"
        "Answer strictly based on the provided context from the standard.\n"
        "If there is no information in the context, say: 'No information on this question in the standard.'\n"
        "No assumptions.\n\n"
        "CONTEXT:\n{context}\n\n"
        "QUESTION: {question}\n\n"
        "ANSWER:"
    )
)

class LoggingRetriever(BaseRetriever):
    retriever: BaseRetriever

    def get_relevant_documents(self, query: str) -> Any:
        logging.info(f"[Retriever] Поиск документов по запросу: {query}")
        docs = self.retriever.get_relevant_documents(query)
        logging.info(f"[Retriever] Найдено документов: {len(docs)}")
        for i, d in enumerate(docs):
            logging.debug(f"[Retriever] Документ {i}: {d.page_content[:200].replace(chr(10), ' ')}...")
        return docs


def get_llm():
    llm_config = CONFIG["llm"]
    logging.info("[LLM] Используется Ollama локальная модель: %s", llm_config["model_name"])
    return OllamaLLM(model=llm_config["model_name"])


def get_standard_qa_chain():
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = LoggingRetriever(retriever=db.as_retriever(search_kwargs={"k": 3}))


    llm = get_llm()

    return RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_PROMPT},
        input_key="query"
    )
