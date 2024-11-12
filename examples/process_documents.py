import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.processor import DocumentProcessor

def main():
    """Example usage of document processor"""
    processor = DocumentProcessor()
    
    # Process all documents
    documents = processor.process_directory()
    
    print(f"Processed {len(documents)} document chunks")
    
    # Print sample of processed documents
    if documents:
        print("\nSample document chunk:")
        print(f"Content: {documents[0].page_content[:200]}...")
        print(f"Metadata: {documents[0].metadata}")

if __name__ == "__main__":
    main()