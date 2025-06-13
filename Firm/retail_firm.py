# retail_firm.py
# NAICS 44-45: Retail Trade

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class RetailChannel(Enum):
    BRICK_AND_MORTAR = "brick_and_mortar"
    E_COMMERCE = "e_commerce"
    MOBILE_APP = "mobile_app"
    CATALOG = "catalog"
    CLICK_AND_COLLECT = "click_and_collect"
    SOCIAL_COMMERCE = "social_commerce"
    MARKETPLACE = "marketplace"  # Amazon, eBay, etc.

class RetailFormat(Enum):
    DEPARTMENT_STORE = "department_store"
    SPECIALTY_STORE = "specialty_store"
    SUPERMARKET = "supermarket"
    CONVENIENCE_STORE = "convenience_store"
    DISCOUNT_STORE = "discount_store"
    WAREHOUSE_CLUB = "warehouse_club"
    OUTLET_STORE = "outlet_store"
    POP_UP_STORE = "pop_up_store"

class MerchandiseCategory(Enum):
    APPAREL = "apparel"
    ELECTRONICS = "electronics"
    HOME_GARDEN = "home_garden"
    FOOD_BEVERAGE = "food_beverage"
    HEALTH_BEAUTY = "health_beauty"
    AUTOMOTIVE = "automotive"
    SPORTING_GOODS = "sporting_goods"
    BOOKS_MEDIA = "books_media"

@dataclass
class StoreLocation:
    store_id: str
    address: str
    square_footage: float
    monthly_rent: float
    daily_foot_traffic: int
    conversion_rate: float
    average_transaction_value: float
    operating_hours: str
    store_format: RetailFormat
    trade_area_demographics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Product:
    sku: str
    product_name: str
    category: MerchandiseCategory
    cost_price: float
    retail_price: float
    supplier_id: str
    lead_time_days: int
    seasonal_item: bool = False
    markdown_eligible: bool = True

@dataclass
class InventoryItem:
    sku: str
    location: str  # store_id or "warehouse"
    quantity_on_hand: int
    quantity_reserved: int  # for online orders
    reorder_point: int
    max_stock_level: int
    last_count_date: date
    shrinkage_rate: float = 0.02

@dataclass
class CustomerSegment:
    segment_id: str
    demographics: Dict[str, Any]
    shopping_behaviors: Dict[str, Any]
    lifetime_value: float
    retention_rate: float
    preferred_channels: List[RetailChannel]

@dataclass
class PromotionalCampaign:
    campaign_id: str
    campaign_type: str  # sale, BOGO, loyalty, etc.
    start_date: date
    end_date: date
    discount_percentage: float
    target_categories: List[MerchandiseCategory]
    budget: float
    expected_lift: float

@dataclass
class RetailFirm(BaseFirm):
    # Store operations and format
    retail_channels: List[RetailChannel] = field(default_factory=list)
    store_locations: List[StoreLocation] = field(default_factory=list)
    store_formats: List[RetailFormat] = field(default_factory=list)
    total_retail_square_footage: float = 0.0
    
    # Product and category management
    product_catalog: List[Product] = field(default_factory=list)
    merchandise_categories: List[MerchandiseCategory] = field(default_factory=list)
    private_label_brands: List[str] = field(default_factory=list)
    vendor_relationships: Dict[str, Any] = field(default_factory=dict)
    
    # Inventory management
    inventory_by_location: List[InventoryItem] = field(default_factory=list)
    inventory_turnover_rate: float = 4.0  # times per year
    shrinkage_rate: float = 0.02  # inventory loss %
    stockout_rate: float = 0.05  # out of stock incidents
    safety_stock_multiplier: float = 1.5
    
    # Pricing and merchandising
    base_markup_percentage: float = 0.50  # 50% markup
    markdown_rate: float = 0.15  # discount %
    promotional_penetration: float = 0.30  # % of sales on promotion
    price_elasticity: Dict[str, float] = field(default_factory=dict)  # category -> elasticity
    competitive_pricing_strategy: str = "market_based"
    
    # Customer experience and analytics
    customer_segments: List[CustomerSegment] = field(default_factory=list)
    loyalty_program_members: int = 0
    customer_satisfaction_score: float = 3.5  # out of 5
    net_promoter_score: float = 25.0  # -100 to 100
    average_transaction_value: float = 50.0
    transactions_per_customer: float = 6.0  # annual
    
    # Digital and omnichannel capabilities
    e_commerce_platform: str = ""
    mobile_app_downloads: int = 0
    online_conversion_rate: float = 0.025  # 2.5%
    buy_online_pickup_in_store: bool = True
    ship_from_store_enabled: bool = False
    curbside_pickup: bool = False
    same_day_delivery: bool = False
    
    # Seasonal operations and planning
    seasonal_multipliers: Dict[str, float] = field(default_factory=dict)  # season -> sales multiplier
    promotional_calendar: List[PromotionalCampaign] = field(default_factory=list)
    holiday_sales_percentage: float = 0.25  # % of annual sales in holiday season
    back_to_school_sales: bool = False
    seasonal_inventory_planning: Dict[str, Any] = field(default_factory=dict)
    
    # Supply chain and logistics
    distribution_centers: List[str] = field(default_factory=list)
    vendor_managed_inventory: bool = False
    drop_ship_capability: bool = False
    cross_docking_operations: bool = False
    supply_chain_visibility: float = 0.80  # visibility into supplier operations
    
    # Store operations metrics
    sales_per_square_foot: float = 200.0  # annual
    foot_traffic_conversion: float = 0.20  # 20% of visitors make purchase
    average_items_per_transaction: float = 3.5
    return_rate: float = 0.08  # 8% of sales returned
    store_labor_productivity: float = 100.0  # sales per labor hour
    
    # Marketing and advertising
    advertising_spend_percentage: float = 0.03  # 3% of sales
    digital_marketing_percentage: float = 0.60  # 60% of ad spend
    customer_acquisition_cost: float = 25.0
    email_marketing_list: int = 0
    social_media_followers: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "44"  # Retail Trade (44-45 range)
    
    # Store operations
    def open_new_store(self, store: StoreLocation) -> bool:
        """Open new retail location"""
        self.store_locations.append(store)
        self.total_retail_square_footage += store.square_footage
        
        # Record store opening costs (fixtures, inventory, etc.)
        opening_cost = store.square_footage * 150  # $150 per sq ft assumption
        self.post("store_assets", "cash", opening_cost, f"Store opening: {store.store_id}")
        
        return True
    
    def process_retail_sale(self, store_id: str, channel: RetailChannel, items_sold: List[Dict], 
                           payment_method: str = "cash") -> str:
        """Process retail sale through specific channel"""
        transaction_id = f"txn_{store_id}_{len(self.ledger)}"
        total_amount = 0.0
        total_cost = 0.0
        
        for item in items_sold:
            sku = item["sku"]
            quantity = item["quantity"]
            
            # Find product and calculate amounts
            product = next((p for p in self.product_catalog if p.sku == sku), None)
            if product:
                sale_amount = product.retail_price * quantity
                cost_amount = product.cost_price * quantity
                total_amount += sale_amount
                total_cost += cost_amount
                
                # Update inventory
                self._update_inventory(sku, store_id, -quantity)
        
        # Record sale
        self.post("cash", "retail_revenue", total_amount, f"Sale: {transaction_id}")
        self.post("cost_of_goods_sold", "inventory", total_cost, f"COGS: {transaction_id}")
        
        self.income_statement["revenue"] += total_amount
        self.income_statement["cogs"] += total_cost
        
        # Update channel-specific metrics
        self._update_channel_metrics(channel, total_amount)
        
        return transaction_id
    
    def _update_inventory(self, sku: str, location: str, quantity_change: int) -> None:
        """Update inventory levels for specific SKU and location"""
        inventory_item = next((i for i in self.inventory_by_location 
                             if i.sku == sku and i.location == location), None)
        
        if inventory_item:
            inventory_item.quantity_on_hand += quantity_change
            
            # Check if reorder is needed
            if inventory_item.quantity_on_hand <= inventory_item.reorder_point:
                self._trigger_reorder(sku, location)
    
    def _trigger_reorder(self, sku: str, location: str) -> None:
        """Trigger reorder when inventory hits reorder point"""
        inventory_item = next((i for i in self.inventory_by_location 
                             if i.sku == sku and i.location == location), None)
        product = next((p for p in self.product_catalog if p.sku == sku), None)
        
        if inventory_item and product:
            reorder_quantity = inventory_item.max_stock_level - inventory_item.quantity_on_hand
            total_cost = reorder_quantity * product.cost_price
            
            self.post("inventory", "accounts_payable", total_cost, f"Reorder: {sku}")
            inventory_item.quantity_on_hand += reorder_quantity
    
    def _update_channel_metrics(self, channel: RetailChannel, sale_amount: float) -> None:
        """Update channel-specific performance metrics"""
        if channel == RetailChannel.E_COMMERCE:
            # Update e-commerce metrics
            self.online_conversion_rate = min(self.online_conversion_rate * 1.001, 0.10)
        elif channel == RetailChannel.BRICK_AND_MORTAR:
            # Update store metrics
            for store in self.store_locations:
                store.average_transaction_value = (store.average_transaction_value * 0.95 + 
                                                 sale_amount * 0.05)
    
    # Pricing and merchandising
    def apply_markdown(self, category: MerchandiseCategory, markdown_percent: float, 
                      store_ids: List[str] = None) -> float:
        """Apply markdown to product category"""
        total_markdown_value = 0.0
        
        # Apply to specific stores or all stores
        locations = store_ids if store_ids else [s.store_id for s in self.store_locations]
        
        for location in locations:
            for inventory_item in self.inventory_by_location:
                if inventory_item.location == location:
                    product = next((p for p in self.product_catalog if p.sku == inventory_item.sku), None)
                    if product and product.category == category and product.markdown_eligible:
                        markdown_value = (inventory_item.quantity_on_hand * 
                                       product.retail_price * markdown_percent)
                        total_markdown_value += markdown_value
                        
                        # Update product price
                        product.retail_price *= (1.0 - markdown_percent)
        
        self.post("markdown_expense", "inventory", total_markdown_value, 
                 f"Markdown: {category.value}")
        self.income_statement["opex"] += total_markdown_value
        return total_markdown_value
    
    def implement_promotional_campaign(self, campaign: PromotionalCampaign) -> None:
        """Launch promotional campaign"""
        self.promotional_calendar.append(campaign)
        
        # Record promotional costs
        self.post("advertising_expense", "cash", campaign.budget, 
                 f"Campaign: {campaign.campaign_id}")
        self.income_statement["opex"] += campaign.budget
    
    def dynamic_pricing_adjustment(self, sku: str, demand_factor: float, 
                                 competition_factor: float) -> float:
        """Adjust pricing based on demand and competition"""
        product = next((p for p in self.product_catalog if p.sku == sku), None)
        if not product:
            return 0.0
        
        # Calculate price adjustment
        elasticity = self.price_elasticity.get(product.category.value, -1.5)
        price_change_factor = 1.0 + (demand_factor * 0.1) - (competition_factor * 0.05)
        
        old_price = product.retail_price
        product.retail_price = old_price * price_change_factor
        
        return product.retail_price - old_price
    
    # Customer experience and loyalty
    def enroll_loyalty_member(self, customer_id: str, enrollment_channel: str) -> bool:
        """Enroll customer in loyalty program"""
        self.loyalty_program_members += 1
        
        # Record enrollment incentive cost
        enrollment_incentive = 10.0  # $10 welcome bonus
        self.post("loyalty_program_costs", "cash", enrollment_incentive, 
                 f"Loyalty enrollment: {customer_id}")
        
        return True
    
    def process_return(self, original_transaction_id: str, items_returned: List[Dict], 
                      reason: str) -> float:
        """Process customer return"""
        total_refund = 0.0
        
        for item in items_returned:
            sku = item["sku"]
            quantity = item["quantity"]
            
            product = next((p for p in self.product_catalog if p.sku == sku), None)
            if product:
                refund_amount = product.retail_price * quantity
                total_refund += refund_amount
                
                # Return inventory to stock (if saleable)
                if reason != "defective":
                    self._update_inventory(sku, "returns_processing", quantity)
        
        # Record return
        self.post("sales_returns", "cash", total_refund, f"Return: {original_transaction_id}")
        self.income_statement["revenue"] -= total_refund
        
        return total_refund
    
    def measure_customer_satisfaction(self, survey_responses: List[Dict]) -> float:
        """Process customer satisfaction survey responses"""
        if not survey_responses:
            return self.customer_satisfaction_score
        
        total_score = sum(response["rating"] for response in survey_responses)
        average_score = total_score / len(survey_responses)
        
        # Update overall satisfaction score (weighted average)
        self.customer_satisfaction_score = (self.customer_satisfaction_score * 0.8 + 
                                          average_score * 0.2)
        
        return self.customer_satisfaction_score
    
    # Digital and omnichannel operations
    def fulfill_online_order(self, order_id: str, items: List[Dict], 
                           fulfillment_method: str) -> bool:
        """Fulfill online order through various methods"""
        total_value = 0.0
        
        for item in items:
            sku = item["sku"]
            quantity = item["quantity"]
            store_id = item.get("fulfillment_location", "warehouse")
            
            # Check inventory availability
            inventory_item = next((i for i in self.inventory_by_location 
                                 if i.sku == sku and i.location == store_id), None)
            
            if not inventory_item or inventory_item.quantity_on_hand < quantity:
                return False  # Cannot fulfill
            
            product = next((p for p in self.product_catalog if p.sku == sku), None)
            if product:
                total_value += product.retail_price * quantity
                
        # Process fulfillment
        fulfillment_cost = self._calculate_fulfillment_cost(fulfillment_method, total_value)
        
        self.post("cash", "online_revenue", total_value, f"Online order: {order_id}")
        self.post("fulfillment_costs", "cash", fulfillment_cost, f"Fulfillment: {order_id}")
        
        self.income_statement["revenue"] += total_value
        self.income_statement["opex"] += fulfillment_cost
        
        return True
    
    def _calculate_fulfillment_cost(self, method: str, order_value: float) -> float:
        """Calculate cost of order fulfillment"""
        cost_factors = {
            "ship_to_home": 8.50,
            "ship_from_store": 6.00,
            "buy_online_pickup_store": 2.50,
            "curbside_pickup": 3.00,
            "same_day_delivery": 15.00
        }
        return cost_factors.get(method, 8.50)
    
    def optimize_inventory_allocation(self) -> Dict[str, int]:
        """Optimize inventory allocation across channels and locations"""
        allocation_changes = {}
        
        for product in self.product_catalog:
            sku = product.sku
            
            # Calculate demand by location
            total_inventory = sum(i.quantity_on_hand for i in self.inventory_by_location 
                                if i.sku == sku)
            
            # Simple allocation based on historical sales velocity
            # In practice, this would use sophisticated demand forecasting
            for store in self.store_locations:
                target_allocation = int(total_inventory * 0.2)  # 20% per store assumption
                current_allocation = next((i.quantity_on_hand for i in self.inventory_by_location 
                                        if i.sku == sku and i.location == store.store_id), 0)
                
                if abs(target_allocation - current_allocation) > 5:
                    allocation_changes[f"{sku}_{store.store_id}"] = target_allocation - current_allocation
        
        return allocation_changes
    
    # Analytics and reporting
    def calculate_key_performance_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive retail KPIs"""
        total_revenue = self.income_statement.get("revenue", 0)
        total_stores = len(self.store_locations)
        
        metrics = {
            "sales_per_square_foot": total_revenue / max(self.total_retail_square_footage, 1),
            "average_transaction_value": self.average_transaction_value,
            "inventory_turnover": self.inventory_turnover_rate,
            "gross_margin": (total_revenue - self.income_statement.get("cogs", 0)) / max(total_revenue, 1),
            "shrinkage_rate": self.shrinkage_rate,
            "customer_satisfaction": self.customer_satisfaction_score,
            "loyalty_penetration": self.loyalty_program_members / max(total_stores * 1000, 1),  # assume 1000 customers per store
            "return_rate": self.return_rate,
            "stockout_rate": self.stockout_rate,
            "markdown_percentage": self.markdown_rate
        }
        
        return metrics
    
    def generate_category_performance_report(self) -> Dict[str, Dict[str, float]]:
        """Generate performance report by merchandise category"""
        category_performance = {}
        
        for category in self.merchandise_categories:
            category_products = [p for p in self.product_catalog if p.category == category]
            
            if category_products:
                total_revenue = sum(p.retail_price * 100 for p in category_products)  # simplified
                total_cost = sum(p.cost_price * 100 for p in category_products)
                
                category_performance[category.value] = {
                    "revenue": total_revenue,
                    "gross_margin": (total_revenue - total_cost) / max(total_revenue, 1),
                    "product_count": len(category_products),
                    "average_price": sum(p.retail_price for p in category_products) / len(category_products)
                }
        
        return category_performance
    
    def forecast_seasonal_demand(self, season: str, category: MerchandiseCategory) -> float:
        """Forecast demand for specific season and category"""
        base_multiplier = self.seasonal_multipliers.get(season, 1.0)
        
        # Category-specific seasonal adjustments
        category_seasonality = {
            MerchandiseCategory.APPAREL: {"winter": 1.3, "spring": 1.1, "summer": 0.9, "fall": 1.2},
            MerchandiseCategory.HOME_GARDEN: {"winter": 0.8, "spring": 1.4, "summer": 1.2, "fall": 1.0},
            MerchandiseCategory.ELECTRONICS: {"winter": 1.5, "spring": 0.9, "summer": 0.8, "fall": 1.1}
        }
        
        category_multiplier = category_seasonality.get(category, {}).get(season, 1.0)
        return base_multiplier * category_multiplier
    
    def analyze_customer_lifetime_value(self, customer_segment_id: str) -> float:
        """Calculate customer lifetime value for segment"""
        segment = next((s for s in self.customer_segments if s.segment_id == customer_segment_id), None)
        
        if not segment:
            return 0.0
        
        # Simplified CLV calculation
        annual_spend = self.average_transaction_value * self.transactions_per_customer
        customer_lifespan = 1.0 / (1.0 - segment.retention_rate)  # years
        
        return annual_spend * customer_lifespan * 0.1  # 10% profit margin assumption 