# src/models/embeddings.py
from typing import List, Dict
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.utils.config import settings

class EmbeddingModel:
    def __init__(self):
        """Initialize the embedding model"""
        self.model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None

    def create_embeddings(self, documents: List[Dict]) -> None:
        """Create embeddings from documents and save to disk"""
        try:
            print("Creating embeddings...")
            self.vector_store = FAISS.from_documents(documents, self.model)
            self.save_embeddings()
            print("Embeddings created successfully!")
        except Exception as e:
            print(f"Error creating embeddings: {str(e)}")
            raise

    def save_embeddings(self) -> None:
        """Save embeddings to disk"""
        if self.vector_store:
            self.vector_store.save_local(settings.EMBEDDINGS_DIR)

    def load_embeddings(self) -> None:
        """Load embeddings from disk"""
        try:
            self.vector_store = FAISS.load_local(settings.EMBEDDINGS_DIR, self.model, allow_dangerous_deserialization=True)  # Add this parameter
        except Exception as e:
            print(f"Error loading embeddings: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents"""
        if not self.vector_store:
            self.load_embeddings()
        return self.vector_store.similarity_search(query, k=k)