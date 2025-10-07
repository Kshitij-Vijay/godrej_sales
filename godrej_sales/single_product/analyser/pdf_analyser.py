from analyser.ollama_clients import *
from analyser.pdf_extractor import extract_pdf_content
def embed_pdf(pdf_path):
    pdf_content = extract_pdf_content(pdf_path)

    print(f"[INFO] Extracted {len(pdf_content.texts)} text blocks, {len(pdf_content.images)} images, {len(pdf_content.tables)} tables.")

    # Combine all texts and tables into one large text for vectorstore creation
    text = "\n\n".join([tb.text for tb in pdf_content.texts] + [tbl.content for tbl in pdf_content.tables])

    # Select Ollama embedding model
    embed_model = choose_model("embedding")
    print(f"[INFO] Using embedding model: {embed_model}")

    embedding_vectors = create_vectorstore(text, model_name=embed_model)

    return embedding_vectors  # list of lists of floats