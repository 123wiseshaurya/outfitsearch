from typing import List, Dict, Optional
import random
from datetime import datetime, timedelta
import numpy as np
from ..models.schemas import (
    ClothingItem,
    Outfit,
    UserInfo,
    OccasionInfo,
    ClothingType,
    WeatherType,
    OccasionType
)

class OutfitCurationEngine:
    def __init__(self):
        self.compatibility_rules = self._initialize_compatibility_rules()
        
    def _initialize_compatibility_rules(self) -> Dict[str, List[str]]:
        """Initialize rules for clothing compatibility"""
        return {
            'top-bottom': {
                'rules': [
                    (['formal_shirt'], ['formal_pants', 'formal_skirt']),
                    (['t-shirt'], ['jeans', 'shorts', 'skirt']),
                    (['blouse'], ['pencil_skirt', 'formal_pants'])
                ]
            },
            'color': {
                'complementary': [
                    ('red', 'green'),
                    ('blue', 'orange'),
                    ('yellow', 'purple')
                ],
                'analogous': 3,  # Number of colors to consider for analogous matching
                'monochromatic': True
            },
            'occasion_specific': {
                OccasionType.FORMAL: {
                    'required_types': [ClothingType.TOP, ClothingType.BOTTOM, ClothingType.SHOES],
                    'recommended_colors': ['black', 'navy', 'gray', 'white']
                },
                OccasionType.BUSINESS_CASUAL: {
                    'required_types': [ClothingType.TOP, ClothingType.BOTTOM, ClothingType.SHOES],
                    'recommended_colors': ['navy', 'gray', 'white', 'black']
                },
                OccasionType.CASUAL: {
                    'required_types': [ClothingType.TOP, ClothingType.BOTTOM],
                    'recommended_colors': []  # No specific color restrictions
                },
                OccasionType.SPORTY: {
                    'required_types': [ClothingType.TOP, ClothingType.BOTTOM, ClothingType.SHOES],
                    'recommended_colors': []
                },
                OccasionType.EVENING: {
                    'required_types': [ClothingType.TOP, ClothingType.BOTTOM, ClothingType.SHOES],
                    'recommended_colors': ['black', 'navy']
                },
                OccasionType.BEACH: {
                    'required_types': [ClothingType.TOP, ClothingType.BOTTOM],
                    'recommended_colors': ['white', 'beige', 'light_blue']
                }
            }
        }
    
    def filter_inventory(
        self, 
        inventory: List[ClothingItem], 
        user_info: UserInfo, 
        occasion: OccasionInfo
    ) -> List[ClothingItem]:
        """Filter inventory based on user attributes and occasion"""
        import logging
        logger = logging.getLogger(__name__)
        
        strict_filtered: List[ClothingItem] = []
        ignore_style_filtered: List[ClothingItem] = []
        ignore_style_weather_filtered: List[ClothingItem] = []

        skipped_occasion = 0
        skipped_weather = 0
        skipped_style = 0
        
        def enum_value(x):
            try:
                return x.value  # Enum
            except AttributeError:
                return str(x)

        req_occ_val = enum_value(occasion.occasion_type)
        req_weather_val = enum_value(occasion.weather)

        logger.info(f"Filtering {len(inventory)} items for occasion: {req_occ_val}, weather: {req_weather_val}")
        logger.info(f"Occasion type: {type(occasion.occasion_type).__name__}, value: {req_occ_val}")
        logger.info(f"Weather type: {type(occasion.weather).__name__}, value: {req_weather_val}")
        
        # Occasion similarity aliases for graceful matching
        occasion_aliases = {
            'formal': ['business_casual'],
            'business_casual': ['casual', 'formal'],
            'party': ['casual', 'formal'],
            'date': ['casual', 'business_casual'],
            'sport': ['casual'],
            'travel': ['casual', 'business_casual'],
        }
        requested_occ = req_occ_val
        allowed_occasions = {requested_occ, *occasion_aliases.get(requested_occ, [])}

        for item in inventory:
            logger.info(f"\n--- Processing item: {item.item_id} ({item.name}) ---")
            logger.info(f"Item type: {item.item_type}")
            logger.info(f"Occasion suitability: {item.occasion_suitability} (type: {type(item.occasion_suitability[0]).__name__ if item.occasion_suitability else 'empty'})")
            logger.info(f"Weather suitability: {item.weather_suitability} (type: {type(item.weather_suitability[0]).__name__ if item.weather_suitability else 'empty'})")

            # Occasion match (uses similarity aliases but not fully ignored)
            occasion_values = [enum_value(occ) for occ in item.occasion_suitability]
            occasion_match = any(val in allowed_occasions for val in occasion_values)
            logger.info(
                f"Occasion match: {occasion_match} (requested: '{requested_occ}', allowed: {sorted(allowed_occasions)}, item: {occasion_values})"
            )
            if not occasion_match:
                skipped_occasion += 1
                logger.info(f"❌ Skipping item {item.item_id} - occasion mismatch: '{occasion.occasion_type}' not in {[str(occ) for occ in item.occasion_suitability]}")
                continue

            # Weather match (can be relaxed)
            weather_values = [enum_value(w) for w in item.weather_suitability]
            weather_match = any(w == req_weather_val for w in weather_values)
            logger.info(f"Weather match: {weather_match} (looking for '{req_weather_val}' in {weather_values})")
            
            # Style match (can be relaxed + business_casual leniency)
            style_match = True
            if user_info.style_preferences:
                if str(occasion.occasion_type) == 'business_casual':
                    style_match = any(s in ['business', 'formal', 'classic'] or s in user_info.style_preferences for s in item.style)
                    logger.info("Style match (business casual leniency) evaluated")
                else:
                    style_match = any(s in user_info.style_preferences for s in item.style)
            logger.info(f"Style match: {style_match} (user prefs: {user_info.style_preferences}, item styles: {item.style})")

            # Build filtered lists according to match combinations
            if weather_match and style_match:
                strict_filtered.append(item)
                logger.info(f"✅ Item {item.item_id} passed strict filters")
            if weather_match:
                ignore_style_filtered.append(item)
            # Always eligible for most-relaxed if occasion matches
            ignore_style_weather_filtered.append(item)

            if not weather_match:
                skipped_weather += 1
            if not style_match:
                skipped_style += 1
        
        logger.info("\n=== Filtering Results (strict) ===")
        logger.info(f"Strict filtered items: {len(strict_filtered)}")
        logger.info(f"Skipped (occasion): {skipped_occasion}, (weather): {skipped_weather}, (style): {skipped_style}")

        # Progressive fallback: relax style, then weather
        if strict_filtered:
            return strict_filtered
        logger.warning("No items after strict filtering. Retrying ignoring style preferences...")
        if ignore_style_filtered:
            return ignore_style_filtered
        logger.warning("Still no items after ignoring style. Retrying ignoring style AND weather suitability...")
        return ignore_style_weather_filtered
    
    def generate_outfits(
        self,
        filtered_inventory: List[ClothingItem],
        user_info: UserInfo,
        occasion: OccasionInfo,
        max_outfits: int = 5,
        consider_previous: bool = True
    ) -> List[Outfit]:
        """Generate outfit recommendations based on filtered inventory"""
        import logging
        logger = logging.getLogger(__name__)
        
        if not filtered_inventory:
            logger.warning("No items in filtered inventory to generate outfits")
            return []
            
        logger.info(f"Generating outfits from {len(filtered_inventory)} filtered items")
            
        # Categorize items by type
        items_by_type = self._categorize_items(filtered_inventory)
        
        # Get required item types for this occasion
        required_types = self.compatibility_rules['occasion_specific'].get(
            occasion.occasion_type, 
            {}
        ).get('required_types', [ClothingType.TOP, ClothingType.BOTTOM])
        
        # Generate possible combinations (with deduplication and light diversity)
        outfits = []
        seen_combos = set()
        # Shuffle item pools a bit for diversity
        for k in list(items_by_type.keys()):
            random.shuffle(items_by_type[k])

        attempts = 0
        max_attempts = max(10, max_outfits * 5)
        while len(outfits) < max_outfits and attempts < max_attempts:
            attempts += 1
            outfit_items = []

            # Try to include at least one item of each required type
            for item_type in required_types:
                pool = items_by_type.get(item_type, [])
                if pool:
                    item = random.choice(pool)
                    outfit_items.append(item)

            # Add complementary items (like accessories, outerwear)
            self._add_complementary_items(outfit_items, items_by_type)

            # Check if outfit is valid
            is_valid = self._is_valid_outfit(outfit_items, occasion)
            if not is_valid:
                logger.debug(f"Skipping invalid outfit with items: {[item.item_id for item in outfit_items]}")
                continue

            combo_key = tuple(sorted([it.item_id for it in outfit_items]))
            if combo_key in seen_combos:
                logger.debug(f"Skipping duplicate outfit combo: {combo_key}")
                continue

            seen_combos.add(combo_key)
            conf = round(self._calculate_confidence(outfit_items, user_info, occasion), 2)
            outfit = Outfit(
                outfit_id=f"outfit_{len(outfits) + 1}",
                items=outfit_items,
                occasion=occasion.occasion_type,
                confidence_score=conf
            )
            outfits.append(outfit)
        
        # Sort by confidence score (desc)
        outfits.sort(key=lambda x: (x.confidence_score or 0), reverse=True)
        return outfits[:max_outfits]
    
    def _categorize_items(self, items: List[ClothingItem]) -> Dict[ClothingType, List[ClothingItem]]:
        """Categorize items by their type"""
        categorized = {}
        for item in items:
            if item.item_type not in categorized:
                categorized[item.item_type] = []
            categorized[item.item_type].append(item)
        return categorized
    
    def _add_complementary_items(
        self, 
        outfit_items: List[ClothingItem],
        available_items: Dict[ClothingType, List[ClothingItem]]
    ) -> None:
        """Add complementary items to the outfit"""
        # Example: Add outerwear if it's cold
        if ClothingType.OUTERWEAR in available_items and len(outfit_items) >= 2:
            if random.random() > 0.7:  # 30% chance to add outerwear
                outfit_items.append(random.choice(available_items[ClothingType.OUTERWEAR]))
        
        # Example: Add accessories
        if ClothingType.ACCESSORY in available_items and len(outfit_items) > 0:
            if random.random() > 0.5:  # 50% chance to add an accessory
                outfit_items.append(random.choice(available_items[ClothingType.ACCESSORY]))
    
    def _is_valid_outfit(
        self, 
        items: List[ClothingItem], 
        occasion: OccasionInfo
    ) -> bool:
        """Check if the combination of items forms a valid outfit"""
        if not items:
            return False
            
        # Check for basic rules (e.g., don't mix formal and casual)
        styles = [style for item in items for style in item.style]
        if 'formal' in styles and 'casual' in styles:
            return False
            
        # Weather-aware sanity checks (shoes stricter than other items)
        def enum_value(x):
            try:
                return x.value
            except AttributeError:
                return str(x)

        current_weather = enum_value(occasion.weather)

        for item in items:
            # Avoid rain-specific footwear unless it's rainy
            if item.item_type == ClothingType.SHOES:
                name_lower = (item.name or '').lower()
                if 'rain' in name_lower and current_weather != 'rainy':
                    return False
                # Enforce shoes match current weather for practicality
                allowed_weathers = [enum_value(w) for w in item.weather_suitability]
                if current_weather not in allowed_weathers:
                    return False

            # For all non-accessory items, require weather suitability to include current weather
            if item.item_type.name.lower() != 'accessory':
                allowed_weathers = [enum_value(w) for w in item.weather_suitability]
                if current_weather not in allowed_weathers:
                    return False

            name_lower = (item.name or '').lower()
            # Heuristics: avoid clearly unsuitable garments for extremes
            if current_weather == 'cold':
                # Avoid T-shirts/Tees in cold
                if item.item_type == ClothingType.TOP and ('tee' in name_lower or 't-shirt' in name_lower):
                    return False
                # Avoid shorts in cold
                if item.item_type == ClothingType.BOTTOM and ('short' in name_lower):
                    return False
            if current_weather == 'hot':
                # Avoid heavy overcoats in hot
                if item.item_type == ClothingType.OUTERWEAR and ('coat' in name_lower or 'jacket' in name_lower) and 'rain' not in name_lower:
                    return False

        # Check color compatibility
        if not self._check_color_compatibility([item.color for item in items]):
            return False
            
        return True
    
    def _check_color_compatibility(self, colors: List[str]) -> bool:
        """Check if colors in the outfit are compatible"""
        if not colors:
            return True
            
        # Simple compatibility check - avoid too many different colors
        if len(set(colors)) > 4:  # More than 4 different colors is probably too much
            return False
            
        # Additional color theory checks could be added here
        return True
    
    def _calculate_confidence(
        self, 
        items: List[ClothingItem], 
        user_info: UserInfo, 
        occasion: OccasionInfo
    ) -> float:
        """Calculate a confidence score for the outfit (0.0 to 1.0)"""
        if not items:
            return 0.0
            
        score = 0.5  # Base score
        
        # Increase score based on occasion matching
        for item in items:
            if occasion.occasion_type in item.occasion_suitability:
                score += 0.1
                
        # Increase score if colors match user preferences
        if user_info.color_preferences:
            for item in items:
                if item.color.lower() in [c.lower() for c in user_info.color_preferences]:
                    score += 0.05
        
        # Normalize score to be between 0 and 1
        return min(1.0, max(0.0, score))
