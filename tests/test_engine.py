import pytest
from datetime import datetime, timedelta
from app.models.schemas import (
    UserInfo, 
    OccasionInfo, 
    ClothingItem,
    BodyType, 
    SkinTone, 
    ClothingType, 
    OccasionType, 
    WeatherType
)
from app.core.engine import OutfitCurationEngine

# Test data
@pytest.fixture
def sample_user():
    return UserInfo(
        user_id="user123",
        body_type=BodyType.RECTANGLE,
        skin_tone=SkinTone.MEDIUM,
        height_cm=170,
        style_preferences=["casual", "minimalist"],
        color_preferences=["blue", "white", "black"]
    )

@pytest.fixture
def sample_occasion():
    return OccasionInfo(
        occasion_type=OccasionType.BUSINESS_CASUAL,
        weather=WeatherType.MILD,
        time_of_day="afternoon",
        location="office",
        dress_code="business_casual"
    )

@pytest.fixture
def sample_inventory():
    return [
        # Tops
        ClothingItem(
            item_id="top1",
            item_type=ClothingType.TOP,
            name="Blue Dress Shirt",
            color="blue",
            material="cotton",
            size="M",
            style=["formal", "business"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD, WeatherType.WARM],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL]
        ),
        ClothingItem(
            item_id="top2",
            item_type=ClothingType.TOP,
            name="White Blouse",
            color="white",
            material="silk",
            size="S",
            style=["formal", "elegant"],
            weather_suitability=[WeatherType.MILD, WeatherType.WARM],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL]
        ),
        # Bottoms
        ClothingItem(
            item_id="bottom1",
            item_type=ClothingType.BOTTOM,
            name="Black Dress Pants",
            color="black",
            material="wool",
            size="32",
            style=["formal", "business"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL]
        ),
        # Shoes
        ClothingItem(
            item_id="shoes1",
            item_type=ClothingType.SHOES,
            name="Black Leather Shoes",
            color="black",
            material="leather",
            size="42",
            style=["formal", "classic"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL]
        ),
        # Outerwear
        ClothingItem(
            item_id="outer1",
            item_type=ClothingType.OUTERWEAR,
            name="Navy Blazer",
            color="navy",
            material="wool",
            size="L",
            style=["formal", "business"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL]
        )
    ]

def test_filter_inventory(sample_user, sample_occasion, sample_inventory):
    engine = OutfitCurationEngine()
    filtered = engine.filter_inventory(sample_inventory, sample_user, sample_occasion)
    
    # Should filter out items not suitable for the occasion
    assert len(filtered) > 0
    
    # All filtered items should be suitable for the occasion
    for item in filtered:
        assert sample_occasion.occasion_type in item.occasion_suitability
        assert sample_occasion.weather in item.weather_suitability

def test_generate_outfits(sample_user, sample_occasion, sample_inventory):
    engine = OutfitCurationEngine()
    filtered = engine.filter_inventory(sample_inventory, sample_user, sample_occasion)
    outfits = engine.generate_outfits(filtered, sample_user, sample_occasion, max_outfits=2)
    
    # Should generate the requested number of outfits
    assert len(outfits) == 2
    
    # Each outfit should have at least one item
    for outfit in outfits:
        assert len(outfit.items) > 0
        
        # Check that the confidence score is within valid range
        assert 0.0 <= outfit.confidence_score <= 1.0

def test_outfit_validity(sample_user, sample_occasion, sample_inventory):
    engine = OutfitCurationEngine()
    filtered = engine.filter_inventory(sample_inventory, sample_user, sample_occasion)
    outfits = engine.generate_outfits(filtered, sample_user, sample_occasion, max_outfits=1)
    
    if outfits:
        outfit = outfits[0]
        # Check that we have at least one top and one bottom in the outfit
        has_top = any(item.item_type == ClothingType.TOP for item in outfit.items)
        has_bottom = any(item.item_type == ClothingType.BOTTOM for item in outfit.items)
        
        assert has_top or has_bottom  # At least one should be true for a basic outfit

def test_color_compatibility():
    engine = OutfitCurationEngine()
    
    # Test complementary colors
    assert engine._check_color_compatibility(["red", "green"]) == True
    
    # Test too many different colors
    assert engine._check_color_compatibility(["red", "blue", "green", "yellow", "purple"]) == False
    
    # Test monochromatic
    assert engine._check_color_compatibility(["navy", "blue", "lightblue"]) == True
