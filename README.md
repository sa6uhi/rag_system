# Azerbaijani Criminal Law RAG System

A Retrieval-Augmented Generation (RAG) system for answering questions about the Azerbaijani Criminal Code using Google's Gemini API.

## Features

- Question answering about Azerbaijani criminal law
- Document retrieval from the structured Criminal Code
- Integration with Google's Gemini API for natural language responses
- REST API for programmatic access
- Web interface for easy interaction
- CLI mode for quick queries

## Prerequisites

- Docker and Docker Compose (for Docker deployment)
- Python 3.11+ (for local deployment)
- Google Gemini API key

## Project Structure

```
rag_system/
├── api/              # Flask REST API
├── data/             # Legal documents (JSON files)
├── processing/       # Document processing modules
├── rag/              # RAG engine components
├── web/              # Web interface
├── config.py         # Configuration
├── main.py           # Main application entry point
├── wsgi.py           # WSGI entry point for Gunicorn
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── run_api.sh        # Script to run API with Gunicorn
├── setup.sh          # Setup script
└── README.md         # This file
```

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd rag_system
```

2. Set up your Google Gemini API key:
```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

3. Build and run the Docker containers:
```bash
docker-compose up --build
```

4. Access the application:
- Web Interface: http://localhost:5000
- API Documentation: http://localhost:5000/docs (when available)

## Local Installation (without Docker)

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

Start the API server using Gunicorn (recommended for production):
```bash
gunicorn --bind 0.0.0.0:5000 --workers 1 wsgi:application
```

Or use the provided script:
```bash
./run_api.sh
```

Or start the API server using the main script:
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

## Docker Deployment

To build and run the application using Docker:

```bash
docker-compose up --build
```

To run in detached mode:
```bash
docker-compose up --build -d
```

To stop the containers:
```bash
docker-compose down
```

## Configuration

The system can be configured through environment variables:

- `GEMINI_API_KEY` - Google Gemini API key
- `FLASK_ENV` - Flask environment (development/production)

## Troubleshooting

If you encounter issues:

1. Ensure your API key is correct and has proper permissions
2. Check that all required files are present in the `data` directory
3. Verify Docker has sufficient resources allocated
4. Check the logs for error messages:
   ```bash
   docker-compose logs
   ```

## Production Deployment

For production deployment, the system uses Gunicorn as the WSGI server, which provides better performance and stability compared to Flask's development server.

To run with custom Gunicorn settings:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 --keep-alive 5 wsgi:application
```

## License

This project is licensed under the MIT License.