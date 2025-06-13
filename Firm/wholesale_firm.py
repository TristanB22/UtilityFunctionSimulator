# wholesale_firm.py
# NAICS 42: Wholesale Trade

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class WholesaleType(Enum):
    MERCHANT_WHOLESALER = "merchant_wholesaler"
    MANUFACTURER_AGENT = "manufacturer_agent"
    COMMISSION_AGENT = "commission_agent"
    IMPORT_EXPORT = "import_export"
    DROP_SHIPPER = "drop_shipper"
    RACK_JOBBER = "rack_jobber"
    CASH_CARRY = "cash_carry"
    TRUCK_DISTRIBUTOR = "truck_distributor"

class ProductCategory(Enum):
    DURABLE_GOODS = "durable_goods"
    NONDURABLE_GOODS = "nondurable_goods"
    AGRICULTURAL_PRODUCTS = "agricultural_products"
    MACHINERY_EQUIPMENT = "machinery_equipment"
    ELECTRONICS = "electronics"
    CHEMICALS = "chemicals"
    PETROLEUM = "petroleum"
    FOOD_BEVERAGES = "food_beverages"
    TEXTILES = "textiles"
    AUTOMOTIVE = "automotive"

class CustomerType(Enum):
    RETAILER = "retailer"
    MANUFACTURER = "manufacturer"
    INSTITUTIONAL = "institutional"
    GOVERNMENT = "government"
    EXPORT = "export"
    SERVICE_BUSINESS = "service_business"

@dataclass
class Supplier:
    supplier_id: str
    company_name: str
    product_categories: List[ProductCategory]
    payment_terms: str = "net_30"  # net_30, net_60, cod, etc.
    reliability_score: float = 0.85  # 0-1 scale
    lead_time_days: int = 14
    minimum_order_quantity: int = 100
    volume_discounts: Dict[int, float] = field(default_factory=dict)  # quantity -> discount %

@dataclass
class Customer:
    customer_id: str
    company_name: str
    customer_type: CustomerType
    credit_limit: float
    payment_terms: str = "net_30"
    credit_rating: str = "A"  # A, B, C, D rating
    annual_volume: float = 0.0
    geographic_region: str = "domestic"

@dataclass
class Product:
    product_id: str
    product_name: str
    category: ProductCategory
    supplier_id: str
    cost_price: float
    wholesale_price: float
    minimum_order_qty: int = 1
    shelf_life_days: Optional[int] = None
    storage_requirements: str = "standard"  # standard, refrigerated, hazmat

@dataclass
class Inventory:
    product_id: str
    quantity_on_hand: int
    quantity_committed: int  # already sold but not shipped
    reorder_point: int
    maximum_stock_level: int
    average_monthly_usage: int
    last_order_date: date
    storage_cost_per_unit: float = 1.0

@dataclass
class SalesOrder:
    order_id: str
    customer_id: str
    order_date: date
    requested_delivery_date: date
    line_items: List[Dict[str, Any]]  # product_id, quantity, unit_price
    total_amount: float
    status: str = "pending"  # pending, confirmed, shipped, delivered, cancelled
    payment_status: str = "pending"  # pending, partial, paid

@dataclass
class PurchaseOrder:
    po_id: str
    supplier_id: str
    order_date: date
    expected_delivery_date: date
    line_items: List[Dict[str, Any]]  # product_id, quantity, unit_cost
    total_cost: float
    status: str = "pending"  # pending, confirmed, received, partial

@dataclass
class Warehouse:
    warehouse_id: str
    location: str
    total_capacity_sqft: float
    current_utilization: float = 0.75
    operating_cost_per_sqft: float = 8.0  # annual cost
    dock_doors: int = 10
    refrigeration_capacity: float = 0.0  # cubic feet

@dataclass
class WholesaleFirm(BaseFirm):
    # Business model characteristics
    wholesale_type: WholesaleType = WholesaleType.MERCHANT_WHOLESALER
    primary_product_categories: List[ProductCategory] = field(default_factory=list)
    territory_coverage: List[str] = field(default_factory=list)  # geographic regions
    business_model: str = "traditional"  # traditional, e_commerce, hybrid
    
    # Supplier relationships
    suppliers: List[Supplier] = field(default_factory=list)
    preferred_supplier_agreements: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    supplier_diversity_programs: bool = False
    average_supplier_lead_time: float = 21.0  # days
    
    # Customer base
    customers: List[Customer] = field(default_factory=list)
    customer_concentration_risk: float = 0.25  # % of revenue from top customer
    customer_acquisition_cost: float = 2500.0
    customer_retention_rate: float = 0.85
    
    # Product portfolio
    products: List[Product] = field(default_factory=list)
    product_lines: Dict[ProductCategory, int] = field(default_factory=dict)  # category -> count
    private_label_products: List[str] = field(default_factory=list)
    seasonal_products: List[str] = field(default_factory=list)
    
    # Inventory management
    inventory: List[Inventory] = field(default_factory=list)
    total_inventory_value: float = 0.0
    inventory_turnover_ratio: float = 6.0  # times per year
    stockout_frequency: float = 0.05  # 5% stockout rate
    obsolete_inventory_rate: float = 0.02  # 2% becomes obsolete
    
    # Sales operations
    sales_orders: List[SalesOrder] = field(default_factory=list)
    gross_sales: float = 0.0
    returns_allowances: float = 0.0
    net_sales: float = 0.0
    average_order_size: float = 5000.0
    order_fill_rate: float = 0.95  # 95% of orders filled completely
    
    # Purchasing and procurement
    purchase_orders: List[PurchaseOrder] = field(default_factory=list)
    total_purchases: float = 0.0
    purchase_volume_discounts: float = 0.0
    early_payment_discounts: float = 0.0
    supplier_payment_terms: Dict[str, str] = field(default_factory=dict)
    
    # Distribution and logistics
    warehouses: List[Warehouse] = field(default_factory=list)
    total_warehouse_capacity: float = 100000.0  # square feet
    distribution_channels: List[str] = field(default_factory=list)
    shipping_methods: List[str] = field(default_factory=list)
    average_delivery_time: float = 3.5  # days
    
    # Trade credit and financing
    accounts_receivable_days: int = 35
    accounts_payable_days: int = 25
    trade_credit_extended: float = 0.0
    bad_debt_rate: float = 0.015  # 1.5%
    credit_insurance_coverage: bool = False
    
    # Pricing and margins
    gross_margin_percentage: float = 0.18  # 18%
    markup_percentage: float = 0.22  # 22%
    price_elasticity_factors: Dict[ProductCategory, float] = field(default_factory=dict)
    competitor_pricing_data: Dict[str, float] = field(default_factory=dict)
    
    # Technology and operations
    erp_system: str = "integrated"
    electronic_data_interchange: bool = True
    order_automation_rate: float = 0.70  # 70% of orders automated
    warehouse_management_system: bool = True
    
    # Market position
    market_share: float = 0.15  # 15% in primary markets
    brand_recognition: float = 0.60
    competitive_advantages: List[str] = field(default_factory=list)
    regulatory_compliance_costs: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "42"  # Wholesale Trade
    
    # Supplier relationship management
    def onboard_supplier(self, supplier: Supplier) -> str:
        """Onboard new supplier"""
        self.suppliers.append(supplier)
        
        # Record onboarding costs
        onboarding_cost = 5000.0  # due diligence, setup, integration
        self.post("supplier_onboarding", "cash", onboarding_cost, f"Supplier: {supplier.supplier_id}")
        
        # Update supplier metrics
        total_lead_time = sum(s.lead_time_days for s in self.suppliers)
        self.average_supplier_lead_time = total_lead_time / len(self.suppliers)
        
        return supplier.supplier_id
    
    def negotiate_supplier_terms(self, supplier_id: str, new_terms: Dict[str, Any]) -> bool:
        """Negotiate better terms with supplier"""
        supplier = next((s for s in self.suppliers if s.supplier_id == supplier_id), None)
        if not supplier:
            return False
        
        # Update terms
        if "payment_terms" in new_terms:
            supplier.payment_terms = new_terms["payment_terms"]
        if "lead_time_days" in new_terms:
            supplier.lead_time_days = new_terms["lead_time_days"]
        if "volume_discounts" in new_terms:
            supplier.volume_discounts.update(new_terms["volume_discounts"])
        
        # Record negotiation costs
        negotiation_cost = 2000.0
        self.post("supplier_relations", "cash", negotiation_cost, f"Negotiations: {supplier_id}")
        
        return True
    
    def evaluate_supplier_performance(self, supplier_id: str) -> Dict[str, float]:
        """Evaluate supplier performance metrics"""
        supplier = next((s for s in self.suppliers if s.supplier_id == supplier_id), None)
        if not supplier:
            return {}
        
        # Calculate performance metrics
        on_time_delivery = min(1.0, supplier.reliability_score + 0.1)
        quality_score = supplier.reliability_score
        cost_competitiveness = 0.80  # simulated
        
        performance_metrics = {
            "on_time_delivery": on_time_delivery,
            "quality_score": quality_score,
            "cost_competitiveness": cost_competitiveness,
            "overall_score": (on_time_delivery + quality_score + cost_competitiveness) / 3
        }
        
        # Update supplier reliability based on performance
        supplier.reliability_score = (supplier.reliability_score * 0.8 + performance_metrics["overall_score"] * 0.2)
        
        return performance_metrics
    
    # Customer relationship management
    def acquire_customer(self, customer: Customer) -> str:
        """Acquire new customer"""
        # Perform credit check
        if not self._perform_credit_check(customer):
            return ""
        
        self.customers.append(customer)
        
        # Record customer acquisition cost
        self.post("customer_acquisition", "cash", self.customer_acquisition_cost, 
                 f"New customer: {customer.customer_id}")
        self.income_statement["opex"] += self.customer_acquisition_cost
        
        return customer.customer_id
    
    def set_customer_credit_limit(self, customer_id: str, credit_limit: float) -> bool:
        """Set or update customer credit limit"""
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            return False
        
        customer.credit_limit = credit_limit
        
        # Higher credit limits for A-rated customers
        if customer.credit_rating == "A":
            customer.credit_limit *= 1.25
        elif customer.credit_rating == "D":
            customer.credit_limit *= 0.50
        
        return True
    
    def analyze_customer_profitability(self, customer_id: str) -> Dict[str, float]:
        """Analyze customer profitability"""
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            return {}
        
        # Calculate customer metrics
        customer_orders = [o for o in self.sales_orders if o.customer_id == customer_id]
        total_revenue = sum(o.total_amount for o in customer_orders)
        
        # Estimate costs
        cost_to_serve = total_revenue * 0.12  # 12% cost to serve
        gross_profit = total_revenue * self.gross_margin_percentage
        net_profit = gross_profit - cost_to_serve
        
        profitability_metrics = {
            "total_revenue": total_revenue,
            "gross_profit": gross_profit,
            "cost_to_serve": cost_to_serve,
            "net_profit": net_profit,
            "profit_margin": net_profit / max(total_revenue, 1)
        }
        
        return profitability_metrics
    
    # Product management
    def add_product_line(self, product: Product) -> str:
        """Add new product to catalog"""
        self.products.append(product)
        
        # Update product line counts
        category = product.category
        current_count = self.product_lines.get(category, 0)
        self.product_lines[category] = current_count + 1
        
        # Create initial inventory record
        initial_inventory = Inventory(
            product_id=product.product_id,
            quantity_on_hand=0,
            quantity_committed=0,
            reorder_point=50,  # default reorder point
            maximum_stock_level=500,  # default max stock
            average_monthly_usage=100,  # estimated usage
            last_order_date=date.today()
        )
        self.inventory.append(initial_inventory)
        
        # Record product setup costs
        setup_cost = 1000.0  # catalog setup, supplier negotiations
        self.post("product_setup", "cash", setup_cost, f"Product: {product.product_id}")
        
        return product.product_id
    
    def update_product_pricing(self, product_id: str, new_wholesale_price: float) -> bool:
        """Update product pricing"""
        product = next((p for p in self.products if p.product_id == product_id), None)
        if not product:
            return False
        
        old_price = product.wholesale_price
        product.wholesale_price = new_wholesale_price
        
        # Update markup percentage
        if product.cost_price > 0:
            self.markup_percentage = (new_wholesale_price - product.cost_price) / product.cost_price
        
        # Analyze price elasticity impact
        price_change_ratio = new_wholesale_price / old_price
        elasticity = self.price_elasticity_factors.get(product.category, 1.0)
        
        # Estimate demand impact
        demand_change = -elasticity * (price_change_ratio - 1)
        
        return True
    
    def develop_private_label(self, product_name: str, category: ProductCategory, 
                             development_cost: float) -> str:
        """Develop private label product"""
        product_id = f"PL_{len(self.private_label_products) + 1}"
        self.private_label_products.append(product_id)
        
        # Record development costs
        self.post("private_label_development", "cash", development_cost, 
                 f"Private label: {product_name}")
        self.income_statement["opex"] += development_cost
        
        # Private label typically has higher margins
        enhanced_margin = self.gross_margin_percentage * 1.4  # 40% higher margin
        
        return product_id
    
    # Inventory management
    def manage_inventory_levels(self) -> Dict[str, int]:
        """Manage inventory levels and trigger reorders"""
        reorder_actions = {}
        
        for inv in self.inventory:
            available_stock = inv.quantity_on_hand - inv.quantity_committed
            
            # Check if reorder needed
            if available_stock <= inv.reorder_point:
                reorder_quantity = inv.maximum_stock_level - available_stock
                reorder_actions[inv.product_id] = reorder_quantity
                
                # Create purchase order
                self._create_purchase_order(inv.product_id, reorder_quantity)
        
        return reorder_actions
    
    def receive_inventory(self, product_id: str, quantity: int, cost_per_unit: float) -> None:
        """Receive inventory from supplier"""
        inventory_item = next((i for i in self.inventory if i.product_id == product_id), None)
        if not inventory_item:
            return
        
        # Update inventory quantities
        inventory_item.quantity_on_hand += quantity
        inventory_item.last_order_date = date.today()
        
        # Update inventory value
        total_cost = quantity * cost_per_unit
        self.total_inventory_value += total_cost
        
        # Record inventory receipt
        self.post("inventory", "accounts_payable", total_cost, f"Inventory: {product_id}")
        
    def calculate_inventory_turnover(self) -> float:
        """Calculate inventory turnover ratio"""
        if self.total_inventory_value == 0:
            return 0.0
        
        # Cost of goods sold for the period
        cogs = self.income_statement.get("cogs", 0)
        self.inventory_turnover_ratio = cogs / self.total_inventory_value
        
        return self.inventory_turnover_ratio
    
    def identify_slow_moving_inventory(self) -> List[str]:
        """Identify slow-moving inventory items"""
        slow_movers = []
        
        for inv in self.inventory:
            # Calculate days of inventory on hand
            if inv.average_monthly_usage > 0:
                days_on_hand = (inv.quantity_on_hand / inv.average_monthly_usage) * 30
                
                # Flag as slow-moving if more than 90 days on hand
                if days_on_hand > 90:
                    slow_movers.append(inv.product_id)
        
        return slow_movers
    
    # Sales operations
    def process_sales_order(self, order: SalesOrder) -> str:
        """Process incoming sales order"""
        # Check customer credit limit
        customer = next((c for c in self.customers if c.customer_id == order.customer_id), None)
        if not customer:
            return ""
        
        outstanding_receivables = self._calculate_customer_receivables(order.customer_id)
        if outstanding_receivables + order.total_amount > customer.credit_limit:
            order.status = "credit_hold"
            return order.order_id
        
        # Check inventory availability
        if not self._check_inventory_availability(order.line_items):
            order.status = "backorder"
            return order.order_id
        
        # Reserve inventory
        self._reserve_inventory(order.line_items)
        
        order.status = "confirmed"
        self.sales_orders.append(order)
        
        # Record sale
        self.gross_sales += order.total_amount
        self.net_sales = self.gross_sales - self.returns_allowances
        
        self.post("accounts_receivable", "sales_revenue", order.total_amount, 
                 f"Sale: {order.order_id}")
        self.income_statement["revenue"] += order.total_amount
        
        return order.order_id
    
    def ship_order(self, order_id: str) -> bool:
        """Ship confirmed order"""
        order = next((o for o in self.sales_orders if o.order_id == order_id), None)
        if not order or order.status != "confirmed":
            return False
        
        # Update inventory
        self._fulfill_inventory(order.line_items)
        
        # Calculate shipping costs
        shipping_cost = self._calculate_shipping_cost(order)
        
        order.status = "shipped"
        
        # Record shipping costs
        self.post("shipping_costs", "cash", shipping_cost, f"Shipping: {order_id}")
        self.income_statement["opex"] += shipping_cost
        
        return True
    
    def process_return(self, order_id: str, return_amount: float, reason: str) -> float:
        """Process customer return"""
        self.returns_allowances += return_amount
        self.net_sales = self.gross_sales - self.returns_allowances
        
        # Record return
        self.post("sales_returns", "accounts_receivable", return_amount, 
                 f"Return: {order_id}")
        
        # Impact on inventory depends on condition
        if reason in ["defective", "damaged"]:
            # Writeoff damaged goods
            writeoff_cost = return_amount * 0.80  # 80% of value lost
            self.post("inventory_writeoffs", "inventory", writeoff_cost, 
                     f"Damaged return: {order_id}")
        
        return return_amount
    
    # Purchasing operations
    def _create_purchase_order(self, product_id: str, quantity: int) -> str:
        """Create purchase order for inventory replenishment"""
        product = next((p for p in self.products if p.product_id == product_id), None)
        if not product:
            return ""
        
        supplier = next((s for s in self.suppliers if s.supplier_id == product.supplier_id), None)
        if not supplier:
            return ""
        
        # Calculate order details
        unit_cost = product.cost_price
        total_cost = quantity * unit_cost
        
        # Apply volume discounts
        for vol_threshold, discount in supplier.volume_discounts.items():
            if quantity >= vol_threshold:
                total_cost *= (1 - discount)
                break
        
        # Create purchase order
        po = PurchaseOrder(
            po_id=f"PO_{len(self.purchase_orders) + 1}",
            supplier_id=supplier.supplier_id,
            order_date=date.today(),
            expected_delivery_date=date.today() + timedelta(days=supplier.lead_time_days),
            line_items=[{"product_id": product_id, "quantity": quantity, "unit_cost": unit_cost}],
            total_cost=total_cost
        )
        
        self.purchase_orders.append(po)
        self.total_purchases += total_cost
        
        return po.po_id
    
    def negotiate_early_payment_discount(self, supplier_id: str, discount_rate: float) -> bool:
        """Negotiate early payment discount with supplier"""
        supplier = next((s for s in self.suppliers if s.supplier_id == supplier_id), None)
        if not supplier:
            return False
        
        # Record potential savings
        recent_purchases = sum(po.total_cost for po in self.purchase_orders 
                             if po.supplier_id == supplier_id)
        potential_savings = recent_purchases * discount_rate
        
        self.early_payment_discounts += potential_savings
        
        return True
    
    # Distribution and logistics
    def add_warehouse(self, warehouse: Warehouse) -> str:
        """Add new warehouse facility"""
        self.warehouses.append(warehouse)
        self.total_warehouse_capacity += warehouse.total_capacity_sqft
        
        # Record setup costs
        setup_cost = warehouse.total_capacity_sqft * 50.0  # $50 per sqft setup
        self.post("warehouse_setup", "cash", setup_cost, f"Warehouse: {warehouse.warehouse_id}")
        
        return warehouse.warehouse_id
    
    def optimize_distribution_network(self) -> Dict[str, Any]:
        """Optimize distribution network for efficiency"""
        # Calculate current distribution costs
        total_shipping_costs = sum(self._calculate_shipping_cost(order) for order in self.sales_orders)
        
        # Analyze warehouse utilization
        avg_utilization = sum(w.current_utilization for w in self.warehouses) / max(len(self.warehouses), 1)
        
        optimization_recommendations = {
            "current_shipping_costs": total_shipping_costs,
            "average_warehouse_utilization": avg_utilization,
            "recommended_consolidation": avg_utilization < 0.60,
            "expansion_needed": avg_utilization > 0.90
        }
        
        return optimization_recommendations
    
    def implement_cross_docking(self, percentage_cross_docked: float) -> float:
        """Implement cross-docking to reduce inventory handling"""
        # Cross-docking reduces storage costs but requires coordination
        storage_cost_savings = self.total_inventory_value * 0.02 * percentage_cross_docked  # 2% savings
    def extend_trade_credit(self, customer_id: str, credit_limit: float, terms: str) -> None:
        """Extend trade credit to customer"""
        credit = TradeCredit(
            customer_id=customer_id,
            credit_limit=credit_limit,
            outstanding_balance=0.0,
            payment_terms=terms,
            last_payment_date=date.today()
        )
        self.trade_credit_accounts.append(credit)
    
    def process_wholesale_order(self, customer_id: str, products: Dict[str, float], 
                               total_value: float) -> bool:
        """Process wholesale order from customer"""
        # Check credit availability
        credit_account = next((c for c in self.trade_credit_accounts if c.customer_id == customer_id), None)
        if credit_account and credit_account.outstanding_balance + total_value > credit_account.credit_limit:
            return False
        
        # Process order
        self.inventory = {k: v - products.get(k, 0) for k, v in self.inventory.items()}
        
        # Record sale and receivable
        if credit_account:
            credit_account.outstanding_balance += total_value
            self.post("accounts_receivable", "wholesale_revenue", total_value, f"Sale to {customer_id}")
        else:
            self.post("cash", "wholesale_revenue", total_value, f"Cash sale to {customer_id}")
        
        self.income_statement["revenue"] += total_value
        return True 