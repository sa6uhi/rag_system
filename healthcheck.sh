#!/bin/bash
# Health check script for the RAG system

# Check if the API is responding
curl -f http://localhost:5000/health || exit 1