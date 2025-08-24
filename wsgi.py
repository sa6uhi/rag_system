#!/usr/bin/env python3
"""
WSGI entry point for the Legal RAG System
This file is used by Gunicorn to run the Flask application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.app import app

application = app

if __name__ == "__main__":
    application.run()