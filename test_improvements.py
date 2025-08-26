#!/usr/bin/env python3
"""
Test script to verify improvements to the RAG system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.engine import get_rag_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_queries():
    """Test various queries to see if improvements work"""
    print("=== Testing Improved RAG System ===")
    
    rag_engine = get_rag_engine()
    
    # Test queries
    test_queries = [
        "İştirakçılıq nədir və necə cəzalandırılır?",
        "Pedofiliya cəzası nə qədərdir?",
        "On altı yaşı tamam olmuş şəxslərin inzibati məsuliyyəti",
        "Cinayət törətmək üçün hansı şərtlər vardır?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Testing query: {query}")
        print('='*50)
        
        # Test search
        results = rag_engine.search_documents(query, top_k=3)
        print(f"Found {len(results)} relevant documents")
        
        for i, (doc, score) in enumerate(results):
            print(f"\nResult {i+1} (Score: {score:.4f}):")
            print(f"  ID: {doc['id']}")
            print(f"  Type: {doc['type']}")
            print(f"  Content preview: {doc['content'][:200]}...")
            
        # Test answer generation
        print(f"\n--- Generated Answer ---")
        answer = rag_engine.generate_answer(query, results)
        print(answer)

if __name__ == "__main__":
    test_queries()