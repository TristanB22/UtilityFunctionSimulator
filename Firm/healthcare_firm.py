# healthcare_firm.py
# NAICS 62: Health Care and Social Assistance

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class HealthcareType(Enum):
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    PHYSICIAN_PRACTICE = "physician_practice"
    NURSING_HOME = "nursing_home"
    HOME_HEALTH = "home_health"
    URGENT_CARE = "urgent_care"
    AMBULATORY_SURGERY = "ambulatory_surgery"
    MENTAL_HEALTH = "mental_health"
    DENTAL_PRACTICE = "dental_practice"
    PHARMACY = "pharmacy"

class InsuranceType(Enum):
    PRIVATE = "private"
    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    UNINSURED = "uninsured"
    WORKERS_COMP = "workers_comp"
    TRICARE = "tricare"

class ServiceLine(Enum):
    EMERGENCY = "emergency"
    SURGERY = "surgery"
    CARDIOLOGY = "cardiology"
    ONCOLOGY = "oncology"
    OBSTETRICS = "obstetrics"
    PEDIATRICS = "pediatrics"
    ORTHOPEDICS = "orthopedics"
    RADIOLOGY = "radiology"
    LABORATORY = "laboratory"
    PHARMACY = "pharmacy"
    PRIMARY_CARE = "primary_care"
    MENTAL_HEALTH = "mental_health"

class PatientStatus(Enum):
    INPATIENT = "inpatient"
    OUTPATIENT = "outpatient"
    EMERGENCY = "emergency"
    DISCHARGED = "discharged"
    TRANSFERRED = "transferred"
    DECEASED = "deceased"

@dataclass
class Patient:
    patient_id: str
    admission_date: datetime
    status: PatientStatus
    insurance_type: InsuranceType
    primary_diagnosis: str
    attending_physician: str
    estimated_length_stay: int = 3  # days
    total_charges: float = 0.0
    insurance_payment: float = 0.0
    patient_payment: float = 0.0
    discharge_date: Optional[datetime] = None

@dataclass
class MedicalStaff:
    staff_id: str
    name: str
    role: str  # physician, nurse, technician, therapist
    department: str
    specialty: str
    salary: float
    licensed: bool = True
    board_certified: bool = False
    years_experience: int = 0
    patients_per_day: int = 10

@dataclass
class MedicalEquipment:
    equipment_id: str
    equipment_type: str
    purchase_cost: float
    annual_maintenance_cost: float
    depreciation_years: int = 10
    utilization_rate: float = 0.75  # 75% utilization
    revenue_per_use: float = 500.0

@dataclass
class Insurance:
    insurance_id: str
    payer_name: str
    contract_terms: Dict[str, float]  # procedure codes and reimbursement rates
    authorization_required: bool = False
    prior_auth_procedures: List[str] = field(default_factory=list)

@dataclass
class ClinicalOutcome:
    outcome_id: str
    patient_id: str
    procedure_type: str
    success_rate: float
    complication_rate: float
    readmission_rate: float
    patient_satisfaction: float

@dataclass
class HealthcareFirm(BaseFirm):
    # Facility characteristics
    healthcare_type: HealthcareType = HealthcareType.HOSPITAL
    bed_capacity: int = 100
    licensed_beds: int = 100
    available_beds: int = 100
    occupancy_rate: float = 0.75
    
    # Service lines and specialties
    service_lines: List[ServiceLine] = field(default_factory=list)
    departments: List[str] = field(default_factory=list)
    specialties_offered: List[str] = field(default_factory=list)
    emergency_services: bool = True
    trauma_level: str = "Level II"  # Level I, II, III, IV
    
    # Patient management
    current_patients: List[Patient] = field(default_factory=list)
    total_admissions: int = 0
    total_discharges: int = 0
    average_length_stay: float = 4.5  # days
    readmission_rate: float = 0.12  # 12%
    
    # Staffing and personnel
    medical_staff: List[MedicalStaff] = field(default_factory=list)
    physician_count: int = 0
    nurse_count: int = 0
    nurse_patient_ratio: float = 6.0  # patients per nurse
    staff_turnover_rate: float = 0.15
    
    # Financial and billing
    gross_patient_revenue: float = 0.0
    net_patient_revenue: float = 0.0
    bad_debt_rate: float = 0.05  # 5% bad debt
    days_in_accounts_receivable: int = 45
    case_mix_index: float = 1.2  # complexity of cases
    
    # Insurance and payers
    insurance_contracts: List[Insurance] = field(default_factory=list)
    payer_mix: Dict[InsuranceType, float] = field(default_factory=dict)
    average_reimbursement_rate: float = 0.85  # 85% of charges
    
    # Medical equipment and technology
    medical_equipment: List[MedicalEquipment] = field(default_factory=list)
    equipment_utilization: float = 0.75
    technology_budget: float = 0.0
    imaging_equipment: List[str] = field(default_factory=list)
    
    # Quality and outcomes
    clinical_outcomes: List[ClinicalOutcome] = field(default_factory=list)
    patient_satisfaction_score: float = 4.2  # out of 5
    mortality_rate: float = 0.02  # 2%
    infection_rate: float = 0.01  # 1%
    
    # Regulatory compliance
    accreditation_status: List[str] = field(default_factory=list)
    regulatory_compliance_score: float = 0.95
    cms_star_rating: int = 4  # CMS 5-star rating
    quality_improvement_programs: List[str] = field(default_factory=list)
    
    # Emergency preparedness
    emergency_capacity: int = 20  # additional surge capacity
    disaster_preparedness_plan: bool = True
    infection_control_protocols: bool = True
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "62"  # Health Care and Social Assistance
        
        # Initialize default payer mix
        if not self.payer_mix:
            self.payer_mix = {
                InsuranceType.PRIVATE: 0.45,
                InsuranceType.MEDICARE: 0.35,
                InsuranceType.MEDICAID: 0.15,
                InsuranceType.UNINSURED: 0.05
            }
    
    # Patient management
    def admit_patient(self, patient: Patient) -> bool:
        """Admit new patient"""
        if len(self.current_patients) >= self.bed_capacity:
            return False
        
        self.current_patients.append(patient)
        self.total_admissions += 1
        self.available_beds -= 1
        
        # Update occupancy rate
        self.occupancy_rate = len(self.current_patients) / self.bed_capacity
        
        # Estimate charges based on diagnosis and insurance
        base_charge = self._calculate_base_charge(patient.primary_diagnosis, patient.status)
        patient.total_charges = base_charge
        
        # Record patient revenue
        self.gross_patient_revenue += base_charge
        
        return True
    
    def discharge_patient(self, patient_id: str) -> bool:
        """Discharge patient"""
        patient = next((p for p in self.current_patients if p.patient_id == patient_id), None)
        if not patient:
            return False
        
        patient.status = PatientStatus.DISCHARGED
        patient.discharge_date = datetime.now()
        
        # Calculate length of stay
        los = (patient.discharge_date - patient.admission_date).days
        self.average_length_stay = (self.average_length_stay * 0.95 + los * 0.05)
        
        # Process billing
        self._process_patient_billing(patient)
        
        # Remove from current patients
        self.current_patients = [p for p in self.current_patients if p.patient_id != patient_id]
        self.total_discharges += 1
        self.available_beds += 1
        
        # Update occupancy rate
        self.occupancy_rate = len(self.current_patients) / self.bed_capacity
        
        return True
    
    def transfer_patient(self, patient_id: str, destination: str) -> bool:
        """Transfer patient to another facility"""
        patient = next((p for p in self.current_patients if p.patient_id == patient_id), None)
        if not patient:
            return False
        
        patient.status = PatientStatus.TRANSFERRED
        
        # Process partial billing
        self._process_patient_billing(patient)
        
        # Remove from current patients
        self.current_patients = [p for p in self.current_patients if p.patient_id != patient_id]
        self.available_beds += 1
        
        return True
    
    # Staffing management
    def hire_medical_staff(self, staff: MedicalStaff) -> bool:
        """Hire new medical staff"""
        self.medical_staff.append(staff)
        
        # Update staff counts
        if "physician" in staff.role.lower():
            self.physician_count += 1
        elif "nurse" in staff.role.lower():
            self.nurse_count += 1
            # Update nurse-patient ratio
            if self.nurse_count > 0:
                current_patients = len(self.current_patients)
                self.nurse_patient_ratio = current_patients / self.nurse_count
        
        # Record salary expense
        self.post("medical_staff_salaries", "cash", staff.salary, f"Staff hire: {staff.staff_id}")
        self.income_statement["opex"] += staff.salary
        
        return True
    
    def schedule_staff(self, department: str, shift: str) -> Dict[str, int]:
        """Schedule staff for department and shift"""
        dept_staff = [s for s in self.medical_staff if s.department == department]
        
        # Calculate staffing requirements
        if department == "emergency":
            required_physicians = 2
            required_nurses = 4
        elif department == "surgery":
            required_physicians = 3
            required_nurses = 6
        else:
            required_physicians = 1
            required_nurses = 3
        
        schedule = {
            "physicians_scheduled": min(required_physicians, 
                                      len([s for s in dept_staff if "physician" in s.role.lower()])),
            "nurses_scheduled": min(required_nurses,
                                  len([s for s in dept_staff if "nurse" in s.role.lower()]))
        }
        
        return schedule
    
    def manage_staff_credentials(self, staff_id: str, credential_type: str, status: bool) -> bool:
        """Manage staff licensing and certification"""
        staff = next((s for s in self.medical_staff if s.staff_id == staff_id), None)
        if not staff:
            return False
        
        if credential_type == "license":
            staff.licensed = status
        elif credential_type == "board_certification":
            staff.board_certified = status
        
        # Record credentialing costs
        credentialing_cost = 500.0
        self.post("credentialing_costs", "cash", credentialing_cost, 
                 f"Credentialing: {staff_id}")
        
        return True
    
    # Equipment and technology management
    def purchase_medical_equipment(self, equipment: MedicalEquipment) -> str:
        """Purchase medical equipment"""
        self.medical_equipment.append(equipment)
        
        # Record capital expenditure
        self.post("medical_equipment", "cash", equipment.purchase_cost, 
                 f"Equipment purchase: {equipment.equipment_id}")
        
        # Add to imaging equipment list if applicable
        if "imaging" in equipment.equipment_type.lower():
            self.imaging_equipment.append(equipment.equipment_id)
        
        return equipment.equipment_id
    
    def maintain_equipment(self, equipment_id: str) -> float:
        """Perform equipment maintenance"""
        equipment = next((e for e in self.medical_equipment if e.equipment_id == equipment_id), None)
        if not equipment:
            return 0.0
        
        maintenance_cost = equipment.annual_maintenance_cost / 12  # monthly cost
        
        self.post("equipment_maintenance", "cash", maintenance_cost, 
                 f"Maintenance: {equipment_id}")
        self.income_statement["opex"] += maintenance_cost
        
        return maintenance_cost
    
    def utilize_equipment(self, equipment_id: str, procedures_count: int) -> float:
        """Use medical equipment for procedures"""
        equipment = next((e for e in self.medical_equipment if e.equipment_id == equipment_id), None)
        if not equipment:
            return 0.0
        
        revenue = procedures_count * equipment.revenue_per_use
        
        # Update utilization rate
        daily_capacity = 8  # 8 procedures per day max
        equipment.utilization_rate = min(1.0, procedures_count / daily_capacity)
        
        # Record procedure revenue
        self.gross_patient_revenue += revenue
        
        return revenue
    
    # Financial operations and billing
    def _calculate_base_charge(self, diagnosis: str, patient_status: PatientStatus) -> float:
        """Calculate base charge for patient"""
        base_charges = {
            "emergency": 5000.0,
            "surgery": 25000.0,
            "cardiology": 15000.0,
            "oncology": 30000.0,
            "obstetrics": 12000.0,
            "orthopedics": 20000.0
        }
        
        # Default charge
        base_charge = base_charges.get(diagnosis.lower(), 8000.0)
        
        # Adjust for patient status
        if patient_status == PatientStatus.INPATIENT:
            base_charge *= 1.5
        elif patient_status == PatientStatus.EMERGENCY:
            base_charge *= 1.2
        
        return base_charge
    
    def _process_patient_billing(self, patient: Patient) -> None:
        """Process patient billing and insurance"""
        # Calculate insurance payment
        reimbursement_rate = self.average_reimbursement_rate
        if patient.insurance_type == InsuranceType.MEDICAID:
            reimbursement_rate *= 0.80  # Medicaid pays less
        elif patient.insurance_type == InsuranceType.UNINSURED:
            reimbursement_rate = 0.30  # Uninsured pay much less
        
        patient.insurance_payment = patient.total_charges * reimbursement_rate
        patient.patient_payment = patient.total_charges - patient.insurance_payment
        
        # Record revenue
        self.net_patient_revenue += patient.insurance_payment
        
        # Post accounting entries
        self.post("cash", "patient_revenue", patient.insurance_payment, 
                 f"Insurance payment: {patient.patient_id}")
        self.post("accounts_receivable", "patient_revenue", patient.patient_payment,
                 f"Patient payment due: {patient.patient_id}")
        
        self.income_statement["revenue"] += patient.insurance_payment
    
    def negotiate_insurance_contract(self, payer_name: str, 
                                   reimbursement_rates: Dict[str, float]) -> str:
        """Negotiate contract with insurance payer"""
        contract = Insurance(
            insurance_id=f"{payer_name}_{len(self.insurance_contracts) + 1}",
            payer_name=payer_name,
            contract_terms=reimbursement_rates,
            authorization_required=True
        )
        
        self.insurance_contracts.append(contract)
        
        # Update average reimbursement rate
        all_rates = [rate for contract in self.insurance_contracts 
                    for rate in contract.contract_terms.values()]
        if all_rates:
            self.average_reimbursement_rate = sum(all_rates) / len(all_rates)
        
        return contract.insurance_id
    
    def manage_accounts_receivable(self) -> float:
        """Manage outstanding patient accounts"""
        # Calculate bad debt write-offs
        total_ar = self.balance_sheet.get("accounts_receivable", 0)
        bad_debt_amount = total_ar * self.bad_debt_rate / 12  # monthly write-off
        
        if bad_debt_amount > 0:
            self.post("bad_debt_expense", "accounts_receivable", bad_debt_amount,
                     "Monthly bad debt write-off")
            self.income_statement["opex"] += bad_debt_amount
        
        return bad_debt_amount
    
    # Quality management
    def track_clinical_outcome(self, outcome: ClinicalOutcome) -> None:
        """Track clinical outcome metrics"""
        self.clinical_outcomes.append(outcome)
        
        # Update aggregate metrics
        outcomes_for_procedure = [o for o in self.clinical_outcomes 
                                if o.procedure_type == outcome.procedure_type]
        
        if outcomes_for_procedure:
            avg_success = sum(o.success_rate for o in outcomes_for_procedure) / len(outcomes_for_procedure)
            avg_complications = sum(o.complication_rate for o in outcomes_for_procedure) / len(outcomes_for_procedure)
            
            # Update quality metrics
            self.mortality_rate = avg_complications * 0.1  # rough correlation
            
    def implement_quality_program(self, program_name: str, annual_cost: float) -> str:
        """Implement quality improvement program"""
        self.quality_improvement_programs.append(program_name)
        
        # Record program costs
        monthly_cost = annual_cost / 12
        self.post("quality_programs", "cash", monthly_cost, f"Quality program: {program_name}")
        self.income_statement["opex"] += monthly_cost
        
        # Improve quality metrics
        self.patient_satisfaction_score = min(5.0, self.patient_satisfaction_score + 0.1)
        self.regulatory_compliance_score = min(1.0, self.regulatory_compliance_score + 0.02)
        
        return program_name
    
    def conduct_patient_survey(self) -> Dict[str, float]:
        """Conduct patient satisfaction survey"""
        # Simulate survey results
        survey_results = {
            "overall_satisfaction": self.patient_satisfaction_score,
            "communication": self.patient_satisfaction_score + 0.2,
            "pain_management": self.patient_satisfaction_score - 0.1,
            "cleanliness": self.patient_satisfaction_score + 0.1,
            "staff_responsiveness": self.patient_satisfaction_score
        }
        
        # Update satisfaction score
        avg_score = sum(survey_results.values()) / len(survey_results)
        self.patient_satisfaction_score = (self.patient_satisfaction_score * 0.9 + avg_score * 0.1)
        
        return survey_results
    
    # Regulatory compliance
    def seek_accreditation(self, accrediting_body: str, cost: float) -> bool:
        """Seek healthcare accreditation"""
        self.accreditation_status.append(accrediting_body)
        
        # Record accreditation costs
        self.post("accreditation_costs", "cash", cost, f"Accreditation: {accrediting_body}")
        self.income_statement["opex"] += cost
        
        # Improve compliance score
        self.regulatory_compliance_score = min(1.0, self.regulatory_compliance_score + 0.05)
        
        return True
    
    def comply_with_regulations(self, regulation_type: str, compliance_cost: float) -> bool:
        """Ensure regulatory compliance"""
        compliance_programs = {
            "hipaa": "HIPAA Privacy and Security",
            "osha": "Occupational Safety",
            "cms": "Medicare/Medicaid Compliance",
            "joint_commission": "Quality Standards"
        }
        
        program_name = compliance_programs.get(regulation_type, regulation_type)
        
        # Record compliance costs
        self.post("regulatory_compliance", "cash", compliance_cost, 
                 f"Compliance: {program_name}")
        self.income_statement["opex"] += compliance_cost
        
        # Improve compliance score
        self.regulatory_compliance_score = min(1.0, self.regulatory_compliance_score + 0.03)
        
        return True
    
    # Emergency preparedness
    def activate_emergency_capacity(self, additional_beds: int) -> bool:
        """Activate emergency surge capacity"""
        if additional_beds > self.emergency_capacity:
            return False
        
        self.bed_capacity += additional_beds
        self.available_beds += additional_beds
        self.emergency_capacity -= additional_beds
        
        # Record emergency costs
        activation_cost = additional_beds * 1000  # $1000 per emergency bed
        self.post("emergency_response", "cash", activation_cost, "Emergency capacity activation")
        
        return True
    
    def implement_infection_control(self, protocol_type: str, cost: float) -> bool:
        """Implement infection control protocols"""
        # Record infection control costs
        self.post("infection_control", "cash", cost, f"Infection control: {protocol_type}")
        self.income_statement["opex"] += cost
        
        # Improve infection rate
        self.infection_rate = max(0.005, self.infection_rate - 0.002)  # reduce by 0.2%
        
        return True
    
    # Analytics and reporting
    def calculate_revenue_per_bed(self) -> float:
        """Calculate revenue per licensed bed"""
        if self.licensed_beds == 0:
            return 0.0
        
        return self.net_patient_revenue / self.licensed_beds
    
    def calculate_cost_per_patient(self) -> float:
        """Calculate cost per patient"""
        total_expenses = self.income_statement.get("opex", 0)
        if self.total_discharges == 0:
            return 0.0
        
        return total_expenses / self.total_discharges
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality metrics report"""
        quality_metrics = {
            "patient_outcomes": {
                "mortality_rate": self.mortality_rate,
                "infection_rate": self.infection_rate,
                "readmission_rate": self.readmission_rate,
                "patient_satisfaction": self.patient_satisfaction_score
            },
            "operational_metrics": {
                "occupancy_rate": self.occupancy_rate,
                "average_length_stay": self.average_length_stay,
                "nurse_patient_ratio": self.nurse_patient_ratio,
                "equipment_utilization": self.equipment_utilization
            },
            "financial_metrics": {
                "revenue_per_bed": self.calculate_revenue_per_bed(),
                "cost_per_patient": self.calculate_cost_per_patient(),
                "bad_debt_rate": self.bad_debt_rate,
                "case_mix_index": self.case_mix_index
            },
            "quality_indicators": {
                "cms_star_rating": self.cms_star_rating,
                "regulatory_compliance": self.regulatory_compliance_score,
                "accreditations": len(self.accreditation_status),
                "quality_programs": len(self.quality_improvement_programs)
            }
        }
        
        return quality_metrics
    
    def generate_clinical_dashboard(self) -> Dict[str, Any]:
        """Generate clinical operations dashboard"""
        current_census = len(self.current_patients)
        
        dashboard = {
            "census_data": {
                "current_census": current_census,
                "available_beds": self.available_beds,
                "occupancy_rate": self.occupancy_rate,
                "patients_by_status": {
                    status.value: len([p for p in self.current_patients if p.status == status])
                    for status in PatientStatus if status != PatientStatus.DISCHARGED
                }
            },
            "staffing_status": {
                "physicians_on_duty": self.physician_count,
                "nurses_on_duty": self.nurse_count,
                "nurse_patient_ratio": self.nurse_patient_ratio,
                "staff_utilization": current_census / max(len(self.medical_staff), 1)
            },
            "service_line_activity": {
                service.value: len([p for p in self.current_patients 
                                  if service.value in p.primary_diagnosis.lower()])
                for service in ServiceLine
            },
            "quality_alerts": {
                "high_readmission_risk": len([p for p in self.current_patients 
                                            if p.estimated_length_stay > 7]),
                "infection_control_alerts": int(current_census * self.infection_rate),
                "patient_satisfaction_below_target": self.patient_satisfaction_score < 4.0
            }
        }
        
        return dashboard 