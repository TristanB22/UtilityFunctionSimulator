# support_services_firm.py
# NAICS 55: Management of Companies and Enterprises
# NAICS 56: Administrative and Support and Waste Management and Remediation Services
# NAICS 81: Other Services (except Public Administration)
# NAICS 92: Public Administration

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class SupportServiceType(Enum):
    MANAGEMENT_COMPANY = "management_company"
    EMPLOYMENT_SERVICES = "employment_services"
    SECURITY_SERVICES = "security_services"
    CLEANING_SERVICES = "cleaning_services"
    WASTE_MANAGEMENT = "waste_management"
    REPAIR_MAINTENANCE = "repair_maintenance"
    PERSONAL_SERVICES = "personal_services"
    GOVERNMENT_AGENCY = "government_agency"

@dataclass
class ServiceContract:
    contract_id: str
    client_id: str
    service_type: str
    contract_value: float
    start_date: date
    end_date: date
    performance_metrics: Dict[str, float] = field(default_factory=dict)

@dataclass
class SupportServicesFirm(BaseFirm):
    # Core service operations
    service_type: SupportServiceType = SupportServiceType.EMPLOYMENT_SERVICES
    service_specializations: List[str] = field(default_factory=list)
    
    # Client contracts
    active_contracts: List[ServiceContract] = field(default_factory=list)
    recurring_revenue_base: float = 0.0
    contract_renewal_rate: float = 0.80
    
    # Workforce management (for labor-intensive services)
    temporary_workforce: int = 0
    placement_success_rate: float = 0.85  # for employment services
    
    # Operational metrics
    service_level_agreements: Dict[str, float] = field(default_factory=dict)
    customer_satisfaction_score: float = 4.2  # out of 5
    
    # Government/regulatory (for NAICS 92)
    public_budget_allocation: float = 0.0
    regulatory_authority: List[str] = field(default_factory=list)
    public_service_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Additional data models
    workforce_analytics: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        # Set NAICS code based on service type
        naics_mapping = {
            SupportServiceType.MANAGEMENT_COMPANY: "55",
            SupportServiceType.EMPLOYMENT_SERVICES: "56",
            SupportServiceType.SECURITY_SERVICES: "56",
            SupportServiceType.CLEANING_SERVICES: "56",
            SupportServiceType.WASTE_MANAGEMENT: "56",
            SupportServiceType.REPAIR_MAINTENANCE: "81",
            SupportServiceType.PERSONAL_SERVICES: "81",
            SupportServiceType.GOVERNMENT_AGENCY: "92"
        }
        if not self.naics:
            self.naics = naics_mapping.get(self.service_type, "56")
    
    def sign_service_contract(self, contract: ServiceContract) -> bool:
        """Sign new service contract with client"""
        self.active_contracts.append(contract)
        
        # For recurring services, add to revenue base
        if contract.service_type in ["cleaning", "security", "maintenance"]:
            monthly_value = contract.contract_value / 12
            self.recurring_revenue_base += monthly_value
        
        return True
    
    def deliver_service(self, contract_id: str, service_value: float) -> None:
        """Deliver service and recognize revenue"""
        contract = next((c for c in self.active_contracts if c.contract_id == contract_id), None)
        if contract:
            self.post("cash", "service_revenue", service_value, f"Service delivery: {contract_id}")
            self.income_statement["revenue"] += service_value
    
    def place_temporary_worker(self, client_id: str, worker_hourly_rate: float, 
                              hours_per_week: float) -> str:
        """Place temporary worker (for employment services)"""
        if self.service_type != SupportServiceType.EMPLOYMENT_SERVICES:
            return ""
        
        placement_id = f"placement_{client_id}_{self.temporary_workforce}"
        self.temporary_workforce += 1
        
        # Weekly revenue (markup on hourly rate)
        markup_rate = worker_hourly_rate * 1.25  # 25% markup
        weekly_revenue = (markup_rate - worker_hourly_rate) * hours_per_week
        
        self.post("cash", "placement_revenue", weekly_revenue, f"Worker placement: {placement_id}")
        self.income_statement["revenue"] += weekly_revenue
        
        return placement_id
    
    def allocate_public_budget(self, budget_amount: float, purpose: str) -> None:
        """Allocate public budget (for government agencies)"""
        if self.service_type != SupportServiceType.GOVERNMENT_AGENCY:
            return
        
        self.public_budget_allocation += budget_amount
        self.post("public_budget", "budget_authority", budget_amount, f"Budget allocation: {purpose}")
    
    def provide_regulatory_service(self, service_type: str, fee_collected: float) -> None:
        """Provide regulatory service and collect fees"""
        if self.service_type == SupportServiceType.GOVERNMENT_AGENCY:
            self.post("cash", "regulatory_fees", fee_collected, f"Regulatory service: {service_type}")
            self.income_statement["revenue"] += fee_collected
    
    def update_workforce_analytics(self, metric: str, value: Any) -> None:
        self.workforce_analytics[metric] = value
    
    def get_operational_summary(self) -> Dict[str, Any]:
        return {
            "active_contracts": len(self.active_contracts),
            "workforce_size": self.temporary_workforce,
            "customer_satisfaction": self.customer_satisfaction_score
        }

# Create specialized classes for each major support service type

@dataclass 
class ManagementCompany(SupportServicesFirm):
    """NAICS 55: Holding company or corporate headquarters"""
    
    # Subsidiary management
    subsidiaries: List[str] = field(default_factory=list)
    management_fees: Dict[str, float] = field(default_factory=dict)  # subsidiary -> fee rate
    shared_services_provided: List[str] = field(default_factory=list)  # HR, IT, Legal, etc.
    
    def __post_init__(self):
        super().__post_init__()
        self.service_type = SupportServiceType.MANAGEMENT_COMPANY
        self.naics = "55"
    
    def charge_management_fee(self, subsidiary_id: str, fee_amount: float) -> None:
        """Charge management fee to subsidiary"""
        self.post("cash", "management_fees", fee_amount, f"Management fee: {subsidiary_id}")
        self.income_statement["revenue"] += fee_amount

@dataclass
class GovernmentAgency(SupportServicesFirm):
    """NAICS 92: Public Administration"""
    
    # Government-specific attributes
    jurisdiction: str = "federal"  # federal, state, local
    regulatory_scope: List[str] = field(default_factory=list)
    public_programs: List[str] = field(default_factory=list)
    citizen_services: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        self.service_type = SupportServiceType.GOVERNMENT_AGENCY
        self.naics = "92"
    
    def issue_permit(self, permit_type: str, applicant_id: str, fee: float) -> str:
        """Issue permit and collect fee"""
        permit_id = f"{permit_type}_{applicant_id}_{len(self.ledger)}"
        self.post("cash", "permit_fees", fee, f"Permit issued: {permit_id}")
        self.income_statement["revenue"] += fee
        return permit_id
    
    def enforce_regulation(self, violation_type: str, entity_id: str, fine_amount: float) -> None:
        """Enforce regulation and collect fines"""
        self.post("cash", "fines_penalties", fine_amount, f"Violation: {violation_type}")
        self.income_statement["revenue"] += fine_amount

# --- ADDITIONAL DATA MODELS ---

# Remove ServiceAgreement and ComplianceRecord dataclasses and their usages.
# Expand SupportServicesFirm with sector-level attributes if needed.

# --- ADDITIONAL METHODS FOR SupportServicesFirm ---

class SupportServicesFirm(BaseFirm):
    # ... existing fields ...
    workforce_analytics: Dict[str, Any] = field(default_factory=dict)
    
    def update_workforce_analytics(self, metric: str, value: Any) -> None:
        self.workforce_analytics[metric] = value
    
    def get_operational_summary(self) -> Dict[str, Any]:
        return {
            "active_contracts": len(self.active_contracts),
            "workforce_size": self.temporary_workforce,
            "customer_satisfaction": self.customer_satisfaction_score
        }
    # ... existing code ... 