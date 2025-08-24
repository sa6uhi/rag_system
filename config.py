import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # File paths
    DATA_DIR = 'data'
    STRUCTURED_JSON_FILE = os.path.join(DATA_DIR, 'cinayet_mecellesi_structured.json')
    OUTPUT_JSON_FILE = os.path.join(DATA_DIR, 'output.json')
    
    # Processing settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # RAG settings
    TOP_K_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.7