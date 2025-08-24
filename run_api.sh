#!/bin/bash
# Script to run the API server with Gunicorn

if ! command -v gunicorn &> /dev/null
then
    echo "Gunicorn is not installed. Please install it with: pip install gunicorn"
    exit 1
fi

echo "Starting API server with Gunicorn..."
gunicorn --bind 0.0.0.0:5000 --workers 1 wsgi:application