import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from rag.engine import get_rag_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../web', static_url_path='')
CORS(app)

rag_engine = get_rag_engine()

@app.route('/')
def serve_web_interface():
    """Serve the main web interface"""
    return send_from_directory('../web', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'legal-rag-api',
        'document_stats': rag_engine.get_document_stats()
    })

@app.route('/query', methods=['POST'])
def query_documents():
    """Query legal documents endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing question in request body'
            }), 400
            
        question = data['question']
        top_k = data.get('top_k', 5)
        
        search_results = rag_engine.search_documents(question, top_k)
        
        answer = rag_engine.generate_answer(question, search_results)
        
        formatted_results = [
            {
                'document': {
                    'id': doc['id'],
                    'content': doc['content'],
                    'type': doc['type'],
                    'metadata': doc['metadata']
                },
                'similarity_score': float(score)
            }
            for doc, score in search_results
        ]
        
        return jsonify({
            'question': question,
            'answer': answer,
            'relevant_documents': formatted_results
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            'error': f'Error processing query: {str(e)}'
        }), 500

@app.route('/search', methods=['POST'])
def search_documents():
    """Search documents endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing query in request body'
            }), 400
            
        query = data['query']
        top_k = data.get('top_k', 5)
        
        search_results = rag_engine.search_documents(query, top_k)
        
        formatted_results = [
            {
                'document': {
                    'id': doc['id'],
                    'content': doc['content'],
                    'type': doc['type'],
                    'metadata': doc['metadata']
                },
                'similarity_score': float(score)
            }
            for doc, score in search_results
        ]
        
        return jsonify({
            'query': query,
            'results': formatted_results
        })
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return jsonify({
            'error': f'Error searching documents: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)