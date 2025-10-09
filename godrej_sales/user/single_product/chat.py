from langchain.chains import RetrievalQA
from langchain_ollama import Ollama
from langchain_community.vectorstores import FAISS

def ask_based_on_embeddings(question: str, llm_model: str = None, embedding_model: str = "nomic-embed-text"):
    if llm_model is None:
        llm_model = choose_model('llm')

    # Load chunks and create vectorstore
    with open('summaries/chunks.pkl', 'rb') as f:
        chunks = pickle.load(f)
    embeddings = OllamaEmbeddings(model=embedding_model)
    vectorstore = FAISS.from_texts(chunks, embeddings)

    # Initialize the LLM
    llm = Ollama(model=llm_model)

    # Create retrieval QA chain that integrates vectorstore retrieval + LLM generation
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

    # Ask the question, chain uses embeddings fully internally
    answer = qa_chain.run(question)

    return answer



# Example usage:
print(chatbot("What is the main topic of the text?"))
