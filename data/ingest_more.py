import os
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="gcp-starter")


def ingest_docs() -> None:
    loader = PyPDFLoader("EDW OM A Rev50.pdf")
    documents = loader.load()
    print(f"loaded {len(documents) } documents")

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents, embeddings, index_name="a340-index")

    index = pinecone.Index("fctm-a340-index")
    vectorstore = Pinecone(index, embeddings.embed_query, documents)
    # vectorstore.add_texts("More text!")
    print("****** Added to Pinecone vectorstore vectors")


if __name__ == "__main__":
    ingest_docs()
