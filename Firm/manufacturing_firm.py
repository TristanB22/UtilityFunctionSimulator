# manufacturing_firm.py
# NAICS 31-33: Manufacturing

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class ManufacturingType(Enum):
    DISCRETE = "discrete"  # automobiles, electronics, furniture
    PROCESS = "process"    # chemicals, food, petroleum
    BATCH = "batch"        # pharmaceuticals, specialty chemicals
    CONTINUOUS = "continuous"  # steel, paper, oil refining

class ProductionStrategy(Enum):
    MAKE_TO_STOCK = "make_to_stock"
    MAKE_TO_ORDER = "make_to_order"
    ASSEMBLE_TO_ORDER = "assemble_to_order"
    ENGINEER_TO_ORDER = "engineer_to_order"

@dataclass
class Product:
    product_id: str
    product_name: str
    category: str
    unit_cost: float
    selling_price: float
    production_time_hours: float
    quality_specifications: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProductionLine:
    line_id: str
    manufacturing_type: ManufacturingType
    capacity_units_per_hour: float
    setup_time_hours: float
    efficiency_rate: float = 0.85  # OEE (Overall Equipment Effectiveness)
    current_product: str = None
    maintenance_schedule: List[date] = field(default_factory=list)

@dataclass
class RawMaterial:
    material_id: str
    material_name: str
    unit_cost: float
    lead_time_days: int
    minimum_order_quantity: float
    supplier_id: str
    quality_grade: str

@dataclass
class QualityControlBatch:
    batch_id: str
    product_id: str
    quantity: float
    test_results: Dict[str, float] = field(default_factory=dict)
    passed_inspection: bool = None
    inspector_id: str = None
    inspection_date: date = None

@dataclass
class ManufacturingFirm(BaseFirm):
    # Manufacturing capabilities
    manufacturing_types: List[ManufacturingType] = field(default_factory=list)
    production_strategy: ProductionStrategy = ProductionStrategy.MAKE_TO_STOCK
    production_lines: List[ProductionLine] = field(default_factory=list)
    total_capacity_utilization: float = 0.75
    
    # Product portfolio
    products: List[Product] = field(default_factory=list)
    product_mix: Dict[str, float] = field(default_factory=dict)  # product_id -> % of production
    finished_goods_inventory: Dict[str, float] = field(default_factory=dict)  # product_id -> quantity
    work_in_process: Dict[str, float] = field(default_factory=dict)  # product_id -> quantity
    
    # Supply chain and materials
    raw_materials: List[RawMaterial] = field(default_factory=list)
    raw_material_inventory: Dict[str, float] = field(default_factory=dict)  # material_id -> quantity
    supplier_relationships: Dict[str, Any] = field(default_factory=dict)  # supplier_id -> details
    just_in_time_enabled: bool = False
    safety_stock_levels: Dict[str, float] = field(default_factory=dict)  # material_id -> min quantity
    
    # Quality management
    quality_control_batches: List[QualityControlBatch] = field(default_factory=list)
    quality_standards: Dict[str, Any] = field(default_factory=dict)  # ISO, Six Sigma, etc.
    defect_rate: float = 0.02  # 2% default defect rate
    rework_rate: float = 0.01  # 1% rework rate
    quality_certifications: List[str] = field(default_factory=list)
    
    # Production planning and control
    production_schedule: Dict[date, Dict[str, float]] = field(default_factory=dict)  # date -> product_id -> quantity
    master_production_schedule: Dict[str, Any] = field(default_factory=dict)
    material_requirements_plan: Dict[str, Any] = field(default_factory=dict)
    capacity_requirements_plan: Dict[str, Any] = field(default_factory=dict)
    
    # Cost accounting
    standard_costs: Dict[str, float] = field(default_factory=dict)  # product_id -> standard_cost
    actual_costs: Dict[str, float] = field(default_factory=dict)  # product_id -> actual_cost
    overhead_allocation_method: str = "activity_based"  # ABC, traditional, etc.
    learning_curve_factor: float = 0.95  # cost reduction with volume
    
    # Energy and environmental
    energy_consumption_kwh: float = 0.0
    waste_generation: Dict[str, float] = field(default_factory=dict)  # waste_type -> quantity
    recycling_programs: List[str] = field(default_factory=list)
    environmental_compliance_costs: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "31"  # Manufacturing base code (31-33 range)
    
    # Production operations
    def schedule_production(self, product_id: str, quantity: float, target_date: date) -> bool:
        """Schedule production of specific product"""
        product = next((p for p in self.products if p.product_id == product_id), None)
        if not product:
            return False
        
        if target_date not in self.production_schedule:
            self.production_schedule[target_date] = {}
        
        self.production_schedule[target_date][product_id] = quantity
        
        # Update WIP
        self.work_in_process[product_id] = self.work_in_process.get(product_id, 0) + quantity
        
        return True
    
    def produce_batch(self, production_line_id: str, product_id: str, quantity: float) -> bool:
        """Execute production batch on specific line"""
        line = next((l for l in self.production_lines if l.line_id == production_line_id), None)
        product = next((p for p in self.products if p.product_id == product_id), None)
        
        if not line or not product:
            return False
        
        # Check capacity
        production_time_needed = quantity / line.capacity_units_per_hour
        if line.current_product and line.current_product != product_id:
            production_time_needed += line.setup_time_hours
        
        # Calculate actual output considering efficiency
        actual_quantity = quantity * line.efficiency_rate
        
        # Consume raw materials
        material_consumed = self._consume_raw_materials_for_production(product_id, actual_quantity)
        if not material_consumed:
            return False
        
        # Update production line
        line.current_product = product_id
        
        # Move from WIP to finished goods
        wip_quantity = self.work_in_process.get(product_id, 0)
        completed_quantity = min(actual_quantity, wip_quantity)
        
        self.work_in_process[product_id] = wip_quantity - completed_quantity
        self.finished_goods_inventory[product_id] = self.finished_goods_inventory.get(product_id, 0) + completed_quantity
        
        # Record production costs
        production_cost = completed_quantity * product.unit_cost
        self.post("production_costs", "finished_goods_inventory", production_cost, 
                 f"Production: {product_id}")
        self.income_statement["cogs"] += production_cost
        
        return True
    
    def _consume_raw_materials_for_production(self, product_id: str, quantity: float) -> bool:
        """Consume raw materials needed for production (simplified BOM)"""
        # Simplified: assume each product unit needs 1 unit of primary material
        primary_material = f"material_for_{product_id}"
        
        available = self.raw_material_inventory.get(primary_material, 0)
        if available < quantity:
            return False
        
        self.raw_material_inventory[primary_material] = available - quantity
        return True
    
    # Quality control
    def conduct_quality_inspection(self, batch_id: str, inspector_id: str) -> bool:
        """Conduct quality inspection on production batch"""
        batch = next((b for b in self.quality_control_batches if b.batch_id == batch_id), None)
        if not batch:
            return False
        
        # Simulate quality test results
        batch.inspection_date = date.today()
        batch.inspector_id = inspector_id
        
        # Simplified quality check - compare against defect rate
        import random
        passed = random.random() > self.defect_rate
        batch.passed_inspection = passed
        
        if not passed:
            # Move defective units to rework or scrap
            defective_quantity = batch.quantity * self.defect_rate
            rework_quantity = defective_quantity * self.rework_rate
            scrap_quantity = defective_quantity - rework_quantity
            
            # Adjust finished goods inventory
            current_fg = self.finished_goods_inventory.get(batch.product_id, 0)
            self.finished_goods_inventory[batch.product_id] = max(0, current_fg - defective_quantity)
            
            # Add rework to WIP
            if rework_quantity > 0:
                self.work_in_process[batch.product_id] = self.work_in_process.get(batch.product_id, 0) + rework_quantity
        
        return passed
    
    def implement_quality_program(self, program_name: str, cost: float, 
                                defect_reduction: float) -> None:
        """Implement quality improvement program"""
        self.quality_certifications.append(program_name)
        self.defect_rate = max(0.001, self.defect_rate - defect_reduction)
        
        self.post("quality_programs", "cash", cost, f"Quality program: {program_name}")
        self.income_statement["opex"] += cost
    
    # Supply chain management
    def order_raw_materials(self, material_id: str, quantity: float) -> bool:
        """Order raw materials from supplier"""
        material = next((m for m in self.raw_materials if m.material_id == material_id), None)
        if not material:
            return False
        
        # Check minimum order quantity
        if quantity < material.minimum_order_quantity:
            quantity = material.minimum_order_quantity
        
        total_cost = quantity * material.unit_cost
        
        # Record purchase
        self.post("raw_materials_inventory", "cash", total_cost, f"Material purchase: {material_id}")
        
        # Add to inventory (simplified - immediate delivery)
        self.raw_material_inventory[material_id] = self.raw_material_inventory.get(material_id, 0) + quantity
        
        return True
    
    def calculate_reorder_point(self, material_id: str) -> float:
        """Calculate reorder point for material"""
        material = next((m for m in self.raw_materials if m.material_id == material_id), None)
        if not material:
            return 0.0
        
        # Simple reorder point calculation: lead time demand + safety stock
        daily_usage = 10.0  # simplified assumption
        lead_time_demand = daily_usage * material.lead_time_days
        safety_stock = self.safety_stock_levels.get(material_id, lead_time_demand * 0.5)
        
        return lead_time_demand + safety_stock
    
    # Cost accounting and analysis
    def calculate_product_costs(self, product_id: str) -> Dict[str, float]:
        """Calculate detailed product costs"""
        product = next((p for p in self.products if p.product_id == product_id), None)
        if not product:
            return {}
        
        # Material costs (simplified)
        material_cost = product.unit_cost * 0.6  # assume 60% material
        
        # Labor costs
        labor_cost = product.unit_cost * 0.25  # assume 25% labor
        
        # Overhead costs
        overhead_cost = product.unit_cost * 0.15  # assume 15% overhead
        
        return {
            "material_cost": material_cost,
            "labor_cost": labor_cost,
            "overhead_cost": overhead_cost,
            "total_cost": material_cost + labor_cost + overhead_cost
        }
    
    def apply_learning_curve(self, product_id: str, cumulative_volume: float) -> float:
        """Apply learning curve to reduce costs with volume"""
        if cumulative_volume <= 1:
            return 1.0
        
        # Learning curve: cost = initial_cost * (cumulative_volume ^ log(learning_curve_factor)/log(2))
        import math
        learning_exponent = math.log(self.learning_curve_factor) / math.log(2)
        cost_factor = cumulative_volume ** learning_exponent
        
        return cost_factor
    
    # Capacity planning
    def calculate_line_utilization(self, line_id: str) -> float:
        """Calculate utilization rate for production line"""
        line = next((l for l in self.production_lines if l.line_id == line_id), None)
        if not line:
            return 0.0
        
        # Simplified utilization calculation
        scheduled_hours = 0.0
        available_hours = 8.0 * 365  # assume 8 hours/day, 365 days/year
        
        for schedule in self.production_schedule.values():
            for prod_id, quantity in schedule.items():
                if line.current_product == prod_id or not line.current_product:
                    scheduled_hours += quantity / line.capacity_units_per_hour
        
        return min(1.0, scheduled_hours / available_hours)
    
    # Environmental and energy management
    def track_energy_consumption(self, kwh_consumed: float, period: str) -> None:
        """Track energy consumption for period"""
        self.energy_consumption_kwh += kwh_consumed
        
        # Record energy costs (assume $0.10/kWh)
        energy_cost = kwh_consumed * 0.10
        self.post("energy_costs", "cash", energy_cost, f"Energy consumption: {period}")
        self.income_statement["opex"] += energy_cost
    
    def implement_waste_reduction(self, program_name: str, cost: float, 
                                waste_reduction_pct: float) -> None:
        """Implement waste reduction program"""
        self.recycling_programs.append(program_name)
        
        # Reduce waste generation
        for waste_type in self.waste_generation:
            self.waste_generation[waste_type] *= (1.0 - waste_reduction_pct)
        
        self.post("environmental_programs", "cash", cost, f"Waste reduction: {program_name}")
        self.environmental_compliance_costs += cost
    
    # Analytics and reporting
    def get_production_summary(self) -> Dict[str, Any]:
        """Generate production performance summary"""
        total_fg_inventory = sum(self.finished_goods_inventory.values())
        total_wip = sum(self.work_in_process.values())
        
        return {
            "total_capacity_utilization": self.total_capacity_utilization,
            "finished_goods_value": total_fg_inventory,
            "work_in_process_value": total_wip,
            "defect_rate": self.defect_rate,
            "product_lines": len(self.production_lines),
            "active_products": len([p for p in self.products if p.product_id in self.finished_goods_inventory]),
            "energy_efficiency": self.energy_consumption_kwh / max(1, total_fg_inventory)  # kWh per unit
        } 