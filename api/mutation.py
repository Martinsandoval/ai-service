from ariadne import convert_kwargs_to_snake_case
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

os.environ["OPENAI_API_KEY"] = "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"


@convert_kwargs_to_snake_case
def generate_new_embedding(obj, info, document):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.create_documents(document)
    persist_directory = 'db'

    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(documents=texts,
                                     embedding=embedding,
                                     persist_directory=persist_directory)

    vectordb.persist()

    return {
        "success": True,
        "errors": []
    }
