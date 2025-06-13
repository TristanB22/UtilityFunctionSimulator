# utilities_firm.py
# NAICS 22: Utilities

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, datetime
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class UtilityType(Enum):
    ELECTRIC = "electric"
    NATURAL_GAS = "natural_gas"
    WATER = "water"
    SEWER = "sewer"
    STEAM = "steam"

class FuelType(Enum):
    COAL = "coal"
    NATURAL_GAS = "natural_gas"
    NUCLEAR = "nuclear"
    HYDRO = "hydro"
    SOLAR = "solar"
    WIND = "wind"
    BIOMASS = "biomass"

class RateStructure(Enum):
    FLAT = "flat"
    TIERED = "tiered"
    TIME_OF_USE = "time_of_use"
    DEMAND_CHARGE = "demand_charge"
    SEASONAL = "seasonal"

@dataclass
class GenerationAsset:
    asset_id: str
    fuel_type: FuelType
    capacity_mw: float
    efficiency_rate: float
    variable_cost_per_mwh: float
    fixed_om_cost_annual: float
    heat_rate: float  # BTU per kWh
    emissions_factor: float  # CO2 per MWh

@dataclass
class NetworkInfrastructure:
    asset_type: str  # transmission, distribution, pipeline
    asset_id: str
    capacity: float
    voltage_level: str = None  # for electric
    pressure_rating: float = None  # for gas/water
    length_miles: float = 0.0
    maintenance_cost_annual: float = 0.0

@dataclass
class RateTariff:
    tariff_id: str
    customer_class: str  # residential, commercial, industrial
    rate_structure: RateStructure
    base_rate: float
    energy_charges: Dict[str, float] = field(default_factory=dict)  # tier/time -> rate
    demand_charges: Dict[str, float] = field(default_factory=dict)
    connection_fees: float = 0.0

@dataclass
class UtilitiesFirm(BaseFirm):
    # Core utility type and service territory
    utility_types: List[UtilityType] = field(default_factory=list)
    service_territory: List[str] = field(default_factory=list)  # geographic areas served
    customer_count: Dict[str, int] = field(default_factory=dict)  # customer_class -> count
    
    # Generation and supply assets
    generation_assets: List[GenerationAsset] = field(default_factory=list)
    fuel_contracts: Dict[str, Any] = field(default_factory=dict)  # fuel procurement
    renewable_capacity_mw: float = 0.0
    capacity_factor: Dict[str, float] = field(default_factory=dict)  # asset_id -> utilization
    
    # Network infrastructure
    transmission_assets: List[NetworkInfrastructure] = field(default_factory=list)
    distribution_assets: List[NetworkInfrastructure] = field(default_factory=list)
    system_peak_demand: float = 0.0
    reserve_margin: float = 0.15  # 15% default reserve margin
    
    # Regulatory and rate-making
    rate_tariffs: List[RateTariff] = field(default_factory=list)
    regulatory_commission: str = None  # state PUC
    allowed_rate_of_return: float = 0.10  # regulated return on equity
    rate_base: float = 0.0  # regulated asset base
    last_rate_case_date: date = None
    
    # Service reliability and performance
    saidi_minutes: float = 0.0  # System Average Interruption Duration Index
    saifi_interruptions: float = 0.0  # System Average Interruption Frequency Index
    service_availability_target: float = 0.9999  # 99.99% uptime
    outage_incidents: List[Dict] = field(default_factory=list)
    
    # Environmental and compliance
    emissions_allowances: Dict[str, float] = field(default_factory=dict)  # CO2, NOx, SO2
    renewable_portfolio_target: float = 0.0  # % renewable by regulation
    energy_efficiency_programs: List[str] = field(default_factory=list)
    environmental_compliance_costs: float = 0.0
    
    # Demand and load management
    peak_demand_by_season: Dict[str, float] = field(default_factory=dict)
    load_forecasts: Dict[str, float] = field(default_factory=dict)  # year -> expected_demand
    demand_response_programs: List[str] = field(default_factory=list)
    smart_meter_deployment: float = 0.0  # percentage of customers
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "22"  # Utilities base code
    
    # Generation and supply management
    def add_generation_asset(self, asset: GenerationAsset) -> None:
        """Add generation capacity"""
        self.generation_assets.append(asset)
        if asset.fuel_type in [FuelType.SOLAR, FuelType.WIND, FuelType.HYDRO]:
            self.renewable_capacity_mw += asset.capacity_mw
    
    def dispatch_generation(self, demand_mw: float) -> Dict[str, float]:
        """Economic dispatch of generation assets"""
        # Sort by variable cost (merit order)
        sorted_assets = sorted(self.generation_assets, key=lambda x: x.variable_cost_per_mwh)
        
        dispatch = {}
        remaining_demand = demand_mw
        
        for asset in sorted_assets:
            if remaining_demand <= 0:
                break
            
            capacity_available = asset.capacity_mw * self.capacity_factor.get(asset.asset_id, 0.85)
            dispatched = min(remaining_demand, capacity_available)
            
            if dispatched > 0:
                dispatch[asset.asset_id] = dispatched
                remaining_demand -= dispatched
        
        return dispatch
    
    def calculate_generation_cost(self, dispatch: Dict[str, float]) -> float:
        """Calculate total cost of generation"""
        total_cost = 0.0
        for asset in self.generation_assets:
            if asset.asset_id in dispatch:
                mwh_generated = dispatch[asset.asset_id]
                variable_cost = mwh_generated * asset.variable_cost_per_mwh
                total_cost += variable_cost
        return total_cost
    
    # Rate-making and revenue
    def file_rate_case(self, requested_revenue_increase: float, justification: str) -> bool:
        """File rate case with regulatory commission"""
        if not self.regulatory_commission:
            return False
        
        # Simplified rate case filing
        self.last_rate_case_date = date.today()
        
        # Calculate rate base return
        allowed_return = self.rate_base * self.allowed_rate_of_return
        
        # Record regulatory asset
        self.post("rate_case_costs", "regulatory_assets", 500000, "Rate case filing costs")
        return True
    
    def calculate_revenue_requirement(self) -> float:
        """Calculate total revenue requirement"""
        # Operating expenses + depreciation + taxes + return on rate base
        operating_expenses = sum(self.income_statement.get(key, 0) for key in ["opex", "cogs"])
        depreciation = self.rate_base * 0.04  # 4% depreciation rate
        return_on_investment = self.rate_base * self.allowed_rate_of_return
        
        return operating_expenses + depreciation + return_on_investment
    
    def apply_rate_tariff(self, customer_class: str, usage_kwh: float, 
                         demand_kw: float = 0.0) -> float:
        """Calculate customer bill based on tariff"""
        tariff = next((t for t in self.rate_tariffs if t.customer_class == customer_class), None)
        if not tariff:
            return usage_kwh * 0.10  # default rate
        
        bill_amount = 0.0
        
        # Base rate
        bill_amount += tariff.base_rate
        
        # Energy charges
        if tariff.rate_structure == RateStructure.FLAT:
            bill_amount += usage_kwh * tariff.energy_charges.get("standard", 0.10)
        elif tariff.rate_structure == RateStructure.TIERED:
            # Implement tiered pricing logic
            remaining_usage = usage_kwh
            for tier, rate in tariff.energy_charges.items():
                tier_limit = float(tier.split("_")[1]) if "_" in tier else 1000
                tier_usage = min(remaining_usage, tier_limit)
                bill_amount += tier_usage * rate
                remaining_usage -= tier_usage
                if remaining_usage <= 0:
                    break
        
        # Demand charges
        if demand_kw > 0:
            bill_amount += demand_kw * tariff.demand_charges.get("peak", 0.0)
        
        return bill_amount
    
    # Reliability and service quality
    def record_outage(self, affected_customers: int, duration_minutes: float, cause: str) -> None:
        """Record service outage incident"""
        self.outage_incidents.append({
            "timestamp": datetime.now(),
            "affected_customers": affected_customers,
            "duration_minutes": duration_minutes,
            "cause": cause
        })
        
        # Update reliability metrics
        total_customers = sum(self.customer_count.values())
        if total_customers > 0:
            self.saidi_minutes += (affected_customers * duration_minutes) / total_customers
            self.saifi_interruptions += affected_customers / total_customers
    
    def calculate_service_availability(self) -> float:
        """Calculate system availability percentage"""
        if not self.outage_incidents:
            return self.service_availability_target
        
        total_outage_minutes = sum(incident["duration_minutes"] for incident in self.outage_incidents)
        annual_minutes = 365 * 24 * 60
        availability = 1.0 - (total_outage_minutes / annual_minutes)
        return max(0.0, availability)
    
    # Environmental and regulatory compliance
    def purchase_emissions_allowances(self, pollutant: str, quantity: float, price_per_ton: float) -> None:
        """Purchase emissions allowances for compliance"""
        cost = quantity * price_per_ton
        self.emissions_allowances[pollutant] = self.emissions_allowances.get(pollutant, 0) + quantity
        self.post("emissions_allowances", "cash", cost, f"Purchased {pollutant} allowances")
        self.environmental_compliance_costs += cost
    
    def calculate_renewable_percentage(self) -> float:
        """Calculate current renewable energy percentage"""
        total_capacity = sum(asset.capacity_mw for asset in self.generation_assets)
        if total_capacity == 0:
            return 0.0
        return self.renewable_capacity_mw / total_capacity
    
    def implement_energy_efficiency_program(self, program_name: str, cost: float, 
                                          savings_mwh_annual: float) -> None:
        """Implement customer energy efficiency program"""
        self.energy_efficiency_programs.append(program_name)
        self.post("efficiency_programs", "cash", cost, f"Energy efficiency: {program_name}")
        
        # Efficiency programs reduce future demand
        demand_reduction = savings_mwh_annual / 8760  # convert to MW
        self.system_peak_demand = max(0, self.system_peak_demand - demand_reduction)
    
    # Infrastructure investment
    def invest_in_infrastructure(self, asset: NetworkInfrastructure, cost: float) -> None:
        """Invest in transmission/distribution infrastructure"""
        if asset.asset_type in ["transmission", "subtransmission"]:
            self.transmission_assets.append(asset)
        else:
            self.distribution_assets.append(asset)
        
        # Add to rate base for regulated utilities
        self.rate_base += cost
        self.post("utility_plant", "cash", cost, f"Infrastructure: {asset.asset_id}")
    
    # Analytics and reporting
    def get_capacity_margin(self) -> float:
        """Calculate current capacity margin"""
        total_capacity = sum(asset.capacity_mw for asset in self.generation_assets)
        if self.system_peak_demand == 0:
            return 1.0
        return (total_capacity - self.system_peak_demand) / self.system_peak_demand 