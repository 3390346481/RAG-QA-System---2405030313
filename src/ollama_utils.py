from langchain_ollama import OllamaLLM, OllamaEmbeddings

def get_ollama_llm(model_name: str = "deepseek-r1:7b") -> OllamaLLM:
    return OllamaLLM(model=model_name)

def get_ollama_embeddings(model_name: str = "nomic-embed-text") -> OllamaEmbeddings:
    return OllamaEmbeddings(model=model_name)

def test_ollama_connection() -> bool:
    try:
        llm = get_ollama_llm()
        response = llm.invoke("Hello, how are you?")
        if response and len(response) > 0:
            print("Ollama connection test successful!")
            print(f"Response: {response[:100]}...")
            return True
        return False
    except Exception as e:
        print(f"Ollama connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_ollama_connection()
