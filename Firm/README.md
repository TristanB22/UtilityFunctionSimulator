# Firm

This directory contains implementations of various business entity types for the World_Sim project.

## Firm Types

### Base Firm
- Abstract base class for all firm types
- Common attributes and methods
- NAICS code mapping

### Specialized Firms

#### Financial Firms (`financial_firm.py`)
- Banking and financial services
- Risk ratings
- Service types

#### Professional Services (`professional_services_firm.py`)
- Consulting and professional services
- Billing models
- Practice areas
- Consultant levels

#### Construction (`construction_firm.py`)
- Construction types
- Project phases
- Resource management

#### Education (`education_firm.py`)
- Education types
- Degree levels
- Student management
- Funding sources

#### Utilities (`utilities_firm.py`)
- Utility types
- Fuel types
- Rate structures

#### Agriculture (`agriculture_firm.py`)
- Crop types
- Livestock types
- Production methods

#### Hospitality (`hospitality_firm.py`)
- Accommodation types
- Reservation management
- Service types

#### Manufacturing (`manufacturing_firm.py`)
- Manufacturing types
- Production strategies
- Inventory management

#### Transportation (`transportation_firm.py`)
- Transport modes
- Service types
- Vehicle management

#### Mining (`mining_firm.py`)
- Extraction types
- Project phases
- Resource management

#### Support Services (`support_services_firm.py`)
- Service types
- Management companies
- Government agencies

#### Wholesale (`wholesale_firm.py`)
- Wholesale types
- Product categories
- Customer types

#### Healthcare (`healthcare_firm.py`)
- Healthcare types
- Insurance types
- Service lines
- Patient management

#### Retail (`retail_firm.py`)
- Retail channels
- Retail formats
- Merchandise categories

#### Information (`information_firm.py`)
- Information types
- Content types
- Revenue models
- Delivery channels

## Usage

```python
from Firm import create_firm

# Create a firm based on NAICS code
firm = create_firm(
    naics_code="441110",
    name="Example Retail Store",
    location="Bar Harbor, ME"
)
```

## Organization Structure

### Org Chart (`org_chart.py`)
- Role types
- Voting rights
- Organizational hierarchy
- Management structure

## Features

Each firm type includes:
- Industry-specific attributes
- Business logic
- Resource management
- Performance metrics
- Market interaction
- Employee management

## Configuration

Firm behavior can be configured through:
- NAICS codes
- Industry parameters
- Market conditions
- Regulatory environment

## Contributing

When adding new firm types:
1. Inherit from BaseFirm
2. Implement required methods
3. Add industry-specific attributes
4. Update NAICS mapping
5. Add appropriate tests
6. Update documentation

## Best Practices

1. Use appropriate design patterns
2. Implement proper error handling
3. Add comprehensive logging
4. Include type hints
5. Document all methods
6. Add unit tests
7. Follow industry standards
8. Consider market dynamics 