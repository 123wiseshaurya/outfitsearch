"""
Example usage of the Outfit Curation Engine.
This script demonstrates how to use the engine to generate outfit recommendations.
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the necessary components
from app.models.schemas import (
    UserInfo,
    OccasionInfo,
    ClothingItem,
    BodyType,
    SkinTone,
    ClothingType,
    OccasionType,
    WeatherType,
    OutfitRecommendationRequest
)
from app.core.engine import OutfitCurationEngine

def create_sample_request():
    """Create a sample outfit recommendation request."""
    logger.info("Creating sample request...")
    
    # Create user information
    user = UserInfo(
        user_id="user123",
        body_type=BodyType.RECTANGLE,
        skin_tone=SkinTone.MEDIUM,
        height_cm=170,
        style_preferences=["casual", "minimalist"],
        color_preferences=["blue", "white", "black"]
    )
    logger.info(f"Created user: {user}")
    
    # Create occasion information
    occasion = OccasionInfo(
        occasion_type=OccasionType.BUSINESS_CASUAL,
        weather=WeatherType.MILD,
        time_of_day="afternoon",
        location="office",
        dress_code="business_casual"
    )
    logger.info(f"Created occasion: {occasion}")
    
    # Create sample inventory with more items
    inventory = [
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
        # Add more tops
        ClothingItem(
            item_id="top3",
            item_type=ClothingType.TOP,
            name="Striped Button-Down",
            color="blue",
            material="cotton",
            size="M",
            style=["casual", "business"],
            weather_suitability=[WeatherType.MILD, WeatherType.WARM],
            occasion_suitability=[OccasionType.CASUAL, OccasionType.BUSINESS_CASUAL]
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
        ClothingItem(
            item_id="bottom2",
            item_type=ClothingType.BOTTOM,
            name="Khaki Chinos",
            color="khaki",
            material="cotton",
            size="32",
            style=["casual", "business"],
            weather_suitability=[WeatherType.MILD, WeatherType.WARM],
            occasion_suitability=[OccasionType.CASUAL, OccasionType.BUSINESS_CASUAL]
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
        ClothingItem(
            item_id="shoes2",
            item_type=ClothingType.SHOES,
            name="Brown Loafers",
            color="brown",
            material="leather",
            size="42",
            style=["casual", "business"],
            weather_suitability=[WeatherType.MILD, WeatherType.WARM],
            occasion_suitability=[OccasionType.CASUAL, OccasionType.BUSINESS_CASUAL]
        ),
        
        # Accessories
        ClothingItem(
            item_id="acc1",
            item_type=ClothingType.ACCESSORY,
            name="Leather Belt",
            color="black",
            material="leather",
            size="M",
            style=["classic"],
            weather_suitability=[],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL, OccasionType.CASUAL]
        ),
        ClothingItem(
            item_id="acc2",
            item_type=ClothingType.ACCESSORY,
            name="Silk Tie",
            color="navy",
            material="silk",
            size="OS",
            style=["formal"],
            weather_suitability=[],
            occasion_suitability=[OccasionType.BUSINESS_CASUAL, OccasionType.FORMAL]
        )
    ]
    
    logger.info(f"Created inventory with {len(inventory)} items")
    
    # Create the recommendation request
    request = OutfitRecommendationRequest(
        user_info=user,
        occasion=occasion,
        inventory=inventory,
        max_outfits=3,
        consider_previous_outfits=True
    )
    
    return request

def print_outfit(outfit, index):
    """Print outfit details in a user-friendly format."""
    print(f"\n=== Outfit #{index + 1} (Confidence: {outfit.confidence_score:.1%}) ===")
    print("Items:")
    for item in outfit.items:
        print(f"- {item.name} ({item.item_type.value}): {item.color} {item.material} (ID: {item.item_id})")
    if outfit.style_notes:
        print(f"\nStyle Notes: {outfit.style_notes}")
    print(f"Suitable for: {', '.join([o.value for o in outfit.occasion_suitability]) if hasattr(outfit, 'occasion_suitability') else 'Various occasions'}")

def main():
    print("=== Outfit Curation Engine Demo ===\n")
    
    try:
        # Create a sample request
        request = create_sample_request()
        
        # Initialize the engine
        engine = OutfitCurationEngine()
        
        # Print inventory stats
        total_items = len(request.inventory)
        items_by_type = {}
        for item in request.inventory:
            if item.item_type not in items_by_type:
                items_by_type[item.item_type] = 0
            items_by_type[item.item_type] += 1
        
        print("\n=== Inventory Summary ===")
        print(f"Total items: {total_items}")
        for item_type, count in items_by_type.items():
            print(f"- {item_type.value}: {count}")
        
        # Filter the inventory
        print("\n=== Filtering Inventory ===")
        print(f"Filtering inventory for occasion: {request.occasion.occasion_type.value}")
        print(f"Weather condition: {request.occasion.weather.value}")
        
        filtered_inventory = engine.filter_inventory(
            inventory=request.inventory,
            user_info=request.user_info,
            occasion=request.occasion
        )
        
        # Print filtered inventory stats
        filtered_items_by_type = {}
        for item in filtered_inventory:
            if item.item_type not in filtered_items_by_type:
                filtered_items_by_type[item.item_type] = 0
            filtered_items_by_type[item.item_type] += 1
        
        print(f"\nFiltered inventory: {len(filtered_inventory)} items (from {total_items} total)")
        for item_type, count in filtered_items_by_type.items():
            print(f"- {item_type.value}: {count}")
        
        # Generate outfit recommendations
        print("\n=== Generating Outfit Recommendations ===")
        print(f"Requesting up to {request.max_outfits} outfit recommendations...")
        
        outfits = engine.generate_outfits(
            filtered_inventory=filtered_inventory,
            user_info=request.user_info,
            occasion=request.occasion,
            max_outfits=request.max_outfits,
            consider_previous=request.consider_previous_outfits
        )
        
        # Display the results
        print(f"\n=== Results ===")
        print(f"Generated {len(outfits)} outfit recommendations:")
        
        if not outfits:
            print("\nNo outfits could be generated with the current inventory and filters.")
            print("This might be due to:")
            print("1. Not enough compatible items in the inventory")
            print("2. Overly restrictive filters (occasion, weather, etc.)")
            print("3. Missing essential item types (e.g., tops and bottoms)")
            
            # Print available item types in filtered inventory
            print("\nAvailable item types in filtered inventory:")
            for item_type in filtered_items_by_type.keys():
                print(f"- {item_type.value}")
        else:
            for i, outfit in enumerate(outfits):
                print_outfit(outfit, i)
        
        # Save the results to a JSON file
        output_file = "outfit_recommendations.json"
        with open(output_file, "w") as f:
            json_str = json.dumps([outfit.dict() for outfit in outfits], indent=2, default=str)
            f.write(json_str)
        
        print(f"\nRecommendations saved to {output_file}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")
        print("\nPlease check the logs for more details.")

if __name__ == "__main__":
    main()
