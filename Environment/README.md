# Environment

This directory contains components for handling geographic and environmental data in the World_Sim project.

## Components

### OSM Data Integration (`osm_pull.py`)
- Pulls OpenStreetMap data for specified locations
- Handles street networks, building footprints, and administrative boundaries
- Supports both city-level and state-level data
- Includes data validation and error handling

### Google Maps Enrichment (`google_maps_enrichment.py`)
- Enriches OSM building data with Google Maps information
- Features:
  - Business names and types
  - Addresses and locations
  - Ratings and reviews
  - Operating hours
  - Contact information
- Implements rate limiting for API quota management
- Includes caching for efficient data reuse

## Usage

### OSM Data Pull
```python
from Environment.osm_pull import pull_osm_data

network_path, features_path, boundary_path = pull_osm_data(
    place="Bar Harbor, Maine, USA",
    output_dir="/path/to/output",
    force=False
)
```

### Google Maps Enrichment
```python
from Environment.google_maps_enrichment import enrich_osm_data

enriched_path = enrich_osm_data(
    features_path="path/to/features.geojson",
    output_path="path/to/output",
    testing=True
)
```

## Data Formats

### OSM Data
- Network: GraphML format
- Features: GeoJSON format
- Boundary: GeoJSON format

### Enriched Data
- Buildings: GeoJSON format with additional Google Maps attributes
- Cache: JSON format for efficient data reuse

## Configuration

Required environment variables:
```
OSM_DATA_DIRECTORY=/path/to/osm/data
TESTING_OSM_DATA_DIRECTORY=/path/to/testing/osm/data
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

## Rate Limiting

The Google Maps API integration includes rate limiting:
- 100 requests per minute
- 10,000 requests per month (free tier)

## Testing

Use the `--testing` flag to:
- Limit data processing to a small subset
- Use testing-specific directories
- Enable verbose logging

## Error Handling

Both modules include comprehensive error handling for:
- API failures
- Data validation
- File I/O operations
- Rate limit exceeded
- Invalid input parameters

## Contributing

When adding new features:
1. Follow the existing code structure
2. Include appropriate error handling
3. Add rate limiting for API calls
4. Update documentation
5. Add tests for new functionality 