# construction_firm.py
# NAICS 23: Construction

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class ConstructionType(Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    INFRASTRUCTURE = "infrastructure"
    SPECIALTY_TRADE = "specialty_trade"

class ProjectPhase(Enum):
    BIDDING = "bidding"
    AWARDED = "awarded"
    PRECONSTRUCTION = "preconstruction"
    CONSTRUCTION = "construction"
    CLOSEOUT = "closeout"
    COMPLETE = "complete"

@dataclass
class ConstructionProject:
    project_id: str
    client_id: str
    construction_type: ConstructionType
    contract_value: float
    phase: ProjectPhase
    start_date: date
    scheduled_completion: date
    percent_complete: float = 0.0
    change_orders: List[Dict] = field(default_factory=list)
    milestone_payments: Dict[float, float] = field(default_factory=dict)  # % complete -> payment

@dataclass
class LaborCrew:
    crew_id: str
    trade_specialty: str
    crew_size: int
    hourly_rates: Dict[str, float] = field(default_factory=dict)  # skill_level -> rate
    certifications: List[str] = field(default_factory=list)
    current_project: str = None

@dataclass
class MaterialInventory:
    material_type: str
    quantity: float
    unit_cost: float
    supplier: str
    delivery_date: date
    quality_grade: str

@dataclass
class ConstructionFirm(BaseFirm):
    # Core business specialization
    construction_types: List[ConstructionType] = field(default_factory=list)
    trade_specialties: List[str] = field(default_factory=list)  # electrical, plumbing, etc.
    geographic_markets: List[str] = field(default_factory=list)
    
    # Project portfolio
    active_projects: List[ConstructionProject] = field(default_factory=list)
    bid_pipeline: List[Dict] = field(default_factory=list)  # pending bids
    completed_projects: List[str] = field(default_factory=list)
    backlog_value: float = 0.0  # contracted but not yet completed
    
    # Workforce management
    labor_crews: List[LaborCrew] = field(default_factory=list)
    subcontractor_network: Dict[str, Any] = field(default_factory=dict)  # trade -> preferred subs
    union_agreements: List[str] = field(default_factory=list)
    workforce_utilization: float = 0.8  # target utilization rate
    
    # Materials and supply chain
    material_inventory: List[MaterialInventory] = field(default_factory=list)
    supplier_contracts: Dict[str, Any] = field(default_factory=dict)
    material_price_volatility: Dict[str, float] = field(default_factory=dict)  # material -> volatility
    just_in_time_delivery: bool = True
    
    # Financial and bonding
    surety_bonds: Dict[str, float] = field(default_factory=dict)  # project_id -> bond amount
    bonding_capacity: float = 0.0  # total available bonding
    retention_receivables: Dict[str, float] = field(default_factory=dict)  # project_id -> retained amount
    performance_guarantees: List[str] = field(default_factory=list)
    
    # Equipment and assets
    construction_equipment: Dict[str, Any] = field(default_factory=dict)  # equipment_type -> details
    equipment_utilization: Dict[str, float] = field(default_factory=dict)  # equipment_id -> utilization
    rental_vs_owned: Dict[str, str] = field(default_factory=dict)  # equipment_type -> strategy
    
    # Risk management
    safety_record: Dict[str, Any] = field(default_factory=dict)  # incidents, training, etc.
    weather_delays: List[Dict] = field(default_factory=list)
    permit_delays: Dict[str, int] = field(default_factory=dict)  # project_id -> days delayed
    quality_control_metrics: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "23"  # Construction base code
    
    # Project management
    def submit_bid(self, project_opportunity: Dict, bid_amount: float) -> str:
        """Submit bid for construction project"""
        bid_id = f"bid_{len(self.bid_pipeline)}"
        bid = {
            "bid_id": bid_id,
            "project_details": project_opportunity,
            "bid_amount": bid_amount,
            "submission_date": date.today(),
            "status": "submitted"
        }
        self.bid_pipeline.append(bid)
        return bid_id
    
    def win_project(self, bid_id: str) -> bool:
        """Convert winning bid to active project"""
        bid = next((b for b in self.bid_pipeline if b["bid_id"] == bid_id), None)
        if not bid:
            return False
        
        project = ConstructionProject(
            project_id=f"proj_{bid_id}",
            client_id=bid["project_details"]["client_id"],
            construction_type=ConstructionType(bid["project_details"]["type"]),
            contract_value=bid["bid_amount"],
            phase=ProjectPhase.AWARDED,
            start_date=date.today() + timedelta(days=30),
            scheduled_completion=date.today() + timedelta(days=bid["project_details"]["duration_days"])
        )
        
        self.active_projects.append(project)
        self.backlog_value += project.contract_value
        
        # Remove from bid pipeline
        self.bid_pipeline = [b for b in self.bid_pipeline if b["bid_id"] != bid_id]
        return True
    
    def update_project_progress(self, project_id: str, new_percent_complete: float) -> bool:
        """Update project completion percentage"""
        project = next((p for p in self.active_projects if p.project_id == project_id), None)
        if not project:
            return False
        
        old_progress = project.percent_complete
        project.percent_complete = min(100.0, new_percent_complete)
        
        # Check for milestone payments
        for milestone_pct, payment_amount in project.milestone_payments.items():
            if old_progress < milestone_pct <= project.percent_complete:
                self.post("cash", "milestone_revenue", payment_amount, 
                         f"Milestone payment: {project_id}")
                self.income_statement["revenue"] += payment_amount
        
        # Update backlog
        progress_delta = (project.percent_complete - old_progress) / 100.0
        revenue_recognized = project.contract_value * progress_delta
        self.backlog_value -= revenue_recognized
        
        return True
    
    # Workforce management
    def assign_crew_to_project(self, crew_id: str, project_id: str) -> bool:
        """Assign labor crew to specific project"""
        crew = next((c for c in self.labor_crews if c.crew_id == crew_id), None)
        project = next((p for p in self.active_projects if p.project_id == project_id), None)
        
        if not crew or not project or crew.current_project:
            return False
        
        crew.current_project = project_id
        return True
    
    def calculate_labor_cost(self, project_id: str, hours_worked: Dict[str, float]) -> float:
        """Calculate labor costs for project"""
        total_cost = 0.0
        assigned_crews = [c for c in self.labor_crews if c.current_project == project_id]
        
        for crew in assigned_crews:
            for skill_level, hours in hours_worked.items():
                rate = crew.hourly_rates.get(skill_level, 25.0)  # default $25/hr
                total_cost += hours * rate
        
        self.post("labor_costs", "cash", total_cost, f"Labor: {project_id}")
        return total_cost
    
    # Materials management
    def order_materials(self, material_type: str, quantity: float, project_id: str) -> bool:
        """Order materials for specific project"""
        # Check supplier contracts for pricing
        supplier_info = self.supplier_contracts.get(material_type, {})
        unit_cost = supplier_info.get("price", 100.0)  # default cost
        
        total_cost = quantity * unit_cost
        
        # Create inventory record
        material = MaterialInventory(
            material_type=material_type,
            quantity=quantity,
            unit_cost=unit_cost,
            supplier=supplier_info.get("supplier", "default"),
            delivery_date=date.today() + timedelta(days=7),
            quality_grade=supplier_info.get("grade", "standard")
        )
        
        self.material_inventory.append(material)
        self.post("material_costs", "cash", total_cost, f"Materials: {project_id}")
        return True
    
    def consume_materials(self, material_type: str, quantity: float, project_id: str) -> bool:
        """Consume materials for project work"""
        available_materials = [m for m in self.material_inventory if m.material_type == material_type]
        
        if not available_materials or sum(m.quantity for m in available_materials) < quantity:
            return False
        
        remaining_needed = quantity
        materials_used = []
        
        for material in available_materials:
            if remaining_needed <= 0:
                break
            
            used = min(remaining_needed, material.quantity)
            material.quantity -= used
            remaining_needed -= used
            
            if material.quantity == 0:
                materials_used.append(material)
        
        # Remove depleted materials
        for used_material in materials_used:
            self.material_inventory.remove(used_material)
        
        return True
    
    # Financial operations
    def post_surety_bond(self, project_id: str, bond_amount: float) -> bool:
        """Post surety bond for project"""
        if bond_amount > self.bonding_capacity:
            return False
        
        self.surety_bonds[project_id] = bond_amount
        self.bonding_capacity -= bond_amount
        
        # Record bond cost (typically 1-3% of bond amount)
        bond_cost = bond_amount * 0.02  # 2% cost
        self.post("bonding_costs", "cash", bond_cost, f"Surety bond: {project_id}")
        return True
    
    def process_change_order(self, project_id: str, change_description: str, 
                           cost_impact: float) -> bool:
        """Process change order for project"""
        project = next((p for p in self.active_projects if p.project_id == project_id), None)
        if not project:
            return False
        
        change_order = {
            "description": change_description,
            "cost_impact": cost_impact,
            "date": date.today(),
            "approved": False
        }
        
        project.change_orders.append(change_order)
        project.contract_value += cost_impact  # assuming approved
        self.backlog_value += cost_impact
        
        return True
    
    # Safety and compliance
    def record_safety_incident(self, project_id: str, incident_type: str, 
                             severity: str, workers_affected: int) -> None:
        """Record safety incident on project"""
        if "incidents" not in self.safety_record:
            self.safety_record["incidents"] = []
        
        incident = {
            "project_id": project_id,
            "incident_type": incident_type,
            "severity": severity,
            "workers_affected": workers_affected,
            "date": date.today()
        }
        
        self.safety_record["incidents"].append(incident)
    
    def calculate_safety_metrics(self) -> Dict[str, float]:
        """Calculate safety performance metrics"""
        incidents = self.safety_record.get("incidents", [])
        total_incidents = len(incidents)
        
        # Calculate incidents per project
        if len(self.active_projects) + len(self.completed_projects) == 0:
            incidents_per_project = 0.0
        else:
            incidents_per_project = total_incidents / (len(self.active_projects) + len(self.completed_projects))
        
        return {
            "total_incidents": total_incidents,
            "incidents_per_project": incidents_per_project,
            "lost_time_incidents": len([i for i in incidents if i["severity"] == "lost_time"])
        }
    
    # Analytics and reporting
    def get_project_portfolio_summary(self) -> Dict[str, Any]:
        """Generate summary of project portfolio"""
        return {
            "active_projects": len(self.active_projects),
            "total_backlog_value": self.backlog_value,
            "average_project_value": self.backlog_value / max(1, len(self.active_projects)),
            "projects_by_type": {ct.value: len([p for p in self.active_projects if p.construction_type == ct]) 
                               for ct in ConstructionType},
            "workforce_utilization": self.workforce_utilization,
            "bonding_capacity_used": sum(self.surety_bonds.values()),
            "safety_metrics": self.calculate_safety_metrics()
        } 