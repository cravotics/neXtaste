# TasteTrailOps - neXtaste

 **AI-Powered Food Analysis System with Superhero-Grade Intelligence**

A modern web application that combines advanced computer vision, Gemini AI, and Food-101 dataset analysis to deliver intelligent food recognition and nutritional insights with a stunning Pixar-style interface.

##  Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd TasteTrailOps

# Start the application
./start_production.sh

# Access the application
# Frontend: http://localhost:8001 (via API server)
# API Docs: http://localhost:8001/docs
```

##  Key Features

###  Modern Web Interface
- **Pixar-Style Loading Screen**: Professional neon animations with smooth transitions
- **Superhero Theme**: Cyan/purple gradient design with glowing effects
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Analysis**: Instant food detection and AI-powered insights

###  AI-Powered Food Analysis
- **Food-101 Dataset Integration**: Trained on 101 food categories with 202,125+ images
- **Enhanced Computer Vision**: Improved food detection with cultural context
- **Gemini AI Integration**: Deep analysis with nutritional recommendations
- **Smart Nutrition Data**: Comprehensive macro/micronutrient information

###  Professional UI/UX
- **Cursive Branding**: Elegant neXtaste logo with neon effects
- **Smooth Animations**: Professional loading transitions and hover effects
- **Glass Morphism**: Modern card designs with gradient borders
- **Accessibility**: Screen reader friendly with proper ARIA support

##  System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │           neXtaste Frontend                     │   │
│  │  • Pixar-style Loading Screen                   │   │
│  │  • Food Upload Interface                        │   │
│  │  • Real-time Analysis Results                   │   │
│  │  • Responsive Design                            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/AJAX Requests
                  ▼
┌─────────────────────────────────────────────────────────┐
│                FastAPI Backend Server                   │
│                    (Port 8001)                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              API Endpoints                      │   │
│  │  • /analyze-food-enhanced (File Upload)        │   │
│  │  • /analyze-food-url-enhanced (URL Analysis)   │   │
│  │  • /docs (API Documentation)                   │   │
│  │  • / (Serves Frontend)                         │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │            Food Analysis Engine                 │   │
│  │  • Food-101 Dataset Integration                │   │
│  │  • Enhanced Detection Algorithms               │   │
│  │  • Nutrition Database Matching                 │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │              AI Integration                     │   │
│  │  • Gemini AI API                              │   │
│  │  • Cultural Context Analysis                   │   │
│  │  • Smart Recommendations                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

##  User Interface

###  Loading Experience
- **Professional Animation**: Neon neXtaste logo with floating particles
- **Smooth Transitions**: X morphs from loading to navigation
- **Pixar-Style Effects**: Atmospheric lighting and blur outlines

###  Food Analysis Interface
1. ** Upload Section**
   - Drag & drop file upload
   - URL-based image analysis
   - Real-time preview

2. ** Analysis Results**
   - Detected food items with confidence scores
   - Nutritional breakdown (calories, protein, etc.)
   - AI-powered recommendations

3. ** AI Insights**
   - Cultural context and origin
   - Cooking tips and preparation methods
   - Health recommendations

##  Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript, Tailwind CSS | Modern responsive UI |
| **Backend** | FastAPI, Python 3.9+ | High-performance API server |
| **AI Analysis** | Food-101 Dataset, Custom Algorithms | Food detection and classification |
| **AI Enhancement** | Google Gemini API | Cultural insights and recommendations |
| **Styling** | CSS3 Animations, Glass Morphism | Professional visual effects |
| **Fonts** | Dancing Script, Orbitron | Elegant cursive and futuristic typography |

##  Project Structure

```
TasteTrailOps/
├── api/                          # FastAPI backend
│   ├── main.py                  # Enhanced production API
│   ├── main_dev.py              # Development version
│   └── services/                # API services
│       ├── qloo_client.py       # External API integration
│       ├── recommendation.py    # Food recommendations
│       └── tags.py              # Cuisine tagging
├── frontend/                     # Web interface
│   ├── index.html               # Main application
│   ├── app.js                   # Enhanced JavaScript
│   └── styles.css               # Professional styling
├── ml/                          # Machine learning components
│   ├── food101_analyzer.py      # Enhanced food detection
│   └── models/                  # Model assets
├── data/                        # Food-101 dataset
│   └── food-101/               # 101 food categories, 202K+ images
├── .env                         # API keys and configuration
├── requirements.txt             # Python dependencies
└── start_production.sh          # Simple startup script
```

##  Environment Setup

Create a `.env` file with your API keys:

```bash
# API Keys
GEMINI_API_KEY='your_gemini_api_key_here'
QLOO_API_KEY='your_qloo_api_key_here'

# Kaggle (for dataset access)
KAGGLE_USERNAME='your_username'
KAGGLE_KEY='your_api_key'
```

##  Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start development server
cd api
uvicorn main:app --reload --port 8001

# Access application
open http://localhost:8001
```

### Production Deployment
```bash
# Start production server
./start_production.sh

# The script will:
# 1. Create virtual environment
# 2. Install dependencies
# 3. Start the server on port 8001
```

##  API Endpoints

### Food Analysis
- **POST** `/analyze-food-enhanced` - Upload image for analysis
- **POST** `/analyze-food-url-enhanced` - Analyze image from URL
- **GET** `/docs` - Interactive API documentation
- **GET** `/` - Serves the frontend application

### Response Format
```json
{
  "detected_foods": [
    {
      "name": "pizza",
      "confidence": 0.92,
      "category": "Italian",
      "nutrition": {
        "calories": 540,
        "protein": "25g",
        "carbs": "45g",
        "fat": "28g"
      }
    }
  ],
  "ai_enhanced": true,
  "recommendations": "This looks like a classic Margherita pizza...",
  "cultural_context": "Pizza originated in Naples, Italy..."
}
```

##  Design Features

- **Superhero Branding**: neXtaste with stylized X
- **Neon Effects**: Cyan/pink color scheme with glow animations
- **Professional Typography**: Dancing Script for elegance, Orbitron for tech feel
- **Responsive Design**: Optimized for all screen sizes
- **Accessibility**: WCAG compliant with proper contrast ratios

##  Food-101 Dataset

- **101 Food Categories**: From apple_pie to waffles
- **202,125+ Images**: High-quality training data
- **Enhanced Detection**: Improved accuracy over basic models
- **Cultural Context**: AI provides origin and preparation insights

---

**Powered by neXtaste** - *Your next taste will be bliss* ✨

*Delivered by Cravotics Studios with superhero-grade code and infinite passion for taste.*
