import os
import csv
from analyser.ollama_clients import choose_model, create_vectorstore
import pickle

def load_and_embed_summaries(summaries_folder='summaries'):
    combined_text = ""

    # Load .txt files and concatenate their text
    for file_name in os.listdir(summaries_folder):
        file_path = os.path.join(summaries_folder, file_name)
        if file_name.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n\n"

        # For CSV files, we convert each row to text and concatenate
        elif file_name.lower().endswith('.csv'):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert the whole row into a formatted string
                    row_text = "; ".join(f"{k}: {v}" for k, v in row.items())
                    combined_text += row_text + "\n"

                combined_text += "\n"

    print(f"[INFO] Loaded text length from summaries: {len(combined_text)} characters")

    # Choose embedding model from Ollama
    embed_model = choose_model("embedding")
    print(f"[INFO] Using embedding model: {embed_model}")

    # Generate embedding vectors for the combined text
    embedding_vectors = create_vectorstore(combined_text, model_name=embed_model)

    print("[INFO] Created embedding vectors.")

    return embedding_vectors


def save_embeddings_locally(embedding_vectors, file_path='summaries/embeddings.pkl'):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        pickle.dump(embedding_vectors, f)
    print(f"[INFO] Embeddings saved locally at {file_path}")

def load_embeddings_locally(file_path='summaries/embeddings.pkl'):
    if not os.path.exists(file_path):
        print(f"[WARN] Embedding file not found at {file_path}")
        return None
    with open(file_path, 'rb') as f:
        embeddings = pickle.load(f)
    print(f"[INFO] Loaded embeddings from {file_path}")
    return embeddings


def store_embeds():
    embeddings = load_and_embed_summaries()
    save_embeddings_locally(embeddings)

store_embeds()






