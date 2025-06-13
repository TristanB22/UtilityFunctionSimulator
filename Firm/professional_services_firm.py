# professional_services_firm.py
# NAICS 54: Professional, Scientific, and Technical Services

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class ServiceType(Enum):
    LEGAL = "legal"
    ACCOUNTING = "accounting"
    ENGINEERING = "engineering"
    ARCHITECTURE = "architecture"
    CONSULTING = "consulting"
    ADVERTISING = "advertising"
    RESEARCH_DEVELOPMENT = "research_development"
    SPECIALIZED_DESIGN = "specialized_design"
    ACTUARIAL = "actuarial"
    ENVIRONMENTAL = "environmental"
    MARKETING = "marketing"
    IT_CONSULTING = "it_consulting"

class BillingModel(Enum):
    HOURLY = "hourly"
    FIXED_FEE = "fixed_fee"
    RETAINER = "retainer"
    CONTINGENCY = "contingency"
    VALUE_BASED = "value_based"
    SUCCESS_FEE = "success_fee"
    BLENDED_RATE = "blended_rate"

class PracticeArea(Enum):
    STRATEGY = "strategy"
    OPERATIONS = "operations"
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HUMAN_RESOURCES = "human_resources"
    MERGERS_ACQUISITIONS = "mergers_acquisitions"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    DIGITAL_TRANSFORMATION = "digital_transformation"

class ConsultantLevel(Enum):
    ANALYST = "analyst"
    ASSOCIATE = "associate"
    SENIOR_ASSOCIATE = "senior_associate"
    MANAGER = "manager"
    SENIOR_MANAGER = "senior_manager"
    DIRECTOR = "director"
    PARTNER = "partner"

class ProjectStatus(Enum):
    PROPOSAL = "proposal"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Consultant:
    consultant_id: str
    name: str
    level: ConsultantLevel
    practice_area: PracticeArea
    billing_rate: float
    target_utilization: float = 0.75  # 75% billable target
    actual_utilization: float = 0.70
    years_experience: int = 5
    certifications: List[str] = field(default_factory=list)
    client_ratings: List[float] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)

@dataclass
class Client:
    client_id: str
    company_name: str
    industry: str
    annual_revenue: float
    relationship_manager: str
    client_since: date
    lifetime_value: float = 0.0
    satisfaction_score: float = 4.0  # out of 5
    credit_rating: str = "A"
    payment_terms: int = 30  # days

@dataclass
class ClientEngagement:
    engagement_id: str
    client_id: str
    service_type: ServiceType
    practice_area: PracticeArea
    billing_model: BillingModel
    contract_value: float
    hours_budgeted: float
    hours_worked: float = 0.0
    billing_rate: float = 150.0  # $ per hour
    start_date: date = None
    end_date: date = None
    status: ProjectStatus = ProjectStatus.PROPOSAL
    team_members: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    client_satisfaction: float = 4.0

@dataclass
class Proposal:
    proposal_id: str
    client_id: str
    service_type: ServiceType
    proposed_value: float
    estimated_hours: float
    win_probability: float = 0.50
    submission_date: date = None
    decision_date: Optional[date] = None
    proposal_team: List[str] = field(default_factory=list)
    competitive_situation: str = "medium"

@dataclass
class KnowledgeAsset:
    asset_id: str
    title: str
    asset_type: str  # methodology, template, case_study, best_practice
    practice_area: PracticeArea
    creation_date: date
    last_updated: date
    usage_count: int = 0
    quality_rating: float = 4.0
    access_level: str = "internal"  # internal, client, public

@dataclass
class Partnership:
    partner_id: str
    partner_name: str
    partnership_type: str  # technology, referral, subcontracting
    revenue_share: float = 0.20  # 20% revenue share
    signed_date: date
    annual_value: float = 0.0

@dataclass
class ProfessionalServicesFirm(BaseFirm):
    # Service offerings and expertise
    service_types: List[ServiceType] = field(default_factory=list)
    practice_areas: List[PracticeArea] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)
    industry_expertise: List[str] = field(default_factory=list)
    
    # Human capital and talent
    consultants: List[Consultant] = field(default_factory=list)
    utilization_targets: Dict[ConsultantLevel, float] = field(default_factory=dict)
    billing_rates: Dict[ConsultantLevel, float] = field(default_factory=dict)
    consultant_training_budget: float = 0.0
    talent_acquisition_cost: float = 50000.0  # per senior hire
    
    # Client portfolio and relationships
    clients: List[Client] = field(default_factory=list)
    active_engagements: List[ClientEngagement] = field(default_factory=list)
    proposals: List[Proposal] = field(default_factory=list)
    repeat_client_rate: float = 0.70  # 70% repeat business
    client_concentration_risk: float = 0.20  # 20% from largest client
    
    # Financial metrics
    billable_utilization_rate: float = 0.75  # 75% of time billable
    average_billing_rate: float = 175.0  # $ per hour
    realization_rate: float = 0.90  # 90% of billed hours collected
    collection_period_days: int = 45
    profit_margin_target: float = 0.25  # 25% profit margin
    
    # Business development
    pipeline_value: float = 0.0  # total value of proposals
    win_rate: float = 0.35  # 35% proposal win rate
    proposal_costs: float = 0.0  # cost of preparing proposals
    marketing_budget: float = 0.0
    thought_leadership_investments: float = 0.0
    
    # Knowledge management and IP
    knowledge_assets: List[KnowledgeAsset] = field(default_factory=list)
    proprietary_methodologies: List[str] = field(default_factory=list)
    intellectual_property_value: float = 0.0
    research_investments: float = 0.0  # annual R&D spending
    knowledge_sharing_sessions: int = 0
    
    # Quality and delivery
    quality_standards: List[str] = field(default_factory=list)
    client_satisfaction_score: float = 4.2  # out of 5
    project_success_rate: float = 0.85  # 85% successful projects
    on_time_delivery_rate: float = 0.80  # 80% on-time delivery
    budget_adherence_rate: float = 0.75  # 75% within budget
    
    # Partnerships and alliances
    partnerships: List[Partnership] = field(default_factory=list)
    subcontractor_network: List[str] = field(default_factory=list)
    technology_partnerships: List[str] = field(default_factory=list)
    referral_revenue: float = 0.0
    
    # Market position
    market_reputation: float = 0.75  # 0-1 scale
    thought_leadership_ranking: int = 50  # industry ranking
    awards_recognitions: List[str] = field(default_factory=list)
    competitive_positioning: str = "premium"  # premium, middle_market, boutique
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "54"  # Professional Services
        
        # Initialize default billing rates by level
        if not self.billing_rates:
            self.billing_rates = {
                ConsultantLevel.ANALYST: 125.0,
                ConsultantLevel.ASSOCIATE: 175.0,
                ConsultantLevel.SENIOR_ASSOCIATE: 225.0,
                ConsultantLevel.MANAGER: 300.0,
                ConsultantLevel.SENIOR_MANAGER: 400.0,
                ConsultantLevel.DIRECTOR: 500.0,
                ConsultantLevel.PARTNER: 750.0
            }
        
        # Initialize utilization targets
        if not self.utilization_targets:
            self.utilization_targets = {
                ConsultantLevel.ANALYST: 0.85,
                ConsultantLevel.ASSOCIATE: 0.80,
                ConsultantLevel.SENIOR_ASSOCIATE: 0.75,
                ConsultantLevel.MANAGER: 0.65,
                ConsultantLevel.SENIOR_MANAGER: 0.55,
                ConsultantLevel.DIRECTOR: 0.45,
                ConsultantLevel.PARTNER: 0.30
            }
    
    # Human capital management
    def hire_consultant(self, consultant: Consultant) -> str:
        """Hire new consultant"""
        self.consultants.append(consultant)
        
        # Set billing rate based on level
        consultant.billing_rate = self.billing_rates.get(consultant.level, 200.0)
        consultant.target_utilization = self.utilization_targets.get(consultant.level, 0.75)
        
        # Record hiring costs
        if consultant.level in [ConsultantLevel.DIRECTOR, ConsultantLevel.PARTNER]:
            hiring_cost = self.talent_acquisition_cost * 2  # senior hires cost more
        else:
            hiring_cost = self.talent_acquisition_cost
        
        self.post("talent_acquisition", "cash", hiring_cost, f"Hire: {consultant.consultant_id}")
        self.income_statement["opex"] += hiring_cost
        
        return consultant.consultant_id
    
    def promote_consultant(self, consultant_id: str, new_level: ConsultantLevel) -> bool:
        """Promote consultant to new level"""
        consultant = next((c for c in self.consultants if c.consultant_id == consultant_id), None)
        if not consultant:
            return False
        
        old_level = consultant.level
        consultant.level = new_level
        consultant.billing_rate = self.billing_rates.get(new_level, consultant.billing_rate * 1.2)
        consultant.target_utilization = self.utilization_targets.get(new_level, 0.75)
        
        # Record promotion costs (training, adjustment period)
        promotion_cost = 25000.0
        self.post("promotion_costs", "cash", promotion_cost, f"Promotion: {consultant_id}")
        
        return True
    
    def provide_consultant_training(self, consultant_id: str, training_type: str, cost: float) -> bool:
        """Provide training to consultant"""
        consultant = next((c for c in self.consultants if c.consultant_id == consultant_id), None)
        if not consultant:
            return False
        
        # Add certification if applicable
        if training_type == "certification":
            certification_name = f"cert_{training_type}_{len(consultant.certifications)}"
            consultant.certifications.append(certification_name)
        
        self.consultant_training_budget += cost
        self.post("training_investment", "cash", cost, f"Training: {consultant_id}")
        
        # Improve billing rate slightly
        consultant.billing_rate *= 1.05  # 5% increase
        
        return True
    
    def track_consultant_utilization(self, consultant_id: str, billable_hours: float, 
                                   period_days: int = 30) -> float:
        """Track and update consultant utilization"""
        consultant = next((c for c in self.consultants if c.consultant_id == consultant_id), None)
        if not consultant:
            return 0.0
        
        # Calculate utilization (assuming 8 hours per day available)
        available_hours = period_days * 8
        consultant.actual_utilization = billable_hours / available_hours
        
        # Update firm-wide utilization
        total_consultants = len(self.consultants)
        if total_consultants > 0:
            avg_utilization = sum(c.actual_utilization for c in self.consultants) / total_consultants
            self.billable_utilization_rate = avg_utilization
        
        return consultant.actual_utilization
    
    # Client relationship management
    def onboard_client(self, client: Client) -> str:
        """Onboard new client"""
        self.clients.append(client)
        
        # Record client onboarding costs
        onboarding_cost = 5000.0  # due diligence, setup, relationship building
        self.post("client_onboarding", "cash", onboarding_cost, f"Client: {client.client_id}")
        
        return client.client_id
    
    def create_proposal(self, proposal: Proposal) -> str:
        """Create proposal for potential engagement"""
        self.proposals.append(proposal)
        
        # Calculate proposal preparation costs
        team_size = len(proposal.proposal_team)
        proposal_cost = team_size * 20 * 200  # 20 hours per team member at $200/hour
        
        self.proposal_costs += proposal_cost
        self.pipeline_value += proposal.proposed_value
        
        self.post("proposal_costs", "cash", proposal_cost, f"Proposal: {proposal.proposal_id}")
        self.income_statement["opex"] += proposal_cost
        
        return proposal.proposal_id
    
    def win_proposal(self, proposal_id: str) -> str:
        """Convert won proposal to active engagement"""
        proposal = next((p for p in self.proposals if p.proposal_id == proposal_id), None)
        if not proposal:
            return ""
        
        # Create engagement from proposal
        engagement = ClientEngagement(
            engagement_id=f"eng_{proposal.client_id}_{len(self.active_engagements)}",
            client_id=proposal.client_id,
            service_type=proposal.service_type,
            practice_area=PracticeArea.STRATEGY,  # would be determined from proposal
            billing_model=BillingModel.HOURLY,
            contract_value=proposal.proposed_value,
            hours_budgeted=proposal.estimated_hours,
            start_date=date.today(),
            status=ProjectStatus.ACTIVE,
            team_members=proposal.proposal_team.copy()
        )
        
        self.active_engagements.append(engagement)
        
        # Update win rate
        total_proposals = len(self.proposals)
        won_proposals = len([p for p in self.proposals if p.decision_date is not None])
        if total_proposals > 0:
            self.win_rate = won_proposals / total_proposals
        
        # Remove from pipeline
        self.pipeline_value -= proposal.proposed_value
        
        return engagement.engagement_id
    
    def start_client_engagement(self, client_id: str, service_type: ServiceType, 
                               billing_model: BillingModel, contract_value: float,
                               estimated_hours: float, practice_area: PracticeArea) -> str:
        """Start new client engagement"""
        engagement = ClientEngagement(
            engagement_id=f"eng_{client_id}_{len(self.active_engagements)}",
            client_id=client_id,
            service_type=service_type,
            practice_area=practice_area,
            billing_model=billing_model,
            contract_value=contract_value,
            hours_budgeted=estimated_hours,
            billing_rate=self.average_billing_rate,
            start_date=date.today(),
            status=ProjectStatus.ACTIVE
        )
        
        self.active_engagements.append(engagement)
        return engagement.engagement_id
    
    # Project delivery and billing
    def assign_team_to_engagement(self, engagement_id: str, team_members: List[str]) -> bool:
        """Assign consultant team to engagement"""
        engagement = next((e for e in self.active_engagements if e.engagement_id == engagement_id), None)
        if not engagement:
            return False
        
        engagement.team_members = team_members
        
        # Calculate blended billing rate for team
        total_rate = 0.0
        for consultant_id in team_members:
            consultant = next((c for c in self.consultants if c.consultant_id == consultant_id), None)
            if consultant:
                total_rate += consultant.billing_rate
        
        if team_members:
            engagement.billing_rate = total_rate / len(team_members)
        
        return True
    
    def bill_client_hours(self, engagement_id: str, consultant_id: str, hours_worked: float, 
                         work_description: str) -> float:
        """Bill client for hours worked"""
        engagement = next((e for e in self.active_engagements if e.engagement_id == engagement_id), None)
        consultant = next((c for c in self.consultants if c.consultant_id == consultant_id), None)
        
        if not engagement or not consultant:
            return 0.0
        
        engagement.hours_worked += hours_worked
        
        # Use consultant's specific billing rate
        billing_amount = hours_worked * consultant.billing_rate
        
        if engagement.billing_model == BillingModel.HOURLY:
            self.post("accounts_receivable", "professional_fees", billing_amount, 
                     f"Hours billed: {engagement_id}")
            self.income_statement["revenue"] += billing_amount
        elif engagement.billing_model == BillingModel.RETAINER:
            # Retainer billing - recognize revenue over time
            monthly_retainer = engagement.contract_value / 12
            self.post("cash", "retainer_revenue", monthly_retainer, f"Retainer: {engagement_id}")
            self.income_statement["revenue"] += monthly_retainer
            billing_amount = monthly_retainer
        
        # Track consultant utilization
        self.track_consultant_utilization(consultant_id, hours_worked, 30)
        
        return billing_amount
    
    def deliver_engagement_milestone(self, engagement_id: str, deliverable: str, 
                                   milestone_value: float) -> bool:
        """Deliver engagement milestone"""
        engagement = next((e for e in self.active_engagements if e.engagement_id == engagement_id), None)
        if not engagement:
            return False
        
        engagement.deliverables.append(deliverable)
        
        # For value-based or success fee billing
        if engagement.billing_model in [BillingModel.VALUE_BASED, BillingModel.SUCCESS_FEE]:
            self.post("accounts_receivable", "success_fees", milestone_value,
                     f"Milestone: {engagement_id}")
            self.income_statement["revenue"] += milestone_value
        
        return True
    
    def complete_engagement(self, engagement_id: str, client_satisfaction: float) -> bool:
        """Complete client engagement"""
        engagement = next((e for e in self.active_engagements if e.engagement_id == engagement_id), None)
        if not engagement:
            return False
        
        engagement.end_date = date.today()
        engagement.status = ProjectStatus.COMPLETED
        engagement.client_satisfaction = client_satisfaction
        
        # Update client satisfaction and lifetime value
        client = next((c for c in self.clients if c.client_id == engagement.client_id), None)
        if client:
            client.lifetime_value += engagement.contract_value
            client.satisfaction_score = (client.satisfaction_score + client_satisfaction) / 2
        
        # For fixed-fee projects, recognize remaining revenue
        if engagement.billing_model == BillingModel.FIXED_FEE:
            hours_billed = engagement.hours_worked * engagement.billing_rate
            remaining_revenue = engagement.contract_value - hours_billed
            if remaining_revenue > 0:
                self.post("accounts_receivable", "professional_fees", remaining_revenue,
                         f"Fixed fee completion: {engagement_id}")
                self.income_statement["revenue"] += remaining_revenue
        
        # Update success metrics
        if client_satisfaction >= 4.0:
            successful_projects = len([e for e in self.active_engagements 
                                     if e.status == ProjectStatus.COMPLETED and e.client_satisfaction >= 4.0])
            total_completed = len([e for e in self.active_engagements if e.status == ProjectStatus.COMPLETED])
            if total_completed > 0:
                self.project_success_rate = successful_projects / total_completed
        
        # Remove from active engagements
        self.active_engagements = [e for e in self.active_engagements if e.engagement_id != engagement_id]
        return True
    
    # Knowledge management
    def create_knowledge_asset(self, asset: KnowledgeAsset) -> str:
        """Create new knowledge asset"""
        self.knowledge_assets.append(asset)
        
        # Record knowledge creation costs
        creation_cost = 5000.0  # time investment in creating asset
        self.post("knowledge_investment", "cash", creation_cost, f"Knowledge: {asset.asset_id}")
        self.intellectual_property_value += creation_cost
        
        return asset.asset_id
    
    def leverage_knowledge_asset(self, asset_id: str, engagement_id: str) -> float:
        """Leverage existing knowledge asset in engagement"""
        asset = next((a for a in self.knowledge_assets if a.asset_id == asset_id), None)
        if not asset:
            return 0.0
        
        asset.usage_count += 1
        
        # Calculate efficiency gains from reusing knowledge
        efficiency_gain = 0.15  # 15% time savings
        engagement = next((e for e in self.active_engagements if e.engagement_id == engagement_id), None)
        
        if engagement:
            time_savings = engagement.hours_budgeted * efficiency_gain
            cost_savings = time_savings * engagement.billing_rate
            
            # Improve project margins
            return cost_savings
        
        return 0.0
    
    def conduct_knowledge_sharing_session(self, topic: str, participants: List[str], 
                                        cost: float) -> None:
        """Conduct knowledge sharing session"""
        self.knowledge_sharing_sessions += 1
        
        # Improve consultant capabilities
        for consultant_id in participants:
            consultant = next((c for c in self.consultants if c.consultant_id == consultant_id), None)
            if consultant:
                # Add specialization if not already present
                if topic not in consultant.specializations:
                    consultant.specializations.append(topic)
        
        self.post("knowledge_sharing", "cash", cost, f"Knowledge session: {topic}")
        self.income_statement["opex"] += cost
    
    # Business development and marketing
    def invest_in_thought_leadership(self, investment: float, topic: str) -> None:
        """Invest in thought leadership content"""
        self.thought_leadership_investments += investment
        
        # Improve market reputation
        self.market_reputation = min(1.0, self.market_reputation + 0.02)
        
        # Add to IP value
        self.intellectual_property_value += investment * 0.5
        
        self.post("thought_leadership", "cash", investment, f"Thought leadership: {topic}")
        self.income_statement["opex"] += investment
    
    def develop_partnership(self, partnership: Partnership) -> str:
        """Develop strategic partnership"""
        self.partnerships.append(partnership)
        
        # Record partnership development costs
        development_cost = 25000.0
        self.post("partnership_development", "cash", development_cost, 
                 f"Partnership: {partnership.partner_id}")
        
        return partnership.partner_id
    
    def generate_referral_revenue(self, partner_id: str, referred_value: float) -> float:
        """Generate revenue from partner referral"""
        partnership = next((p for p in self.partnerships if p.partner_id == partner_id), None)
        if not partnership:
            return 0.0
        
        referral_fee = referred_value * partnership.revenue_share
        self.referral_revenue += referral_fee
        partnership.annual_value += referral_fee
        
        self.post("cash", "referral_revenue", referral_fee, f"Referral from: {partner_id}")
        self.income_statement["revenue"] += referral_fee
        
        return referral_fee
    
    def conduct_market_research(self, research_topic: str, budget: float) -> Dict[str, Any]:
        """Conduct market research to inform strategy"""
        self.research_investments += budget
        
        # Simulate research insights
        research_results = {
            "market_size": "growing",
            "competitive_landscape": "fragmented",
            "client_needs": ["digital_transformation", "cost_reduction", "innovation"],
            "pricing_trends": "increasing",
            "service_gaps": ["ai_strategy", "sustainability_consulting"]
        }
        
        self.post("market_research", "cash", budget, f"Research: {research_topic}")
        self.income_statement["opex"] += budget
        
        return research_results
    
    # Quality assurance and client satisfaction
    def implement_quality_standard(self, standard_name: str, implementation_cost: float) -> None:
        """Implement quality standard across firm"""
        self.quality_standards.append(standard_name)
        
        # Improve delivery metrics
        self.on_time_delivery_rate = min(1.0, self.on_time_delivery_rate + 0.05)
        self.budget_adherence_rate = min(1.0, self.budget_adherence_rate + 0.05)
        
        self.post("quality_implementation", "cash", implementation_cost, 
                 f"Quality standard: {standard_name}")
        self.income_statement["opex"] += implementation_cost
    
    def conduct_client_satisfaction_survey(self) -> Dict[str, float]:
        """Conduct client satisfaction survey"""
        if not self.clients:
            return {}
        
        # Calculate satisfaction metrics
        avg_satisfaction = sum(c.satisfaction_score for c in self.clients) / len(self.clients)
        self.client_satisfaction_score = avg_satisfaction
        
        survey_results = {
            "overall_satisfaction": avg_satisfaction,
            "service_quality": avg_satisfaction + 0.1,
            "responsiveness": avg_satisfaction - 0.1,
            "value_for_money": avg_satisfaction - 0.2,
            "likelihood_to_recommend": avg_satisfaction + 0.2
        }
        
        return survey_results
    
    def handle_client_complaint(self, client_id: str, complaint_type: str, 
                              resolution_cost: float) -> bool:
        """Handle client complaint and service recovery"""
        client = next((c for c in self.clients if c.client_id == client_id), None)
        if not client:
            return False
        
        # Impact on client satisfaction
        if complaint_type == "serious":
            client.satisfaction_score = max(1.0, client.satisfaction_score - 0.5)
        else:
            client.satisfaction_score = max(1.0, client.satisfaction_score - 0.2)
        
        # Record resolution costs
        self.post("client_service_recovery", "cash", resolution_cost, f"Complaint: {client_id}")
        self.income_statement["opex"] += resolution_cost
        
        return True
    
    # Analytics and performance metrics
    def calculate_utilization_metrics(self) -> Dict[str, float]:
        """Calculate key utilization metrics"""
        if not self.consultants:
            return {"utilization_rate": 0.0, "avg_billing_rate": 0.0}
        
        # Calculate weighted averages
        total_utilization = sum(c.actual_utilization for c in self.consultants)
        avg_utilization = total_utilization / len(self.consultants)
        
        total_rate = sum(c.billing_rate for c in self.consultants)
        avg_rate = total_rate / len(self.consultants)
        
        # Calculate total billable hours
        total_billable_hours = sum(e.hours_worked for e in self.active_engagements)
        
        return {
            "utilization_rate": avg_utilization,
            "avg_billing_rate": avg_rate,
            "total_billable_hours": total_billable_hours,
            "target_vs_actual_utilization": avg_utilization / self.billable_utilization_rate
        }
    
    def calculate_financial_metrics(self) -> Dict[str, float]:
        """Calculate key financial performance metrics"""
        total_revenue = self.income_statement.get("revenue", 0)
        total_expenses = self.income_statement.get("opex", 0)
        
        # Revenue per consultant
        revenue_per_consultant = total_revenue / max(len(self.consultants), 1)
        
        # Realization and collection metrics
        total_billed = sum(e.hours_worked * e.billing_rate for e in self.active_engagements)
        actual_realization = total_revenue / max(total_billed, 1)
        
        financial_metrics = {
            "total_revenue": total_revenue,
            "revenue_per_consultant": revenue_per_consultant,
            "realization_rate": actual_realization,
            "profit_margin": (total_revenue - total_expenses) / max(total_revenue, 1),
            "pipeline_to_revenue_ratio": self.pipeline_value / max(total_revenue, 1),
            "repeat_client_revenue": total_revenue * self.repeat_client_rate
        }
        
        return financial_metrics
    
    def generate_practice_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive practice performance report"""
        practice_metrics = {}
        
        for practice in self.practice_areas:
            practice_engagements = [e for e in self.active_engagements if e.practice_area == practice]
            practice_consultants = [c for c in self.consultants if c.practice_area == practice]
            
            if practice_engagements or practice_consultants:
                practice_revenue = sum(e.contract_value for e in practice_engagements)
                practice_utilization = sum(c.actual_utilization for c in practice_consultants) / max(len(practice_consultants), 1)
                
                practice_metrics[practice.value] = {
                    "revenue": practice_revenue,
                    "consultant_count": len(practice_consultants),
                    "active_engagements": len(practice_engagements),
                    "utilization_rate": practice_utilization,
                    "avg_engagement_value": practice_revenue / max(len(practice_engagements), 1)
                }
        
        return practice_metrics
    
    def invest_in_capability(self, capability_name: str, investment_amount: float) -> None:
        """Invest in new capabilities or methodologies"""
        self.proprietary_methodologies.append(capability_name)
        self.research_investments += investment_amount
        self.intellectual_property_value += investment_amount
        
        self.post("capability_development", "cash", investment_amount, 
                 f"Investment in {capability_name}")
        self.income_statement["opex"] += investment_amount 