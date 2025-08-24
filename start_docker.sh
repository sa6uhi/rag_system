#!/bin/bash
# Script to initialize and run the RAG system with Docker

set -e

echo "=== Azerbaijani Criminal Law RAG System ==="
echo "Setting up Docker environment..."

if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "# Google Gemini API Key" > .env
    echo "GEMINI_API_KEY=your_api_key_here" >> .env
    echo ""
    echo "Please update the .env file with your actual Gemini API key"
    echo "You can get one from: https://aistudio.google.com/app/apikey"
    echo ""
fi

if [ ! -d "data" ]; then
    echo "Warning: Data directory not found. Please ensure you have the required JSON files in the data directory."
fi

echo "Building Docker images..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo ""
echo "=== System Started Successfully ==="
echo "Web Interface: http://localhost:5000"
echo "Health Check: http://localhost:5000/health"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"