# Outfit Curation Engine — Model and System Explanation

This document explains the “ML model” approach used (currently a deterministic recommendation engine with ML-ready interfaces), the system architecture, and key design decisions made to satisfy the assignment requirements.

## Overview

- The engine recommends outfits from a user’s inventory given `user_info`, an `occasion`, and desired `max_outfits`.
- The system exposes a FastAPI service with two endpoints:
  - `POST /api/v1/recommend-outfits`
  - `POST /api/v1/filter-inventory`
- A simple static frontend (served at `/ui/`) allows interactive testing of the API.

## Data Model (Schemas)

Defined in `app/models/schemas.py` (Pydantic v2):

- `OccasionType`: `formal`, `casual`, `business_casual`, `sporty`, `evening`, `beach`, `party`
- `WeatherType`: `cool`, `mild`, `warm`, `hot`, `cold`, `rainy`
- `ClothingType`: `top`, `bottom`, `shoes`, `outerwear`, `accessory`, ...
- `ClothingItem`: includes `style`, `weather_suitability`, `occasion_suitability`
- `UserInfo`: body type, style/color preferences, etc.
- `OccasionInfo`: occasion + weather + context
- `Outfit`: a list of `ClothingItem`s with metadata and a `confidence_score`
- `OutfitRecommendationRequest`: request wrapper for recommendations

These enums and schemas enforce strict validity; the UI and test payloads serialize enums as strings.

## Recommendation Engine (Current Approach)

Implemented in `app/core/engine.py` as `OutfitCurationEngine`.

1. Filtering (`filter_inventory()`)
   - Filters inventory by:
     - Occasion suitability (with similarity aliases: e.g., `formal` ~ `business_casual`)
     - Weather suitability (normalized enum/string comparison)
     - Style preferences (with leniency for `business_casual`)
   - Progressive fallback:
     - Strict: occasion + weather + style
     - Fallback 1: occasion + weather (ignore style)
     - Fallback 2: occasion only (ignore style and weather)
   - Extensive logging explains per-item filter decisions.

2. Generation (`generate_outfits()`)
   - Determines required item types per occasion (e.g., `formal` requires `top`, `bottom`, `shoes`).
   - Randomly samples items per required type; adds complementary items opportunistically.
   - Deduplicates by item-id combinations; attempts multiple times for diversity.
   - Computes a confidence score and sorts results.

3. Validation (`_is_valid_outfit()`)
   - Blocks mixing contradictory styles (`formal` + `casual`).
   - Weather-aware checks:
     - Shoes must match current weather; rain boots only in `rainy` weather.
     - All non-accessory items must include current weather in `weather_suitability`.
     - Heuristics to avoid tees/shorts in `cold` and heavy coats in `hot` (unless rain).
   - Color compatibility (simple cap on number of distinct colors).

4. Confidence Scoring (`_calculate_confidence()`)
   - Base score with bonuses for:
     - Items explicitly suitable for the current occasion
     - Items whose colors match user preferences
   - Returns 0.0–1.0 and is rounded to 2 decimals for UI display (as 0–100%).

## Why This Approach (and ML Readiness)

- The assignment prioritizes deterministic, explainable logic with detailed logging for debugging.
- The filtering and generation layers are designed to be replaced or augmented by ML:
  - Learn a compatibility function f(item, context) for ranking.
  - Replace fallback rules with a learned calibration model for sparsity conditions.
  - Use a learned reranker for final outfit scoring that considers interactions (color theory, occasion norms, user taste), trained from implicit/explicit feedback.

### Integrating an ML Model (Future Work)

1. Feature Engineering
   - Item embeddings: color, material, style, brand, historical co-wear patterns.
   - Context features: occasion, weather, time of day, location.
   - User features: preferences, past accept/reject, body type.

2. Model Candidates
   - Pairwise ranking (e.g., XGBoost/LightGBM) over item-context.
   - Graph-based co-occurrence for multi-item compatibility.
   - Transformer-based reranker over sets for outfit-level scoring.

3. Training Signals
   - Clickthrough and dwell time (implicit)
   - Saves/likes/purchases (explicit)
   - Negative signals: skipped, quickly discarded outfits

4. Online Inference
   - Keep `filter_inventory()` as a first-pass recall filter.
   - Use ML model for ranking/scoring; optionally diversify results with MMR/coverage constraints.

## System Architecture

- `app/main.py`: FastAPI app, CORS, static files (`/ui`), logging.
- `app/api/endpoints.py`: endpoints, with detailed request/response logging.
- `app/core/engine.py`: core logic (filter, generate, validate, score).
- `app/static/`: `index.html`, `app.js`, `styles.css` (simple UI for testing).
- `test_api_clean.py`: end-to-end test against the running API.

## Logging & Debugging

- Engine and API log per-item decisions and outcomes to `app.log`.
- Test script also logs payloads and responses to `test.log`.
- Common pitfalls addressed:
  - Enum serialization mismatches (fixed by converting to string values in payloads)
  - Overly strict style filtering (added leniency + fallbacks)
  - No results for edge cases (occasion similarity + progressive relaxation)

## Assumptions & Limitations

- Inventory is user-specific and can be edited in the UI.
- Current engine is rule-based for transparency; not a trained ML model yet.
- Confidence scoring is heuristic; a learned model would outperform it.
- Weather/occasion suitability must be curated; poor metadata reduces quality.

## How This Meets the Assignment

- Fully functional API with deterministic, explainable logic.
- Comprehensive logging to debug why zero outfits are returned.
- UI to interactively test all Occasion × Weather combinations.
- Schema-compatible dataset expanded to guarantee coverage.
- Clear path to integrate ML for ranking/reranking without changing the API.
