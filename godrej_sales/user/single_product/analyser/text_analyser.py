from analyser.ollama_clients import *
def embed_text(text: str):
    embed_model = choose_model("embedding")
    print(f"[INFO] Using embedding model: {embed_model}")

    embedding_vectors = create_vectorstore(text, model_name=embed_model)

    return embedding_vectors  # list of lists of floats

