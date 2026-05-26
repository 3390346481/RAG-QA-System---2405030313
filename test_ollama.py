from src.ollama_utils import test_ollama_connection

if __name__ == "__main__":
    print("Testing Ollama connection...")
    success = test_ollama_connection()
    if success:
        print("Ollama API is working correctly!")
    else:
        print("Failed to connect to Ollama. Please ensure Ollama is installed and running.")
