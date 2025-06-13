# org_chart.py
# comprehensive organizational chart and corporate governance module

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum
from datetime import date

# ---------------------------------------------------------------------------
# helper types and enums
# ---------------------------------------------------------------------------

class RoleType(Enum):
    BOARD_MEMBER = "board_member"
    EXECUTIVE = "executive"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    CONSULTANT = "consultant"
    ADVISOR = "advisor"

class VotingRights(Enum):
    FULL = "full"           # Can vote on all matters
    LIMITED = "limited"     # Can vote on specific matters only
    ADVISORY = "advisory"   # Non-binding votes only
    NONE = "none"          # No voting rights

@dataclass
class Shareholder:
    entity_id: str
    pct_ownership: float  # 0‒1
    voting_pct: float = None  # Can differ from ownership (e.g., non-voting shares)
    share_class: str = "common"  # common, preferred, etc.
    
    def __post_init__(self):
        if self.voting_pct is None:
            self.voting_pct = self.pct_ownership

@dataclass
class Role:
    title: str
    role_type: RoleType
    department: str = ""
    level: int = 0  # 0 = board, 1 = C-suite, 2 = VP, 3 = director, etc.
    can_hire: bool = False
    can_fire: bool = False
    can_fire_roles: List[str] = field(default_factory=list)  # Specific roles this can fire
    voting_rights: VotingRights = VotingRights.NONE
    voting_matters: List[str] = field(default_factory=list)  # What they can vote on
    salary_band: Tuple[float, float] = (0.0, 0.0)

@dataclass
class PersonInOrg:
    person_id: str
    roles: List[Role] = field(default_factory=list)
    direct_reports: List[str] = field(default_factory=list)  # person_ids
    manager: Optional[str] = None  # person_id
    start_date: date = None
    employment_status: str = "active"  # active, terminated, on_leave
    
    def add_role(self, role: Role) -> None:
        """Add a role to this person"""
        self.roles.append(role)
    
    def remove_role(self, role_title: str) -> bool:
        """Remove a role by title, returns True if found and removed"""
        for i, role in enumerate(self.roles):
            if role.title == role_title:
                self.roles.pop(i)
                return True
        return False
    
    def has_role(self, role_title: str) -> bool:
        """Check if person has a specific role"""
        return any(role.title == role_title for role in self.roles)
    
    def get_highest_level_role(self) -> Optional[Role]:
        """Get the role with the lowest level number (highest in hierarchy)"""
        if not self.roles:
            return None
        return min(self.roles, key=lambda r: r.level)
    
    def can_fire_person(self, target_person_id: str, org_chart: 'OrgChart') -> bool:
        """Check if this person can fire another person"""
        target = org_chart.get_person(target_person_id)
        if not target:
            return False
        
        # Check if any of this person's roles can fire any of target's roles
        for my_role in self.roles:
            if my_role.can_fire:
                # Can fire direct reports
                if target_person_id in self.direct_reports:
                    return True
                
                # Can fire specific roles
                for target_role in target.roles:
                    if target_role.title in my_role.can_fire_roles:
                        return True
                    
                    # Can fire people at higher levels (lower hierarchy)
                    if my_role.level < target_role.level:
                        return True
        
        return False

# ---------------------------------------------------------------------------
# main organizational chart class
# ---------------------------------------------------------------------------

class OrgChart:
    def __init__(self):
        self.people: Dict[str, PersonInOrg] = {}
        self.shareholders: Dict[str, Shareholder] = {}
        self.board_composition: List[str] = []  # person_ids of board members
        self.committees: Dict[str, List[str]] = {}  # committee_name -> person_ids
        self.org_policies: Dict[str, Any] = {
            "board_quorum": 0.5,  # Fraction needed for quorum
            "majority_vote_threshold": 0.5,
            "supermajority_threshold": 0.67,
            "board_term_length": 365,  # days
        }
    
    # -----------------------------------------------------------------------
    # basic person management
    # -----------------------------------------------------------------------
    
    def add_person(self, person_id: str, roles: List[Role] = None, 
                   manager: str = None) -> PersonInOrg:
        """Add a person to the organization"""
        if person_id in self.people:
            raise ValueError(f"Person {person_id} already exists in org chart")
        
        person = PersonInOrg(
            person_id=person_id,
            roles=roles or [],
            manager=manager
        )
        self.people[person_id] = person
        
        # Update manager's direct reports
        if manager and manager in self.people:
            self.people[manager].direct_reports.append(person_id)
        
        # Add to board if has board role
        for role in person.roles:
            if role.role_type == RoleType.BOARD_MEMBER:
                if person_id not in self.board_composition:
                    self.board_composition.append(person_id)
        
        return person
    
    def remove_person(self, person_id: str) -> bool:
        """Remove a person from the organization"""
        if person_id not in self.people:
            return False
        
        person = self.people[person_id]
        
        # Remove from manager's direct reports
        if person.manager and person.manager in self.people:
            manager = self.people[person.manager]
            if person_id in manager.direct_reports:
                manager.direct_reports.remove(person_id)
        
        # Reassign direct reports
        for report_id in person.direct_reports:
            if report_id in self.people:
                self.people[report_id].manager = person.manager
                if person.manager and person.manager in self.people:
                    self.people[person.manager].direct_reports.append(report_id)
        
        # Remove from board
        if person_id in self.board_composition:
            self.board_composition.remove(person_id)
        
        # Remove from committees
        for committee_members in self.committees.values():
            if person_id in committee_members:
                committee_members.remove(person_id)
        
        del self.people[person_id]
        return True
    
    def get_person(self, person_id: str) -> Optional[PersonInOrg]:
        """Get a person from the org chart"""
        return self.people.get(person_id)
    
    # -----------------------------------------------------------------------
    # role management
    # -----------------------------------------------------------------------
    
    def assign_role(self, person_id: str, role: Role) -> bool:
        """Assign a role to a person"""
        if person_id not in self.people:
            return False
        
        self.people[person_id].add_role(role)
        
        # Add to board if board role
        if role.role_type == RoleType.BOARD_MEMBER:
            if person_id not in self.board_composition:
                self.board_composition.append(person_id)
        
        return True
    
    def remove_role(self, person_id: str, role_title: str) -> bool:
        """Remove a role from a person"""
        if person_id not in self.people:
            return False
        
        person = self.people[person_id]
        success = person.remove_role(role_title)
        
        # Remove from board if no longer has board role
        if success and not any(r.role_type == RoleType.BOARD_MEMBER for r in person.roles):
            if person_id in self.board_composition:
                self.board_composition.remove(person_id)
        
        return success
    
    # -----------------------------------------------------------------------
    # hierarchy management
    # -----------------------------------------------------------------------
    
    def set_manager(self, person_id: str, manager_id: str) -> bool:
        """Set someone's manager"""
        if person_id not in self.people or manager_id not in self.people:
            return False
        
        person = self.people[person_id]
        
        # Remove from old manager's reports
        if person.manager and person.manager in self.people:
            old_manager = self.people[person.manager]
            if person_id in old_manager.direct_reports:
                old_manager.direct_reports.remove(person_id)
        
        # Set new manager
        person.manager = manager_id
        new_manager = self.people[manager_id]
        if person_id not in new_manager.direct_reports:
            new_manager.direct_reports.append(person_id)
        
        return True
    
    def get_direct_reports(self, person_id: str) -> List[str]:
        """Get list of direct report person_ids"""
        person = self.get_person(person_id)
        return person.direct_reports if person else []
    
    def get_all_reports(self, person_id: str) -> List[str]:
        """Get all reports (direct and indirect) recursively"""
        all_reports = []
        direct_reports = self.get_direct_reports(person_id)
        
        for report_id in direct_reports:
            all_reports.append(report_id)
            all_reports.extend(self.get_all_reports(report_id))
        
        return all_reports
    
    def get_chain_of_command(self, person_id: str) -> List[str]:
        """Get the chain of command from person to top"""
        chain = []
        current_id = person_id
        
        while current_id and current_id in self.people:
            chain.append(current_id)
            current_id = self.people[current_id].manager
        
        return chain
    
    # -----------------------------------------------------------------------
    # shareholder management
    # -----------------------------------------------------------------------
    
    def add_shareholder(self, shareholder: Shareholder) -> None:
        """Add a shareholder"""
        self.shareholders[shareholder.entity_id] = shareholder
    
    def remove_shareholder(self, entity_id: str) -> bool:
        """Remove a shareholder"""
        if entity_id in self.shareholders:
            del self.shareholders[entity_id]
            return True
        return False
    
    def get_shareholder(self, entity_id: str) -> Optional[Shareholder]:
        """Get shareholder info"""
        return self.shareholders.get(entity_id)
    
    def get_voting_power(self, entity_id: str) -> float:
        """Get total voting power for an entity (including as employee)"""
        total_voting = 0.0
        
        # Add shareholder voting power
        if entity_id in self.shareholders:
            total_voting += self.shareholders[entity_id].voting_pct
        
        # Add employee voting power from roles
        person = self.get_person(entity_id)
        if person:
            for role in person.roles:
                if role.voting_rights in [VotingRights.FULL, VotingRights.LIMITED]:
                    # This would need to be defined based on company bylaws
                    # For now, board members get equal voting weight
                    if role.role_type == RoleType.BOARD_MEMBER:
                        if len(self.board_composition) > 0:
                            total_voting += 1.0 / len(self.board_composition)
        
        return total_voting
    
    def get_total_ownership(self) -> Dict[str, float]:
        """Get ownership percentages for all shareholders"""
        return {entity_id: sh.pct_ownership 
                for entity_id, sh in self.shareholders.items()}
    
    # -----------------------------------------------------------------------
    # board and committee management
    # -----------------------------------------------------------------------
    
    def add_to_committee(self, committee_name: str, person_id: str) -> bool:
        """Add person to a committee"""
        if person_id not in self.people:
            return False
        
        if committee_name not in self.committees:
            self.committees[committee_name] = []
        
        if person_id not in self.committees[committee_name]:
            self.committees[committee_name].append(person_id)
        
        return True
    
    def remove_from_committee(self, committee_name: str, person_id: str) -> bool:
        """Remove person from committee"""
        if committee_name in self.committees and person_id in self.committees[committee_name]:
            self.committees[committee_name].remove(person_id)
            return True
        return False
    
    def get_committee_members(self, committee_name: str) -> List[str]:
        """Get members of a committee"""
        return self.committees.get(committee_name, [])
    
    def can_remove_board_member(self, remover_id: str, target_id: str) -> bool:
        """Check if someone can remove a board member"""
        # Typically requires board vote or shareholder vote
        # This is simplified - real implementation would check bylaws
        
        if remover_id not in self.people or target_id not in self.people:
            return False
        
        # If remover is a major shareholder (>50% voting)
        if self.get_voting_power(remover_id) > 0.5:
            return True
        
        # If remover is board chair (would need to track this role)
        remover = self.people[remover_id]
        for role in remover.roles:
            if "chair" in role.title.lower() and role.role_type == RoleType.BOARD_MEMBER:
                return True
        
        return False
    
    # -----------------------------------------------------------------------
    # query and analysis functions
    # -----------------------------------------------------------------------
    
    def get_people_by_role_type(self, role_type: RoleType) -> List[str]:
        """Get all people with a specific role type"""
        result = []
        for person_id, person in self.people.items():
            if any(role.role_type == role_type for role in person.roles):
                result.append(person_id)
        return result
    
    def get_people_by_department(self, department: str) -> List[str]:
        """Get all people in a department"""
        result = []
        for person_id, person in self.people.items():
            if any(role.department == department for role in person.roles):
                result.append(person_id)
        return result
    
    def get_org_depth(self) -> int:
        """Get the maximum depth of the organization"""
        max_depth = 0
        for person_id in self.people:
            chain = self.get_chain_of_command(person_id)
            max_depth = max(max_depth, len(chain))
        return max_depth
    
    def get_span_of_control(self, person_id: str) -> int:
        """Get number of direct reports"""
        return len(self.get_direct_reports(person_id))
    
    def find_common_manager(self, person1_id: str, person2_id: str) -> Optional[str]:
        """Find the lowest common manager of two people"""
        chain1 = set(self.get_chain_of_command(person1_id))
        chain2 = self.get_chain_of_command(person2_id)
        
        for person_id in chain2:
            if person_id in chain1:
                return person_id
        
        return None
    
    def can_person_fire(self, firer_id: str, target_id: str) -> bool:
        """Check if one person can fire another"""
        firer = self.get_person(firer_id)
        return firer.can_fire_person(target_id, self) if firer else False
    
    # -----------------------------------------------------------------------
    # serialization
    # -----------------------------------------------------------------------
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert org chart to dictionary"""
        return {
            "people": {pid: {
                "person_id": p.person_id,
                "roles": [{"title": r.title, "role_type": r.role_type.value, 
                          "department": r.department, "level": r.level} for r in p.roles],
                "direct_reports": p.direct_reports,
                "manager": p.manager,
                "employment_status": p.employment_status
            } for pid, p in self.people.items()},
            "shareholders": {sid: {
                "entity_id": s.entity_id,
                "pct_ownership": s.pct_ownership,
                "voting_pct": s.voting_pct,
                "share_class": s.share_class
            } for sid, s in self.shareholders.items()},
            "board_composition": self.board_composition,
            "committees": self.committees,
            "org_policies": self.org_policies
        } 