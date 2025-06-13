# mining_firm.py
# NAICS 21: Mining, Quarrying, and Oil and Gas Extraction

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class ExtractionType(Enum):
    OIL = "oil"
    NATURAL_GAS = "natural_gas"
    COAL = "coal"
    METALS = "metals"
    MINERALS = "minerals"
    QUARRYING = "quarrying"

class ProjectPhase(Enum):
    EXPLORATION = "exploration"
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    DECOMMISSIONING = "decommissioning"

@dataclass
class MineralReserve:
    reserve_id: str
    location: str
    extraction_type: ExtractionType
    proven_reserves: float  # tons, barrels, etc.
    probable_reserves: float
    current_phase: ProjectPhase
    extraction_cost_per_unit: float
    environmental_bond: float

@dataclass
class ExplorationProject:
    project_id: str
    location: str
    target_resource: ExtractionType
    investment_to_date: float
    success_probability: float
    estimated_reserves: float
    start_date: date

@dataclass
class MiningFirm(BaseFirm):
    # Resource assets
    mineral_reserves: List[MineralReserve] = field(default_factory=list)
    exploration_projects: List[ExplorationProject] = field(default_factory=list)
    production_capacity: Dict[str, float] = field(default_factory=dict)  # reserve_id -> daily output
    
    # Operations infrastructure
    extraction_equipment: Dict[str, Any] = field(default_factory=dict)  # rigs, miners, etc.
    processing_facilities: List[str] = field(default_factory=list)
    transportation_infrastructure: Dict[str, str] = field(default_factory=dict)  # pipelines, rail
    
    # Financial and market factors
    commodity_hedging_contracts: Dict[str, Any] = field(default_factory=dict)
    price_volatility_exposure: Dict[ExtractionType, float] = field(default_factory=dict)
    finding_development_costs: float = 0.0  # exploration costs per unit found
    
    # Regulatory and environmental
    mining_permits: List[str] = field(default_factory=list)
    environmental_bonds: Dict[str, float] = field(default_factory=dict)  # reserve_id -> bond amount
    safety_certifications: List[str] = field(default_factory=list)
    remediation_liabilities: float = 0.0
    
    # Operational metrics
    daily_production_targets: Dict[str, float] = field(default_factory=dict)
    safety_incident_count: int = 0
    environmental_compliance_score: float = 1.0
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "21"  # Mining base code
    
    # Exploration and development
    def start_exploration_project(self, project: ExplorationProject) -> None:
        """Begin new exploration project"""
        self.exploration_projects.append(project)
        self.post("exploration_capex", "cash", project.investment_to_date, 
                 f"Exploration: {project.project_id}")
    
    def complete_exploration(self, project_id: str, success: bool, 
                           actual_reserves: float = 0) -> bool:
        """Complete exploration and potentially move to development"""
        project = next((p for p in self.exploration_projects if p.project_id == project_id), None)
        if not project:
            return False
        
        if success and actual_reserves > 0:
            # Convert to proven reserve
            new_reserve = MineralReserve(
                reserve_id=project_id,
                location=project.location,
                extraction_type=project.target_resource,
                proven_reserves=actual_reserves,
                probable_reserves=0,
                current_phase=ProjectPhase.DEVELOPMENT,
                extraction_cost_per_unit=100.0,  # placeholder
                environmental_bond=1000000.0  # placeholder
            )
            self.mineral_reserves.append(new_reserve)
            self.environmental_bonds[project_id] = new_reserve.environmental_bond
        
        # Remove from exploration projects
        self.exploration_projects = [p for p in self.exploration_projects if p.project_id != project_id]
        return success
    
    # Production operations
    def start_production(self, reserve_id: str, daily_capacity: float) -> bool:
        """Begin production at a reserve"""
        reserve = next((r for r in self.mineral_reserves if r.reserve_id == reserve_id), None)
        if not reserve or reserve.current_phase != ProjectPhase.DEVELOPMENT:
            return False
        
        reserve.current_phase = ProjectPhase.PRODUCTION
        self.production_capacity[reserve_id] = daily_capacity
        self.daily_production_targets[reserve_id] = daily_capacity * 0.8  # 80% target utilization
        return True
    
    def extract_resources(self, reserve_id: str, amount: float) -> float:
        """Extract resources and update reserves"""
        reserve = next((r for r in self.mineral_reserves if r.reserve_id == reserve_id), None)
        if not reserve or reserve.current_phase != ProjectPhase.PRODUCTION:
            return 0.0
        
        # Check capacity constraints
        max_daily = self.production_capacity.get(reserve_id, 0)
        actual_amount = min(amount, max_daily, reserve.proven_reserves)
        
        if actual_amount > 0:
            # Update reserves
            reserve.proven_reserves -= actual_amount
            
            # Record production costs
            production_cost = actual_amount * reserve.extraction_cost_per_unit
            self.post("production_costs", "cash", production_cost, 
                     f"Extraction: {reserve_id}")
            
            # Add to inventory
            resource_type = reserve.extraction_type.value
            self.inventory[resource_type] = self.inventory.get(resource_type, 0) + actual_amount
        
        return actual_amount
    
    # Financial operations
    def sell_commodity(self, resource_type: str, quantity: float, market_price: float) -> Money:
        """Sell extracted commodities"""
        if self.inventory.get(resource_type, 0) < quantity:
            return 0.0
        
        revenue = quantity * market_price
        self.inventory[resource_type] -= quantity
        
        self.post("cash", "commodity_revenue", revenue, f"Sold {quantity} {resource_type}")
        self.income_statement["revenue"] += revenue
        return revenue
    
    def hedge_price_risk(self, resource_type: ExtractionType, quantity: float, 
                        strike_price: float, contract_type: str) -> None:
        """Enter commodity hedging contract"""
        contract_id = f"{resource_type.value}_{contract_type}_{len(self.commodity_hedging_contracts)}"
        self.commodity_hedging_contracts[contract_id] = {
            "resource_type": resource_type,
            "quantity": quantity,
            "strike_price": strike_price,
            "contract_type": contract_type
        }
    
    # Safety and compliance
    def report_safety_incident(self, incident_type: str, severity: str) -> None:
        """Record safety incident"""
        self.safety_incident_count += 1
        # In real implementation, this might trigger regulatory reporting
        
    def conduct_environmental_assessment(self, reserve_id: str) -> float:
        """Assess environmental compliance for a reserve"""
        # Simplified compliance check
        reserve = next((r for r in self.mineral_reserves if r.reserve_id == reserve_id), None)
        if not reserve:
            return 0.0
        
        # Check if proper permits and bonds are in place
        has_permits = len(self.mining_permits) > 0
        has_bond = reserve_id in self.environmental_bonds
        
        compliance_score = (0.5 if has_permits else 0) + (0.5 if has_bond else 0)
        return compliance_score
    
    def update_remediation_liability(self, additional_liability: float) -> None:
        """Update environmental remediation liability"""
        self.remediation_liabilities += additional_liability
        self.post("remediation_liability", "remediation_reserve", additional_liability,
                 "Environmental remediation provision")
    
    # Analytics
    def get_total_reserves(self) -> Dict[ExtractionType, float]:
        """Calculate total reserves by type"""
        reserves_by_type = {}
        for reserve in self.mineral_reserves:
            resource_type = reserve.extraction_type
            total = reserves_by_type.get(resource_type, 0)
            reserves_by_type[resource_type] = total + reserve.proven_reserves + reserve.probable_reserves
        return reserves_by_type
    
    def calculate_reserve_life(self, reserve_id: str) -> float:
        """Calculate years of production remaining at current rate"""
        reserve = next((r for r in self.mineral_reserves if r.reserve_id == reserve_id), None)
        if not reserve:
            return 0.0
        
        daily_production = self.production_capacity.get(reserve_id, 0)
        if daily_production == 0:
            return float('inf')
        
        return reserve.proven_reserves / (daily_production * 365) 