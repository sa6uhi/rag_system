#!/usr/bin/env python3
"""
Main application entry point for the Legal RAG System
"""
import argparse
import sys
import os
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.engine import get_rag_engine
from api.app import app
import webbrowser
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_web_interface():
    """Run the web interface"""
    logger.info("Starting web interface...")
    app.run(host='0.0.0.0', port=5000, debug=False)

def open_browser():
    """Open browser after a delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Legal RAG System for Azerbaijani Criminal Law')
    parser.add_argument('--mode', choices=['api', 'web', 'cli'], default='cli',
                       help='Run mode: api (REST API), web (Web interface), cli (Command line)')
    parser.add_argument('--question', type=str, help='Question to ask (for CLI mode)')
    
    args = parser.parse_args()
    
    # Initialize RAG engine
    logger.info("Initializing RAG engine...")
    rag_engine = get_rag_engine()
    
    logger.info("RAG system initialized successfully")
    stats = rag_engine.get_document_stats()
    logger.info(f"Indexed documents: {stats}")
    
    if args.mode == 'cli':
        if args.question:
            # Process single question
            logger.info(f"Processing question: {args.question}")
            answer = rag_engine.generate_answer(args.question)
            print(f"\nQuestion: {args.question}")
            print(f"\nAnswer: {answer}")
        else:
            # Interactive CLI mode
            print("Legal RAG System - Azerbaijani Criminal Law")
            print("=" * 50)
            print("Type your questions or 'quit' to exit")
            
            while True:
                try:
                    question = input("\nEnter your question: ").strip()
                    if question.lower() in ['quit', 'exit', 'çıxış']:
                        break
                    
                    if question:
                        print("Processing...")
                        answer = rag_engine.generate_answer(question)
                        print(f"\nAnswer: {answer}")
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    
    elif args.mode == 'api':
        # Run API server
        logger.info("Starting API server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    elif args.mode == 'web':
        # Run web interface
        logger.info("Starting web interface...")
        
        # Start server in background thread
        server_thread = threading.Thread(target=run_web_interface)
        server_thread.daemon = True
        server_thread.start()
        
        # Open browser
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    main()