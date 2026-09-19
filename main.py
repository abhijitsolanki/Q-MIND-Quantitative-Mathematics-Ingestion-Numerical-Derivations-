import os
from glob import glob
from tqdm import tqdm
from config import PipelineConfig
from ingest import process_single_pdf
from database import VectorDatabaseManager, CheckpointManager


def run_pipeline():
    cfg = PipelineConfig()
    os.makedirs(cfg.CHROMA_PERSIST_DIR, exist_ok=True)
    os.makedirs(cfg.PDF_FOLDER_PATH, exist_ok=True)

    print(f"[Init] Initializing Vector DB at '{cfg.CHROMA_PERSIST_DIR}'...")
    db = VectorDatabaseManager(
        persist_dir=cfg.CHROMA_PERSIST_DIR,
        collection_name=cfg.COLLECTION_NAME,
        model_name=cfg.EMBEDDING_MODEL_NAME
    )
    checkpoint_mgr = CheckpointManager(cfg.CHECKPOINT_FILE)

    pdf_files = sorted(glob(os.path.join(cfg.PDF_FOLDER_PATH, "*.pdf")))
    if not pdf_files:
        print(f"[Notice] No PDF files found in '{cfg.PDF_FOLDER_PATH}'. Place your books there and rerun.")
        return

    print(f"[Pipeline] Found {len(pdf_files)} PDF file(s). Starting Phase 1 & 2...")

    for pdf_path in tqdm(pdf_files, desc="Processing Books"):
        book_name = os.path.basename(pdf_path)
        
        # Skip if already processed in a previous run
        if checkpoint_mgr.is_processed(book_name):
            continue

        # Phase 1: Extract & chunk
        chunks = process_single_pdf(
            pdf_path, 
            chunk_size=cfg.CHUNK_SIZE, 
            chunk_overlap=cfg.CHUNK_OVERLAP
        )
        
        # Phase 2: Embed & upsert to Vector DB
        if chunks:
            db.add_chunks_in_batches(chunks, batch_size=cfg.BATCH_SIZE)

        # Mark book as completed
        checkpoint_mgr.mark_completed(book_name)

    total_vectors = db.collection.count()
    print(f"\n[Done] Pipeline complete. Total vector count in collection: {total_vectors}")


if __name__ == "__main__":
    run_pipeline()