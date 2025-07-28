from typing import List, Dict, Any, Optional
import logging
from ..qloo_client import QlooClient

logger = logging.getLogger(__name__)

class TagsService:
    """
    Service for managing Qloo tags and audiences.
    Ensures compliance by fetching valid tags/audiences before insights requests.
    """
    
    def __init__(self, qloo_client: QlooClient):
        self.qloo_client = qloo_client
        self._tags_cache: Optional[List[Dict[str, Any]]] = None
        self._audiences_cache: Optional[List[Dict[str, Any]]] = None
    
    async def get_cuisine_tags(self) -> List[Dict[str, Any]]:
        """
        Get all available cuisine tags from Qloo.
        Required for compliance before making insights requests.
        
        Returns:
            List of cuisine tags with URNs
        """
        try:
            if not self._tags_cache:
                self._tags_cache = await self.qloo_client.get_tags()
            
            # Filter for cuisine tags
            cuisine_tags = [
                tag for tag in self._tags_cache 
                if tag.get("urn", "").startswith("urn:tag:cuisine:")
            ]
            
            logger.info(f"Retrieved {len(cuisine_tags)} cuisine tags from Qloo")
            return cuisine_tags
            
        except Exception as e:
            logger.error(f"Failed to get cuisine tags: {e}")
            return []
    
    async def get_interest_tags(self) -> List[Dict[str, Any]]:
        """
        Get all available interest tags from Qloo.
        Used for signal.interests.tags parameters.
        
        Returns:
            List of interest tags with URNs
        """
        try:
            if not self._tags_cache:
                self._tags_cache = await self.qloo_client.get_tags()
            
            # Filter for interest/activity tags
            interest_tags = [
                tag for tag in self._tags_cache 
                if any(keyword in tag.get("urn", "") for keyword in ["nightlife", "activity", "interest"])
            ]
            
            logger.info(f"Retrieved {len(interest_tags)} interest tags from Qloo")
            return interest_tags
            
        except Exception as e:
            logger.error(f"Failed to get interest tags: {e}")
            return []
    
    async def get_all_audiences(self) -> List[Dict[str, Any]]:
        """
        Get all available audiences from Qloo.
        Required for compliance before using audience IDs in insights.
        
        Returns:
            List of audiences with IDs and descriptions
        """
        try:
            if not self._audiences_cache:
                self._audiences_cache = await self.qloo_client.get_audiences()
            
            logger.info(f"Retrieved {len(self._audiences_cache)} audiences from Qloo")
            return self._audiences_cache
            
        except Exception as e:
            logger.error(f"Failed to get audiences: {e}")
            return []
    
    async def validate_cuisine_tag(self, cuisine_urn: str) -> bool:
        """
        Validate that a cuisine URN exists in Qloo's available tags.
        
        Args:
            cuisine_urn: Cuisine tag URN to validate
            
        Returns:
            True if tag is valid, False otherwise
        """
        cuisine_tags = await self.get_cuisine_tags()
        valid_urns = {tag.get("urn") for tag in cuisine_tags}
        return cuisine_urn in valid_urns
    
    async def validate_audience_id(self, audience_id: str) -> bool:
        """
        Validate that an audience ID exists in Qloo's available audiences.
        
        Args:
            audience_id: Audience ID to validate
            
        Returns:
            True if audience ID is valid, False otherwise
        """
        audiences = await self.get_all_audiences()
        valid_ids = {audience.get("id") for audience in audiences}
        return audience_id in valid_ids
    
    async def find_cuisine_tag_by_name(self, cuisine_name: str) -> Optional[str]:
        """
        Find cuisine tag URN by cuisine name.
        
        Args:
            cuisine_name: Human-readable cuisine name (e.g., "Thai", "Italian")
            
        Returns:
            Cuisine tag URN if found, None otherwise
        """
        cuisine_tags = await self.get_cuisine_tags()
        
        for tag in cuisine_tags:
            # Check if cuisine name appears in tag name or URN
            tag_name = tag.get("name", "").lower()
            tag_urn = tag.get("urn", "").lower()
            
            if cuisine_name.lower() in tag_name or cuisine_name.lower() in tag_urn:
                return tag.get("urn")
        
        return None
    
    async def get_recommended_tags_for_food(self, food_name: str) -> List[str]:
        """
        Get recommended Qloo tags for a specific food item.
        Maps food names to appropriate cuisine and interest tags.
        
        Args:
            food_name: Name of the food item
            
        Returns:
            List of relevant tag URNs
        """
        # Food to cuisine mapping
        food_cuisine_map = {
            "pizza": "italian",
            "pasta": "italian", 
            "sushi": "japanese",
            "ramen": "japanese",
            "tacos": "mexican",
            "burrito": "mexican",
            "curry": "indian",
            "tikka": "indian",
            "pad thai": "thai",
            "pho": "vietnamese",
            "burger": "american",
            "sandwich": "american"
        }
        
        recommended_tags = []
        food_lower = food_name.lower()
        
        # Find matching cuisine
        for food_keyword, cuisine in food_cuisine_map.items():
            if food_keyword in food_lower:
                cuisine_urn = await self.find_cuisine_tag_by_name(cuisine)
                if cuisine_urn:
                    recommended_tags.append(cuisine_urn)
                break
        
        return recommended_tags
    
    async def refresh_cache(self):
        """
        Refresh the cached tags and audiences from Qloo.
        Should be called periodically to keep data fresh.
        """
        logger.info("Refreshing Qloo tags and audiences cache")
        self._tags_cache = None
        self._audiences_cache = None
        
        # Pre-populate cache
        await self.get_cuisine_tags()
        await self.get_all_audiences()
        
        logger.info("Qloo cache refreshed successfully")
