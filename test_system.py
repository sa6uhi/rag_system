#!/usr/bin/env python3
"""
Test script for the Legal RAG System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.engine import get_rag_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_system():
    """Test the RAG system"""
    print("Testing Legal RAG System...")
    
    # Initialize RAG engine
    print("Initializing RAG engine...")
    rag_engine = get_rag_engine()
    
    # Get document stats
    stats = rag_engine.get_document_stats()
    print(f"Document stats: {stats}")
    
    # Test search
    print("\nTesting document search...")
    test_query = "Cinayət törətmək üçün hansı şərtlər vardır?"
    results = rag_engine.search_documents(test_query, top_k=3)
    print(f"Found {len(results)} relevant documents")
    
    for i, (doc, score) in enumerate(results):
        print(f"\nResult {i+1} (Score: {score:.4f}):")
        print(f"  ID: {doc['id']}")
        print(f"  Type: {doc['type']}")
        print(f"  Content preview: {doc['content'][:100]}...")
    
    # Test answer generation (without API key this will use fallback)
    print("\nTesting answer generation...")
    answer = rag_engine.generate_answer(test_query, results[:2])
    print(f"Generated answer:\n{answer}")

if __name__ == "__main__":
    test_system()
