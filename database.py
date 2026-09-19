# database.py
import json
import os
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions

class VectorDatabaseManager:
    def __init__(self, persist_dir: str, collection_name: str, model_name: str = None):
        # Initialize Persistent Client
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Use ChromaDB's default lightweight embedding function (DefaultEmbeddingFunction uses ONNX)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks_in_batches(self, chunks: List[Dict[str, Any]], batch_size: int = 64):
        total = len(chunks)
        for i in range(0, total, batch_size):
            batch = chunks[i : i + batch_size]
            ids = [item["id"] for item in batch]
            documents = [item["text"] for item in batch]
            metadatas = [item["metadata"] for item in batch]
            
            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    def query(self, query_text: str, n_results: int = 5):
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

class CheckpointManager:
    def __init__(self, checkpoint_file: str):
        self.file_path = checkpoint_file
        self.completed_books = set(self._load())

    def _load(self) -> List[str]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def is_processed(self, book_filename: str) -> bool:
        return book_filename in self.completed_books

    def mark_completed(self, book_filename: str):
        self.completed_books.add(book_filename)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(list(self.completed_books), f, indent=2)