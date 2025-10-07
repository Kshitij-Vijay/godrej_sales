from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA


def run_chatbot(faiss_index_path="faiss_index", ollama_model_name="smollm2:latest"):
    embeddings = OllamaEmbeddings(model=ollama_model_name)
    vector_store = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)

    llm = OllamaLLM(model=ollama_model_name)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        query = input("You: ").strip()
        if query.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        answer = qa_chain.run(query)
        print(f"Bot: {answer}\n")


if __name__ == "__main__":
    run_chatbot()
