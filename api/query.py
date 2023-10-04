from ariadne import convert_kwargs_to_snake_case
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = "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"


@convert_kwargs_to_snake_case
def query_text(obj, info, query):
    persist_directory = 'db'
    embedding = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True)

    llm_response = qa_chain(query)
    return process_llm_response(llm_response)


def process_llm_response(llm_response):
    return llm_response['result']
