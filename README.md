# Outfit Curation Engine
<img src="docs/images/ui_preview.png" alt="Outfit Curation Engine UI" width="900" />
An intelligent outfit recommendation system that curates outfits based on user preferences, inventory, and occasion.

## Features

- **User-Centric Filtering**: Personalize recommendations based on body type, skin tone, and style preferences.
- **Occasion-Aware Suggestions**: Get outfit recommendations tailored to specific events, weather conditions, and dress codes.
- **Intelligent Matching**: Advanced algorithms ensure color coordination and style compatibility.
- **RESTful API**: Easy integration with web and mobile applications.

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/outfit-curation-engine.git
   cd outfit-curation-engine
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the FastAPI server:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`

3. Access the interactive API documentation at:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

### Frontend UI (Static)

- A minimal static UI is served from `app/static/` and mounted at `/ui`.
- Open `http://127.0.0.1:8000/ui/` to test the API interactively.
- The UI pre-fills a schema-compatible inventory that covers all Occasion × Weather combinations and can be edited inline.

## API Endpoints

### Get Outfit Recommendations

```http
POST /api/v1/recommend-outfits
```

**Request Body:**
```json
{
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
    {
      "item_id": "item1",
      "item_type": "top",
      "name": "Blue Dress Shirt",
      "color": "blue",
      "material": "cotton",
      "size": "M",
      "style": ["formal", "business"],
      "weather_suitability": ["cool", "mild", "warm"],
      "occasion_suitability": ["business_casual", "formal"]
    }
  ],
  "max_outfits": 3,
  "consider_previous_outfits": true
}
```

### Filter Inventory

```http
POST /api/v1/filter-inventory
```

**Request Body:**
```json
{
  "inventory": [
    {
      "item_id": "item1",
      "item_type": "top",
      "name": "T-Shirt",
      "color": "red",
      "material": "cotton",
      "size": "M",
      "style": ["casual"],
      "weather_suitability": ["warm", "hot"],
      "occasion_suitability": ["casual"]
    }
  ],
  "user_info": {
    "user_id": "user123",
    "body_type": "rectangle",
    "skin_tone": "medium",
    "height_cm": 170
  },
  "occasion": {
    "occasion_type": "casual",
    "weather": "warm",
    "time_of_day": "afternoon"
  }
}
```

## Project Structure

```
outfit-curation-engine/
├── app/
│   ├── api/
│   │   └── endpoints.py       # API route handlers
│   ├── core/
│   │   └── engine.py          # Outfit recommendation logic
│   ├── models/
│   │   └── schemas.py         # Pydantic models and schemas
│   └── main.py                # FastAPI application
├── app/static/                # Simple web UI (index.html, app.js, styles.css)
├── tests/                     # Unit and integration tests
├── data/                      # Sample data and resources (optional)
├── docs/
│   └── ASSIGNMENT_EXPLANATION.md  # Model/system explanation per assignment
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Testing

Run the test suite with:

```bash
pytest
```

## Assignment Notes

- The recommendation engine is rule-based and ML-ready. See `docs/ASSIGNMENT_EXPLANATION.md` for details on the model approach, system architecture, logging, and how an ML ranker can be integrated without changing the API.


## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by modern fashion recommendation systems
- Built with FastAPI and Pydantic
- Color theory and style compatibility algorithms
