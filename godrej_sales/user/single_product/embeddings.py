import os
import csv
from analyser.ollama_clients import choose_model, create_vectorstore, OllamaEmbeddings
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from analyser.ollama_clients import choose_model


FAISS_INDEX_FOLDER = 'faiss_index'

def combine_texts(summaries_folder='summaries'):
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

    return combined_text


def save_text_embeddings(text: str, model_name: str = None):
    if model_name is None:
        model_name = choose_model('embedding')

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    # Save chunks
    os.makedirs('summaries', exist_ok=True)
    with open(os.path.join('summaries', 'chunks.pkl'), 'wb') as f:
        pickle.dump(chunks, f)

    embeddings = create_vectorstore(text, model_name)

    with open(os.path.join('summaries', 'embeddings.pkl'), 'wb') as f:
        pickle.dump(embeddings, f)

    print("Saved embeddings and chunks to 'summaries/'")






def load_embeddings_locally(file_path='summaries/embeddings.pkl'):
    if not os.path.exists(file_path):
        print(f"[WARN] Embedding file not found at {file_path}")
        return None
    with open(file_path, 'rb') as f:
        embeddings = pickle.load(f)
    print(f"[INFO] Loaded embeddings from {file_path}")
    return embeddings


def store_embeds():
    save_text_embeddings(combine_texts(),None)

# store_embeds()






