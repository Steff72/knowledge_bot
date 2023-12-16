import os
from typing import Any, List, Dict

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Pinecone
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.document_loaders import PyPDFLoader


import pinecone

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="gcp-starter")

chat = ChatOpenAI(verbose=True, temperature=0, model="gpt-4")
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(
    index_name="a340-index", embedding=embeddings
)

sources = ["data/EDW CSPM Rev37.pdf", "data/EDW FCOM A340 15SEP23.pdf", "data/EDW FCTM A340 01SEP23.pdf", "data/EDW OM A Rev50.pdf"]
documents = []

for source in sources:
        loader = PyPDFLoader(source)
        documents.extend(loader.load())

bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5

ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, docsearch.as_retriever(search_kwargs={"k": 5})], weights=[0.5, 0.5])


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=ensemble_retriever,
        return_source_documents=True,
    )
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    print(run_llm("What is DH?"))
