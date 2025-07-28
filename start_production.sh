#!/bin/bash

# TasteTrailOps Production Startup Script
echo "Starting TasteTrailOps Production Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if needed
echo "Installing/updating dependencies..."
pip install -r requirements.txt

# Start the enhanced API server
echo "Starting API server on port 8001..."
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

echo "Application started! Visit http://localhost:8001 for API docs"
echo "Frontend available at frontend/index.html"
