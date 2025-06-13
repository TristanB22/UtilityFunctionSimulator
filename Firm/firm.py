# base_firm.py
# universal shell for any kind of firm, bank, nonprofit, or government agency

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Any
from uuid import uuid4
from datetime import date
import yaml
import pathlib

# Import from our new org_chart module
from .org_chart import OrgChart, Shareholder, Role, RoleType, VotingRights

# ---------------------------------------------------------------------------
# helper types
# ---------------------------------------------------------------------------

Money = float  # usd unless otherwise noted

@dataclass
class License:
    name: str
    issuing_authority: str
    expiry: date | None = None

@dataclass
class Transaction:
    """simple double-entry journal line"""
    debit_account: str
    credit_account: str
    amount: Money
    memo: str = ""

# ---------------------------------------------------------------------------
# the firm
# ---------------------------------------------------------------------------

@dataclass
class BaseFirm:
    # identity
    name: str
    entity_id: str = field(default_factory=lambda: uuid4().hex)
    legal_form: str = "corporation"              # llc, coop, agency…
    naics: str | None = None                     # 6-digit industry code
    founded: date | None = None
    hq_location: str | None = None               # e.g. "us/ca/san_francisco"

    # organizational structure - now using comprehensive org chart
    org_chart: OrgChart = field(default_factory=OrgChart)

    # regulatory footprint
    licenses: List[License] = field(default_factory=list)
    regulation_tags: List[str] = field(default_factory=list)       # e.g. ["epa","osha"]

    # financial statements (period close; all Money units)
    balance_sheet: Dict[str, Money] = field(default_factory=lambda: {
        "assets": 0.0, "liabilities": 0.0, "equity": 0.0
    })
    income_statement: Dict[str, Money] = field(default_factory=lambda: {
        "revenue": 0.0, "cogs": 0.0, "opex": 0.0,
        "interest": 0.0, "tax": 0.0, "net_income": 0.0
    })
    cash_flow: Dict[str, Money] = field(default_factory=lambda: {
        "operating": 0.0, "investing": 0.0, "financing": 0.0
    })

    # live operational state
    inventory: Dict[str, float] = field(default_factory=dict)      # good_id → qty
    resources: Dict[str, float] = field(default_factory=dict)      # ore reserves, bandwidth, etc.
    ledger: List[Transaction] = field(default_factory=list)        # raw journal lines

    # -----------------------------------------------------------------------
    # workforce management (now delegated to org_chart)
    # -----------------------------------------------------------------------

    def hire(self, person_id: str, roles: List[Role] = None, manager: str = None) -> None:
        """add a person to the organization with specified roles"""
        self.org_chart.add_person(person_id, roles, manager)

    def fire(self, person_id: str) -> bool:
        """remove a person from organization"""
        return self.org_chart.remove_person(person_id)

    def promote(self, person_id: str, new_role: Role) -> bool:
        """promote someone by adding a new role"""
        return self.org_chart.assign_role(person_id, new_role)

    def get_employees(self) -> List[str]:
        """get all employee IDs"""
        return list(self.org_chart.people.keys())

    def get_managers(self) -> List[str]:
        """get all people with management roles"""
        return self.org_chart.get_people_by_role_type(RoleType.MANAGER)

    def get_executives(self) -> List[str]:
        """get all executives"""
        return self.org_chart.get_people_by_role_type(RoleType.EXECUTIVE)

    def get_board_members(self) -> List[str]:
        """get all board members"""
        return self.org_chart.board_composition

    # -----------------------------------------------------------------------
    # shareholder management (delegated to org_chart)
    # -----------------------------------------------------------------------

    def add_shareholder(self, entity_id: str, ownership_pct: float, 
                       voting_pct: float = None, share_class: str = "common") -> None:
        """add a shareholder"""
        shareholder = Shareholder(
            entity_id=entity_id,
            pct_ownership=ownership_pct,
            voting_pct=voting_pct,
            share_class=share_class
        )
        self.org_chart.add_shareholder(shareholder)

    def get_shareholders(self) -> Dict[str, Shareholder]:
        """get all shareholders"""
        return self.org_chart.shareholders

    def get_ownership_structure(self) -> Dict[str, float]:
        """get ownership percentages"""
        return self.org_chart.get_total_ownership()

    def get_voting_power(self, entity_id: str) -> float:
        """get total voting power for an entity"""
        return self.org_chart.get_voting_power(entity_id)

    # -----------------------------------------------------------------------
    # accounting helpers
    # -----------------------------------------------------------------------

    def post(self, debit: str, credit: str, amount: Money, memo: str = "") -> None:
        """record a double-entry transaction and update balance sheet"""
        self.ledger.append(Transaction(debit, credit, amount, memo))

        # simplistic: assets positive, liabilities & equity negative
        self._update_bs(debit, amount)
        self._update_bs(credit, -amount)

    def _update_bs(self, account: str, delta: Money) -> None:
        if account not in self.balance_sheet:
            self.balance_sheet[account] = 0.0
        self.balance_sheet[account] += delta
        # maintain accounting identity
        assets = self.balance_sheet.get("assets", 0.0)
        liab = self.balance_sheet.get("liabilities", 0.0)
        self.balance_sheet["equity"] = assets - liab

    # -----------------------------------------------------------------------
    # period close utilities
    # -----------------------------------------------------------------------

    def close_income_statement(self) -> None:
        """transfer net income to equity and zero income statement"""
        ni = (self.income_statement["revenue"]
              - self.income_statement["cogs"]
              - self.income_statement["opex"]
              - self.income_statement["interest"]
              - self.income_statement["tax"])
        self.income_statement["net_income"] = ni
        self.post("income_summary", "equity", ni)
        for k in self.income_statement:
            if k != "net_income":
                self.income_statement[k] = 0.0

    # -----------------------------------------------------------------------
    # compliance stubs
    # -----------------------------------------------------------------------

    def has_license(self, name: str) -> bool:
        return any(l.name == name for l in self.licenses)

    def check_risk_limits(self) -> bool:
        """placeholder for solvency / capital rules"""
        return self.balance_sheet["equity"] >= 0

    # -----------------------------------------------------------------------
    # governance and authority checks
    # -----------------------------------------------------------------------

    def can_fire_employee(self, firer_id: str, target_id: str) -> bool:
        """check if someone can fire another employee"""
        return self.org_chart.can_person_fire(firer_id, target_id)

    def can_remove_board_member(self, remover_id: str, target_id: str) -> bool:
        """check if someone can remove a board member"""
        return self.org_chart.can_remove_board_member(remover_id, target_id)

    def get_chain_of_command(self, person_id: str) -> List[str]:
        """get the management chain for a person"""
        return self.org_chart.get_chain_of_command(person_id)

    # -----------------------------------------------------------------------
    # serialization helpers
    # -----------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["type"] = self.__class__.__name__
        # Convert org_chart to dict
        d["org_chart"] = self.org_chart.to_dict()
        return d

    # -----------------------------------------------------------------------
    # yaml factory (for data-driven instantiation)
    # -----------------------------------------------------------------------

    @classmethod
    def from_yaml(cls, path: str | pathlib.Path) -> "BaseFirm":
        with open(path, "r", encoding="utf-8") as fp:
            cfg = yaml.safe_load(fp)
        
        # Handle org_chart if present in YAML
        if "org_chart" in cfg:
            org_data = cfg.pop("org_chart")
            # This would need more complex logic to reconstruct the org chart
            # For now, create empty org chart and let user populate it
        
        # convert nested license dicts to dataclasses
        cfg["licenses"] = [License(**l) for l in cfg.get("licenses", [])]
        return cls(**cfg)
