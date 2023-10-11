from ariadne import convert_kwargs_to_snake_case
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = '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'


@convert_kwargs_to_snake_case
def get_suggestion_for_text(obj, info, text):
    persist_directory = 'db'
    embedding = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True)

    llm_response = qa_chain(text)
    result = llm_response['result']

    return {
        "result": result,
        "errors": []
    }
