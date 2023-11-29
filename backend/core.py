import os
from typing import Any, List, Dict

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Pinecone

import pinecone

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="gcp-starter")

chat = ChatOpenAI(verbose=True, temperature=0, model="gpt-4-1106-preview")
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(
    index_name="a340-index", embedding=embeddings
)


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=docsearch.as_retriever(search_kwargs={"k": 20}),
        return_source_documents=True,
    )
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    print(run_llm("What is DH?"))
