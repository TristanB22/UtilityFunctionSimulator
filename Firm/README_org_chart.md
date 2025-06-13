# Organizational Chart Module

This module provides comprehensive organizational chart and corporate governance functionality for firms.

## Overview

The `org_chart.py` module contains:

- **OrgChart**: Main class managing the entire organizational structure
- **Role**: Defines positions with hierarchies, permissions, and voting rights
- **PersonInOrg**: Represents individuals within the organization
- **Shareholder**: Manages ownership and voting rights
- **Enums**: RoleType, VotingRights for standardized classifications

## Key Features

### 1. Complex Role Management
- Multiple roles per person (e.g., CEO who is also board member)
- Hierarchical levels (0=board, 1=C-suite, 2=VP, etc.)
- Permission-based firing/hiring authorities
- Department-based organization

### 2. Governance & Voting
- Shareholder voting rights (can differ from ownership percentage)
- Board member voting on specific matters
- Committee management (audit, compensation, etc.)
- Authority checks for firing and board removal

### 3. Management Hierarchy
- Chain of command tracking
- Direct and indirect reporting relationships
- Span of control analysis
- Manager assignment and reassignment

### 4. Advanced Queries
- Find common managers between employees
- Get all reports (direct/indirect) for a manager
- Department and role-type based searches
- Organizational depth analysis

## Usage Examples

### Basic Setup

```python
from Firm.org_chart import OrgChart, Role, RoleType, VotingRights, Shareholder
from Firm.firm import BaseFirm

# Create a firm
firm = BaseFirm(name="My Company")

# Define roles
ceo_role = Role(
    title="CEO",
    role_type=RoleType.EXECUTIVE,
    level=1,
    can_hire=True,
    can_fire=True,
    voting_rights=VotingRights.FULL
)

# Hire someone with multiple roles
board_role = Role(title="Board Member", role_type=RoleType.BOARD_MEMBER, level=0)
firm.hire("alice", [ceo_role, board_role])
```

### Shareholder Management

```python
# Add shareholders with different voting rights
firm.add_shareholder("alice", 0.25, voting_pct=0.30)  # More voting than ownership
firm.add_shareholder("investor", 0.40, share_class="preferred")

# Check voting power
alice_power = firm.get_voting_power("alice")  # Includes employee + shareholder voting
```

### Authority Checks

```python
# Check if someone can fire another person
can_fire = firm.can_fire_employee("manager_id", "employee_id")

# Check board removal authority
can_remove = firm.can_remove_board_member("chair_id", "member_id")

# Get management chain
chain = firm.get_chain_of_command("employee_id")  # Returns path to CEO
```

### Committee Management

```python
# Add people to committees
firm.org_chart.add_to_committee("audit", "board_member_id")
firm.org_chart.add_to_committee("compensation", "ceo_id")

# Get committee members
audit_members = firm.org_chart.get_committee_members("audit")
```

## Role Hierarchy Levels

- **Level 0**: Board of Directors
- **Level 1**: C-Suite (CEO, CTO, CFO, etc.)
- **Level 2**: Vice Presidents
- **Level 3**: Directors/Senior Managers
- **Level 4**: Managers
- **Level 5+**: Individual contributors

## Authority Rules

1. **Firing Authority**: Based on role permissions and hierarchy levels
2. **Hiring Authority**: Specified per role with `can_hire` flag
3. **Board Removal**: Requires significant voting power or chair authority
4. **Direct Reports**: Managers can typically fire their direct reports

## Integration with BaseFirm

The `BaseFirm` class has been updated to use the new organizational chart:

- `org_chart` field replaces simple role dictionary
- `hire()`, `fire()`, `promote()` methods use the new system
- Shareholder management integrated
- Authority checking methods added

## Example Output

Running the example (`Examples/org_chart_example.py`) shows:

```
=== TECHCORP INC. ORGANIZATIONAL ANALYSIS ===

1. ORGANIZATIONAL STRUCTURE:
Total employees: 7
Executives: ['alice_ceo', 'bob_cto']
Managers: ['eve_manager']
Board members: ['alice_ceo', 'charlie_board', 'diana_board']

4. OWNERSHIP STRUCTURE:
alice_ceo: 25.0% ownership, 58.3% voting power
venture_capital: 40.0% ownership, 40.0% voting power

5. AUTHORITY CHECKS:
CEO can fire CTO: True
Manager can fire engineer: True
Engineer can fire CEO: False
```

## Future Enhancements

Potential additions:
- Term limits for board members
- Voting thresholds for different decision types
- Salary/compensation integration
- Performance review workflows
- Succession planning
- Stock option management 