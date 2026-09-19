from config import PipelineConfig
from database import VectorDatabaseManager

def test_query():
    cfg = PipelineConfig()
    db = VectorDatabaseManager(
        persist_dir=cfg.CHROMA_PERSIST_DIR,
        collection_name=cfg.COLLECTION_NAME,
        model_name=cfg.EMBEDDING_MODEL_NAME
    )

    query = "Derivation of Black-Scholes PDE using Itô's Lemma"
    print(f"Executing search for: '{query}'\n")

    results = db.query(query_text=query, n_results=3)

    for i, (doc, meta, dist) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
        print(f"--- Rank {i+1} (Cosine Distance: {dist:.4f}) ---")
        print(f"Book: {meta['book_title']} | Page: {meta['page_number']}")
        print(f"Excerpt:\n{doc[:300]}...\n")

if __name__ == "__main__":
    test_query()