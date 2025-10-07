from langchain_ollama import OllamaLLM
from analyser.ollama_clients import choose_model  

def summarize_text(text):
    # Select a model for LLM
    llm_model = choose_model(model_type="llm")
    
    # Initialize the Ollama client for the chosen model
    llm = OllamaLLM(model=llm_model)
    
    # Create the prompt with the user text for summary
    prompt = f"summarise this text very long and dont leave any detail: {text}"
    
    response = llm.generate([prompt])
    answer = response.generations[0][0].text
    print("\nAnswer:\n" + answer + "\n")
    return answer


# print(summarize_text("minu is a cute cat. It is good kitty"))