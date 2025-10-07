import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings



def choose_model(model_type="llm"):
    resp = ollama.list()
    models = resp.get("models", [])

    if model_type == "embedding":
        models = [m.model for m in models if "embed" in m.model.lower()]
    else:
        models = [m.model for m in models if "embed" not in m.model.lower()]

    if not models:
        print(f"No {model_type} models found in Ollama. Please pull some first!")
        exit(1)

    print(f"\nAvailable {model_type.upper()} models:")
    for idx, model in enumerate(models, 1):
        print(f"{idx}. {model}")

    choice = int(input(f"Select a {model_type} model [1-{len(models)}]: "))
    return models[choice - 1]

def create_vectorstore(text: str, model_name: str = "nomic-embed-text"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    embeddings = OllamaEmbeddings(model=model_name)

    # Use embed_documents method for batch embedding
    embedding_vectors = embeddings.embed_documents(chunks)

    # Optionally create FAISS index if you want
    # vectorstore = FAISS.from_texts(chunks, embeddings)

    return embedding_vectors
