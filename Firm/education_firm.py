# education_firm.py
# NAICS 61: Educational Services

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class EducationType(Enum):
    K12_PUBLIC = "k12_public"
    K12_PRIVATE = "k12_private"
    K12_CHARTER = "k12_charter"
    HIGHER_ED_PUBLIC = "higher_ed_public"
    HIGHER_ED_PRIVATE = "higher_ed_private"
    COMMUNITY_COLLEGE = "community_college"
    VOCATIONAL = "vocational"
    ONLINE = "online"
    GRADUATE_SCHOOL = "graduate_school"
    PROFESSIONAL_SCHOOL = "professional_school"

class DegreeLevel(Enum):
    CERTIFICATE = "certificate"
    ASSOCIATE = "associate"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORAL = "doctoral"
    PROFESSIONAL = "professional"  # JD, MD, etc.

class StudentStatus(Enum):
    ENROLLED = "enrolled"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"
    DROPPED_OUT = "dropped_out"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"

class FundingSource(Enum):
    TUITION = "tuition"
    STATE_FUNDING = "state_funding"
    FEDERAL_GRANTS = "federal_grants"
    PRIVATE_DONATIONS = "private_donations"
    ENDOWMENT = "endowment"
    RESEARCH_GRANTS = "research_grants"
    AUXILIARY_SERVICES = "auxiliary_services"

@dataclass
class Student:
    student_id: str
    enrollment_date: date
    tuition_rate: float
    financial_aid: float
    program: str
    degree_level: DegreeLevel
    status: StudentStatus = StudentStatus.ENROLLED
    gpa: float = 0.0
    credits_completed: int = 0
    credits_required: int = 120  # default bachelor's requirement
    demographics: Dict[str, Any] = field(default_factory=dict)
    housing: str = "off_campus"  # on_campus, off_campus

@dataclass
class AcademicProgram:
    program_id: str
    program_name: str
    degree_level: DegreeLevel
    department: str
    credit_hours: int
    tuition_per_credit: float
    enrollment_capacity: int
    current_enrollment: int = 0
    accreditation_status: str = "accredited"
    faculty_requirements: int = 5  # minimum faculty needed

@dataclass
class Faculty:
    faculty_id: str
    name: str
    department: str
    rank: str  # professor, associate, assistant, lecturer
    tenure_status: str  # tenured, tenure_track, non_tenure
    salary: float
    research_active: bool = False
    teaching_load: int = 12  # credit hours per semester
    publications: int = 0

@dataclass
class Course:
    course_id: str
    course_name: str
    credit_hours: int
    instructor_id: str
    enrollment_limit: int
    current_enrollment: int = 0
    tuition_revenue: float = 0.0
    semester: str = "fall"

@dataclass
class ResearchGrant:
    grant_id: str
    funding_agency: str
    principal_investigator: str
    amount: float
    start_date: date
    end_date: date
    indirect_cost_rate: float = 0.30  # 30% overhead

@dataclass
class EducationFirm(BaseFirm):
    # Institutional characteristics
    education_type: EducationType = EducationType.HIGHER_ED_PRIVATE
    accreditation_status: List[str] = field(default_factory=list)
    founding_year: int = 1900
    campus_size_acres: float = 100.0
    
    # Enrollment and capacity
    enrollment_capacity: int = 1000
    current_enrollment: int = 0
    enrollment_by_level: Dict[DegreeLevel, int] = field(default_factory=dict)
    target_enrollment_growth: float = 0.05  # 5% annual growth
    
    # Student body and demographics
    enrolled_students: List[Student] = field(default_factory=list)
    student_demographics: Dict[str, float] = field(default_factory=dict)
    international_student_percentage: float = 0.10
    
    # Academic programs and curriculum
    academic_programs: List[AcademicProgram] = field(default_factory=list)
    degree_programs: List[str] = field(default_factory=list)
    courses_offered: List[Course] = field(default_factory=list)
    academic_departments: List[str] = field(default_factory=list)
    
    # Faculty and staff
    faculty_members: List[Faculty] = field(default_factory=list)
    faculty_student_ratio: float = 15.0  # students per faculty
    tenure_track_percentage: float = 0.60
    average_faculty_salary: float = 75000.0
    
    # Financial structure and funding
    funding_sources: Dict[FundingSource, float] = field(default_factory=dict)
    tuition_revenue: float = 0.0
    endowment_value: float = 0.0
    endowment_payout_rate: float = 0.05  # 5% annual distribution
    grants_and_donations: float = 0.0
    
    # Financial aid and affordability
    financial_aid_budget: float = 0.0
    average_aid_per_student: float = 5000.0
    aid_recipients_percentage: float = 0.70  # 70% receive aid
    scholarship_programs: List[str] = field(default_factory=list)
    
    # Student outcomes and success metrics
    graduation_rate: float = 0.75
    retention_rate: float = 0.85
    employment_rate_post_graduation: float = 0.90
    average_starting_salary: float = 50000.0
    student_satisfaction_score: float = 4.0  # out of 5
    
    # Research and scholarly activity
    research_grants: List[ResearchGrant] = field(default_factory=list)
    total_research_funding: float = 0.0
    research_publications: int = 0
    technology_transfer_revenue: float = 0.0
    
    # Facilities and infrastructure
    classroom_capacity: int = 50  # students per classroom
    library_holdings: int = 100000  # books/resources
    laboratory_facilities: int = 10
    dormitory_capacity: int = 500
    dining_facilities: int = 3
    
    # Technology and digital learning
    learning_management_system: str = "canvas"
    online_course_percentage: float = 0.20
    technology_budget: float = 0.0
    computer_labs: int = 5
    wifi_coverage: float = 1.0  # 100% campus coverage
    
    # Student services and support
    counseling_services: bool = True
    career_services: bool = True
    tutoring_programs: bool = True
    health_services: bool = True
    student_organizations: int = 50
    
    # Athletics and extracurriculars
    athletic_programs: List[str] = field(default_factory=list)
    athletic_budget: float = 0.0
    ncaa_division: str = "III"  # I, II, III, or None
    intramural_programs: int = 10
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "61"  # Educational Services
    
    # Student enrollment and management
    def enroll_student(self, student: Student) -> bool:
        """Enroll new student"""
        if self.current_enrollment >= self.enrollment_capacity:
            return False
        
        # Find appropriate program
        program = next((p for p in self.academic_programs if p.program_id == student.program), None)
        if not program or program.current_enrollment >= program.enrollment_capacity:
            return False
        
        self.enrolled_students.append(student)
        self.current_enrollment += 1
        program.current_enrollment += 1
        
        # Update enrollment by level
        self.enrollment_by_level[student.degree_level] = self.enrollment_by_level.get(student.degree_level, 0) + 1
        
        # Record tuition revenue
        net_tuition = student.tuition_rate - student.financial_aid
        self.post("cash", "tuition_revenue", net_tuition, f"Enrollment: {student.student_id}")
        self.income_statement["revenue"] += net_tuition
        self.tuition_revenue += net_tuition
        
        # Provide financial aid if applicable
        if student.financial_aid > 0:
            self.post("financial_aid_expense", "cash", student.financial_aid, 
                     f"Financial aid: {student.student_id}")
            self.income_statement["opex"] += student.financial_aid
        
        return True
    
    def graduate_student(self, student_id: str) -> bool:
        """Graduate student who has completed requirements"""
        student = next((s for s in self.enrolled_students if s.student_id == student_id), None)
        if not student:
            return False
        
        # Check if requirements are met
        if student.credits_completed < student.credits_required:
            return False
        
        student.status = StudentStatus.GRADUATED
        self.current_enrollment -= 1
        
        # Update graduation statistics
        self.graduation_rate = (self.graduation_rate * 0.95 + 1.0 * 0.05)  # weighted average
        
        # Remove from enrolled students list
        self.enrolled_students = [s for s in self.enrolled_students if s.student_id != student_id]
        
        return True
    
    def process_student_retention(self) -> float:
        """Process student retention and dropouts"""
        students_at_risk = [s for s in self.enrolled_students if s.gpa < 2.0]
        
        # Some at-risk students drop out
        dropout_count = int(len(students_at_risk) * 0.20)  # 20% of at-risk students
        
        for i in range(dropout_count):
            if students_at_risk:
                student = students_at_risk.pop(0)
                student.status = StudentStatus.DROPPED_OUT
                self.current_enrollment -= 1
                self.enrolled_students.remove(student)
        
        # Update retention rate
        if self.current_enrollment > 0:
            current_retention = (self.current_enrollment - dropout_count) / self.current_enrollment
            self.retention_rate = (self.retention_rate * 0.9 + current_retention * 0.1)
        
        return self.retention_rate
    
    # Academic program management
    def create_academic_program(self, program: AcademicProgram) -> str:
        """Create new academic program"""
        self.academic_programs.append(program)
        self.degree_programs.append(program.program_name)
        
        # Add to appropriate department
        if program.department not in self.academic_departments:
            self.academic_departments.append(program.department)
        
        # Record program development costs
        development_cost = 50000.0  # curriculum development, accreditation
        self.post("program_development", "cash", development_cost, 
                 f"New program: {program.program_id}")
        
        return program.program_id
    
    def seek_program_accreditation(self, program_id: str, accrediting_body: str, cost: float) -> bool:
        """Seek accreditation for academic program"""
        program = next((p for p in self.academic_programs if p.program_id == program_id), None)
        if not program:
            return False
        
        program.accreditation_status = "pending"
        self.accreditation_status.append(f"{program_id}_{accrediting_body}")
        
        # Record accreditation costs
        self.post("accreditation_costs", "cash", cost, f"Accreditation: {program_id}")
        self.income_statement["opex"] += cost
        
        return True
    
    def schedule_course(self, course: Course) -> str:
        """Schedule course offering"""
        # Check if instructor is available
        instructor = next((f for f in self.faculty_members if f.faculty_id == course.instructor_id), None)
        if not instructor:
            return ""
        
        # Check instructor teaching load
        current_load = sum(c.credit_hours for c in self.courses_offered 
                          if c.instructor_id == instructor.faculty_id)
        if current_load + course.credit_hours > instructor.teaching_load:
            return ""
        
        self.courses_offered.append(course)
        return course.course_id
    
    # Faculty management
    def hire_faculty(self, faculty: Faculty) -> bool:
        """Hire new faculty member"""
        self.faculty_members.append(faculty)
        
        # Record salary expense
        annual_salary = faculty.salary
        self.post("faculty_salaries", "cash", annual_salary, f"Faculty hire: {faculty.faculty_id}")
        self.income_statement["opex"] += annual_salary
        
        # Update faculty metrics
        total_faculty = len(self.faculty_members)
        self.average_faculty_salary = sum(f.salary for f in self.faculty_members) / total_faculty
        
        tenure_track_count = len([f for f in self.faculty_members if f.tenure_status in ["tenured", "tenure_track"]])
        self.tenure_track_percentage = tenure_track_count / total_faculty
        
        return True
    
    def grant_tenure(self, faculty_id: str) -> bool:
        """Grant tenure to faculty member"""
        faculty = next((f for f in self.faculty_members if f.faculty_id == faculty_id), None)
        if not faculty or faculty.tenure_status != "tenure_track":
            return False
        
        faculty.tenure_status = "tenured"
        faculty.salary *= 1.15  # 15% salary increase with tenure
        
        return True
    
    def promote_faculty(self, faculty_id: str, new_rank: str) -> bool:
        """Promote faculty to new rank"""
        faculty = next((f for f in self.faculty_members if f.faculty_id == faculty_id), None)
        if not faculty:
            return False
        
        old_rank = faculty.rank
        faculty.rank = new_rank
        
        # Salary adjustment for promotion
        promotion_increases = {
            "assistant": {"associate": 1.20},
            "associate": {"professor": 1.25}
        }
        
        if old_rank in promotion_increases and new_rank in promotion_increases[old_rank]:
            faculty.salary *= promotion_increases[old_rank][new_rank]
        
        return True
    
    # Financial operations
    def receive_grant(self, grant: ResearchGrant) -> None:
        """Receive research grant"""
        self.research_grants.append(grant)
        self.total_research_funding += grant.amount
        
        # Calculate direct and indirect costs
        direct_cost = grant.amount * (1 - grant.indirect_cost_rate)
        indirect_cost = grant.amount * grant.indirect_cost_rate
        
        # Record grant revenue
        self.post("cash", "grant_revenue", grant.amount, f"Grant: {grant.grant_id}")
        self.income_statement["revenue"] += grant.amount
        
        # Allocate to research and overhead
        self.post("research_expenses", "grant_funds", direct_cost, f"Research: {grant.grant_id}")
        self.post("indirect_costs", "grant_funds", indirect_cost, f"Overhead: {grant.grant_id}")
    
    def receive_donation(self, donor_id: str, amount: float, purpose: str = "general") -> None:
        """Receive philanthropic donation"""
        self.grants_and_donations += amount
        
        if purpose == "endowment":
            self.endowment_value += amount
            self.post("endowment_fund", "cash", amount, f"Endowment gift: {donor_id}")
        else:
            self.post("cash", "donations", amount, f"Donation: {donor_id}")
            self.income_statement["revenue"] += amount
    
    def distribute_endowment_payout(self) -> float:
        """Distribute annual endowment payout"""
        if self.endowment_value == 0:
            return 0.0
        
        annual_payout = self.endowment_value * self.endowment_payout_rate
        
        self.post("cash", "endowment_income", annual_payout, "Annual endowment distribution")
        self.income_statement["revenue"] += annual_payout
        
        return annual_payout
    
    def award_financial_aid(self, student_id: str, aid_amount: float, aid_type: str) -> bool:
        """Award financial aid to student"""
        student = next((s for s in self.enrolled_students if s.student_id == student_id), None)
        if not student:
            return False
        
        student.financial_aid += aid_amount
        self.financial_aid_budget += aid_amount
        
        # Record aid expense
        self.post("financial_aid_expense", "cash", aid_amount, 
                 f"Financial aid: {student_id}")
        
        return True
    
    # Research and scholarly activities
    def conduct_research_project(self, project_id: str, funding_amount: float, 
                                faculty_investigators: List[str]) -> str:
        """Conduct research project"""
        # Create research grant record
        grant = ResearchGrant(
            grant_id=project_id,
            funding_agency="internal",
            principal_investigator=faculty_investigators[0],
            amount=funding_amount,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
        
        self.research_grants.append(grant)
        
        # Update faculty research activity
        for faculty_id in faculty_investigators:
            faculty = next((f for f in self.faculty_members if f.faculty_id == faculty_id), None)
            if faculty:
                faculty.research_active = True
        
        return project_id
    
    def publish_research(self, faculty_id: str, publication_count: int) -> None:
        """Record research publications"""
        faculty = next((f for f in self.faculty_members if f.faculty_id == faculty_id), None)
        if faculty:
            faculty.publications += publication_count
            self.research_publications += publication_count
    
    def commercialize_technology(self, technology_id: str, licensing_revenue: float) -> None:
        """Commercialize research technology"""
        self.technology_transfer_revenue += licensing_revenue
        
        self.post("cash", "technology_licensing", licensing_revenue, 
                 f"Tech transfer: {technology_id}")
        self.income_statement["revenue"] += licensing_revenue
    
    # Student services and support
    def provide_student_services(self, service_type: str, annual_budget: float) -> None:
        """Provide student support services"""
        service_costs = {
            "counseling": annual_budget * 0.20,
            "career_services": annual_budget * 0.25,
            "tutoring": annual_budget * 0.15,
            "health_services": annual_budget * 0.30,
            "student_activities": annual_budget * 0.10
        }
        
        cost = service_costs.get(service_type, annual_budget)
        
        self.post("student_services", "cash", cost, f"Student services: {service_type}")
        self.income_statement["opex"] += cost
    
    def track_student_outcomes(self, graduating_class: List[str]) -> Dict[str, float]:
        """Track post-graduation outcomes"""
        employed_count = int(len(graduating_class) * self.employment_rate_post_graduation)
        
        outcomes = {
            "employment_rate": employed_count / len(graduating_class),
            "average_starting_salary": self.average_starting_salary,
            "graduate_school_rate": 0.25,  # 25% continue to graduate school
            "satisfaction_rate": 0.85  # 85% satisfied with education
        }
        
        return outcomes
    
    # Facilities and infrastructure
    def invest_in_facilities(self, facility_type: str, investment: float) -> None:
        """Invest in campus facilities"""
        if facility_type == "classroom":
            self.classroom_capacity += int(investment / 10000)  # $10k per seat
        elif facility_type == "dormitory":
            self.dormitory_capacity += int(investment / 50000)  # $50k per bed
        elif facility_type == "laboratory":
            self.laboratory_facilities += int(investment / 100000)  # $100k per lab
        elif facility_type == "library":
            self.library_holdings += int(investment / 50)  # $50 per book/resource
        
        self.post("facilities_investment", "cash", investment, 
                 f"Facility investment: {facility_type}")
    
    def upgrade_technology_infrastructure(self, upgrade_cost: float) -> None:
        """Upgrade campus technology"""
        self.technology_budget += upgrade_cost
        
        # Improve online learning capabilities
        self.online_course_percentage = min(1.0, self.online_course_percentage + 0.05)
        self.wifi_coverage = 1.0  # ensure full coverage
        
        self.post("technology_investment", "cash", upgrade_cost, "Technology upgrade")
        self.income_statement["opex"] += upgrade_cost
    
    # Analytics and reporting
    def calculate_cost_per_student(self) -> float:
        """Calculate cost per student"""
        total_expenses = self.income_statement.get("opex", 0)
        if self.current_enrollment == 0:
            return 0.0
        
        return total_expenses / self.current_enrollment
    
    def calculate_net_tuition_revenue(self) -> float:
        """Calculate net tuition revenue after financial aid"""
        gross_tuition = sum(s.tuition_rate for s in self.enrolled_students)
        total_aid = sum(s.financial_aid for s in self.enrolled_students)
        
        return gross_tuition - total_aid
    
    def generate_institutional_effectiveness_report(self) -> Dict[str, Any]:
        """Generate comprehensive institutional effectiveness metrics"""
        total_faculty = len(self.faculty_members)
        
        effectiveness_metrics = {
            "enrollment_metrics": {
                "total_enrollment": self.current_enrollment,
                "capacity_utilization": self.current_enrollment / self.enrollment_capacity,
                "enrollment_by_level": self.enrollment_by_level,
                "retention_rate": self.retention_rate,
                "graduation_rate": self.graduation_rate
            },
            "academic_metrics": {
                "faculty_student_ratio": self.current_enrollment / max(total_faculty, 1),
                "programs_offered": len(self.academic_programs),
                "courses_per_semester": len(self.courses_offered),
                "research_publications": self.research_publications
            },
            "financial_metrics": {
                "tuition_revenue": self.tuition_revenue,
                "cost_per_student": self.calculate_cost_per_student(),
                "endowment_per_student": self.endowment_value / max(self.current_enrollment, 1),
                "research_funding": self.total_research_funding
            },
            "student_success_metrics": {
                "employment_rate": self.employment_rate_post_graduation,
                "average_starting_salary": self.average_starting_salary,
                "student_satisfaction": self.student_satisfaction_score,
                "financial_aid_recipients": self.aid_recipients_percentage
            },
            "infrastructure_metrics": {
                "classroom_utilization": self.current_enrollment / max(self.classroom_capacity, 1),
                "dormitory_occupancy": 0.85,  # would calculate from actual data
                "technology_investment": self.technology_budget
            }
        }
        
        return effectiveness_metrics 