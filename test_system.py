# test_system.py
# test_system.py
import os
from dotenv import load_dotenv

load_dotenv()

def print_separator(title):
    print("\n" + "="*50)
    print(f"  {title}")
    print("="*50)

def test_vector_db():
    print_separator("TEST 1: Vector Database")
    persist_dir = os.environ.get("CHROMA_PERSIST_DIR", "./vector_db")
    collection_name = os.environ.get("COLLECTION_NAME", "financial_mathematics_library")
    
    import chromadb
    from chromadb.utils import embedding_functions

    client = chromadb.PersistentClient(path=persist_dir)
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_collection(name=collection_name, embedding_function=embedding_fn)
    
    count = collection.count()
    print(f"[OK] Collection '{collection_name}' verified with {count} vectors.")
    return True

def test_gemini():
    print_separator("TEST 2: Google Gemini 3.5 Flash-Lite")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    gemini_model = os.environ.get("GEMINI_MODEL_NAME", "gemini-3.5-flash-lite")

    from google import genai
    client = genai.Client(api_key=gemini_key)
    
    response = client.models.generate_content(
        model=gemini_model,
        contents="Reply with 'Gemini Connection OK'"
    )
    print(f"Response: {response.text.strip()}")
    print("[PASS] Gemini is verified and ready.")
    return True

def test_full_pipeline():
    print_separator("TEST 3: End-to-End Two-Stage Pipeline")
    from rag_pipeline import run_financial_rag
    
    query = "Derive the Black-Scholes differential equation using Itô's Lemma and delta hedging."
    output = run_financial_rag(query=query, top_k=5, output_file="test_output.md")
    
    word_count = len(output.split())
    print(f"\n[Generated Output Length]: ~{word_count} words")
    print("[PASS] Full pipeline run succeeded! Open 'test_output.md' to see the result.")

if __name__ == "__main__":
    if test_vector_db() and test_gemini():
        test_full_pipeline()