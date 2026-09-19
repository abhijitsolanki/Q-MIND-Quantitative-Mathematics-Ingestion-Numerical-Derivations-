import os
from dataclasses import dataclass

@dataclass
class PipelineConfig:
    # Directory paths
    PDF_FOLDER_PATH: str = r"E:\Ringtones\FinMathematics-master\FinMathematics-master"        # Folder containing your 45-50 PDFs
    CHROMA_PERSIST_DIR: str = "./vector_db"   # Where ChromaDB persists index
    CHECKPOINT_FILE: str = "./processed_books.json"
    
    # Chunking parameters
    CHUNK_SIZE: int = 1000                    # Characters (~250-300 tokens)
    CHUNK_OVERLAP: int = 200                  # Overlap to preserve derivations
    
    # Embedding configuration
    # BGE models perform well on technical and scientific text; alternatives: "all-mpnet-base-v2"
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-base-en-v1.5"
    COLLECTION_NAME: str = "financial_mathematics_library"
    BATCH_SIZE: int = 64                      # Batch size for embedding upserts