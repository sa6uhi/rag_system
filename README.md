# Azerbaijani Criminal Law RAG System

A Retrieval-Augmented Generation (RAG) system for answering questions about the Azerbaijani Criminal Code using Google's Gemini API.

## Features

- Question answering about Azerbaijani criminal law
- Document retrieval from the structured Criminal Code
- Integration with Google's Gemini API for natural language responses
- REST API for programmatic access
- Web interface for easy interaction
- CLI mode for quick queries

## Project Structure

```
rag_system/
├── api/           # Flask REST API
├── data/          # Legal documents (JSON files)
├── processing/    # Document processing modules
├── rag/           # RAG engine components
├── web/           # Web interface
├── config.py      # Configuration
├── main.py        # Main application entry point
└── requirements.txt # Python dependencies
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google Gemini API key:
```bash
export GEMINI_API_KEY="your_api_key_here"
```
Or create a `.env` file with:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface (CLI)

Interactive mode:
```bash
python main.py --mode cli
```

Single question:
```bash
python main.py --mode cli --question "Cinayət törətmək üçün hansı şərtlər vardır?"
```

### REST API

Start the API server:
```bash
python main.py --mode api
```

API endpoints:
- `GET /health` - Health check
- `POST /query` - Ask a question
- `POST /search` - Search documents

Example query request:
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Cinayət törətmək üçün hansı şərtlər vardır?"}'
```

### Web Interface

Start the web interface:
```bash
python main.py --mode web
```

The web interface will be available at http://localhost:5000

## Data Sources

The system uses two JSON files containing the Azerbaijani Criminal Code:
- `cinayet_mecellesi_structured.json` - Structured version with sections, chapters, and articles
- `output.json` - Raw text version

## Components

### Document Processor
Processes JSON files and converts them into searchable document sections.

### Vector Store
Implements TF-IDF based document retrieval for finding relevant sections.

### RAG Engine
Main engine that combines document retrieval with language model generation.

### API
Flask-based REST API for programmatic access.

### Web Interface
Simple HTML/JavaScript interface for user interaction.

## Development

To extend the system:

1. Add new data sources in `processing/document_processor.py`
2. Improve the vector store in `rag/vector_store.py`
3. Enhance the RAG engine in `rag/engine.py`
4. Extend the API in `api/app.py`

## License

This project is licensed under the MIT License.