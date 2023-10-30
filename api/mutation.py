from ariadne import convert_kwargs_to_snake_case
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os
import logging
from utils.process import write_code_from_response

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


def create_embeddings_from_project(obj, info, repo_path, file_extensions, use_default_db):
    docs = []
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for file in filenames:
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in file_extensions:
                try:
                    loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                    docs.extend(loader.load_and_split())
                except Exception as e:
                    logging.exception(e)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    if use_default_db:
        persist_directory = 'db'
    else:
        persist_directory = 'db_code'

    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(documents=texts,
                                     embedding=embedding,
                                     persist_directory=persist_directory)
    vectordb.persist()

    return {
        "result": True,
        "errors": []
    }

@convert_kwargs_to_snake_case
def get_answer_for_question_and_create_file(obj, info, question, directory_path, filename="new_file"):
    persist_directory = 'db_code'
    embedding = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    model = ChatOpenAI(model='gpt-3.5-turbo')
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

    chat_history = []

    result = qa({"question": question, "chat_history": chat_history})

    code_result = write_code_from_response(result['answer'], directory_path, filename)
    if code_result == 1:
        return {
            "result": f"File '{filename}' successfully created in '{directory_path}'",
            "errors": []
        }
    else:
        return {
            "result": "Fail",
            "errors": []
        }
