# information_firm.py
# NAICS 51: Information

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class InformationType(Enum):
    PUBLISHING = "publishing"
    BROADCASTING = "broadcasting"
    TELECOMMUNICATIONS = "telecommunications"
    DATA_PROCESSING = "data_processing"
    SOFTWARE_DEVELOPMENT = "software_development"
    STREAMING_SERVICES = "streaming_services"
    SOCIAL_MEDIA = "social_media"
    SEARCH_ENGINES = "search_engines"
    CLOUD_SERVICES = "cloud_services"

class ContentType(Enum):
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    INTERACTIVE = "interactive"
    GAMES = "games"
    EDUCATIONAL = "educational"
    NEWS = "news"
    ENTERTAINMENT = "entertainment"

class RevenueModel(Enum):
    SUBSCRIPTION = "subscription"
    ADVERTISING = "advertising"
    TRANSACTION = "transaction"
    FREEMIUM = "freemium"
    LICENSING = "licensing"
    DATA_MONETIZATION = "data_monetization"
    PLATFORM_FEES = "platform_fees"

class DeliveryChannel(Enum):
    STREAMING = "streaming"
    BROADCAST = "broadcast"
    DIGITAL_DOWNLOAD = "digital_download"
    PHYSICAL_MEDIA = "physical_media"
    CLOUD_PLATFORM = "cloud_platform"
    MOBILE_APP = "mobile_app"
    WEB_PORTAL = "web_portal"

@dataclass
class ContentAsset:
    content_id: str
    title: str
    content_type: ContentType
    creation_date: date
    production_cost: float
    runtime_minutes: float = 0.0
    content_rating: str = "G"
    views_count: int = 0
    revenue_generated: float = 0.0
    licensing_rights: List[str] = field(default_factory=list)
    distribution_channels: List[DeliveryChannel] = field(default_factory=list)

@dataclass
class Subscriber:
    subscriber_id: str
    subscription_tier: str
    monthly_fee: float
    start_date: date
    renewal_date: date
    usage_hours: float = 0.0
    demographics: Dict[str, Any] = field(default_factory=dict)
    engagement_score: float = 0.5

@dataclass
class AdvertisingCampaign:
    campaign_id: str
    advertiser_id: str
    campaign_type: str  # display, video, audio, native
    budget: float
    start_date: date
    end_date: date
    target_demographics: Dict[str, Any] = field(default_factory=dict)
    impressions_delivered: int = 0
    click_through_rate: float = 0.02

@dataclass
class TechnologyInfrastructure:
    system_id: str
    system_type: str  # CDN, servers, networking
    capacity: float
    utilization_rate: float = 0.70
    maintenance_cost_monthly: float = 0.0
    upgrade_date: date = None

@dataclass
class DataSet:
    dataset_id: str
    data_type: str  # user behavior, market research, etc.
    records_count: int
    collection_date: date
    privacy_compliance: List[str] = field(default_factory=list)  # GDPR, CCPA, etc.
    monetization_value: float = 0.0

@dataclass
class InformationFirm(BaseFirm):
    # Core information services and content
    information_types: List[InformationType] = field(default_factory=list)
    content_library: List[ContentAsset] = field(default_factory=list)
    intellectual_property: List[str] = field(default_factory=list)  # copyrights, patents, trademarks
    content_categories: List[ContentType] = field(default_factory=list)
    
    # Revenue streams and business models
    revenue_models: List[RevenueModel] = field(default_factory=list)
    subscription_tiers: Dict[str, float] = field(default_factory=dict)  # tier -> monthly_price
    subscribers: List[Subscriber] = field(default_factory=list)
    advertising_inventory: Dict[str, float] = field(default_factory=dict)  # ad_type -> available_spots
    
    # Technology infrastructure and capacity
    infrastructure: List[TechnologyInfrastructure] = field(default_factory=list)
    server_capacity: float = 0.0  # compute units
    bandwidth_capacity: float = 0.0  # Mbps
    data_storage_tb: float = 0.0  # terabytes
    uptime_target: float = 0.999  # 99.9% uptime
    content_delivery_network: bool = True
    
    # Content production and management
    content_production_budget: float = 0.0
    content_acquisition_costs: float = 0.0
    original_content_percentage: float = 0.30  # 30% original content
    content_refresh_rate: float = 0.20  # 20% content updated monthly
    content_moderation_system: bool = True
    
    # User engagement and analytics
    active_users: int = 0
    daily_active_users: int = 0
    monthly_active_users: int = 0
    content_consumption_hours: float = 0.0
    user_engagement_rate: float = 0.15  # 15% daily active users
    session_duration_minutes: float = 45.0
    user_retention_rate: Dict[str, float] = field(default_factory=dict)  # day_1, day_7, day_30
    
    # Data and analytics
    data_assets: List[DataSet] = field(default_factory=list)
    user_data_collection: bool = True
    privacy_compliance_programs: List[str] = field(default_factory=list)
    data_monetization_revenue: float = 0.0
    analytics_capabilities: List[str] = field(default_factory=list)
    
    # Advertising and marketing
    advertising_campaigns: List[AdvertisingCampaign] = field(default_factory=list)
    ad_revenue_share: float = 0.70  # 70% to content creators/partners
    programmatic_advertising: bool = True
    targeted_advertising: bool = True
    ad_blocking_rate: float = 0.25  # 25% of users use ad blockers
    
    # Distribution and partnerships
    distribution_channels: List[DeliveryChannel] = field(default_factory=list)
    content_licensing_deals: Dict[str, Any] = field(default_factory=dict)
    platform_partnerships: List[str] = field(default_factory=list)
    syndication_revenue: float = 0.0
    
    # Regulatory and compliance
    content_rating_system: str = "internal"
    censorship_compliance: List[str] = field(default_factory=list)  # regional requirements
    data_privacy_regulations: List[str] = field(default_factory=list)
    content_takedown_requests: int = 0
    transparency_reports: bool = True
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "51"  # Information
    
    # Content creation and management
    def create_content(self, content: ContentAsset) -> str:
        """Create and publish new content"""
        self.content_library.append(content)
        
        # Record production investment
        self.post("content_assets", "cash", content.production_cost, 
                 f"Content production: {content.content_id}")
        self.content_production_budget += content.production_cost
        
        # Add to appropriate distribution channels
        if not content.distribution_channels:
            content.distribution_channels = self.distribution_channels[:2]  # default channels
        
        return content.content_id
    
    def acquire_content_library(self, library_size: int, acquisition_cost: float, 
                               content_type: ContentType) -> None:
        """Acquire existing content library"""
        self.content_acquisition_costs += acquisition_cost
        
        # Create content assets for acquired library
        for i in range(library_size):
            content = ContentAsset(
                content_id=f"acquired_{content_type.value}_{i}",
                title=f"Acquired {content_type.value} {i}",
                content_type=content_type,
                creation_date=date.today(),
                production_cost=acquisition_cost / library_size
            )
            self.content_library.append(content)
        
        self.post("content_library", "cash", acquisition_cost, 
                 f"Content acquisition: {content_type.value}")
    
    def moderate_content(self, content_id: str, moderation_action: str) -> bool:
        """Moderate content based on platform policies"""
        content = next((c for c in self.content_library if c.content_id == content_id), None)
        if not content:
            return False
        
        moderation_cost = 50.0  # cost per moderation action
        
        if moderation_action == "remove":
            self.content_library.remove(content)
            self.content_takedown_requests += 1
        elif moderation_action == "age_restrict":
            content.content_rating = "R"
        elif moderation_action == "demonetize":
            content.revenue_generated = 0.0
        
        self.post("content_moderation", "cash", moderation_cost, 
                 f"Moderation: {content_id}")
        
        return True
    
    # User and subscription management
    def acquire_subscriber(self, subscriber: Subscriber) -> str:
        """Acquire new subscriber"""
        self.subscribers.append(subscriber)
        self.active_users += 1
        
        # Record customer acquisition cost
        acquisition_cost = 15.0  # average CAC
        self.post("customer_acquisition", "cash", acquisition_cost, 
                 f"New subscriber: {subscriber.subscriber_id}")
        
        return subscriber.subscriber_id
    
    def process_subscription_billing(self) -> float:
        """Process monthly subscription billing"""
        total_subscription_revenue = 0.0
        
        for subscriber in self.subscribers:
            if subscriber.renewal_date <= date.today():
                # Charge subscription fee
                monthly_revenue = subscriber.monthly_fee
                total_subscription_revenue += monthly_revenue
                
                # Update renewal date
                subscriber.renewal_date = date.today() + timedelta(days=30)
        
        self.post("cash", "subscription_revenue", total_subscription_revenue, "Monthly subscriptions")
        self.income_statement["revenue"] += total_subscription_revenue
        
        return total_subscription_revenue
    
    def track_user_engagement(self, user_id: str, session_duration: float, 
                            content_consumed: List[str]) -> None:
        """Track user engagement metrics"""
        subscriber = next((s for s in self.subscribers if s.subscriber_id == user_id), None)
        
        if subscriber:
            subscriber.usage_hours += session_duration / 60.0
            subscriber.engagement_score = min(1.0, subscriber.engagement_score + 0.01)
        
        # Update content view counts
        for content_id in content_consumed:
            content = next((c for c in self.content_library if c.content_id == content_id), None)
            if content:
                content.views_count += 1
        
        # Update platform metrics
        self.content_consumption_hours += session_duration / 60.0
        self.session_duration_minutes = (self.session_duration_minutes * 0.95 + 
                                       session_duration * 0.05)
    
    # Advertising operations
    def sell_advertising_space(self, campaign: AdvertisingCampaign) -> str:
        """Sell advertising inventory"""
        self.advertising_campaigns.append(campaign)
        
        # Calculate ad revenue
        if campaign.campaign_type == "video":
            cpm = 15.0  # $15 per thousand impressions
        elif campaign.campaign_type == "display":
            cpm = 5.0   # $5 per thousand impressions
        else:
            cpm = 8.0   # default CPM
        
        estimated_impressions = campaign.budget / cpm * 1000
        campaign.impressions_delivered = int(estimated_impressions * 0.9)  # 90% delivery rate
        
        self.post("cash", "advertising_revenue", campaign.budget, 
                 f"Ad campaign: {campaign.campaign_id}")
        self.income_statement["revenue"] += campaign.budget
        
        return campaign.campaign_id
    
    def optimize_ad_targeting(self, campaign_id: str) -> float:
        """Optimize advertising targeting to improve performance"""
        campaign = next((c for c in self.advertising_campaigns if c.campaign_id == campaign_id), None)
        if not campaign:
            return 0.0
        
        # Use user data to improve targeting
        targeting_improvement = 0.15  # 15% CTR improvement
        campaign.click_through_rate += targeting_improvement
        
        # Generate additional revenue from improved performance
        performance_bonus = campaign.budget * 0.10  # 10% performance bonus
        
        self.post("cash", "advertising_performance_bonus", performance_bonus, 
                 f"Ad optimization: {campaign_id}")
        self.income_statement["revenue"] += performance_bonus
        
        return performance_bonus
    
    # Data monetization
    def collect_user_data(self, data_type: str, records_count: int) -> str:
        """Collect user data for analytics and monetization"""
        dataset = DataSet(
            dataset_id=f"data_{data_type}_{len(self.data_assets)}",
            data_type=data_type,
            records_count=records_count,
            collection_date=date.today(),
            privacy_compliance=["GDPR", "CCPA"]  # ensure compliance
        )
        
        self.data_assets.append(dataset)
        
        # Calculate data value
        value_per_record = 0.50  # $0.50 per user record
        dataset.monetization_value = records_count * value_per_record
        
        return dataset.dataset_id
    
    def monetize_data(self, dataset_id: str, buyer_id: str) -> float:
        """Monetize data through licensing or sale"""
        dataset = next((d for d in self.data_assets if d.dataset_id == dataset_id), None)
        if not dataset:
            return 0.0
        
        # Check privacy compliance
        if "GDPR" not in dataset.privacy_compliance:
            return 0.0  # Cannot monetize non-compliant data
        
        revenue = dataset.monetization_value
        self.data_monetization_revenue += revenue
        
        self.post("cash", "data_licensing_revenue", revenue, 
                 f"Data monetization: {dataset_id}")
        self.income_statement["revenue"] += revenue
        
        return revenue
    
    # Technology infrastructure
    def scale_infrastructure(self, capacity_increase: float, investment: float) -> None:
        """Scale technology infrastructure to handle growth"""
        # Add server capacity
        new_infrastructure = TechnologyInfrastructure(
            system_id=f"scale_{len(self.infrastructure)}",
            system_type="cloud_servers",
            capacity=capacity_increase,
            maintenance_cost_monthly=investment * 0.05  # 5% monthly maintenance
        )
        
        self.infrastructure.append(new_infrastructure)
        self.server_capacity += capacity_increase
        
        self.post("infrastructure_investment", "cash", investment, 
                 "Infrastructure scaling")
    
    def optimize_content_delivery(self) -> float:
        """Optimize content delivery network performance"""
        if not self.content_delivery_network:
            return 0.0
        
        # Calculate bandwidth savings from optimization
        bandwidth_savings = self.bandwidth_capacity * 0.15  # 15% efficiency gain
        cost_savings = bandwidth_savings * 0.10  # $0.10 per Mbps monthly
        
        # Improve user experience
        self.uptime_target = min(0.9999, self.uptime_target + 0.0001)
        
        return cost_savings
    
    def implement_ai_recommendations(self, implementation_cost: float) -> None:
        """Implement AI-powered content recommendation system"""
        self.analytics_capabilities.append("ai_recommendations")
        
        # Improve user engagement
        engagement_lift = 0.25  # 25% improvement in engagement
        for subscriber in self.subscribers:
            subscriber.engagement_score = min(1.0, subscriber.engagement_score * (1 + engagement_lift))
        
        self.post("ai_implementation", "cash", implementation_cost, "AI recommendations")
        self.income_statement["opex"] += implementation_cost
    
    # Content licensing and distribution
    def license_content_to_platform(self, content_id: str, licensee_id: str, 
                                  licensing_fee: float, duration_months: int) -> str:
        """License content to external platform"""
        content = next((c for c in self.content_library if c.content_id == content_id), None)
        if not content:
            return ""
        
        licensing_deal_id = f"license_{content_id}_{licensee_id}"
        
        # Add licensing rights
        content.licensing_rights.append(licensee_id)
        
        # Record licensing revenue
        self.syndication_revenue += licensing_fee
        self.post("cash", "licensing_revenue", licensing_fee, 
                 f"Content licensing: {licensing_deal_id}")
        self.income_statement["revenue"] += licensing_fee
        
        self.content_licensing_deals[licensing_deal_id] = {
            "content_id": content_id,
            "licensee": licensee_id,
            "fee": licensing_fee,
            "duration": duration_months,
            "start_date": date.today()
        }
        
        return licensing_deal_id
    
    def distribute_content_multi_platform(self, content_id: str, 
                                        platforms: List[str]) -> Dict[str, float]:
        """Distribute content across multiple platforms"""
        content = next((c for c in self.content_library if c.content_id == content_id), None)
        if not content:
            return {}
        
        distribution_revenue = {}
        
        for platform in platforms:
            # Calculate platform-specific revenue
            if platform == "streaming":
                revenue = content.views_count * 0.02  # $0.02 per view
            elif platform == "broadcast":
                revenue = 5000.0  # flat broadcast fee
            elif platform == "digital_download":
                revenue = content.views_count * 0.50  # $0.50 per download
            else:
                revenue = 1000.0  # default platform revenue
            
            distribution_revenue[platform] = revenue
            content.revenue_generated += revenue
        
        total_revenue = sum(distribution_revenue.values())
        self.post("cash", "distribution_revenue", total_revenue, 
                 f"Multi-platform distribution: {content_id}")
        self.income_statement["revenue"] += total_revenue
        
        return distribution_revenue
    
    # Analytics and reporting
    def generate_audience_analytics(self) -> Dict[str, Any]:
        """Generate comprehensive audience analytics"""
        if not self.subscribers:
            return {}
        
        total_subscribers = len(self.subscribers)
        average_engagement = sum(s.engagement_score for s in self.subscribers) / total_subscribers
        total_usage_hours = sum(s.usage_hours for s in self.subscribers)
        
        analytics = {
            "audience_metrics": {
                "total_subscribers": total_subscribers,
                "monthly_active_users": self.monthly_active_users,
                "daily_active_users": self.daily_active_users,
                "average_engagement_score": average_engagement
            },
            "content_metrics": {
                "total_content_library": len(self.content_library),
                "total_views": sum(c.views_count for c in self.content_library),
                "content_consumption_hours": self.content_consumption_hours,
                "average_session_duration": self.session_duration_minutes
            },
            "revenue_metrics": {
                "subscription_revenue": sum(s.monthly_fee for s in self.subscribers),
                "advertising_revenue": sum(c.budget for c in self.advertising_campaigns),
                "licensing_revenue": self.syndication_revenue,
                "data_monetization": self.data_monetization_revenue
            },
            "engagement_metrics": {
                "user_retention_day_1": self.user_retention_rate.get("day_1", 0.8),
                "user_retention_day_7": self.user_retention_rate.get("day_7", 0.6),
                "user_retention_day_30": self.user_retention_rate.get("day_30", 0.4),
                "content_completion_rate": 0.75  # would calculate from actual data
            }
        }
        
        return analytics
    
    def calculate_content_roi(self, content_id: str) -> float:
        """Calculate return on investment for specific content"""
        content = next((c for c in self.content_library if c.content_id == content_id), None)
        if not content or content.production_cost == 0:
            return 0.0
        
        roi = (content.revenue_generated - content.production_cost) / content.production_cost
        return roi
    
    def forecast_subscriber_growth(self, months_ahead: int) -> Dict[str, int]:
        """Forecast subscriber growth based on current trends"""
        current_subscribers = len(self.subscribers)
        
        # Simple growth model - would use more sophisticated forecasting in practice
        monthly_growth_rate = 0.05  # 5% monthly growth
        churn_rate = 0.03  # 3% monthly churn
        
        net_growth_rate = monthly_growth_rate - churn_rate
        
        forecast = {}
        for month in range(1, months_ahead + 1):
            projected_subscribers = int(current_subscribers * (1 + net_growth_rate) ** month)
            forecast[f"month_{month}"] = projected_subscribers
        
        return forecast 