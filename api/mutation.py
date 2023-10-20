from ariadne import convert_kwargs_to_snake_case
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import os
import logging


os.environ["OPENAI_API_KEY"] = "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"


@convert_kwargs_to_snake_case
def create_embedding(obj, info, document):
    arr_docs = [document]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.create_documents(arr_docs)
    persist_directory = 'db'

    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(documents=texts,
                                     embedding=embedding,
                                     persist_directory=persist_directory)

    vectordb.persist()

    return {
        "result": True,
        "errors": []
    }


def create_embeddings_from_project(obj, info, repo_path):
    docs = []
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for file in filenames:
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e:
                logging.exception(e)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    persist_directory = 'db'

    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(documents=texts,
                                     embedding=embedding,
                                     persist_directory=persist_directory)
    vectordb.persist()

    return {
        "result": True,
        "errors": []
    }
