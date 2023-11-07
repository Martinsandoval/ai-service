from ariadne import convert_kwargs_to_snake_case
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from utils.process import extract_code_from_response

os.environ['OPENAI_API_KEY'] = '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'


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


@convert_kwargs_to_snake_case
def get_code_solution_for_question(obj, info, question):
    persist_directory = 'db_code'
    embedding = OpenAIEmbeddings()

    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    model = ChatOpenAI(model='gpt-4-1106-preview')
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

    chat_history = []

    result = qa({"question": question, "chat_history": chat_history})

    code_blocks = extract_code_from_response(result['answer'])

    if code_blocks.__len__() > 0:
        return {
            "result": code_blocks[0][1],
            "errors": []
        }
    else:
        return {
            "result": result['answer'],
            "errors": []
        }
