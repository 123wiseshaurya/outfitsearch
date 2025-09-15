import json
import requests
import logging
from pprint import pformat

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API endpoints
BASE_URL = "http://127.0.0.1:8000"
RECOMMEND_ENDPOINT = f"{BASE_URL}/api/v1/recommend-outfits"
FILTER_ENDPOINT = f"{BASE_URL}/api/v1/filter-inventory"
HEALTH_ENDPOINT = f"{BASE_URL}/health"

def check_health():
    """Check if the API is running and healthy."""
    try:
        response = requests.get(HEALTH_ENDPOINT)
        if response.status_code == 200:
            logger.info("✅ API is healthy and running!")
            return True
        else:
            logger.error(f"❌ API returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to connect to the API: {e}")
        return False

def create_sample_request():
    """Create a sample request payload with more items for better testing."""
    return {
  "user_info": {
    "user_id": "user123",
    "body_type": "rectangle",
    "skin_tone": "medium",
    "height_cm": 170,
    "style_preferences": ["casual", "minimalist"],
    "color_preferences": ["blue", "white", "black"]
  },
  "occasion": {
    "occasion_type": "business_casual",
    "weather": "mild",
    "time_of_day": "afternoon",
    "location": "office",
    "dress_code": "business_casual"
  },
  "inventory": [
    # Tops
    {
      "item_id": "top1",
      "item_type": "top",
      "name": "Blue Dress Shirt",
      "color": "blue",
      "material": "cotton",
      "size": "M",
      "style": ["formal", "business"],
      "weather_suitability": ["cool", "mild", "warm"],
      "occasion_suitability": ["business_casual", "formal"]
    },
    {
      "item_id": "top2",
      "item_type": "top",
      "name": "White Blouse",
      "color": "white",
      "material": "silk",
      "size": "S",
      "style": ["formal", "elegant"],
      "weather_suitability": ["mild", "warm"],
      "occasion_suitability": ["business_casual", "formal"]
    },
    # Bottoms
    {
      "item_id": "bottom1",
      "item_type": "bottom",
      "name": "Black Dress Pants",
      "color": "black",
      "material": "wool",
      "size": "32",
      "style": ["formal", "business"],
      "weather_suitability": ["cool", "mild"],
      "occasion_suitability": ["business_casual", "formal"]
    },
    {
      "item_id": "bottom2",
      "item_type": "bottom",
      "name": "Navy Chinos",
      "color": "navy",
      "material": "cotton",
      "size": "32",
      "style": ["casual", "business_casual"],
      "weather_suitability": ["cool", "mild", "warm"],
      "occasion_suitability": ["business_casual", "casual"]
    },
    # Shoes
    {
      "item_id": "shoes1",
      "item_type": "shoes",
      "name": "Black Leather Shoes",
      "color": "black",
      "material": "leather",
      "size": "42",
      "style": ["formal", "classic"],
      "weather_suitability": ["cool", "mild"],
      "occasion_suitability": ["business_casual", "formal"]
    },
    # Accessories
    {
      "item_id": "acc1",
      "item_type": "accessory",
      "name": "Leather Belt",
      "color": "black",
      "material": "leather",
      "size": "M",
      "style": ["classic"],
      "weather_suitability": [],
      "occasion_suitability": ["business_casual", "formal", "casual"]
    },
    {
      "item_id": "acc2",
      "item_type": "accessory",
      "name": "Silver Watch",
      "color": "silver",
      "material": "metal",
      "size": "M",
      "style": ["classic", "elegant"],
      "weather_suitability": [],
      "occasion_suitability": ["business_casual", "formal", "casual"]
    },
    # Outerwear
    {
      "item_id": "out1",
      "item_type": "outerwear",
      "name": "Navy Blazer",
      "color": "navy",
      "material": "wool",
      "size": "M",
      "style": ["formal", "business"],
      "weather_suitability": ["cool", "mild"],
      "occasion_suitability": ["business_casual", "formal"]
    }
  ],
  "max_outfits": 5,
  "consider_previous_outfits": True
}

def test_recommend_outfits():
    """Test the recommend-outfits endpoint."""
    logger.info("🚀 Testing recommend-outfits endpoint...")
    
    # Create request payload
    payload = create_sample_request()
    
    # Log request details
    logger.info(f"Sending request to {RECOMMEND_ENDPOINT}")
    logger.debug(f"Request payload:\n{pformat(payload, indent=2)}")
    
    try:
        # Make the POST request
        response = requests.post(
            RECOMMEND_ENDPOINT,
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json=payload
        )
        
        # Log response status
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            outfits = response.json()
            logger.info(f"✅ Success! Received {len(outfits)} outfit recommendations")
            
            # Print each outfit with details
            for i, outfit in enumerate(outfits, 1):
                print(f"\n{'='*50}")
                print(f"👕 Outfit #{i} (Confidence: {outfit.get('confidence_score', 0) * 100:.1f}%)")
                print("-"*50)
                
                # Group items by type for better display
                items_by_type = {}
                for item in outfit.get('items', []):
                    item_type = item.get('item_type', 'other')
                    if item_type not in items_by_type:
                        items_by_type[item_type] = []
                    items_by_type[item_type].append(item)
                
                # Print items grouped by type
                for item_type, items in items_by_type.items():
                    print(f"{item_type.upper()}:")
                    for item in items:
                        print(f"  • {item.get('name')} - {item.get('color').title()} {item.get('material').title()}")
                
                # Print compatibility notes if available
                if 'compatibility_notes' in outfit and outfit['compatibility_notes']:
                    print("\n📝 Compatibility Notes:")
                    for note in outfit['compatibility_notes']:
                        print(f"  • {note}")
                
                print(f"{'='*50}")
            
            return True
        else:
            logger.error(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to connect to the API: {e}")
        return False

def test_filter_inventory():
    """Test the filter-inventory endpoint."""
    logger.info("\n🔍 Testing filter-inventory endpoint...")
    
    # Create request payload (using the same as recommend-outfits)
    payload = create_sample_request()
    
    try:
        # Make the POST request
        response = requests.post(
            FILTER_ENDPOINT,
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "user_info": payload["user_info"],
                "occasion": payload["occasion"],
                "inventory": payload["inventory"]
            }
        )
        
        # Log response status
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_items = response.json()
            logger.info(f"✅ Success! Filtered inventory to {len(filtered_items)} items")
            
            # Group items by type for better display
            items_by_type = {}
            for item in filtered_items:
                item_type = item.get('item_type', 'other')
                if item_type not in items_by_type:
                    items_by_type[item_type] = []
                items_by_type[item_type].append(item)
            
            # Print items grouped by type
            print("\n📦 Filtered Inventory:")
            print("="*50)
            for item_type, items in items_by_type.items():
                print(f"\n{item_type.upper()}:")
                for item in items:
                    print(f"  • {item.get('name')} - {item.get('color').title()} {item.get('material').title()}")
                    print(f"    Occasion: {', '.join(item.get('occasion_suitability', []))}")
                    print(f"    Weather: {', '.join(item.get('weather_suitability', []))}")
                    print()
            
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
    
    # Run tests
    test_recommend_outfits()
    test_filter_inventory()
    
    print("\n✅ Test script completed!")
    print("\nYou can also access the interactive API documentation at:")
    print("http://127.0.0.1:8000/docs\n")
      "material": "silk",
      "size": "S",
      "style": ["formal", "elegant"],
      "weather_suitability": ["mild", "warm"],
      "occasion_suitability": ["business_casual", "formal"]
    },
    {
      "item_id": "acc1",
      "item_type": "accessory",
      "name": "Leather Belt",
      "color": "black",
      "material": "leather",
      "size": "M",
      "style": ["classic"],
      "weather_suitability": [],
      "occasion_suitability": ["business_casual", "formal", "casual"]
    }
  ],
  "max_outfits": 3,
  "consider_previous_outfits": True
}

# Headers
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

print("Sending request to the API...")
try:
    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Print the response status code and content
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\nSuccess! Here are the recommended outfits:")
        outfits = response.json()
        for i, outfit in enumerate(outfits, 1):
            print(f"\n=== Outfit #{i} (Confidence: {outfit.get('confidence_score', 0) * 100:.1f}%) ===")
            print("Items:")
            for item in outfit.get('items', []):
                print(f"- {item.get('name')} ({item.get('item_type')}): {item.get('color')} {item.get('material')}")
    else:
        print(f"\nError: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"\nFailed to connect to the API: {e}")
    print("\nPlease make sure the FastAPI server is running.")
    print("You can start it with:")
    print("1. cd /Users/veerraghuvanshi/CascadeProjects/outfit_curation_engine")
    print("2. source venv/bin/activate")
    print("3. PYTHONPATH=/Users/veerraghuvanshi/CascadeProjects/outfit_curation_engine uvicorn app.main:app --reload")
