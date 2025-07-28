import httpx
import asyncio
import random
import logging
import os
from typing import Dict, Any, Optional, List
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class QlooClient:
    """
    Qloo API client compliant with hackathon requirements.
    All calls use https://hackathon.api.qloo.com base URL.
    """
    
    BASE_URL = "https://hackathon.api.qloo.com"
    MAX_RETRIES = 3
    BACKOFF_BASE = 2.0  # seconds
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("QLOO_API_KEY")
        if not self.api_key:
            raise ValueError("QLOO_API_KEY must be set in environment variables")
        
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Qloo API with retry logic and rate limit handling.
        Compliant with hackathon requirements for error handling and backoff.
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        for attempt in range(self.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    if method.upper() == "GET":
                        response = await client.get(url, params=params, headers=self.headers)
                    elif method.upper() == "POST":
                        response = await client.post(url, params=params, json=json_data, headers=self.headers)
                    else:
                        raise ValueError(f"Unsupported HTTP method: {method}")
                    
                    # Handle rate limiting (429 status code)
                    if response.status_code == 429:
                        if attempt < self.MAX_RETRIES - 1:
                            # Exponential backoff with jitter
                            backoff_time = self.BACKOFF_BASE ** attempt + random.uniform(0, 1)
                            logger.warning(f"Rate limited by Qloo API. Retrying in {backoff_time:.2f}s (attempt {attempt + 1}/{self.MAX_RETRIES})")
                            await asyncio.sleep(backoff_time)
                            continue
                        else:
                            logger.error("Max retries exceeded for rate limited request")
                            raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
                    
                    # Handle other HTTP errors
                    if response.status_code != 200:
                        logger.error(f"Qloo API error: {response.status_code} - {response.text}")
                        raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
                    
                    # Validate response has content
                    try:
                        json_response = response.json()
                        if not json_response:
                            raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
                        return json_response
                    except Exception as e:
                        logger.error(f"Failed to parse Qloo API response: {e}")
                        raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
                        
            except httpx.TimeoutException:
                if attempt < self.MAX_RETRIES - 1:
                    backoff_time = self.BACKOFF_BASE ** attempt
                    logger.warning(f"Qloo API timeout. Retrying in {backoff_time}s (attempt {attempt + 1}/{self.MAX_RETRIES})")
                    await asyncio.sleep(backoff_time)
                    continue
                else:
                    logger.error("Max retries exceeded for timeout")
                    raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
            except Exception as e:
                logger.error(f"Unexpected error calling Qloo API: {e}")
                raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
        
        raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
    
    async def get_insights(
        self, 
        filter_type: str,
        filter_tags: Optional[str] = None,
        signal_interests_tags: Optional[str] = None,
        additional_params: Optional[Dict[str, Any]] = None,
        use_post: bool = False,
        post_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get insights from Qloo /v2/insights endpoint.
        
        Args:
            filter_type: Required. Must be valid URN like 'urn:entity:destination'
            filter_tags: Optional tags for filtering
            signal_interests_tags: Optional interest signals
            additional_params: Optional additional parameters
            use_post: If True, use POST method (document reason in post_reason)
            post_reason: Required if use_post=True, explains why POST is needed
            
        Returns:
            Dict containing Qloo insights response
            
        Compliance:
        - Always includes filter.type parameter (required)
        - Uses GET by default, POST only when documented
        - Validates response contains recommendations
        """
        # Validate required parameters
        if not filter_type:
            raise ValueError("filter.type is required for all /v2/insights calls")
        
        # Build parameters
        params = {
            "filter.type": filter_type
        }
        
        if filter_tags:
            params["filter.tags"] = filter_tags
        
        if signal_interests_tags:
            params["signal.interests.tags"] = signal_interests_tags
            
        if additional_params:
            params.update(additional_params)
        
        # Determine HTTP method
        method = "GET"
        json_data = None
        
        if use_post:
            if not post_reason:
                raise ValueError("post_reason is required when using POST method")
            
            logger.info(f"Using POST for /v2/insights: {post_reason}")
            method = "POST"
            # For POST, complex parameters go in body
            json_data = {"params": params}
            params = None
        
        # Make request
        response = await self._make_request(method, "/v2/insights", params=params, json_data=json_data)
        
        # Validate response contains recommendations
        if "recommendations" not in response:
            logger.warning("Qloo insights response missing 'recommendations' field")
            raise HTTPException(status_code=502, detail={"error": "Qloo API failure"})
        
        return response
    
    async def search(self, query: str, entity_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Search Qloo entities using /search endpoint.
        
        Args:
            query: Search query string
            entity_type: Optional entity type filter
            
        Returns:
            Dict containing search results
        """
        params = {"q": query}
        if entity_type:
            params["type"] = entity_type
            
        return await self._make_request("GET", "/search", params=params)
    
    async def get_tags(self, tag_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get available tags from /v2/tags endpoint.
        Required before making insights requests with tag filters.
        
        Args:
            tag_type: Optional filter for specific tag types
            
        Returns:
            List of available tags
        """
        params = {}
        if tag_type:
            params["type"] = tag_type
            
        response = await self._make_request("GET", "/v2/tags", params=params)
        return response.get("tags", [])
    
    async def get_audiences(self) -> List[Dict[str, Any]]:
        """
        Get available audiences from /v2/audiences endpoint.
        Required before making insights requests with audience filters.
        
        Returns:
            List of available audiences
        """
        response = await self._make_request("GET", "/v2/audiences")
        return response.get("audiences", [])
    
    async def validate_connection(self) -> bool:
        """
        Validate Qloo API connection and credentials.
        Performs the manual sanity test from compliance checklist.
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            # Manual sanity test: GET insights with minimal valid parameters
            params = {
                "filter.type": "urn:entity:destination",
                "filter.tags": "urn:tag:cuisine:thai"
            }
            
            response = await self._make_request("GET", "/v2/insights", params=params)
            
            # Check if response contains recommendations (indicates valid key/params)
            return "recommendations" in response and len(response["recommendations"]) > 0
            
        except Exception as e:
            logger.error(f"Qloo connection validation failed: {e}")
            return False
