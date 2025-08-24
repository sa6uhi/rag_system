import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    DATA_DIR = 'data'
    STRUCTURED_JSON_FILE = os.path.join(DATA_DIR, 'cinayet_mecellesi_structured.json')
    OUTPUT_JSON_FILE = os.path.join(DATA_DIR, 'output.json')
    
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    TOP_K_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.01