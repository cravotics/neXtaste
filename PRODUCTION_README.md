# TasteTrailOps - Clean Production Ready

A streamlined food analysis web application with AI-powered detection and nutritional insights.

## Quick Start

```bash
./start_production.sh
```

## Project Structure

- `api/` - FastAPI backend with enhanced food analysis
- `frontend/` - Professional web interface 
- `ml/` - Food analysis algorithms
- `data/` - Food-101 dataset (101 categories, 202k images)
- `docker/` - Containerization setup

## Features

- ✅ AI-powered food detection
- ✅ Enhanced nutritional analysis
- ✅ Cultural dish insights  
- ✅ Professional UI with animations
- ✅ File upload & URL analysis
- ✅ Redis caching
- ✅ Docker support

## API Endpoints

- `POST /analyze-food-enhanced` - Enhanced food analysis from file
- `POST /analyze-food-url-enhanced` - Enhanced analysis from URL
- `GET /docs` - API documentation

## Technology Stack

- **Backend**: FastAPI, TensorFlow, OpenCV
- **Frontend**: Vanilla JS, Professional CSS animations
- **AI**: Gemini AI integration, Food-101 dataset
- **Cache**: Redis
- **Deploy**: Docker, Uvicorn

## Clean Production Build

This is a production-ready version with:
- All development/training files removed
- Optimized dependencies
- Simple startup process
- Essential files only
