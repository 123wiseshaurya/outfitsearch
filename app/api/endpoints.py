from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime

from app.models.schemas import (
    OutfitRecommendationRequest,
    Outfit,
    UserInfo,
    OccasionInfo,
    ClothingItem
)
from app.core.engine import OutfitCurationEngine

router = APIRouter()
engine = OutfitCurationEngine()

import logging
from pprint import pformat

logger = logging.getLogger(__name__)

@router.post("/recommend-outfits", response_model=List[Outfit])
async def recommend_outfits(request: OutfitRecommendationRequest):
    """
    Generate outfit recommendations based on user info, occasion, and inventory.
    """
    try:
        logger.info("Received outfit recommendation request")
        logger.debug(f"Request data type: {type(request)}")
        logger.debug(f"Request model_dump: {request.model_dump()}")
        
        # Log the occasion type and weather being used
        logger.info(f"Processing request for occasion: {request.occasion.occasion_type}, weather: {request.occasion.weather}")
        logger.debug(f"Occasion type: {type(request.occasion.occasion_type).__name__}, value: {request.occasion.occasion_type}")
        logger.debug(f"Weather type: {type(request.occasion.weather).__name__}, value: {request.occasion.weather}")
        
        # Log inventory items
        logger.info(f"Received {len(request.inventory)} items in inventory")
        for i, item in enumerate(request.inventory[:3]):  # Log first 3 items to avoid too much output
            logger.debug(f"Item {i+1}: {item.item_id} ({item.item_type}) - Occasions: {item.occasion_suitability}, Weather: {item.weather_suitability}")
        
        # Filter inventory based on user and occasion
        filtered_inventory = engine.filter_inventory(
            inventory=request.inventory,
            user_info=request.user_info,
            occasion=request.occasion
        )
        
        logger.info(f"Filtered inventory has {len(filtered_inventory)} items")
        for i, item in enumerate(filtered_inventory[:3]):  # Log first 3 filtered items
            logger.debug(f"Filtered item {i+1}: {item.item_id} ({item.item_type})")
        
        # Generate outfit recommendations
        outfits = engine.generate_outfits(
            filtered_inventory=filtered_inventory,
            user_info=request.user_info,
            occasion=request.occasion,
            max_outfits=request.max_outfits,
            consider_previous=request.consider_previous_outfits
        )
        
        logger.info(f"Generated {len(outfits)} outfit recommendations")
        return outfits
        
    except Exception as e:
        logger.error(f"Error in recommend_outfits: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Include more detailed error information in the response
        error_detail = f"{type(e).__name__}: {str(e)}"
        if hasattr(e, '__traceback__'):
            import traceback
            error_detail += f"\n\nTraceback:\n{''.join(traceback.format_tb(e.__traceback__))}"
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )

@router.post("/filter-inventory", response_model=List[ClothingItem])
async def filter_inventory(
    inventory: List[ClothingItem],
    user_info: UserInfo,
    occasion: OccasionInfo
):
    """
    Filter inventory based on user attributes and occasion.
    """
    try:
        return engine.filter_inventory(inventory, user_info, occasion)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error filtering inventory: {str(e)}"
        )

@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
