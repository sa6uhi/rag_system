import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Simple vector store implementation using TF-IDF for document retrieval"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words=None,
            ngram_range=(1, 2)
        )
        self.document_vectors = None
        self.documents = []
        
    def add_documents(self, documents: List[Dict[str, any]]) -> None:
        """Add documents to the vector store"""
        logger.info(f"Adding {len(documents)} documents to vector store...")
        
        self.documents = documents
        contents = [doc['content'] for doc in documents]
        
        self.document_vectors = self.vectorizer.fit_transform(contents)
        
        logger.info(f"Vector store updated with {len(documents)} documents")
        
    def search(self, query: str, top_k: int = 5, threshold: float = 0.1) -> List[Tuple[Dict, float]]:
        """Search for relevant documents based on query"""
        if self.document_vectors is None or len(self.documents) == 0:
            logger.warning("No documents in vector store")
            return []
            
        query_vector = self.vectorizer.transform([query])
        
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        valid_indices = np.where(similarities >= threshold)[0]
        valid_similarities = similarities[valid_indices]
        
        sorted_indices = valid_indices[np.argsort(valid_similarities)[::-1]]
        
        results = []
        for i, idx in enumerate(sorted_indices[:top_k]):
            if i < len(self.documents):
                results.append((self.documents[idx], similarities[idx]))
                
        return results
        
    def get_document_count(self) -> int:
        """Get the number of documents in the vector store"""
        return len(self.documents) if self.documents else 0

if __name__ == "__main__":
    vector_store = VectorStore()
    
    sample_docs = [
        {
            'id': '1',
            'content': 'Bu cinayət qanunu haqqında ümumi məlumatdır.',
            'type': 'intro',
            'metadata': {}
        },
        {
            'id': '2', 
            'content': 'Cinayət törətmək üçün təqsirli olmaq lazımdır.',
            'type': 'principle',
            'metadata': {}
        }
    ]
    
    vector_store.add_documents(sample_docs)
    
    results = vector_store.search('cinayət törətmək')
    print(f"Found {len(results)} results")
    for doc, score in results:
        print(f"Document ID: {doc['id']}, Score: {score:.4f}")
        print(f"Content: {doc['content']}")