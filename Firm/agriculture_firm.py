# agriculture_firm.py
# NAICS 11: Agriculture, Forestry, Fishing and Hunting

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class CropType(Enum):
    GRAIN = "grain"
    FRUIT = "fruit"
    VEGETABLE = "vegetable"
    LIVESTOCK_FEED = "livestock_feed"
    CASH_CROP = "cash_crop"

class LivestockType(Enum):
    CATTLE = "cattle"
    POULTRY = "poultry"
    SWINE = "swine"
    DAIRY = "dairy"
    SHEEP = "sheep"

class ProductionMethod(Enum):
    ORGANIC = "organic"
    CONVENTIONAL = "conventional"
    SUSTAINABLE = "sustainable"
    INTENSIVE = "intensive"

@dataclass
class Land:
    parcel_id: str
    acreage: float
    soil_quality: float  # 0-1 rating
    water_rights: bool
    current_use: str
    location: str
    last_rotation: date = None

@dataclass
class Crop:
    crop_type: CropType
    variety: str
    planted_acreage: float
    planting_date: date
    expected_harvest_date: date
    expected_yield_per_acre: float
    input_costs_per_acre: float
    production_method: ProductionMethod

@dataclass
class Livestock:
    livestock_type: LivestockType
    head_count: int
    breed: str
    avg_weight: float
    feeding_cost_per_head_per_day: float
    expected_market_date: date = None

@dataclass
class WeatherRisk:
    drought_probability: float
    flood_probability: float
    frost_probability: float
    impact_factor: float  # multiplier on yields

@dataclass
class AgriculturalFirm(BaseFirm):
    # Land and resource management
    land_holdings: List[Land] = field(default_factory=list)
    water_rights: Dict[str, float] = field(default_factory=dict)  # location -> acre-feet
    soil_health_scores: Dict[str, float] = field(default_factory=dict)  # parcel_id -> score
    
    # Production planning
    current_crops: List[Crop] = field(default_factory=list)
    livestock_inventory: List[Livestock] = field(default_factory=list)
    rotation_schedule: Dict[str, List[str]] = field(default_factory=dict)  # parcel_id -> crop sequence
    
    # Seasonal and biological cycles
    growing_season_start: date = None
    growing_season_end: date = None
    harvest_schedule: Dict[date, List[str]] = field(default_factory=dict)  # date -> crop_ids
    
    # Risk management
    weather_risk_profile: WeatherRisk = None
    crop_insurance_policies: List[str] = field(default_factory=list)
    diversification_index: float = 0.0  # measure of crop/livestock diversity
    
    # Market and policy factors
    commodity_contracts: Dict[str, Any] = field(default_factory=dict)  # futures/forward contracts
    subsidy_programs: List[str] = field(default_factory=list)
    organic_certifications: List[str] = field(default_factory=list)
    
    # Equipment and infrastructure
    machinery_inventory: Dict[str, Any] = field(default_factory=dict)  # equipment_type -> details
    storage_capacity: Dict[str, float] = field(default_factory=dict)  # crop_type -> bushels/tons
    cold_storage_capacity: float = 0.0  # for perishables
    
    # Sub-industry specializations
    crop_focus: List[CropType] = field(default_factory=list)
    irrigation_systems: Dict[str, Any] = field(default_factory=dict)  # system_id -> details
    pesticide_use: Dict[str, float] = field(default_factory=dict)  # chemical -> lbs/acre
    seed_contracts: List[str] = field(default_factory=list)
    precision_ag_tech: List[str] = field(default_factory=list)
    
    livestock_focus: List[LivestockType] = field(default_factory=list)
    feed_contracts: List[str] = field(default_factory=list)
    veterinary_records: Dict[str, Any] = field(default_factory=dict)  # animal_id -> records
    grazing_management: Dict[str, float] = field(default_factory=dict)  # parcel_id -> days grazed
    
    integration_methods: List[str] = field(default_factory=list)  # e.g., manure recycling
    
    # Additional data models
    equipment_list: List[Equipment] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    extension_services: List[str] = field(default_factory=list)
    sustainability_score: float = 0.0
    
    # Sector-level attributes
    timber_inventory: Dict[str, float] = field(default_factory=dict)  # species -> board feet
    fishery_quotas: Dict[str, float] = field(default_factory=dict)  # species -> tons
    catch_records: Dict[str, float] = field(default_factory=dict)  # species -> tons caught
    reforestation_programs: List[str] = field(default_factory=list)
    vessel_inventory: List[str] = field(default_factory=list)
    harvest_permits: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "11"  # Agriculture base code
    
    # Land management methods
    def add_land_parcel(self, parcel: Land) -> None:
        """Add a land parcel to holdings"""
        self.land_holdings.append(parcel)
        self.soil_health_scores[parcel.parcel_id] = parcel.soil_quality
    
    def get_total_acreage(self) -> float:
        """Calculate total land holdings"""
        return sum(land.acreage for land in self.land_holdings)
    
    def plan_crop_rotation(self, parcel_id: str, crop_sequence: List[str]) -> bool:
        """Set rotation schedule for a parcel"""
        if any(land.parcel_id == parcel_id for land in self.land_holdings):
            self.rotation_schedule[parcel_id] = crop_sequence
            return True
        return False
    
    # Production methods
    def plant_crop(self, crop: Crop, parcel_id: str) -> bool:
        """Plant a crop on specified parcel"""
        parcel = next((land for land in self.land_holdings if land.parcel_id == parcel_id), None)
        if not parcel or crop.planted_acreage > parcel.acreage:
            return False
        
        self.current_crops.append(crop)
        parcel.current_use = f"{crop.crop_type.value}_{crop.variety}"
        
        # Record input costs
        total_input_cost = crop.planted_acreage * crop.input_costs_per_acre
        self.post("crop_inputs", "cash", total_input_cost, f"Planting {crop.variety}")
        
        return True
    
    def harvest_crop(self, crop_variety: str) -> float:
        """Harvest a specific crop and return yield"""
        crops_to_harvest = [c for c in self.current_crops if c.variety == crop_variety]
        if not crops_to_harvest:
            return 0.0
        
        total_yield = 0.0
        for crop in crops_to_harvest:
            base_yield = crop.planted_acreage * crop.expected_yield_per_acre
            weather_factor = 1.0 - (self.weather_risk_profile.impact_factor if self.weather_risk_profile else 0.0)
            
            actual_yield = base_yield * weather_factor
            total_yield += actual_yield
            
            self.inventory[crop.variety] = self.inventory.get(crop.variety, 0) + actual_yield
        
        self.current_crops = [c for c in self.current_crops if c.variety != crop_variety]
        return total_yield
    
    def calculate_diversification_index(self) -> float:
        """Calculate crop/livestock diversification to reduce risk"""
        crop_types = set(crop.crop_type for crop in self.current_crops)
        livestock_types = set(animal.livestock_type for animal in self.livestock_inventory)
        
        total_enterprises = len(crop_types) + len(livestock_types)
        self.diversification_index = min(total_enterprises / 5.0, 1.0)
        return self.diversification_index

    # Sub-industry specific methods
    def irrigate(self, parcel_id: str, inches: float) -> bool:
        """Apply irrigation to a parcel"""
        if parcel_id not in [l.parcel_id for l in self.land_holdings]:
            return False
        self.water_rights[parcel_id] = self.water_rights.get(parcel_id, 0) - inches
        return True
    
    def apply_pesticide(self, parcel_id: str, chemical: str, amount: float) -> None:
        self.pesticide_use[chemical] = self.pesticide_use.get(chemical, 0) + amount
    
    def record_vet_visit(self, animal_id: str, visit_details: Dict[str, Any]) -> None:
        self.veterinary_records[animal_id] = visit_details
    
    def rotate_grazing(self, parcel_id: str, days: int) -> None:
        self.grazing_management[parcel_id] = self.grazing_management.get(parcel_id, 0) + days
    
    def integrate_operations(self) -> None:
        """Simulate integration benefits (e.g., manure to fertilizer)"""
        # Placeholder for integration logic
        pass

    # Additional methods for AgriculturalFirm
    def add_equipment(self, equipment: Equipment) -> None:
        self.equipment_list.append(equipment)
    
    def schedule_maintenance(self, equipment_id: str, record: Dict[str, Any]) -> bool:
        eq = next((e for e in self.equipment_list if e.equipment_id == equipment_id), None)
        if not eq:
            return False
        eq.maintenance_records.append(record)
        return True
    
    def add_certification(self, cert: Certification) -> None:
        self.certifications.append(cert)
    
    def update_sustainability_score(self, new_score: float) -> None:
        self.sustainability_score = new_score
    
    def get_operational_summary(self) -> Dict[str, Any]:
        return {
            "total_acreage": self.get_total_acreage(),
            "diversification_index": self.diversification_index,
            "equipment_count": len(self.equipment_list),
            "certifications": [c.name for c in self.certifications],
            "sustainability_score": self.sustainability_score
        }

    # Sector-level methods
    def harvest_timber(self, species: str, amount: float) -> bool:
        available = self.timber_inventory.get(species, 0)
        if available < amount:
            return False
        self.timber_inventory[species] -= amount
        self.inventory[species] = self.inventory.get(species, 0) + amount
        return True
    
    def plant_trees(self, species: str, count: int) -> None:
        self.timber_inventory[species] = self.timber_inventory.get(species, 0) + count
        self.reforestation_programs.append(f"Planted {count} {species}")
    
    def record_catch(self, species: str, amount: float) -> None:
        self.catch_records[species] = self.catch_records.get(species, 0) + amount
        self.inventory[species] = self.inventory.get(species, 0) + amount
    
    def check_quota(self, species: str) -> float:
        return self.quota_allocations.get(species, 0) - self.catch_records.get(species, 0) 