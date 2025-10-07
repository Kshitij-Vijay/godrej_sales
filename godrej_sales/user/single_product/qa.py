import json
import numpy as np
from langchain_ollama import OllamaLLM
from analyser.ollama_clients import choose_model
from sklearn.metrics.pairwise import cosine_similarity


METADATA_JSON = "metadata/all_metadata.json"  # Combined metadata file


def load_metadata():
    with open(METADATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def find_most_relevant(metadata, query_embedding, top_k=1):
    embeddings = []
    contexts = []
    paths = []
    for item in metadata:
        # Average chunk embeddings (if list of lists)
        avg_embedding = np.mean(item["embedding"], axis=0)
        embeddings.append(avg_embedding)
        contexts.append(item["description"])
        paths.append(item["path"])

    embeddings = np.array(embeddings)
    query_embedding = np.array(query_embedding).reshape(1, -1)

    similarities = cosine_similarity(query_embedding, embeddings).flatten()
    top_idxs = similarities.argsort()[-top_k:][::-1]

    # Return full info (context + file path + similarity score)
    return [(contexts[i], paths[i], similarities[i]) for i in top_idxs]


def embed_query(text, embedding_model):
    from analyser.text_analyser import embed_text
    return embed_text(text)


def main():
    metadata = load_metadata()
    llm_model_name = choose_model("llm")
    llm = OllamaLLM(model=llm_model_name)

    print("\nType 'exit' to quit.\n")
    while True:
        query = input("Enter your question: ").strip()
        if query.lower() == "exit":
            break
        try:
            query_embedding = embed_query(query, llm_model_name)
            relevant = find_most_relevant(metadata, query_embedding, top_k=3)

            prompt = "Use the following context to answer the question:\n\n"
            for context, path, score in relevant:
                prompt += f"- {context} (from file: {path}, similarity: {score:.3f})\n"
            prompt += f"\nQuestion: {query}\nAnswer:"

            response = llm.generate([prompt])
            answer = response.generations[0][0].text
            print("\nAnswer:\n" + answer + "\n")

        except Exception as e:
            print("Error:", e)


def qa():
    main()

if __name__ == "__main__":
    main()
