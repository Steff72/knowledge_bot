import os
from typing import Any, List, Dict


from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_openai import OpenAIEmbeddings

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient

chat = ChatOpenAI(verbose=True, temperature=0, model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Initialize Pinecone client and index
pc = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("edw-knowledge-bot")

vectordb = PineconeVectorStore(index=index, embedding=embeddings, text_key="text", namespace="default")

# Define a QA prompt that includes full chat history and retrieved context
qa_prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template="""
You are a helpful assistant. Use the entire conversation history and the retrieved context to answer the user's question.

Conversation History:
{chat_history}

Retrieved Context:
{context}

Question: {question}
Answer:
"""
)

# Create a runnable sequence: template followed by chat model
chain = qa_prompt | chat

# Use in-memory list for chat history to replace deprecated ConversationBufferMemory
memory_history: list = []

# Setup retriever for manual retrieval + generation
# retriever = vectordb.as_retriever(search_kwargs={"k": 10})


def run_llm(prompt: str):
    # Automatically clear memory after 5 user questions
    human_count = sum(1 for m in memory_history if isinstance(m, HumanMessage))
    if human_count >= 5:
        memory_history.clear()

    # Retrieve relevant documents directly from the vector store
    docs = vectordb.similarity_search(prompt, k=20)
    context = "\n\n".join([doc.page_content for doc in docs])
    # Debug: print the retrieved context passed to the LLM
    print("=== Debug: Context passed to LLM ===")
    print(context)
    print("=== End Debug Context ===")

    # Build conversation history string
    history = "\n".join(
        [
            f"User: {m.content}" if isinstance(m, HumanMessage) else f"Assistant: {m.content}"
            for m in memory_history
        ]
    )

    raw_output = chain.invoke({"chat_history": history, "context": context, "question": prompt})
    # Ensure we extract the text and message correctly
    if isinstance(raw_output, AIMessage):
        text = raw_output.content
        msg = raw_output
    else:
        text = raw_output
        msg = AIMessage(content=text)
    # Save to memory
    memory_history.append(HumanMessage(content=prompt))
    memory_history.append(msg)
    return {"answer": text, "source_documents": docs}


if __name__ == "__main__":
    print(run_llm("What is DH?"))
