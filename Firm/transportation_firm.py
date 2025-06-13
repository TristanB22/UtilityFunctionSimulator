# transportation_firm.py
# NAICS 48-49: Transportation and Warehousing

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class TransportMode(Enum):
    TRUCKING = "trucking"
    RAIL = "rail"
    AIR_FREIGHT = "air_freight"
    OCEAN_SHIPPING = "ocean_shipping"
    INLAND_WATERWAY = "inland_waterway"
    PIPELINE = "pipeline"
    COURIER_EXPRESS = "courier_express"
    WAREHOUSING = "warehousing"
    INTERMODAL = "intermodal"

class ServiceType(Enum):
    LESS_THAN_TRUCKLOAD = "ltl"
    FULL_TRUCKLOAD = "ftl"
    EXPEDITED = "expedited"
    TEMPERATURE_CONTROLLED = "temperature_controlled"
    HAZMAT = "hazmat"
    OVERSIZED = "oversized"
    WHITE_GLOVE = "white_glove"
    LAST_MILE = "last_mile"

class VehicleType(Enum):
    DRY_VAN = "dry_van"
    REFRIGERATED = "refrigerated"
    FLATBED = "flatbed"
    TANKER = "tanker"
    CONTAINER = "container"
    BOX_TRUCK = "box_truck"
    DELIVERY_VAN = "delivery_van"
    AIRCRAFT = "aircraft"
    VESSEL = "vessel"

@dataclass
class Vehicle:
    vehicle_id: str
    vehicle_type: VehicleType
    capacity_weight: float  # pounds or tons
    capacity_volume: float  # cubic feet
    fuel_efficiency: float  # mpg or equivalent
    maintenance_cost_per_mile: float
    current_location: str
    driver_id: str = None
    utilization_rate: float = 0.75
    last_inspection_date: date = None
    next_maintenance_due: date = None

@dataclass
class Route:
    route_id: str
    origin: str
    destination: str
    distance_miles: float
    estimated_transit_time: float  # hours
    fuel_cost: float
    tolls: float
    difficulty_factor: float = 1.0  # mountain, urban, etc.

@dataclass
class Shipment:
    shipment_id: str
    customer_id: str
    origin: str
    destination: str
    weight: float
    dimensions: Dict[str, float]  # length, width, height
    service_type: ServiceType
    pickup_date: date
    delivery_date: date
    freight_rate: float
    special_requirements: List[str] = field(default_factory=list)

@dataclass
class Warehouse:
    warehouse_id: str
    location: str
    total_square_footage: float
    available_square_footage: float
    loading_docks: int
    temperature_controlled: bool
    automation_level: str  # manual, semi_automated, automated
    storage_cost_per_sqft: float
    throughput_capacity: float  # packages per hour

@dataclass
class Driver:
    driver_id: str
    license_class: str  # CDL-A, CDL-B, etc.
    endorsements: List[str] = field(default_factory=list)  # hazmat, passenger, etc.
    hours_of_service_remaining: float = 11.0  # DOT regulations
    last_drug_test: date = None
    safety_score: float = 100.0  # 0-100 scale
    years_experience: float = 5.0

@dataclass
class TransportationFirm(BaseFirm):
    # Core transportation capabilities
    transport_modes: List[TransportMode] = field(default_factory=list)
    service_types: List[ServiceType] = field(default_factory=list)
    geographic_coverage: List[str] = field(default_factory=list)  # states/regions served
    operating_authorities: List[str] = field(default_factory=list)  # DOT numbers, licenses
    
    # Fleet management
    vehicle_fleet: List[Vehicle] = field(default_factory=list)
    fleet_size_by_type: Dict[VehicleType, int] = field(default_factory=dict)
    vehicle_utilization_target: float = 0.85
    average_vehicle_age: float = 5.0  # years
    maintenance_schedule: Dict[str, date] = field(default_factory=dict)  # vehicle_id -> next_service
    
    # Driver management
    drivers: List[Driver] = field(default_factory=list)
    driver_to_vehicle_ratio: float = 1.3  # drivers per vehicle
    driver_turnover_rate: float = 0.15  # annual
    training_programs: List[str] = field(default_factory=list)
    safety_training_hours: float = 40.0  # annual requirement
    
    # Route and network optimization
    route_network: Dict[str, List[Route]] = field(default_factory=dict)  # origin -> routes
    hub_locations: List[str] = field(default_factory=list)
    cross_dock_facilities: List[str] = field(default_factory=list)
    linehaul_network: Dict[str, Any] = field(default_factory=dict)
    
    # Warehousing and logistics
    warehouses: List[Warehouse] = field(default_factory=list)
    total_warehouse_capacity: float = 0.0  # square feet
    warehouse_utilization: float = 0.80
    inventory_management_system: str = "wms"  # WMS, TMS, etc.
    pick_pack_efficiency: float = 95.0  # accuracy percentage
    
    # Active shipments and operations
    active_shipments: List[Shipment] = field(default_factory=list)
    daily_shipment_volume: int = 0
    average_shipment_weight: float = 1000.0  # pounds
    load_factor: float = 0.85  # percentage of capacity utilized
    
    # Financial and pricing
    fuel_cost_per_gallon: float = 3.50
    fuel_surcharge_rate: float = 0.15  # percentage of base rate
    accessorial_charges: Dict[str, float] = field(default_factory=dict)  # detention, residential, etc.
    revenue_per_mile: float = 2.50
    cost_per_mile: float = 1.80
    
    # Performance metrics
    on_time_delivery_rate: float = 0.95
    damage_claim_rate: float = 0.001  # percentage of shipments
    customer_satisfaction_score: float = 4.2  # out of 5
    safety_score: float = 95.0  # DOT safety rating
    fuel_efficiency_mpg: float = 6.5  # fleet average
    
    # Regulatory compliance
    dot_safety_rating: str = "satisfactory"
    hours_of_service_compliance: float = 0.98
    driver_qualification_files: Dict[str, Any] = field(default_factory=dict)
    vehicle_inspection_program: str = "pre_trip_daily"
    hazmat_certifications: List[str] = field(default_factory=list)
    
    # Technology and automation
    fleet_tracking_system: bool = True
    route_optimization_software: bool = True
    electronic_logging_devices: bool = True  # ELD mandate
    warehouse_management_system: bool = True
    customer_portal: bool = True
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "48"  # Transportation (48-49 range)
    
    # Fleet operations
    def add_vehicle_to_fleet(self, vehicle: Vehicle) -> None:
        """Add vehicle to fleet"""
        self.vehicle_fleet.append(vehicle)
        self.fleet_size_by_type[vehicle.vehicle_type] = self.fleet_size_by_type.get(vehicle.vehicle_type, 0) + 1
        
        # Schedule first maintenance
        self.maintenance_schedule[vehicle.vehicle_id] = date.today() + timedelta(days=90)
    
    def hire_driver(self, driver: Driver) -> bool:
        """Hire new driver"""
        self.drivers.append(driver)
        
        # Record hiring costs
        hiring_cost = 5000.0  # recruitment, training, licensing
        self.post("driver_hiring_costs", "cash", hiring_cost, f"Driver hire: {driver.driver_id}")
        self.income_statement["opex"] += hiring_cost
        
        return True
    
    def assign_driver_to_vehicle(self, driver_id: str, vehicle_id: str) -> bool:
        """Assign driver to specific vehicle"""
        driver = next((d for d in self.drivers if d.driver_id == driver_id), None)
        vehicle = next((v for v in self.vehicle_fleet if v.vehicle_id == vehicle_id), None)
        
        if driver and vehicle and not vehicle.driver_id:
            vehicle.driver_id = driver_id
            return True
        return False
    
    def perform_vehicle_maintenance(self, vehicle_id: str, maintenance_type: str, cost: float) -> None:
        """Perform scheduled or unscheduled maintenance"""
        vehicle = next((v for v in self.vehicle_fleet if v.vehicle_id == vehicle_id), None)
        if vehicle:
            self.post("vehicle_maintenance", "cash", cost, f"Maintenance: {vehicle_id}")
            self.income_statement["opex"] += cost
            
            # Update next maintenance date
            if maintenance_type == "scheduled":
                next_service = date.today() + timedelta(days=90)
                self.maintenance_schedule[vehicle_id] = next_service
    
    # Shipment and route management
    def schedule_shipment(self, shipment: Shipment) -> str:
        """Schedule a new shipment"""
        self.active_shipments.append(shipment)
        self.daily_shipment_volume += 1
        
        # Calculate and record revenue
        distance = self._calculate_distance(shipment.origin, shipment.destination)
        base_rate = distance * self.revenue_per_mile
        
        # Apply service type multipliers
        service_multipliers = {
            ServiceType.EXPEDITED: 1.5,
            ServiceType.TEMPERATURE_CONTROLLED: 1.3,
            ServiceType.HAZMAT: 1.4,
            ServiceType.WHITE_GLOVE: 1.6
        }
        multiplier = service_multipliers.get(shipment.service_type, 1.0)
        
        total_revenue = base_rate * multiplier + self._calculate_accessorial_charges(shipment)
        shipment.freight_rate = total_revenue
        
        self.post("cash", "transportation_revenue", total_revenue, f"Shipment: {shipment.shipment_id}")
        self.income_statement["revenue"] += total_revenue
        
        # Assign vehicle and driver
        self._assign_shipment_to_vehicle(shipment)
        
        return shipment.shipment_id
    
    def _calculate_distance(self, origin: str, destination: str) -> float:
        """Calculate distance between two locations"""
        # Simplified distance calculation - in practice would use routing API
        route_key = f"{origin}_{destination}"
        if route_key in [r.route_id for routes in self.route_network.values() for r in routes]:
            route = next((r for routes in self.route_network.values() for r in routes 
                         if r.route_id == route_key), None)
            return route.distance_miles if route else 500.0  # default
        return 500.0  # default distance assumption
    
    def _calculate_accessorial_charges(self, shipment: Shipment) -> float:
        """Calculate additional charges for special services"""
        total_charges = 0.0
        
        # Weight-based charges
        if shipment.weight > 2000:  # over 2000 lbs
            total_charges += 50.0
        
        # Special requirement charges
        for requirement in shipment.special_requirements:
            charge = self.accessorial_charges.get(requirement, 0.0)
            total_charges += charge
        
        return total_charges
    
    def _assign_shipment_to_vehicle(self, shipment: Shipment) -> bool:
        """Assign shipment to available vehicle"""
        # Find suitable vehicle based on capacity and type
        suitable_vehicles = [v for v in self.vehicle_fleet 
                           if v.capacity_weight >= shipment.weight and v.driver_id]
        
        if suitable_vehicles:
            # Choose vehicle with best utilization
            vehicle = min(suitable_vehicles, key=lambda v: v.utilization_rate)
            
            # Update vehicle utilization
            capacity_used = shipment.weight / vehicle.capacity_weight
            vehicle.utilization_rate = min(1.0, vehicle.utilization_rate + capacity_used)
            
            return True
        return False
    
    def complete_delivery(self, shipment_id: str, delivery_status: str) -> bool:
        """Complete shipment delivery"""
        shipment = next((s for s in self.active_shipments if s.shipment_id == shipment_id), None)
        if not shipment:
            return False
        
        # Update on-time performance
        if delivery_status == "on_time":
            delivered_on_time = 1
        else:
            delivered_on_time = 0
        
        # Update rolling average
        self.on_time_delivery_rate = (self.on_time_delivery_rate * 0.95 + 
                                    delivered_on_time * 0.05)
        
        # Calculate operating costs
        distance = self._calculate_distance(shipment.origin, shipment.destination)
        operating_cost = distance * self.cost_per_mile
        fuel_cost = distance / self.fuel_efficiency_mpg * self.fuel_cost_per_gallon
        
        total_cost = operating_cost + fuel_cost
        self.post("operating_costs", "cash", total_cost, f"Delivery costs: {shipment_id}")
        self.income_statement["opex"] += total_cost
        
        # Remove from active shipments
        self.active_shipments = [s for s in self.active_shipments if s.shipment_id != shipment_id]
        
        return True
    
    # Route optimization
    def optimize_routes(self, shipments: List[str]) -> Dict[str, List[str]]:
        """Optimize routing for multiple shipments"""
        # Simplified route optimization - in practice would use sophisticated algorithms
        optimized_routes = {}
        
        # Group shipments by geographic region
        region_shipments = {}
        for shipment_id in shipments:
            shipment = next((s for s in self.active_shipments if s.shipment_id == shipment_id), None)
            if shipment:
                region = shipment.destination[:2]  # simplified by state code
                if region not in region_shipments:
                    region_shipments[region] = []
                region_shipments[region].append(shipment_id)
        
        # Create routes for each region
        for region, region_shipment_ids in region_shipments.items():
            route_id = f"route_{region}_{len(optimized_routes)}"
            optimized_routes[route_id] = region_shipment_ids
        
        return optimized_routes
    
    def calculate_route_efficiency(self, route_id: str) -> float:
        """Calculate efficiency metrics for a route"""
        route_shipments = []  # would contain actual route shipments
        
        if not route_shipments:
            return 0.0
        
        total_distance = sum(self._calculate_distance(s.origin, s.destination) 
                           for s in route_shipments)
        total_revenue = sum(s.freight_rate for s in route_shipments)
        total_cost = total_distance * self.cost_per_mile
        
        efficiency = (total_revenue - total_cost) / max(total_revenue, 1)
        return efficiency
    
    # Warehousing operations
    def add_warehouse(self, warehouse: Warehouse) -> None:
        """Add warehouse facility"""
        self.warehouses.append(warehouse)
        self.total_warehouse_capacity += warehouse.total_square_footage
        
        # Record warehouse setup costs
        setup_cost = warehouse.total_square_footage * 25.0  # $25 per sq ft
        self.post("warehouse_assets", "cash", setup_cost, f"Warehouse: {warehouse.warehouse_id}")
    
    def process_warehouse_shipment(self, warehouse_id: str, shipment_type: str, 
                                 volume: float) -> float:
        """Process inbound or outbound warehouse shipment"""
        warehouse = next((w for w in self.warehouses if w.warehouse_id == warehouse_id), None)
        if not warehouse:
            return 0.0
        
        # Calculate processing time and cost
        processing_rate = warehouse.throughput_capacity  # packages per hour
        processing_time = volume / processing_rate
        labor_cost = processing_time * 25.0  # $25 per hour labor cost
        
        self.post("warehouse_operations", "cash", labor_cost, 
                 f"Warehouse processing: {warehouse_id}")
        self.income_statement["opex"] += labor_cost
        
        # Update warehouse utilization
        if shipment_type == "inbound":
            space_used = volume * 0.1  # simplified: 0.1 sq ft per package
            warehouse.available_square_footage -= space_used
        else:  # outbound
            space_used = volume * 0.1
            warehouse.available_square_footage += space_used
        
        warehouse.available_square_footage = max(0, min(warehouse.available_square_footage, 
                                                       warehouse.total_square_footage))
        
        return processing_time
    
    def implement_warehouse_automation(self, warehouse_id: str, automation_cost: float) -> bool:
        """Implement automation in warehouse"""
        warehouse = next((w for w in self.warehouses if w.warehouse_id == warehouse_id), None)
        if not warehouse:
            return False
        
        warehouse.automation_level = "automated"
        warehouse.throughput_capacity *= 2.5  # significant efficiency gain
        
        self.post("automation_investment", "cash", automation_cost, 
                 f"Warehouse automation: {warehouse_id}")
        
        return True
    
    # Safety and compliance
    def conduct_driver_training(self, driver_id: str, training_type: str, cost: float) -> None:
        """Conduct driver training program"""
        driver = next((d for d in self.drivers if d.driver_id == driver_id), None)
        if driver:
            # Update driver safety score
            if training_type == "safety":
                driver.safety_score = min(100.0, driver.safety_score + 5.0)
            
            self.post("training_costs", "cash", cost, f"Driver training: {driver_id}")
            self.income_statement["opex"] += cost
    
    def perform_dot_inspection(self, vehicle_id: str) -> Dict[str, Any]:
        """Perform DOT safety inspection"""
        vehicle = next((v for v in self.vehicle_fleet if v.vehicle_id == vehicle_id), None)
        if not vehicle:
            return {}
        
        # Simulate inspection results
        inspection_result = {
            "vehicle_id": vehicle_id,
            "inspection_date": date.today(),
            "violations": [],  # would contain actual violations
            "out_of_service": False,
            "score": 95.0
        }
        
        vehicle.last_inspection_date = date.today()
        
        # Record inspection cost
        inspection_cost = 200.0
        self.post("compliance_costs", "cash", inspection_cost, f"DOT inspection: {vehicle_id}")
        
        return inspection_result
    
    def manage_hours_of_service(self, driver_id: str, hours_driven: float) -> bool:
        """Track and manage driver hours of service"""
        driver = next((d for d in self.drivers if d.driver_id == driver_id), None)
        if not driver:
            return False
        
        # Update remaining hours (simplified HOS rules)
        driver.hours_of_service_remaining -= hours_driven
        
        # Check if driver needs rest
        if driver.hours_of_service_remaining <= 0:
            # Driver must take 10-hour break
            driver.hours_of_service_remaining = 11.0  # reset after break
            return False  # cannot continue driving
        
        return True
    
    # Performance analytics
    def calculate_fleet_utilization(self) -> Dict[str, float]:
        """Calculate utilization metrics for fleet"""
        if not self.vehicle_fleet:
            return {}
        
        total_vehicles = len(self.vehicle_fleet)
        vehicles_in_use = len([v for v in self.vehicle_fleet if v.driver_id])
        
        utilization_metrics = {
            "vehicle_utilization": vehicles_in_use / total_vehicles,
            "average_load_factor": sum(v.utilization_rate for v in self.vehicle_fleet) / total_vehicles,
            "revenue_per_vehicle": self.income_statement.get("revenue", 0) / max(total_vehicles, 1),
            "miles_per_vehicle": 50000.0,  # would calculate from actual data
            "fuel_efficiency": self.fuel_efficiency_mpg
        }
        
        return utilization_metrics
    
    def generate_performance_dashboard(self) -> Dict[str, Any]:
        """Generate comprehensive performance dashboard"""
        total_revenue = self.income_statement.get("revenue", 0)
        total_costs = self.income_statement.get("opex", 0)
        
        dashboard = {
            "financial_metrics": {
                "revenue": total_revenue,
                "operating_ratio": total_costs / max(total_revenue, 1),
                "revenue_per_mile": self.revenue_per_mile,
                "cost_per_mile": self.cost_per_mile
            },
            "operational_metrics": {
                "on_time_delivery": self.on_time_delivery_rate,
                "fleet_utilization": sum(v.utilization_rate for v in self.vehicle_fleet) / max(len(self.vehicle_fleet), 1),
                "average_transit_time": 24.0,  # hours, would calculate from actual data
                "damage_claims": self.damage_claim_rate
            },
            "safety_metrics": {
                "dot_safety_rating": self.dot_safety_rating,
                "safety_score": self.safety_score,
                "hours_compliance": self.hours_of_service_compliance,
                "driver_turnover": self.driver_turnover_rate
            },
            "customer_metrics": {
                "satisfaction_score": self.customer_satisfaction_score,
                "repeat_customer_rate": 0.75,  # would track actual data
                "service_quality": self.on_time_delivery_rate
            }
        }
        
        return dashboard
    
    def forecast_capacity_needs(self, growth_rate: float) -> Dict[str, int]:
        """Forecast future capacity needs based on growth projections"""
        current_shipment_volume = self.daily_shipment_volume
        projected_volume = current_shipment_volume * (1 + growth_rate)
        
        # Calculate additional capacity needed
        current_capacity = len(self.vehicle_fleet) * 365 * 2  # 2 shipments per vehicle per day
        capacity_shortfall = max(0, projected_volume * 365 - current_capacity)
        
        additional_vehicles_needed = int(capacity_shortfall / (365 * 2))
        additional_drivers_needed = int(additional_vehicles_needed * self.driver_to_vehicle_ratio)
        
        return {
            "additional_vehicles": additional_vehicles_needed,
            "additional_drivers": additional_drivers_needed,
            "additional_warehouse_sqft": int(projected_volume * 0.5),  # 0.5 sq ft per daily shipment
            "investment_required": additional_vehicles_needed * 150000 + additional_drivers_needed * 5000
        } 