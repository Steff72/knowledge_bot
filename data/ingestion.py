import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="gcp-starter")


def ingest_docs() -> None:
    sources = ["data/EDW CSPM Rev37.pdf", "data/EDW FCOM A340 15SEP23.pdf", "data/EDW FCTM A340 01SEP23.pdf", "data/EDW OM A Rev50.pdf"]
    documents = []

    for source in sources:
        loader = PyPDFLoader(source)
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    doc_split = text_splitter.split_documents(documents)
    print(f"loaded {len(doc_split) } documents")

    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(doc_split, embeddings, index_name="a340-index")
    print("Docs added to Pinecone vectorstore vectors")


if __name__ == "__main__":
    ingest_docs()
