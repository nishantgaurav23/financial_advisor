# examples/test_advisor.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.config import settings  # Add this import at the top with other imports

from src.data.processor import DocumentProcessor
from src.models.embeddings import EmbeddingModel
from src.models.llm import FinancialLLM
from src.rag.engine import RAGEngine
from src.utils.config import settings  # Add this import at the top with other imports

def main():
    # Process documents
    # processor = DocumentProcessor()
    # documents = processor.process_directory()
    # print(f"Processed {len(documents)} document chunks")

    # # Create embeddings
    # embedding_model = EmbeddingModel()
    # embedding_model.create_embeddings(documents)
    # print("Created embeddings")

    # Initialize LLM and RAG engine
    llm = FinancialLLM()
    # Make sure embeddings exist before creating RAG engine
    if not os.path.exists(os.path.join(settings.EMBEDDINGS_DIR, "index.faiss")):
        print("No embeddings found. Please process documents first.")
        return
    
    rag_engine = RAGEngine(llm)

    # Test query
    #query = "What are the basics of retirement planning?"
    query = "I want to retire in 20 years, how much do I need to save?"
    response = rag_engine.query(query)
    
    print("\nQuery:", query)
    print("\nResponse:", response["answer"])
    print("\nSources used:", len(response["sources"]))

if __name__ == "__main__":
    main()