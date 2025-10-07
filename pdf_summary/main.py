from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import BaseRetriever, Document
from langchain_ollama import OllamaLLM
from langchain.vectorstores.base import BaseRetriever
from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from typing import List

from langchain.schema import BaseRetriever
from langchain.schema import Document
from typing import List

class SimpleRetriever(BaseRetriever):
    def __init__(self, docs: List[Document]):
        self.docs = docs

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Return all docs (no retrieval)
        return self.docs


def setup_simple_chat(pdf_path):
    # Load and split PDF into chunks
    loader = PyPDFLoader(pdf_path)
    docs = loader.load_and_split()

    # Initialize the Ollama smollm2 LLM
    llm = OllamaLLM(model="smollm2")

    # Create our custom retriever
    retriever = SimpleRetriever(docs)

    # Use simple buffer memory to keep conversation context
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Setup conversational chain
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
    )

    return chat_chain

# Example usage
chat_chain = setup_simple_chat("zurina_bed.pdf")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    answer = chat_chain.run(user_input)
    print("Bot:", answer)
