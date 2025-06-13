# __init__.py
# Firm module with comprehensive NAICS-based firm specializations

from .firm import BaseFirm, Money, Transaction, License
from .org_chart import (
    OrgChart, Role, RoleType, VotingRights, 
    PersonInOrg, Shareholder
)

# Import all specialized firm classes
from .agriculture_firm import AgriculturalFirm, CropType, LivestockType, ProductionMethod
from .mining_firm import MiningFirm, ExtractionType, ProjectPhase
from .utilities_firm import UtilitiesFirm, UtilityType, FuelType, RateStructure
from .construction_firm import ConstructionFirm, ConstructionType, ProjectPhase as ConstructionPhase
from .manufacturing_firm import ManufacturingFirm, ManufacturingType, ProductionStrategy
from .wholesale_firm import WholesaleFirm, WholesaleType
from .retail_firm import RetailFirm, RetailChannel
from .transportation_firm import TransportationFirm, TransportMode
from .information_firm import InformationFirm, InformationType
from .financial_firm import FinancialFirm, FinancialServiceType, RiskRating
from .professional_services_firm import ProfessionalServicesFirm, ServiceType, BillingModel
from .support_services_firm import SupportServicesFirm, ManagementCompany, GovernmentAgency, SupportServiceType
from .education_firm import EducationFirm, EducationType
from .healthcare_firm import HealthcareFirm, HealthcareType, InsuranceType
from .hospitality_firm import HospitalityFirm, HospitalityType

# NAICS classification mapping
NAICS_FIRM_MAPPING = {
    "11": AgriculturalFirm,      # Agriculture, Forestry, Fishing and Hunting
    "21": MiningFirm,            # Mining, Quarrying, and Oil and Gas Extraction
    "22": UtilitiesFirm,         # Utilities
    "23": ConstructionFirm,      # Construction
    "31": ManufacturingFirm,     # Manufacturing (31-33)
    "32": ManufacturingFirm,
    "33": ManufacturingFirm,
    "42": WholesaleFirm,         # Wholesale Trade
    "44": RetailFirm,            # Retail Trade (44-45)
    "45": RetailFirm,
    "48": TransportationFirm,    # Transportation and Warehousing (48-49)
    "49": TransportationFirm,
    "51": InformationFirm,       # Information
    "52": FinancialFirm,         # Finance and Insurance
    "53": FinancialFirm,         # Real Estate (can use financial firm as base)
    "54": ProfessionalServicesFirm,  # Professional, Scientific, and Technical Services
    "55": ManagementCompany,     # Management of Companies and Enterprises
    "56": SupportServicesFirm,   # Administrative and Support Services
    "61": EducationFirm,         # Educational Services
    "62": HealthcareFirm,        # Health Care and Social Assistance
    "71": HospitalityFirm,       # Arts, Entertainment, and Recreation
    "72": HospitalityFirm,       # Accommodation and Food Services
    "81": SupportServicesFirm,   # Other Services (except Public Administration)
    "92": GovernmentAgency,      # Public Administration
}

def create_firm_by_naics(naics_code: str, **kwargs) -> BaseFirm:
    """
    Factory function to create appropriate firm class based on NAICS code.
    
    Args:
        naics_code: 2-digit NAICS industry code
        **kwargs: Additional arguments to pass to firm constructor
    
    Returns:
        Specialized firm instance based on NAICS classification
    """
    # Extract 2-digit code from longer NAICS codes
    naics_2digit = naics_code[:2] if len(naics_code) >= 2 else naics_code
    
    firm_class = NAICS_FIRM_MAPPING.get(naics_2digit, BaseFirm)
    return firm_class(naics=naics_code, **kwargs)

def get_available_naics_codes() -> dict:
    """
    Get dictionary of available NAICS codes and their descriptions.
    
    Returns:
        Dictionary mapping NAICS codes to industry descriptions
    """
    return {
        "11": "Agriculture, Forestry, Fishing and Hunting",
        "21": "Mining, Quarrying, and Oil and Gas Extraction", 
        "22": "Utilities",
        "23": "Construction",
        "31-33": "Manufacturing",
        "42": "Wholesale Trade",
        "44-45": "Retail Trade", 
        "48-49": "Transportation and Warehousing",
        "51": "Information",
        "52": "Finance and Insurance",
        "53": "Real Estate and Rental and Leasing",
        "54": "Professional, Scientific, and Technical Services",
        "55": "Management of Companies and Enterprises",
        "56": "Administrative and Support and Waste Management Services",
        "61": "Educational Services",
        "62": "Health Care and Social Assistance",
        "71": "Arts, Entertainment, and Recreation",
        "72": "Accommodation and Food Services",
        "81": "Other Services (except Public Administration)",
        "92": "Public Administration"
    }

# Export all classes and utilities
__all__ = [
    # Base classes
    'BaseFirm', 'Money', 'Transaction', 'License',
    'OrgChart', 'Role', 'RoleType', 'VotingRights', 'PersonInOrg', 'Shareholder',
    
    # Specialized firm classes
    'AgriculturalFirm', 'MiningFirm', 'UtilitiesFirm', 'ConstructionFirm',
    'ManufacturingFirm', 'WholesaleFirm', 'RetailFirm', 'TransportationFirm',
    'InformationFirm', 'FinancialFirm', 'ProfessionalServicesFirm',
    'SupportServicesFirm', 'ManagementCompany', 'GovernmentAgency',
    'EducationFirm', 'HealthcareFirm', 'HospitalityFirm',
    
    # Utility functions
    'create_firm_by_naics', 'get_available_naics_codes', 'NAICS_FIRM_MAPPING'
] 