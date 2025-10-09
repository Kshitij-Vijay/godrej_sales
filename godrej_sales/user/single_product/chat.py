from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM,OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import pickle
from analyser.ollama_clients import choose_model
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def llm_chain(llm_model: str = None, embedding_model: str = "nomic-embed-text"):
    if llm_model is None:
        llm_model = choose_model('llm')

    # Load chunks and create vectorstore
    with open('summaries/chunks.pkl', 'rb') as f:
        chunks = pickle.load(f)
    embeddings = OllamaEmbeddings(model=embedding_model)
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Initialize the LLM
    llm = OllamaLLM(model=llm_model)

    # Setup conversation memory buffer
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create conversational retrieval chain that integrates memory, retrieval, and LLM
    chatbot = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=False
    )
    return chatbot


def chatbot():
    qa_chain = llm_chain()
    while True:
        q = input("Enter query, [type 'exit' to quit] : ")
        if q=="exit":
            break
        else: 
            ans = qa_chain.run(q)
            print(ans)



# Example usage:
# chatbot()