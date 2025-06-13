# financial_firm.py
# NAICS 52: Finance and Insurance

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class FinancialServiceType(Enum):
    BANKING = "banking"
    INVESTMENT_BANKING = "investment_banking"
    INSURANCE = "insurance"
    ASSET_MANAGEMENT = "asset_management"
    SECURITIES_TRADING = "securities_trading"
    CREDIT_UNION = "credit_union"

class RiskRating(Enum):
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    CCC = "CCC"
    DEFAULT = "DEFAULT"

@dataclass
class LoanPortfolio:
    loan_id: str
    borrower_id: str
    principal_amount: float
    interest_rate: float
    maturity_date: date
    collateral_value: float
    risk_rating: RiskRating
    payment_schedule: Dict[date, float] = field(default_factory=dict)

@dataclass
class SecurityHolding:
    security_id: str
    security_type: str  # bond, stock, derivative
    quantity: float
    purchase_price: float
    current_market_value: float
    portfolio_allocation: str  # trading, available_for_sale, held_to_maturity

@dataclass
class FinancialFirm(BaseFirm):
    # Core financial services
    service_types: List[FinancialServiceType] = field(default_factory=list)
    regulatory_authorizations: List[str] = field(default_factory=list)  # banking license, etc.
    
    # Banking operations
    deposit_accounts: Dict[str, float] = field(default_factory=dict)  # account_id -> balance
    loan_portfolio: List[LoanPortfolio] = field(default_factory=list)
    credit_loss_reserves: float = 0.0
    net_interest_margin: float = 0.035  # 3.5% default NIM
    
    # Investment portfolio
    security_holdings: List[SecurityHolding] = field(default_factory=list)
    trading_portfolio_value: float = 0.0
    available_for_sale_portfolio: float = 0.0
    mark_to_market_adjustments: Dict[str, float] = field(default_factory=dict)
    
    # Risk management
    value_at_risk: float = 0.0  # VaR calculation
    tier_1_capital_ratio: float = 0.12  # regulatory capital
    risk_weighted_assets: float = 0.0
    stress_test_results: Dict[str, float] = field(default_factory=dict)
    
    # Regulatory compliance
    regulatory_capital_requirements: Dict[str, float] = field(default_factory=dict)
    liquidity_coverage_ratio: float = 1.0
    leverage_ratio: float = 0.05
    compliance_costs: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            self.naics = "52"  # Finance and Insurance
    
    # Banking operations
    def create_deposit_account(self, customer_id: str, initial_deposit: float) -> str:
        """Create new deposit account"""
        account_id = f"dep_{customer_id}_{len(self.deposit_accounts)}"
        self.deposit_accounts[account_id] = initial_deposit
        
        # Record deposit liability
        self.post("cash", "customer_deposits", initial_deposit, f"New deposit: {account_id}")
        return account_id
    
    def originate_loan(self, borrower_id: str, amount: float, rate: float, 
                      maturity: date, collateral_value: float = 0) -> str:
        """Originate new loan"""
        loan = LoanPortfolio(
            loan_id=f"loan_{borrower_id}_{len(self.loan_portfolio)}",
            borrower_id=borrower_id,
            principal_amount=amount,
            interest_rate=rate,
            maturity_date=maturity,
            collateral_value=collateral_value,
            risk_rating=RiskRating.BBB  # default rating
        )
        
        self.loan_portfolio.append(loan)
        
        # Record loan asset and cash outflow
        self.post("loans_receivable", "cash", amount, f"Loan origination: {loan.loan_id}")
        
        return loan.loan_id
    
    def calculate_interest_income(self) -> float:
        """Calculate total interest income from loan portfolio"""
        total_income = 0.0
        for loan in self.loan_portfolio:
            annual_income = loan.principal_amount * loan.interest_rate
            total_income += annual_income
        
        self.income_statement["revenue"] += total_income
        return total_income
    
    def assess_credit_risk(self, loan_id: str) -> RiskRating:
        """Assess credit risk for specific loan"""
        loan = next((l for l in self.loan_portfolio if l.loan_id == loan_id), None)
        if not loan:
            return RiskRating.DEFAULT
        
        # Simplified risk assessment based on collateral coverage
        collateral_ratio = loan.collateral_value / loan.principal_amount if loan.principal_amount > 0 else 0
        
        if collateral_ratio > 1.5:
            return RiskRating.AAA
        elif collateral_ratio > 1.2:
            return RiskRating.AA
        elif collateral_ratio > 1.0:
            return RiskRating.A
        elif collateral_ratio > 0.8:
            return RiskRating.BBB
        else:
            return RiskRating.BB
    
    # Investment operations
    def purchase_security(self, security_id: str, security_type: str, quantity: float, 
                         price: float, portfolio_type: str) -> None:
        """Purchase securities for investment portfolio"""
        holding = SecurityHolding(
            security_id=security_id,
            security_type=security_type,
            quantity=quantity,
            purchase_price=price,
            current_market_value=quantity * price,
            portfolio_allocation=portfolio_type
        )
        
        self.security_holdings.append(holding)
        
        # Record investment
        total_cost = quantity * price
        account_name = f"securities_{portfolio_type}"
        self.post(account_name, "cash", total_cost, f"Security purchase: {security_id}")
        
        if portfolio_type == "trading":
            self.trading_portfolio_value += total_cost
        elif portfolio_type == "available_for_sale":
            self.available_for_sale_portfolio += total_cost
    
    def mark_to_market(self, security_id: str, new_market_price: float) -> float:
        """Mark security to market value"""
        holding = next((h for h in self.security_holdings if h.security_id == security_id), None)
        if not holding:
            return 0.0
        
        old_value = holding.current_market_value
        new_value = holding.quantity * new_market_price
        mark_to_market_gain_loss = new_value - old_value
        
        holding.current_market_value = new_value
        
        # Record unrealized gain/loss based on portfolio type
        if holding.portfolio_allocation == "trading":
            # Trading securities: gains/losses go to income statement
            self.income_statement["revenue"] += mark_to_market_gain_loss
        elif holding.portfolio_allocation == "available_for_sale":
            # AFS securities: gains/losses go to other comprehensive income
            self.mark_to_market_adjustments[security_id] = mark_to_market_gain_loss
        
        return mark_to_market_gain_loss
    
    # Risk management
    def calculate_value_at_risk(self, confidence_level: float = 0.95, 
                              time_horizon_days: int = 1) -> float:
        """Calculate Value at Risk for portfolio"""
        # Simplified VaR calculation using portfolio value and volatility assumption
        total_portfolio_value = (self.trading_portfolio_value + 
                               self.available_for_sale_portfolio)
        
        # Assume 2% daily volatility for simplification
        daily_volatility = 0.02
        
        # Normal distribution VaR calculation
        import math
        z_score = 1.645 if confidence_level == 0.95 else 2.33  # 95% or 99%
        var = total_portfolio_value * daily_volatility * z_score * math.sqrt(time_horizon_days)
        
        self.value_at_risk = var
        return var
    
    def calculate_capital_ratios(self) -> Dict[str, float]:
        """Calculate regulatory capital ratios"""
        # Simplified capital calculation
        tier1_capital = self.balance_sheet.get("equity", 0) * 0.8  # assume 80% qualifies as Tier 1
        
        # Risk-weighted assets calculation (simplified)
        self.risk_weighted_assets = sum(loan.principal_amount * 1.0 for loan in self.loan_portfolio)  # 100% risk weight
        self.risk_weighted_assets += self.trading_portfolio_value * 1.25  # 125% risk weight for trading
        
        if self.risk_weighted_assets > 0:
            self.tier_1_capital_ratio = tier1_capital / self.risk_weighted_assets
            self.leverage_ratio = tier1_capital / self.balance_sheet.get("assets", 1)
        
        return {
            "tier1_capital_ratio": self.tier_1_capital_ratio,
            "leverage_ratio": self.leverage_ratio,
            "risk_weighted_assets": self.risk_weighted_assets
        }
    
    # Regulatory compliance
    def conduct_stress_test(self, scenario_name: str, loss_rate: float) -> float:
        """Conduct regulatory stress test"""
        # Apply stress scenario to loan portfolio
        stressed_losses = 0.0
        for loan in self.loan_portfolio:
            stressed_loss = loan.principal_amount * loss_rate
            stressed_losses += stressed_loss
        
        # Apply to trading portfolio
        trading_losses = self.trading_portfolio_value * loss_rate * 1.5  # higher impact on trading
        
        total_stressed_losses = stressed_losses + trading_losses
        self.stress_test_results[scenario_name] = total_stressed_losses
        
        # Check if capital would remain adequate
        post_stress_capital = self.balance_sheet.get("equity", 0) - total_stressed_losses
        post_stress_capital_ratio = post_stress_capital / max(self.risk_weighted_assets, 1)
        
        return post_stress_capital_ratio
    
    def file_regulatory_reports(self, report_type: str) -> bool:
        """File required regulatory reports"""
        if report_type == "call_report":
            # Bank Call Report (quarterly)
            report_cost = 50000
        elif report_type == "stress_test":
            # Annual stress test submission
            report_cost = 200000
        else:
            report_cost = 25000
        
        self.compliance_costs += report_cost
        self.post("compliance_costs", "cash", report_cost, f"Regulatory filing: {report_type}")
        return True
    
    # Fee-based services
    def generate_fee_income(self, service_type: str, fee_amount: float) -> None:
        """Generate fee income from services"""
        self.post("cash", "fee_income", fee_amount, f"Fee income: {service_type}")
        self.income_statement["revenue"] += fee_amount
    
    def provide_investment_advisory(self, client_id: str, assets_under_management: float, 
                                  fee_rate: float) -> float:
        """Provide investment advisory services"""
        annual_fee = assets_under_management * fee_rate
        quarterly_fee = annual_fee / 4
        
        self.generate_fee_income("investment_advisory", quarterly_fee)
        return quarterly_fee
    
    # Analytics and reporting
    def get_financial_performance_summary(self) -> Dict[str, Any]:
        """Generate financial performance summary"""
        total_loans = sum(loan.principal_amount for loan in self.loan_portfolio)
        total_deposits = sum(self.deposit_accounts.values())
        
        return {
            "net_interest_margin": self.net_interest_margin,
            "loan_portfolio_size": total_loans,
            "deposit_base": total_deposits,
            "tier1_capital_ratio": self.tier_1_capital_ratio,
            "value_at_risk": self.value_at_risk,
            "credit_loss_reserves": self.credit_loss_reserves,
            "trading_portfolio_value": self.trading_portfolio_value,
            "service_types": [st.value for st in self.service_types]
        } 