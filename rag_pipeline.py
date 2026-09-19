# rag_pipeline.py
# rag_pipeline.py
# rag_pipeline.py
# rag_pipeline.py
import os
from dotenv import load_dotenv

load_dotenv()

import chromadb
from chromadb.utils import embedding_functions
from google import genai
from google.genai import types

from config import PipelineConfig
from templates import (
    LLM1_SYSTEM_PROMPT, 
    LLM1_USER_TEMPLATE, 
    LLM2_SYSTEM_PROMPT, 
    LLM2_USER_TEMPLATE
)

# ---------------------------------------------------------------------------
# 1. Vector DB Retriever
# ---------------------------------------------------------------------------
class RAGRetriever:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_collection(
            name=collection_name, 
            embedding_function=self.embedding_fn
        )

    def retrieve(self, query: str, top_k: int = 5) -> str:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        context_blocks = []
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            block = (
                f"[Source {i+1}]\n"
                f"Book: {meta.get('book_title', 'Unknown')}\n"
                f"Page: {meta.get('page_number', 'N/A')}\n"
                f"Excerpt:\n{doc}\n"
            )
            context_blocks.append(block)
            
        return "\n".join(context_blocks)


# ---------------------------------------------------------------------------
# 2. Stage 1: Prompt Synthesizer & Notation Harmonizer (Template 1)
# ---------------------------------------------------------------------------
def call_llm1_stage(client: genai.Client, model_name: str, user_query: str, retrieved_context: str) -> str:
    prompt = LLM1_USER_TEMPLATE.format(
        user_query=user_query,
        retrieved_context=retrieved_context
    )
    
    print(f"[Stage 1] Verifying context and harmonizing notation with {model_name}...")
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=LLM1_SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=1500
        )
    )
    return response.text


# ---------------------------------------------------------------------------
# 3. Stage 2: Deep Mathematical & Financial Reasoner (Template 2)
# ---------------------------------------------------------------------------
def call_llm2_stage(client: genai.Client, model_name: str, llm1_output: str) -> str:
    prompt = LLM2_USER_TEMPLATE.format(llm1_output=llm1_output)
    
    print(f"[Stage 2] Generating ~1,500-word mathematical derivation with {model_name}...")
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=LLM2_SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=4096
        )
    )
    return response.text


# ---------------------------------------------------------------------------
# 4. Master Orchestrator
# ---------------------------------------------------------------------------
def run_financial_rag(query: str, top_k: int = 5, output_file: str = "output.md"):
    cfg = PipelineConfig()
    gemini_key = os.environ.get("GEMINI_API_KEY")
    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-3.5-flash-lite")
    
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is not set in your .env file.")

    client = genai.Client(api_key=gemini_key)
    retriever = RAGRetriever(
        persist_dir=cfg.CHROMA_PERSIST_DIR, 
        collection_name=cfg.COLLECTION_NAME
    )
    
    print(f"\n[Query] {query}")
    print(f"[Search] Retrieving top {top_k} relevant excerpts from 25,871 vectors...")
    context = retriever.retrieve(query, top_k=top_k)
    
    # Stage 1: LLM 1 checks relevance, cleans notation, builds prompt
    structured_spec = call_llm1_stage(client, model_name, query, context)
    
    # Stage 2: LLM 2 creates the ~1,500-word math breakdown with variable definitions
    final_output = call_llm2_stage(client, model_name, structured_spec)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_output)
        
    print(f"\n[Done] Analysis completed and saved to '{output_file}'!")
    return final_output


if __name__ == "__main__":
    test_query = "Derive the Black-Scholes PDE using Itô's Lemma, explain delta-hedging, and define all variables."
    run_financial_rag(test_query, top_k=5, output_file="test_output.md")