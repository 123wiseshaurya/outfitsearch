import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test.log')
    ]
)
logger = logging.getLogger(__name__)

# Enable debug logging for our application
logging.getLogger('app').setLevel(logging.DEBUG)

# API endpoints
BASE_URL = "http://127.0.0.1:8000"
RECOMMEND_ENDPOINT = f"{BASE_URL}/api/v1/recommend-outfits"
FILTER_ENDPOINT = f"{BASE_URL}/api/v1/filter-inventory"
HEALTH_ENDPOINT = f"{BASE_URL}"  # Health check is at the root path

def check_health():
    """Check if the API is running and healthy."""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            logger.info("✅ API is healthy and running!")
            return True
        else:
            logger.error(f"❌ API returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to connect to the API: {e}")
        return False

def test_recommend_outfits():
    """Test the recommend-outfits endpoint with a simple request."""
    logger.info("🚀 Testing recommend-outfits endpoint...")
    
    from app.models.schemas import (
        UserInfo, 
        OccasionInfo, 
        ClothingItem, 
        OccasionType, 
        WeatherType, 
        ClothingType
    )
    
    # Create test inventory items with proper enums
    inventory = [
        ClothingItem(
            item_id="top1",
            item_type=ClothingType.TOP,
            name="Blue Dress Shirt",
            color="blue",
            material="cotton",
            size="M",
            style=["formal", "business"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD, WeatherType.WARM],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.CASUAL]
        ),
        ClothingItem(
            item_id="bottom1",
            item_type=ClothingType.BOTTOM,
            name="Black Dress Pants",
            color="black",
            material="wool",
            size="32",
            style=["formal", "business"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.CASUAL]
        ),
        ClothingItem(
            item_id="shoes1",
            item_type=ClothingType.SHOES,
            name="Black Leather Shoes",
            color="black",
            material="leather",
            size="42",
            style=["formal", "classic"],
            weather_suitability=[WeatherType.COOL, WeatherType.MILD],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.CASUAL]
        )
    ]
    
    # Create request payload with proper enums
    user_info = UserInfo(
        user_id="user123",
        body_type="rectangle",
        skin_tone="medium",
        height_cm=170,
        style_preferences=["casual", "minimalist"],
        color_preferences=["blue", "white", "black"]
    )
    
    occasion = OccasionInfo(
        occasion_type=OccasionType.BUSINESS_CASUAL,
        weather=WeatherType.MILD,
        time_of_day="afternoon",
        location="office",
        dress_code="business_casual"
    )
    
    # Log the enums being used
    logger.debug(f"Using OccasionType: {occasion.occasion_type} (type: {type(occasion.occasion_type).__name__})")
    logger.debug(f"Using WeatherType: {occasion.weather} (type: {type(occasion.weather).__name__})")
    
    # Helper function to convert enums to strings in a dictionary
    def convert_enums_to_strings(data):
        if isinstance(data, dict):
            return {k: convert_enums_to_strings(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [convert_enums_to_strings(item) for item in data]
        elif hasattr(data, 'value') and hasattr(data, '__class__') and hasattr(data, '__module__'):
            return data.value
        return data
    
    # Convert to dict using model_dump() and ensure enums are converted to strings
    payload = {
        "user_info": convert_enums_to_strings(user_info.model_dump()),
        "occasion": convert_enums_to_strings(occasion.model_dump()),
        "inventory": [convert_enums_to_strings(item.model_dump()) for item in inventory],
        "max_outfits": 2,
        "consider_previous_outfits": True
    }
    
    # Log the payload
    logger.debug(f"Request payload: {payload}")
    
    try:
        response = requests.post(
            RECOMMEND_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            outfits = response.json()
            logger.info(f"✅ Success! Received {len(outfits)} outfit recommendations")
            for i, outfit in enumerate(outfits, 1):
                print(f"\n👕 Outfit #{i} (Confidence: {outfit.get('confidence_score', 0) * 100:.1f}%)")
                for item in outfit.get('items', []):
                    print(f"  • {item.get('name')} ({item.get('item_type')})")
            return True
        else:
            logger.error(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to connect to the API: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("👗 Outfit Curation Engine - API Test Script")
    print("="*50 + "\n")
    
    # Check if API is running
    if not check_health():
        print("\nPlease start the FastAPI server first with:")
        print("1. cd /Users/veerraghuvanshi/CascadeProjects/outfit_curation_engine")
        print("2. source venv/bin/activate")
        print("3. PYTHONPATH=/Users/veerraghuvanshi/CascadeProjects/outfit_curation_engine uvicorn app.main:app --reload\n")
        exit(1)
    
    # Run test
    test_recommend_outfits()
    
    print("\n✅ Test script completed!")
    print("\nYou can also access the interactive API documentation at:")
    print("http://127.0.0.1:8000/docs\n")
