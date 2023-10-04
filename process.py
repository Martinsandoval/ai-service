import re
import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

document_id = 1


def process_files(document):
    f = open("myfile.txt", "w")
    f.write(document)

    loader = TextLoader("myfile.txt")
    documents = loader.load()
    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # # create the open-source embedding function
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #
    # # load it into Chroma
    # db = Chroma.from_documents(docs, embedding_function)
    #
    # db.persist()

    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                             persist_directory="local_db"
                                             ))
    collection = chroma_client.get_or_create_collection(name="khoros_posts")


    generate_embeddings(docs, "sarasa", "sarasa", collection)
    chroma_client.persist()

    # print results
    print(chroma_client.get_collection("docs_rust_collection"))
    return True


def generate_embeddings(chunks, document_title, file_name, collection):
    global document_id
    for chunk in chunks:
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": file_name
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        document_id = document_id + 1


def get_title(file):
    match = re.search(r"title:\s+(.+)\s+", file)
    if match:
        title = match.group(1)
        return title
    else:
        " "


def split_text(file):
    separator = "\n### "
    return file.split(separator)


def query_collection(query):
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                             persist_directory="local_db"
                                             ))
    collection = chroma_client.get_or_create_collection(name="my_collection")
    return collection.query(
        query_texts=[query],
        n_results=2,
    )
