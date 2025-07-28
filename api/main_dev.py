from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import os
from datetime import datetime
import json

# Optional imports for better local development
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Using in-memory storage.")

try:
    from prometheus_fastapi_instrumentator import Instrumentator
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("Prometheus instrumentation not available.")

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logger.warning("httpx not available. External API calls disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TasteTrailOps API",
    description="Food recommendation system with computer vision and ML",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics instrumentation (if available)
if PROMETHEUS_AVAILABLE:
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)

# Environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OVMS_URL = os.getenv("OVMS_URL", "http://localhost:9000")
FEAST_URL = os.getenv("FEAST_URL", "http://localhost:6566")
QLOO_API_KEY = os.getenv("QLOO_API_KEY", "your_qloo_api_key_here")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# In-memory storage for development
memory_store = {}

# Redis connection with fallback
redis_client = None
if REDIS_AVAILABLE:
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}. Using in-memory storage.")
        redis_client = None

# Pydantic models
class FoodRecommendationRequest(BaseModel):
    user_id: str
    location: Optional[str] = None
    meal_type: Optional[str] = None
    budget_range: Optional[str] = None
    cuisine_preferences: Optional[List[str]] = []
    dietary_restrictions: Optional[List[str]] = []

class FoodImageAnalysisRequest(BaseModel):
    user_id: str
    image_url: str

class UserPreferences(BaseModel):
    user_id: str
    dietary_restrictions: List[str] = []
    cuisine_preferences: List[str] = []
    allergies: List[str] = []

# Storage helper functions
def store_data(key: str, value: Any, expire: int = 3600):
    """Store data in Redis or memory"""
    if redis_client:
        try:
            redis_client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Redis store error: {e}")
    
    # Fallback to memory
    memory_store[key] = {
        "value": value,
        "expires": datetime.now().timestamp() + expire
    }
    return True

def get_data(key: str):
    """Get data from Redis or memory"""
    if redis_client:
        try:
            data = redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
    
    # Fallback to memory
    if key in memory_store:
        entry = memory_store[key]
        if datetime.now().timestamp() < entry["expires"]:
            return entry["value"]
        else:
            del memory_store[key]
    
    return None

# Dependency for storage
async def get_storage():
    return {"store": store_data, "get": get_data}

# Qloo client (simplified for development)
class SimplifiedQlooClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://hackathon.api.qloo.com"
    
    async def get_insights(self, filter_type: str, tags: List[str] = None, location: str = None):
        """Get insights from Qloo API or return sample data"""
        if not HTTPX_AVAILABLE or self.api_key == "your_qloo_api_key_here":
            # Return sample data for development
            return {
                "recommendations": [
                    {
                        "id": "sample_1",
                        "name": "Sample Restaurant 1",
                        "cuisine": "Italian",
                        "rating": 4.5,
                        "price_range": "$$"
                    },
                    {
                        "id": "sample_2", 
                        "name": "Sample Restaurant 2",
                        "cuisine": "Thai",
                        "rating": 4.2,
                        "price_range": "$"
                    }
                ],
                "insights": ["Popular choice", "Great reviews", "Recommended for dinner"]
            }
        
        # Real API call (if available)
        try:
            import httpx
            params = {"filter.type": filter_type}
            if tags:
                params["filter.tags"] = ",".join(tags)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    headers={"x-api-key": self.api_key},
                    params=params,
                    timeout=10.0
                )
                return response.json()
        except Exception as e:
            logger.error(f"Qloo API error: {e}")
            return {"recommendations": [], "insights": []}

# Initialize Qloo client
qloo_client = SimplifiedQlooClient(QLOO_API_KEY)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": ENVIRONMENT,
            "services": {
                "api": "healthy",
                "redis": "connected" if redis_client else "unavailable",
                "qloo": "configured" if QLOO_API_KEY != "your_qloo_api_key_here" else "not_configured"
            }
        }
        
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Recommendations endpoint
@app.post("/recommendations")
async def get_recommendations(request: FoodRecommendationRequest, storage = Depends(get_storage)):
    """Get food recommendations based on user preferences and location"""
    try:
        logger.info(f"Getting recommendations for user: {request.user_id}")
        
        # Check cache first
        cache_key = f"recommendations:{request.user_id}:{hash(str(request.dict()))}"
        cached_result = storage["get"](cache_key)
        if cached_result:
            logger.info("Returning cached recommendations")
            return cached_result
        
        # Get user preferences
        user_prefs_key = f"preferences:{request.user_id}"
        user_preferences = storage["get"](user_prefs_key) or {}
        
        # Combine request preferences with stored preferences
        dietary_restrictions = list(set(
            (request.dietary_restrictions or []) + 
            (user_preferences.get("dietary_restrictions", []))
        ))
        cuisine_preferences = list(set(
            (request.cuisine_preferences or []) + 
            (user_preferences.get("cuisine_preferences", []))
        ))
        
        # Build tags for Qloo
        tags = []
        if cuisine_preferences:
            tags.extend([f"urn:tag:cuisine:{cuisine}" for cuisine in cuisine_preferences])
        if dietary_restrictions:
            tags.extend([f"urn:tag:diet:{diet}" for diet in dietary_restrictions])
        
        # Get insights from Qloo
        qloo_data = await qloo_client.get_insights(
            filter_type="urn:entity:destination",
            tags=tags,
            location=request.location
        )
        
        # Process and format recommendations
        recommendations = []
        for i, rec in enumerate(qloo_data.get("recommendations", [])[:10]):
            recommendation = {
                "id": rec.get("id", f"rec_{i}"),
                "name": rec.get("name", f"Restaurant {i+1}"),
                "description": f"Great {request.meal_type or 'food'} option",
                "cuisine_type": rec.get("cuisine", "International"),
                "price": 15.99 + (i * 2.5),  # Sample pricing
                "rating": rec.get("rating", 4.0 + (i * 0.1)),
                "location": request.location or "Local Area",
                "meal_type": request.meal_type,
                "qloo_insights": qloo_data.get("insights", [])[:3]
            }
            recommendations.append(recommendation)
        
        # Add some sample recommendations if none from Qloo
        if not recommendations:
            sample_cuisines = ["Italian", "Thai", "Mexican", "Indian", "Japanese"]
            for i, cuisine in enumerate(sample_cuisines):
                recommendations.append({
                    "id": f"sample_{i}",
                    "name": f"Best {cuisine} Restaurant",
                    "description": f"Authentic {cuisine} cuisine with modern twist",
                    "cuisine_type": cuisine,
                    "price": 12.99 + (i * 3),
                    "rating": 4.0 + (i * 0.2),
                    "location": request.location or "Your Area",
                    "meal_type": request.meal_type or "Any",
                    "qloo_insights": ["Popular choice", "Great reviews"]
                })
        
        result = {
            "recommendations": recommendations,
            "filters_applied": {
                "location": request.location,
                "meal_type": request.meal_type,
                "budget_range": request.budget_range,
                "dietary_restrictions": dietary_restrictions,
                "cuisine_preferences": cuisine_preferences
            },
            "total_count": len(recommendations)
        }
        
        # Cache results
        storage["store"](cache_key, result, 3600)
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Food image analysis endpoint
@app.post("/analyze-food-image")
async def analyze_food_image(request: FoodImageAnalysisRequest, storage = Depends(get_storage)):
    """Analyze food image using computer vision"""
    try:
        logger.info(f"Analyzing image for user: {request.user_id}")
        
        # Check cache
        cache_key = f"analysis:{hash(request.image_url)}"
        cached_result = storage["get"](cache_key)
        if cached_result:
            return cached_result
        
        # Simulate image analysis (in real implementation, call OpenVINO)
        analysis_result = {
            "image_url": request.image_url,
            "detected_foods": [
                {
                    "name": "Caesar Salad",
                    "confidence": 0.92,
                    "nutritional_info": {
                        "calories": "320",
                        "protein": "15g",
                        "carbs": "12g",
                        "fat": "25g",
                        "fiber": "3g",
                        "sodium": "680mg"
                    },
                    "ingredients": ["Romaine lettuce", "Parmesan cheese", "Croutons", "Caesar dressing"]
                }
            ],
            "qloo_insights": [
                "Popular among health-conscious diners",
                "Great for lunch or light dinner", 
                "Pairs well with white wine"
            ],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Cache result
        storage["store"](cache_key, analysis_result, 7200)
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# User preferences endpoints
@app.post("/user-preferences")
async def save_user_preferences(preferences: UserPreferences, storage = Depends(get_storage)):
    """Save user preferences"""
    try:
        key = f"preferences:{preferences.user_id}"
        prefs_data = preferences.dict()
        del prefs_data["user_id"]  # Don't store user_id in the data
        
        storage["store"](key, prefs_data, 86400 * 30)  # 30 days
        
        return {
            "message": "Preferences saved successfully",
            "user_id": preferences.user_id,
            "preferences": prefs_data
        }
    except Exception as e:
        logger.error(f"Error saving preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user-preferences/{user_id}")
async def get_user_preferences(user_id: str, storage = Depends(get_storage)):
    """Get user preferences"""
    try:
        key = f"preferences:{user_id}"
        preferences = storage["get"](key)
        
        if not preferences:
            return {
                "user_id": user_id,
                "preferences": {
                    "dietary_restrictions": [],
                    "cuisine_preferences": [],
                    "allergies": []
                }
            }
        
        return {
            "user_id": user_id,
            "preferences": preferences
        }
    except Exception as e:
        logger.error(f"Error getting preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Metrics endpoint (if Prometheus available)
if PROMETHEUS_AVAILABLE:
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(
            instrumentator.openmetrics_instrumentation_handler(),
            media_type="text/plain"
        )

# Add exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "general_error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
