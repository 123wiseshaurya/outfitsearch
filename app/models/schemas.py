from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

# Enums for various attributes
class BodyType(str, Enum):
    HOURGLASS = "hourglass"
    TRIANGLE = "triangle"
    INVERTED_TRIANGLE = "inverted_triangle"
    RECTANGLE = "rectangle"
    OVAL = "oval"
    DIAMOND = "diamond"

class SkinTone(str, Enum):
    FAIR = "fair"
    LIGHT = "light"
    MEDIUM = "medium"
    OLIVE = "olive"
    BROWN = "brown"
    DARK = "dark"

class ClothingType(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"
    DRESS = "dress"
    OUTERWEAR = "outerwear"
    SHOES = "shoes"
    ACCESSORY = "accessory"

class OccasionType(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    BUSINESS_CASUAL = "business_casual"
    SPORTY = "sporty"
    EVENING = "evening"
    BEACH = "beach"
    PARTY = "party"

class WeatherType(str, Enum):
    HOT = "hot"
    WARM = "warm"
    MILD = "mild"
    COOL = "cool"
    COLD = "cold"
    RAINY = "rainy"
    SNOWY = "snowy"

# Core Models
class UserInfo(BaseModel):
    user_id: str
    body_type: BodyType
    skin_tone: SkinTone
    height_cm: float
    age: Optional[int] = None
    style_preferences: List[str] = Field(default_factory=list)
    color_preferences: List[str] = Field(default_factory=list)
    fit_preferences: Dict[str, str] = Field(default_factory=dict)

class OccasionInfo(BaseModel):
    occasion_type: OccasionType
    weather: WeatherType
    time_of_day: str  # morning, afternoon, evening, night
    location: Optional[str] = None
    dress_code: Optional[str] = None
    additional_notes: Optional[str] = None

class ClothingItem(BaseModel):
    item_id: str
    item_type: ClothingType
    name: str
    brand: Optional[str] = None
    color: str
    pattern: Optional[str] = None
    material: str
    size: str
    style: List[str] = Field(default_factory=list)
    weather_suitability: List[WeatherType] = Field(default_factory=list)
    occasion_suitability: List[OccasionType] = Field(default_factory=list)
    image_url: Optional[HttpUrl] = None
    last_worn: Optional[datetime] = None
    is_clean: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Outfit(BaseModel):
    outfit_id: str
    items: List[ClothingItem]
    occasion: OccasionType
    confidence_score: float = Field(ge=0.0, le=1.0)
    style_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_worn: Optional[datetime] = None

class OutfitRecommendationRequest(BaseModel):
    user_info: UserInfo
    occasion: OccasionInfo
    inventory: List[ClothingItem]
    max_outfits: int = 5
    consider_previous_outfits: bool = True
    style_preferences: Optional[List[str]] = None
    color_preferences: Optional[List[str]] = None
