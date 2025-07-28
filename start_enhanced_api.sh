#!/bin/bash

# Enhanced TasteTrailOps API Startup Script
echo "🚀 Starting Enhanced TasteTrailOps API with Food-101 + Gemini AI"
echo "=" * 60

# Check if we're in the right directory
if [ ! -f "api/main.py" ]; then
    echo "❌ Please run this script from the TasteTrailOps root directory"
    exit 1
fi

# Check for required environment variables
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with:"
    echo "   GEMINI_API_KEY=your_gemini_api_key"
    echo "   REDIS_URL=redis://localhost:6379/0"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing/upgrading dependencies..."
pip install --upgrade pip
pip install -r api/requirements.txt

# Check if Food-101 dataset exists
if [ ! -d "data/food-101" ]; then
    echo "⚠️ Food-101 dataset not found. Enhanced analysis may be limited."
    echo "💡 Run 'python3 download_food101.py' to download the dataset"
fi

# Start Redis if not running (optional)
if ! pgrep -x "redis-server" > /dev/null; then
    echo "🗄️ Starting Redis server..."
    redis-server --daemonize yes --port 6379
fi

# Start the API server
echo "🌟 Starting Enhanced API server..."
echo "📱 API will be available at: http://localhost:8000"
echo "📖 API docs available at: http://localhost:8000/docs"
echo "🍔 Enhanced Food Analysis: /analyze-food-enhanced"
echo ""
echo "💡 Features:"
echo "   • Food-101 dataset integration (101 food categories)"
echo "   • Gemini AI-powered analysis"
echo "   • Advanced nutritional insights"
echo "   • Cultural food context"
echo "   • Smart recommendations"
echo ""

# Run the API
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
