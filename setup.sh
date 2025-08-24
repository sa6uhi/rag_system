#!/bin/bash
# Setup script

echo "Setting up Legal RAG System..."

# if ! command -v pip &> /dev/null
# then
#     echo "pip could not be found, please install Python and pip first"
#     exit 1
# fi

# echo "Installing Python dependencies..."
# pip install -r requirements.txt

# if [ $? -eq 0 ]; then
#     echo "Dependencies installed successfully!"
# else
#     echo "Failed to install dependencies"
#     exit 1
# fi

if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "# Google Gemini API Key" > .env
    echo "GEMINI_API_KEY=your_api_key_here" >> .env
    echo "Please update the .env file with your actual Gemini API key"
fi

echo "Setup completed!"
echo "Next steps:"
echo "1. Update the .env file with your Gemini API key"
echo "2. Run the system with: python main.py --mode cli"