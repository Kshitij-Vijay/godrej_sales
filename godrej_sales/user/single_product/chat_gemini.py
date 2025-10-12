import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini LLM

def llm_chain(
    embedding_model: str = "nomic-embed-text"
):
    # Load chat chunks (text passages)
    with open('summaries/chunks.pkl', 'rb') as f:
        chunks = pickle.load(f)
    
    # Embedd chunks with Ollama embeddings, must match how you built pkl!
    embeddings = OllamaEmbeddings(model=embedding_model)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    
    # Set up Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3  # Adjust as required
    )
    
    # Setup conversation memory buffer
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Build conversational retrieval chain
    chatbot = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=False
    )
    return chatbot

def chatbot():
    qa_chain = llm_chain()
    print("Chatbot (Gemini LLM) is ready! Type 'exit' to quit.")
    while True:
        q = input("You: ").strip()
        if q.lower() == "exit":
            print("Goodbye!")
            break
        ans = qa_chain.run(q)
        print(f"Bot: {ans}\n")

if __name__ == "__main__":
    # Optionally, set API key here if not set in environment
    # os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
    chatbot()


chatbot()