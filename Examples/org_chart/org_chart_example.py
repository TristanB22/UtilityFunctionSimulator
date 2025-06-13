# org_chart_example.py
# Example demonstrating the comprehensive organizational chart functionality

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Firm.org_chart import OrgChart, Role, RoleType, VotingRights, Shareholder
from Firm.firm import BaseFirm

def create_example_company():
    """Create an example company with a complex org structure"""
    
    # Create a firm
    firm = BaseFirm(
        name="TechCorp Inc.",
        legal_form="corporation",
        naics="541511",  # Custom Computer Programming Services
        hq_location="us/ca/san_francisco"
    )
    
    # Define some roles
    ceo_role = Role(
        title="Chief Executive Officer",
        role_type=RoleType.EXECUTIVE,
        department="Executive",
        level=1,
        can_hire=True,
        can_fire=True,
        can_fire_roles=["Vice President", "Director", "Manager", "Employee"],
        voting_rights=VotingRights.FULL,
        salary_band=(300000, 500000)
    )
    
    board_member_role = Role(
        title="Board Member",
        role_type=RoleType.BOARD_MEMBER,
        level=0,
        voting_rights=VotingRights.FULL,
        voting_matters=["strategic_decisions", "executive_compensation", "board_elections"]
    )
    
    cto_role = Role(
        title="Chief Technology Officer",
        role_type=RoleType.EXECUTIVE,
        department="Engineering",
        level=1,
        can_hire=True,
        can_fire=True,
        can_fire_roles=["Vice President", "Director", "Manager", "Employee"],
        salary_band=(250000, 400000)
    )
    
    eng_manager_role = Role(
        title="Engineering Manager",
        role_type=RoleType.MANAGER,
        department="Engineering",
        level=3,
        can_hire=True,
        can_fire=True,
        can_fire_roles=["Engineer", "Senior Engineer"],
        salary_band=(150000, 200000)
    )
    
    engineer_role = Role(
        title="Software Engineer",
        role_type=RoleType.EMPLOYEE,
        department="Engineering",
        level=4,
        salary_band=(120000, 180000)
    )
    
    # Add people to the organization
    
    # CEO who is also a board member (multiple roles)
    firm.hire("alice_ceo", [ceo_role, board_member_role])
    
    # CTO reporting to CEO
    firm.hire("bob_cto", [cto_role], manager="alice_ceo")
    
    # Board members (some external, some internal)
    external_board_role = Role(
        title="Independent Board Member",
        role_type=RoleType.BOARD_MEMBER,
        level=0,
        voting_rights=VotingRights.FULL
    )
    
    firm.hire("charlie_board", [external_board_role])
    firm.hire("diana_board", [external_board_role])
    
    # Engineering team
    firm.hire("eve_manager", [eng_manager_role], manager="bob_cto")
    firm.hire("frank_engineer", [engineer_role], manager="eve_manager")
    firm.hire("grace_engineer", [engineer_role], manager="eve_manager")
    
    # Add shareholders
    firm.add_shareholder("alice_ceo", 0.25, share_class="common")      # CEO owns 25%
    firm.add_shareholder("venture_capital", 0.40, share_class="preferred")  # VC owns 40%
    firm.add_shareholder("founder_pool", 0.20, share_class="common")   # Other founders 20%
    firm.add_shareholder("employee_pool", 0.15, share_class="common")  # Employee stock 15%
    
    # Add some committees
    firm.org_chart.add_to_committee("compensation", "alice_ceo")
    firm.org_chart.add_to_committee("compensation", "charlie_board")
    firm.org_chart.add_to_committee("audit", "diana_board")
    firm.org_chart.add_to_committee("audit", "charlie_board")
    
    return firm

def demonstrate_org_functionality(firm):
    """Demonstrate various organizational chart capabilities"""
    
    print("=== TECHCORP INC. ORGANIZATIONAL ANALYSIS ===\n")
    
    # 1. Basic org structure
    print("1. ORGANIZATIONAL STRUCTURE:")
    print(f"Total employees: {len(firm.get_employees())}")
    print(f"Executives: {firm.get_executives()}")
    print(f"Managers: {firm.get_managers()}")
    print(f"Board members: {firm.get_board_members()}")
    print()
    
    # 2. Chain of command
    print("2. CHAIN OF COMMAND:")
    for person_id in ["frank_engineer", "eve_manager", "bob_cto"]:
        chain = firm.get_chain_of_command(person_id)
        print(f"{person_id}: {' → '.join(chain)}")
    print()
    
    # 3. Management spans
    print("3. MANAGEMENT SPANS:")
    for person_id in ["alice_ceo", "bob_cto", "eve_manager"]:
        reports = firm.org_chart.get_direct_reports(person_id)
        all_reports = firm.org_chart.get_all_reports(person_id)
        print(f"{person_id}: {len(reports)} direct, {len(all_reports)} total reports")
    print()
    
    # 4. Ownership structure
    print("4. OWNERSHIP STRUCTURE:")
    ownership = firm.get_ownership_structure()
    for entity, pct in ownership.items():
        voting_power = firm.get_voting_power(entity)
        print(f"{entity}: {pct:.1%} ownership, {voting_power:.1%} voting power")
    print()
    
    # 5. Authority checks
    print("5. AUTHORITY CHECKS:")
    
    # Can CEO fire people?
    can_fire_cto = firm.can_fire_employee("alice_ceo", "bob_cto")
    can_fire_engineer = firm.can_fire_employee("alice_ceo", "frank_engineer")
    print(f"CEO can fire CTO: {can_fire_cto}")
    print(f"CEO can fire engineer: {can_fire_engineer}")
    
    # Can manager fire engineer?
    can_manager_fire = firm.can_fire_employee("eve_manager", "frank_engineer")
    print(f"Manager can fire engineer: {can_manager_fire}")
    
    # Can engineer fire CEO? (should be False)
    can_engineer_fire_ceo = firm.can_fire_employee("frank_engineer", "alice_ceo")
    print(f"Engineer can fire CEO: {can_engineer_fire_ceo}")
    
    # Board dynamics
    can_remove_board = firm.can_remove_board_member("alice_ceo", "charlie_board")
    print(f"CEO can remove board member: {can_remove_board}")
    print()
    
    # 6. Committee membership
    print("6. COMMITTEE MEMBERSHIP:")
    for committee in ["compensation", "audit"]:
        members = firm.org_chart.get_committee_members(committee)
        print(f"{committee.title()} Committee: {members}")
    print()
    
    # 7. Role analysis
    print("7. ROLE ANALYSIS:")
    alice = firm.org_chart.get_person("alice_ceo")
    if alice:
        print(f"Alice's roles:")
        for role in alice.roles:
            print(f"  - {role.title} (Level {role.level}, {role.role_type.value})")
            print(f"    Can hire: {role.can_hire}, Can fire: {role.can_fire}")
            print(f"    Voting rights: {role.voting_rights.value}")
    print()
    
    # 8. Department breakdown
    print("8. DEPARTMENT BREAKDOWN:")
    eng_people = firm.org_chart.get_people_by_department("Engineering")
    exec_people = firm.org_chart.get_people_by_department("Executive")
    print(f"Engineering: {eng_people}")
    print(f"Executive: {exec_people}")
    print()

if __name__ == "__main__":
    # Create and analyze the example company
    company = create_example_company()
    demonstrate_org_functionality(company)
    
    print("=== TESTING ORGANIZATIONAL CHANGES ===\n")
    
    # Test some organizational changes
    print("9. TESTING ORGANIZATIONAL CHANGES:")
    
    # Promote an engineer to senior engineer
    senior_eng_role = Role(
        title="Senior Software Engineer",
        role_type=RoleType.EMPLOYEE,
        department="Engineering",
        level=4,
        can_hire=True,  # Senior engineers can hire junior engineers
        salary_band=(140000, 200000)
    )
    
    success = company.promote("frank_engineer", senior_eng_role)
    print(f"Promoted Frank to Senior Engineer: {success}")
    
    # Check Frank's new roles
    frank = company.org_chart.get_person("frank_engineer")
    if frank:
        print(f"Frank's roles after promotion: {[r.title for r in frank.roles]}")
    
    # Fire someone (manager fires engineer)
    company.hire("new_junior", [Role(
        title="Junior Engineer",
        role_type=RoleType.EMPLOYEE,
        department="Engineering",
        level=5,
        salary_band=(90000, 120000)
    )], manager="eve_manager")
    
    print(f"Hired new junior engineer")
    print(f"Eve's reports before firing: {company.org_chart.get_direct_reports('eve_manager')}")
    
    # Manager fires the junior
    if company.can_fire_employee("eve_manager", "new_junior"):
        fired = company.fire("new_junior")
        print(f"Manager fired junior engineer: {fired}")
        print(f"Eve's reports after firing: {company.org_chart.get_direct_reports('eve_manager')}")
    
    print("\nExample completed successfully!") 