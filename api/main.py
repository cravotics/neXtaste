from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import redis
import httpx
import logging
import os
import sys
from datetime import datetime
import json
from pathlib import Path
import tempfile
import shutil
from prometheus_fastapi_instrumentator import Instrumentator
from .qloo_client import QlooClient
from .services.tags import TagsService
from .exception_handlers import qloo_api_exception_handler, general_exception_handler

# Add project root to path for importing ml modules
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from ml.food101_analyzer import analyze_food_image as analyze_with_food101
    FOOD101_AVAILABLE = True
    logger.info("✅ Food-101 analyzer loaded successfully")
except ImportError as e:
    FOOD101_AVAILABLE = False
    logger.warning(f"⚠️ Food-101 analyzer not available: {e}")

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

# Prometheus metrics instrumentation
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
OVMS_URL = os.getenv("OVMS_URL", "http://ovms:9000")
FEAST_URL = os.getenv("FEAST_URL", "http://feast:6566")
QLOO_API_KEY = os.getenv("QLOO_API_KEY")

# Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Qloo client initialization
qloo_client = QlooClient(QLOO_API_KEY)
tags_service = TagsService(qloo_client)

# Add exception handlers for Qloo compliance
app.add_exception_handler(HTTPException, qloo_api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Pydantic models for request/response validation
class FoodImageRequest(BaseModel):
    image_url: str
    user_id: str

class UserPreferences(BaseModel):
    user_id: str
    dietary_restrictions: List[str] = []
    cuisine_preferences: List[str] = []
    allergies: List[str] = []

class RecommendationRequest(BaseModel):
    user_id: str
    location: Optional[str] = None
    meal_type: Optional[str] = None
    budget_range: Optional[str] = None

class FoodItem(BaseModel):
    id: str
    name: str
    cuisine_type: str
    description: str
    price: float
    rating: float
    ingredients: List[str]
    image_url: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[FoodItem]
    user_id: str
    timestamp: datetime
    confidence_score: float

# Dependency for Redis connection
async def get_redis():
    try:
        redis_client.ping()
        return redis_client
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise HTTPException(status_code=503, detail="Cache service unavailable")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify service status"""
    try:
        # Check Redis connection
        redis_client.ping()
        
        # Check OVMS connection
        async with httpx.AsyncClient() as client:
            ovms_response = await client.get(f"{OVMS_URL}/v1/models")
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "services": {
                "redis": "connected",
                "ovms": "connected" if ovms_response.status_code == 200 else "disconnected"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to TasteTrailOps API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Food image recognition endpoint
@app.post("/analyze-food-image")
async def analyze_food_image(request: FoodImageRequest):
    """
    Analyze food image using OpenVINO model server
    Returns detected food items and nutritional information
    """
    try:
        # Call OpenVINO Model Server for food detection
        async with httpx.AsyncClient() as client:
            payload = {
                "instances": [{"image_url": request.image_url}]
            }
            
            response = await client.post(
                f"{OVMS_URL}/v1/models/yolo:predict",
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Image analysis failed")
            
            predictions = response.json()
            
            # Process predictions and extract food items
            detected_foods = process_food_predictions(predictions)
            
            # Cache results in Redis
            cache_key = f"food_analysis:{request.user_id}:{hash(request.image_url)}"
            redis_client.setex(
                cache_key, 
                3600,  # 1 hour expiry
                json.dumps(detected_foods)
            )
            
            return {
                "user_id": request.user_id,
                "detected_foods": detected_foods,
                "timestamp": datetime.now(),
                "cache_key": cache_key
            }
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Image analysis timeout")
    except Exception as e:
        logger.error(f"Food image analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Enhanced Food Analysis with Food-101 + Gemini AI
@app.post("/analyze-food-enhanced")
async def analyze_food_enhanced(file: UploadFile = File(...), user_id: Optional[str] = None):
    """
    Enhanced food analysis using Food-101 dataset + Gemini AI
    Upload an image file for comprehensive food analysis
    """
    try:
        if not FOOD101_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced food analysis not available. Food-101 analyzer not loaded."
            )
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        try:
            # Analyze with Food-101 enhanced analyzer
            analysis_result = analyze_with_food101(temp_path)
            
            # Cache results if user_id provided
            if user_id:
                cache_key = f"food_analysis_enhanced:{user_id}:{hash(file.filename)}"
                redis_client.setex(
                    cache_key,
                    3600,  # 1 hour expiry
                    json.dumps(analysis_result, default=str)
                )
                analysis_result['cache_key'] = cache_key
            
            # Add metadata
            analysis_result.update({
                "user_id": user_id,
                "filename": file.filename,
                "timestamp": datetime.now().isoformat(),
                "enhanced_analysis": True,
                "powered_by": "Food-101 + Gemini AI"
            })
            
            logger.info(f"✅ Enhanced food analysis completed for {file.filename}")
            return analysis_result
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced food analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-food-url-enhanced")
async def analyze_food_url_enhanced(image_url: str, user_id: Optional[str] = None):
    """
    Enhanced food analysis from image URL using Food-101 + Gemini AI
    """
    try:
        if not FOOD101_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Enhanced food analysis not available. Food-101 analyzer not loaded."
            )
        
        # Download image from URL
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url, timeout=30.0)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Could not download image from URL")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Analyze with Food-101 enhanced analyzer
            analysis_result = analyze_with_food101(temp_path)
            
            # Cache results if user_id provided
            if user_id:
                cache_key = f"food_analysis_enhanced:{user_id}:{hash(image_url)}"
                redis_client.setex(
                    cache_key,
                    3600,  # 1 hour expiry
                    json.dumps(analysis_result, default=str)
                )
                analysis_result['cache_key'] = cache_key
            
            # Add metadata
            analysis_result.update({
                "user_id": user_id,
                "image_url": image_url,
                "timestamp": datetime.now().isoformat(),
                "enhanced_analysis": True,
                "powered_by": "Food-101 + Gemini AI"
            })
            
            logger.info(f"✅ Enhanced food analysis completed for URL: {image_url}")
            return analysis_result
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced food analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# User preferences endpoint
@app.post("/user-preferences")
async def save_user_preferences(preferences: UserPreferences, redis_conn = Depends(get_redis)):
    """Save user dietary preferences and restrictions"""
    try:
        cache_key = f"user_preferences:{preferences.user_id}"
        redis_conn.setex(
            cache_key,
            86400,  # 24 hours
            json.dumps(preferences.dict())
        )
        
        return {
            "message": "Preferences saved successfully",
            "user_id": preferences.user_id
        }
    except Exception as e:
        logger.error(f"Error saving preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to save preferences")

@app.get("/user-preferences/{user_id}")
async def get_user_preferences(user_id: str, redis_conn = Depends(get_redis)):
    """Retrieve user preferences from cache"""
    try:
        cache_key = f"user_preferences:{user_id}"
        cached_prefs = redis_conn.get(cache_key)
        
        if not cached_prefs:
            return {"message": "No preferences found", "user_id": user_id}
        
        return {
            "preferences": json.loads(cached_prefs),
            "user_id": user_id
        }
    except Exception as e:
        logger.error(f"Error retrieving preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve preferences")

# Food recommendations endpoint
@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest, background_tasks: BackgroundTasks):
    """
    Get personalized food recommendations using ML features from Feast and Qloo insights
    """
    try:
        # Get user preferences from cache
        prefs_key = f"user_preferences:{request.user_id}"
        user_prefs = redis_client.get(prefs_key)
        
        # Get features from Feast feature store
        features = await get_user_features(request.user_id)
        
        # Get Qloo insights for enhanced recommendations
        qloo_insights = await get_qloo_recommendations(request, user_prefs)
        
        # Generate recommendations using ML model + Qloo insights
        recommendations = await generate_recommendations(request, user_prefs, features, qloo_insights)
        
        # Log recommendation event for analytics
        background_tasks.add_task(log_recommendation_event, request.user_id, recommendations)
        
        response = RecommendationResponse(
            recommendations=recommendations,
            user_id=request.user_id,
            timestamp=datetime.now(),
            confidence_score=0.85  # This would come from your ML model
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

# Qloo integration endpoints
@app.get("/qloo/cuisine-tags")
async def get_cuisine_tags():
    """Get available cuisine tags from Qloo for user preference selection"""
    try:
        tags = await tags_service.get_cuisine_tags()
        return {"cuisine_tags": tags}
    except Exception as e:
        logger.error(f"Failed to get cuisine tags: {e}")
        raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})

@app.get("/qloo/audiences")
async def get_qloo_audiences():
    """Get available Qloo audiences for targeting"""
    try:
        audiences = await tags_service.get_all_audiences()
        return {"audiences": audiences}
    except Exception as e:
        logger.error(f"Failed to get audiences: {e}")
        raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})

@app.post("/qloo/insights")
async def get_qloo_insights(
    filter_type: str = "urn:entity:destination",
    filter_tags: Optional[str] = None,
    signal_interests_tags: Optional[str] = None
):
    """
    Get Qloo insights with proper compliance validation.
    All calls include required filter.type parameter.
    """
    try:
        # Validate required parameters
        if not filter_type:
            raise HTTPException(status_code=400, detail="filter.type is required")
        
        # Validate tags if provided
        if filter_tags:
            is_valid = await tags_service.validate_cuisine_tag(filter_tags)
            if not is_valid:
                available_tags = await tags_service.get_cuisine_tags()
                return {
                    "error": "Invalid cuisine tag",
                    "available_tags": [tag["urn"] for tag in available_tags[:10]]
                }
        
        insights = await qloo_client.get_insights(
            filter_type=filter_type,
            filter_tags=filter_tags,
            signal_interests_tags=signal_interests_tags
        )
        
        return insights
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions (already handled by exception handler)
    except Exception as e:
        logger.error(f"Qloo insights error: {e}")
        raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})

@app.get("/qloo/validate")
async def validate_qloo_connection():
    """Validate Qloo API connection and credentials"""
    try:
        is_valid = await qloo_client.validate_connection()
        return {
            "valid": is_valid,
            "base_url": qloo_client.BASE_URL,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Qloo validation error: {e}")
        return {
            "valid": False,
            "error": str(e),
            "timestamp": datetime.now()
        }

# Restaurant search endpoint
@app.get("/restaurants")
async def search_restaurants(
    location: str,
    cuisine: Optional[str] = None,
    price_range: Optional[str] = None,
    radius: Optional[int] = 5
):
    """Search for restaurants based on location and filters"""
    try:
        # This would integrate with restaurant APIs (Google Places, Yelp, etc.)
        # For now, return mock data
        restaurants = [
            {
                "id": "rest_1",
                "name": "Sample Restaurant",
                "cuisine": cuisine or "International",
                "location": location,
                "rating": 4.5,
                "price_range": price_range or "$$",
                "distance": 2.3
            }
        ]
        
        return {
            "restaurants": restaurants,
            "location": location,
            "total_results": len(restaurants)
        }
        
    except Exception as e:
        logger.error(f"Restaurant search error: {e}")
        raise HTTPException(status_code=500, detail="Restaurant search failed")

# Analytics endpoint
@app.get("/analytics/{user_id}")
async def get_user_analytics(user_id: str):
    """Get user behavior analytics and insights"""
    try:
        # Retrieve analytics data from cache/database
        analytics_key = f"analytics:{user_id}"
        analytics_data = redis_client.get(analytics_key)
        
        if not analytics_data:
            return {"message": "No analytics data available", "user_id": user_id}
        
        return {
            "user_id": user_id,
            "analytics": json.loads(analytics_data),
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

# Helper functions
def process_food_predictions(predictions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process OpenVINO model predictions into food items"""
    # This is a placeholder - implement based on your YOLO model output
    detected_foods = []
    
    # Example processing logic
    if "predictions" in predictions:
        for pred in predictions["predictions"]:
            food_item = {
                "name": pred.get("class_name", "Unknown"),
                "confidence": pred.get("confidence", 0.0),
                "bounding_box": pred.get("bbox", []),
                "nutritional_info": get_nutritional_info(pred.get("class_name"))
            }
            detected_foods.append(food_item)
    
    return detected_foods

async def get_user_features(user_id: str) -> Dict[str, Any]:
    """Retrieve user features from Feast feature store"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FEAST_URL}/get-online-features", params={
                "entity_id": user_id,
                "feature_service": "user_features"
            })
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to get features for user {user_id}")
                return {}
                
    except Exception as e:
        logger.error(f"Feature store error: {e}")
        return {}

async def get_qloo_recommendations(
    request: RecommendationRequest, 
    user_prefs: Optional[str]
) -> Optional[Dict[str, Any]]:
    """
    Get Qloo insights for enhanced recommendations.
    Ensures compliance with all hackathon requirements.
    """
    try:
        # Parse user preferences
        prefs = {}
        if user_prefs:
            prefs = json.loads(user_prefs)
        
        # Get cuisine preferences and map to Qloo tags
        cuisine_preferences = prefs.get("cuisine_preferences", [])
        filter_tags = None
        
        if cuisine_preferences:
            # Get first cuisine preference and find corresponding tag
            cuisine_name = cuisine_preferences[0]
            cuisine_urn = await tags_service.find_cuisine_tag_by_name(cuisine_name)
            if cuisine_urn:
                filter_tags = cuisine_urn
        
        # Build signal interests based on meal type
        signal_interests = None
        if request.meal_type:
            meal_interest_map = {
                "breakfast": "urn:tag:meal:breakfast",
                "lunch": "urn:tag:meal:lunch", 
                "dinner": "urn:tag:meal:dinner",
                "brunch": "urn:tag:meal:brunch"
            }
            signal_interests = meal_interest_map.get(request.meal_type.lower())
        
        # Make Qloo insights request with required filter.type
        insights = await qloo_client.get_insights(
            filter_type="urn:entity:destination",  # Required parameter
            filter_tags=filter_tags,
            signal_interests_tags=signal_interests
        )
        
        logger.info(f"Retrieved {len(insights.get('recommendations', []))} Qloo insights for user {request.user_id}")
        return insights
        
    except Exception as e:
        logger.warning(f"Failed to get Qloo insights: {e}")
        return None

async def generate_recommendations(
    request: RecommendationRequest, 
    user_prefs: Optional[str], 
    features: Dict[str, Any],
    qloo_insights: Optional[Dict[str, Any]] = None
) -> List[FoodItem]:
    """Generate food recommendations using ML model enhanced with Qloo insights"""
    
    # Base recommendations
    base_recommendations = [
        FoodItem(
            id="food_1",
            name="Margherita Pizza",
            cuisine_type="Italian",
            description="Classic pizza with tomato, mozzarella, and basil",
            price=12.99,
            rating=4.5,
            ingredients=["tomato", "mozzarella", "basil", "dough"],
            image_url="https://example.com/pizza.jpg"
        ),
        FoodItem(
            id="food_2",
            name="Chicken Tikka Masala",
            cuisine_type="Indian",
            description="Creamy tomato-based curry with tender chicken",
            price=15.99,
            rating=4.7,
            ingredients=["chicken", "tomato", "cream", "spices"],
            image_url="https://example.com/tikka.jpg"
        )
    ]
    
    # Enhance with Qloo insights if available
    if qloo_insights and "recommendations" in qloo_insights:
        qloo_recs = qloo_insights["recommendations"]
        
        # Convert Qloo recommendations to FoodItem format
        for i, qloo_rec in enumerate(qloo_recs[:3]):  # Take top 3 Qloo recommendations
            enhanced_item = FoodItem(
                id=f"qloo_{qloo_rec.get('id', i)}",
                name=qloo_rec.get("name", "Qloo Recommendation"),
                cuisine_type=qloo_rec.get("category", "International"),
                description=qloo_rec.get("description", "Recommended by Qloo"),
                price=float(qloo_rec.get("price", 15.99)),
                rating=float(qloo_rec.get("rating", 4.0)),
                ingredients=qloo_rec.get("ingredients", ["mixed ingredients"]),
                image_url=qloo_rec.get("image_url")
            )
            base_recommendations.append(enhanced_item)
    
    return base_recommendations

def get_nutritional_info(food_name: str) -> Dict[str, Any]:
    """Get nutritional information for detected food"""
    # This would integrate with nutrition APIs
    return {
        "calories": 250,
        "protein": "15g",
        "carbs": "30g",
        "fat": "10g"
    }

async def log_recommendation_event(user_id: str, recommendations: List[FoodItem]):
    """Log recommendation events for analytics"""
    event = {
        "user_id": user_id,
        "event_type": "recommendation_generated",
        "timestamp": datetime.now().isoformat(),
        "recommendation_count": len(recommendations),
        "recommendation_ids": [r.id for r in recommendations]
    }
    
    # This would send to Kafka for real-time processing
    logger.info(f"Recommendation event logged: {event}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
