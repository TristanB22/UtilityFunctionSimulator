# Agent

This directory contains the agent-based modeling components for the World_Sim project.

## Components

### Agent Class
- Base agent implementation
- Individual behavior modeling
- State management
- Interaction protocols

### L2 Data Integration
- L2 data object handling
- Demographic data processing
- Geographic data integration
- Data validation

## Features

### Agent Behavior
- Decision making
- Resource management
- Interaction with other agents
- State transitions
- Goal-oriented behavior

### Data Management
- L2 data processing
- Demographic information
- Geographic location
- Economic status
- Social characteristics

## Usage

```python
from Agent import Agent
from Agent import L2_Data_Object

# Create an agent with L2 data
l2_obj = L2_Data_Object(row_data)
agent = Agent(id=1, l2_object=l2_obj)

# Access agent properties
print(agent.demographics)
print(agent.location)
print(agent.economic_status)
```

## Agent Types

### Individual Agents
- Personal characteristics
- Economic behavior
- Social interactions
- Decision making

### Household Agents
- Family composition
- Resource sharing
- Collective decision making
- Economic unit behavior

### Business Agents
- Firm interactions
- Employment decisions
- Economic transactions
- Market participation

## Data Integration

### L2 Data
- Demographic information
- Geographic location
- Economic indicators
- Social characteristics

### Geographic Data
- Location coordinates
- Administrative boundaries
- Neighborhood information
- Transportation access

## Configuration

Agent behavior can be configured through:
- Individual parameters
- Environmental settings
- Social norms
- Economic conditions

## Contributing

When adding new agent types:
1. Inherit from base Agent class
2. Implement required methods
3. Add type-specific attributes
4. Update data processing
5. Add appropriate tests
6. Update documentation

## Best Practices

1. Use appropriate design patterns
2. Implement proper error handling
3. Add comprehensive logging
4. Include type hints
5. Document all methods
6. Add unit tests
7. Consider social dynamics
8. Model realistic behavior

## Testing

- Unit tests for agent behavior
- Integration tests for interactions
- Data validation tests
- Performance testing
- Scenario testing 