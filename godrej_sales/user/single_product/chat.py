from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM,OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import pickle
from analyser.ollama_clients import choose_model

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

    # Create retrieval QA chain that integrates vectorstore retrieval + LLM generation
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

    return qa_chain


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
chatbot()