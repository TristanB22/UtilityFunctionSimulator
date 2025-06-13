# World_Sim

A comprehensive economic and social simulation environment that models real-world interactions using both OpenStreetMap (OSM) and Google Maps data.

## Project Structure

```
World_Sim/
├── Agent/           # Agent-based modeling components
├── Analysis/        # Data analysis and visualization tools
├── Environment/     # Geographic and environmental data handling
├── Firm/           # Business entity implementations
├── Institution/     # Institutional framework components
├── Labor/          # Labor market simulation
├── Settings/       # Configuration and parameters
└── Tools/          # Utility functions and evaluation tools
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in a `.env` file:
```
OSM_DATA_DIRECTORY=/path/to/osm/data
TESTING_OSM_DATA_DIRECTORY=/path/to/testing/osm/data
L2_DATA_DIRECTORY=/path/to/l2/data
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

## Core Features

### Geographic Data Integration
- OpenStreetMap data integration for real-world locations
- Google Maps enrichment for detailed building information
- Support for both city-level and state-level data

### Economic Simulation
- Multiple firm types (Retail, Manufacturing, Healthcare, etc.)
- Labor market dynamics
- Institutional frameworks
- Agent-based modeling

### Analysis Tools
- Data visualization
- Economic metrics calculation
- Performance evaluation

## Usage

### Basic OSM Data Pull
```bash
python run.py --place "Bar Harbor, Maine, USA"
```

### Using Individual Components
```bash
python run.py --city "Bar Harbor" --state-name "Maine" --country "USA"
```

### Using L2 State Data
```bash
python run.py --state DE
```

### Testing Mode
```bash
python run.py --place "Bar Harbor, Maine, USA" --testing
```

### Google Maps Enrichment
```bash
python run.py --place "Bar Harbor, Maine, USA" --enrich-google
```

## Directory-Specific Documentation

- [Agent/README.md](Agent/README.md) - Agent-based modeling components
- [Analysis/README.md](Analysis/README.md) - Analysis tools and visualizations
- [Environment/README.md](Environment/README.md) - Geographic data handling
- [Firm/README.md](Firm/README.md) - Business entity implementations
- [Institution/README.md](Institution/README.md) - Institutional frameworks
- [Labor/README.md](Labor/README.md) - Labor market simulation
- [Settings/README.md](Settings/README.md) - Configuration management
- [Tools/README.md](Tools/README.md) - Utility functions and evaluation tools

## Development

### Adding New Features
1. Create appropriate tests in the relevant directory
2. Implement the feature following the existing code structure
3. Update documentation
4. Submit a pull request

### Testing
- Use `--testing` flag for development and testing
- Follow the testing guidelines in each directory's README

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Rate Limiting

The Google Maps API integration includes rate limiting to stay within the free tier limits:
- 100 requests per minute
- 10,000 requests per month

In testing mode, only the first 10 buildings are enriched to conserve API quota.

## Output Files

When using Google Maps enrichment, the following files are generated:
- `{place}_network.graphml`: OSM street network
- `{place}_all_features.geojson`: All OSM features
- `{place}_boundary.geojson`: Administrative boundary
- `{place}_all_features_enriched.geojson`: Enriched building data
- `{place}_all_features_enriched_cache.json`: Cache of enriched data

## Notes

- The Google Maps enrichment is designed to work within the free tier limits
- In testing mode, only a small subset of buildings is processed
- A cache is maintained to avoid re-processing buildings
- Rate limiting is implemented to prevent API quota exhaustion 