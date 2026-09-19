"""
Financial Utilities Module

This module provides comprehensive financial utilities including:
- Financial calculations (interest, loans, investments)
- Currency conversion
- Stock price tracking
- Portfolio management
- Risk analysis
- Financial data analysis
- Tax calculations
- Budget management
- Financial reporting

Note: This module uses requests for API calls.
Install with: pip install requests

All functions include comprehensive docstrings and type hints.
"""

import math
import json
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class InvestmentType(Enum):
    """Types of investments."""
    STOCK = "stock"
    BOND = "bond"
    MUTUAL_FUND = "mutual_fund"
    ETF = "etf"
    CRYPTO = "crypto"
    REAL_ESTATE = "real_estate"
    COMMODITY = "commodity"


class RiskLevel(Enum):
    """Risk levels for investments."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class Investment:
    """Represents an investment."""
    symbol: str
    name: str
    type: InvestmentType
    quantity: float
    purchase_price: float
    current_price: float
    purchase_date: datetime
    risk_level: RiskLevel


@dataclass
class Portfolio:
    """Represents an investment portfolio."""
    name: str
    investments: List[Investment]
    cash_balance: float
    created_date: datetime


@dataclass
class Transaction:
    """Represents a financial transaction."""
    transaction_id: str
    type: str  # buy, sell, deposit, withdraw
    symbol: Optional[str]
    quantity: float
    price: float
    timestamp: datetime
    fees: float = 0.0


class FinancialCalculator:
    """Financial calculation utilities."""
    
    @staticmethod
    def compound_interest(principal: float, rate: float, periods: int,
                        compounding_frequency: int = 1) -> float:
        """Calculate compound interest."""
        # A = P(1 + r/n)^(nt)
        amount = principal * (1 + rate / compounding_frequency) ** (compounding_frequency * periods)
        return amount
    
    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> float:
        """Calculate simple interest."""
        # I = P * r * t
        return principal * rate * time
    
    @staticmethod
    def loan_payment(principal: float, annual_rate: float, 
                    months: int) -> float:
        """Calculate monthly loan payment (amortization)."""
        # M = P * [r(1+r)^n] / [(1+r)^n - 1]
        monthly_rate = annual_rate / 12 / 100
        if monthly_rate == 0:
            return principal / months
        
        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                 ((1 + monthly_rate) ** months - 1)
        return payment
    
    @staticmethod
    def present_value(future_value: float, rate: float, periods: int) -> float:
        """Calculate present value."""
        # PV = FV / (1 + r)^n
        return future_value / (1 + rate) ** periods
    
    @staticmethod
    def future_value(present_value: float, rate: float, periods: int) -> float:
        """Calculate future value."""
        # FV = PV * (1 + r)^n
        return present_value * (1 + rate) ** periods
    
    @staticmethod
    def annuity_payment(present_value: float, rate: float, periods: int) -> float:
        """Calculate annuity payment."""
        # PMT = PV * [r(1+r)^n] / [(1+r)^n - 1]
        if rate == 0:
            return present_value / periods
        
        payment = present_value * (rate * (1 + rate) ** periods) / \
                 ((1 + rate) ** periods - 1)
        return payment
    
    @staticmethod
    def calculate_roi(initial_investment: float, final_value: float) -> float:
        """Calculate return on investment (ROI)."""
        if initial_investment == 0:
            return 0.0
        return ((final_value - initial_investment) / initial_investment) * 100
    
    @staticmethod
    def calculate_cagr(initial_value: float, final_value: float, years: float) -> float:
        """Calculate compound annual growth rate (CAGR)."""
        if initial_value == 0 or years == 0:
            return 0.0
        return ((final_value / initial_value) ** (1 / years) - 1) * 100
    
    @staticmethod
    def calculate_apr(rate: float, compounding_frequency: int = 12) -> float:
        """Calculate annual percentage rate (APR)."""
        return rate * compounding_frequency
    
    @staticmethod
    def calculate_apy(apr: float, compounding_frequency: int = 12) -> float:
        """Calculate annual percentage yield (APY)."""
        return (1 + apr / compounding_frequency) ** compounding_frequency - 1


class CurrencyConverter:
    """Currency conversion utilities."""
    
    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        """Convert currency using exchange rates."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        try:
            # Using free exchange rate API
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get("rates", {})
                
                if to_currency in rates:
                    return amount * rates[to_currency]
            
            return None
        except Exception as e:
            print(f"Currency conversion failed: {e}")
            return None
    
    @staticmethod
    def get_exchange_rates(base_currency: str = "USD") -> Optional[Dict[str, float]]:
        """Get current exchange rates."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required")
        
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("rates", {})
            
            return None
        except Exception as e:
            print(f"Failed to get exchange rates: {e}")
            return None


class StockTracker:
    """Stock price tracking utilities."""
    
    @staticmethod
    def get_stock_price(symbol: str) -> Optional[float]:
        """Get current stock price."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required")
        
        try:
            # Using free financial API (example)
            url = f"https://api.example.com/stock/{symbol}/price"
            # Note: This is a placeholder - in production use real API like Alpha Vantage, Yahoo Finance
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("price")
            
            return None
        except Exception as e:
            print(f"Failed to get stock price: {e}")
            return None
    
    @staticmethod
    def get_stock_history(symbol: str, days: int = 30) -> Optional[List[Dict]]:
        """Get historical stock prices."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required")
        
        try:
            # Placeholder for real API call
            url = f"https://api.example.com/stock/{symbol}/history?days={days}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("history", [])
            
            return None
        except Exception as e:
            print(f"Failed to get stock history: {e}")
            return None


class PortfolioManager:
    """Portfolio management utilities."""
    
    def __init__(self):
        """Initialize portfolio manager."""
        self.portfolios: Dict[str, Portfolio] = {}
        self.transactions: List[Transaction] = []
    
    def create_portfolio(self, name: str, initial_cash: float = 0.0) -> Portfolio:
        """Create a new portfolio."""
        portfolio = Portfolio(
            name=name,
            investments=[],
            cash_balance=initial_cash,
            created_date=datetime.now()
        )
        self.portfolios[name] = portfolio
        return portfolio
    
    def add_investment(self, portfolio_name: str, investment: Investment) -> bool:
        """Add investment to portfolio."""
        if portfolio_name not in self.portfolios:
            return False
        
        self.portfolios[portfolio_name].investments.append(investment)
        return True
    
    def remove_investment(self, portfolio_name: str, symbol: str) -> bool:
        """Remove investment from portfolio."""
        if portfolio_name not in self.portfolios:
            return False
        
        portfolio = self.portfolios[portfolio_name]
        portfolio.investments = [inv for inv in portfolio.investments if inv.symbol != symbol]
        return True
    
    def get_portfolio_value(self, portfolio_name: str) -> float:
        """Calculate total portfolio value."""
        if portfolio_name not in self.portfolios:
            return 0.0
        
        portfolio = self.portfolios[portfolio_name]
        total_value = portfolio.cash_balance
        
        for investment in portfolio.investments:
            total_value += investment.quantity * investment.current_price
        
        return total_value
    
    def get_portfolio_allocation(self, portfolio_name: str) -> Dict[str, float]:
        """Get portfolio allocation by investment."""
        if portfolio_name not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_name]
        allocation = {}
        total_value = self.get_portfolio_value(portfolio_name)
        
        if total_value == 0:
            return allocation
        
        for investment in portfolio.investments:
            value = investment.quantity * investment.current_price
            allocation[investment.symbol] = (value / total_value) * 100
        
        allocation["cash"] = (portfolio.cash_balance / total_value) * 100
        
        return allocation
    
    def calculate_portfolio_return(self, portfolio_name: str) -> float:
        """Calculate portfolio return."""
        if portfolio_name not in self.portfolios:
            return 0.0
        
        portfolio = self.portfolios[portfolio_name]
        total_invested = sum(inv.quantity * inv.purchase_price for inv in portfolio.investments)
        current_value = self.get_portfolio_value(portfolio_name)
        
        if total_invested == 0:
            return 0.0
        
        return FinancialCalculator.calculate_roi(total_invested, current_value)
    
    def rebalance_portfolio(self, portfolio_name: str, 
                          target_allocation: Dict[str, float]) -> Dict[str, float]:
        """Calculate required trades to rebalance portfolio."""
        if portfolio_name not in self.portfolios:
            return {}
        
        portfolio = self.portfolios[portfolio_name]
        current_allocation = self.get_portfolio_allocation(portfolio_name)
        total_value = self.get_portfolio_value(portfolio_name)
        
        required_trades = {}
        
        for symbol, target_percent in target_allocation.items():
            current_percent = current_allocation.get(symbol, 0)
            difference = target_percent - current_percent
            
            required_value = (difference / 100) * total_value
            required_trades[symbol] = required_value
        
        return required_trades


class RiskAnalyzer:
    """Risk analysis utilities."""
    
    @staticmethod
    def calculate_volatility(prices: List[float]) -> float:
        """Calculate volatility (standard deviation of returns)."""
        if len(prices) < 2:
            return 0.0
        
        returns = []
        for i in range(1, len(prices)):
            return_rate = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(return_rate)
        
        if not returns:
            return 0.0
        
        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / len(returns)
        volatility = math.sqrt(variance)
        
        return volatility
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        if not returns:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        volatility = RiskAnalyzer.calculate_volatility([1 + r for r in returns])
        
        if volatility == 0:
            return 0.0
        
        sharpe_ratio = (mean_return - risk_free_rate) / volatility
        return sharpe_ratio
    
    @staticmethod
    def calculate_beta(asset_returns: List[float], market_returns: List[float]) -> float:
        """Calculate beta (systematic risk)."""
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            return 0.0
        
        # Calculate covariance and variance
        mean_asset = sum(asset_returns) / len(asset_returns)
        mean_market = sum(market_returns) / len(market_returns)
        
        covariance = sum((a - mean_asset) * (m - mean_market) 
                       for a, m in zip(asset_returns, market_returns)) / len(asset_returns)
        
        variance = sum((m - mean_market) ** 2 for m in market_returns) / len(market_returns)
        
        if variance == 0:
            return 0.0
        
        beta = covariance / variance
        return beta
    
    @staticmethod
    def calculate_var(prices: List[float], confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk (VaR)."""
        if not prices:
            return 0.0
        
        # Calculate returns
        returns = []
        for i in range(1, len(prices)):
            return_rate = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(return_rate)
        
        if not returns:
            return 0.0
        
        # Sort returns
        sorted_returns = sorted(returns)
        
        # Calculate VaR
        index = int((1 - confidence_level) * len(sorted_returns))
        var = sorted_returns[index] if index < len(sorted_returns) else sorted_returns[-1]
        
        return abs(var)


class TaxCalculator:
    """Tax calculation utilities."""
    
    @staticmethod
    def calculate_income_tax(income: float, tax_brackets: List[Tuple[float, float]]) -> float:
        """Calculate income tax using progressive tax brackets."""
        # tax_brackets: list of (upper_limit, rate) tuples
        total_tax = 0.0
        remaining_income = income
        
        for i, (limit, rate) in enumerate(tax_brackets):
            if i == 0:
                taxable = min(income, limit)
            else:
                taxable = min(max(0, income - tax_brackets[i-1][0]), limit - tax_brackets[i-1][0])
            
            total_tax += taxable * rate
            remaining_income -= taxable
            
            if remaining_income <= 0:
                break
        
        return total_tax
    
    @staticmethod
    def calculate_capital_gains_tax(profit: float, holding_period: int,
                                   short_term_rate: float = 0.25,
                                   long_term_rate: float = 0.15) -> float:
        """Calculate capital gains tax."""
        if holding_period >= 365:  # Long-term (1 year)
            return profit * long_term_rate
        else:  # Short-term
            return profit * short_term_rate
    
    @staticmethod
    def calculate_dividend_tax(dividend: float, tax_rate: float = 0.15) -> float:
        """Calculate dividend tax."""
        return dividend * tax_rate


class BudgetManager:
    """Budget management utilities."""
    
    def __init__(self):
        """Initialize budget manager."""
        self.income: List[Dict] = []
        self.expenses: List[Dict] = []
        self.categories: Dict[str, float] = {}
        self.savings_goals: Dict[str, float] = {}
    
    def add_income(self, source: str, amount: float, frequency: str = "monthly") -> None:
        """Add income source."""
        self.income.append({
            "source": source,
            "amount": amount,
            "frequency": frequency,
            "date": datetime.now()
        })
    
    def add_expense(self, category: str, amount: float, 
                   description: str = "") -> None:
        """Add expense."""
        self.expenses.append({
            "category": category,
            "amount": amount,
            "description": description,
            "date": datetime.now()
        })
    
    def set_category_budget(self, category: str, budget: float) -> None:
        """Set budget for a category."""
        self.categories[category] = budget
    
    def get_total_income(self) -> float:
        """Calculate total monthly income."""
        total = 0.0
        for income in self.income:
            if income["frequency"] == "monthly":
                total += income["amount"]
            elif income["frequency"] == "weekly":
                total += income["amount"] * 4
            elif income["frequency"] == "yearly":
                total += income["amount"] / 12
        return total
    
    def get_total_expenses(self) -> float:
        """Calculate total monthly expenses."""
        return sum(expense["amount"] for expense in self.expenses)
    
    def get_category_spending(self, category: str) -> float:
        """Get spending for specific category."""
        return sum(expense["amount"] for expense in self.expenses 
                  if expense["category"] == category)
    
    def get_budget_status(self) -> Dict[str, Dict]:
        """Get budget status for all categories."""
        status = {}
        
        for category, budget in self.categories.items():
            spent = self.get_category_spending(category)
            remaining = budget - spent
            percentage = (spent / budget * 100) if budget > 0 else 0
            
            status[category] = {
                "budget": budget,
                "spent": spent,
                "remaining": remaining,
                "percentage": percentage,
                "over_budget": spent > budget
            }
        
        return status
    
    def set_savings_goal(self, goal_name: str, target_amount: float) -> None:
        """Set savings goal."""
        self.savings_goals[goal_name] = target_amount
    
    def get_savings_progress(self) -> Dict[str, Dict]:
        """Get progress towards savings goals."""
        total_income = self.get_total_income()
        total_expenses = self.get_total_expenses()
        monthly_savings = total_income - total_expenses
        
        progress = {}
        for goal_name, target_amount in self.savings_goals.items():
            progress[goal_name] = {
                "target": target_amount,
                "monthly_savings": monthly_savings,
                "months_required": target_amount / monthly_savings if monthly_savings > 0 else float('inf')
            }
        
        return progress


class FinancialReporter:
    """Financial reporting utilities."""
    
    @staticmethod
    def generate_income_statement(income: List[Dict], expenses: List[Dict]) -> Dict:
        """Generate income statement."""
        total_income = sum(item["amount"] for item in income)
        total_expenses = sum(item["amount"] for item in expenses)
        net_income = total_income - total_expenses
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "profit_margin": (net_income / total_income * 100) if total_income > 0 else 0
        }
    
    @staticmethod
    def generate_balance_sheet(assets: Dict, liabilities: Dict) -> Dict:
        """Generate balance sheet."""
        total_assets = sum(assets.values())
        total_liabilities = sum(liabilities.values())
        equity = total_assets - total_liabilities
        
        return {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "equity": equity,
            "debt_to_equity": total_liabilities / equity if equity > 0 else 0
        }
    
    @staticmethod
    def generate_cash_flow(inflows: List[Dict], outflows: List[Dict]) -> Dict:
        """Generate cash flow statement."""
        total_inflows = sum(item["amount"] for item in inflows)
        total_outflows = sum(item["amount"] for item in outflows)
        net_cash_flow = total_inflows - total_outflows
        
        return {
            "total_inflows": total_inflows,
            "total_outflows": total_outflows,
            "net_cash_flow": net_cash_flow
        }


class InvestmentAnalyzer:
    """Investment analysis utilities."""
    
    @staticmethod
    def calculate_dividend_yield(dividend: float, stock_price: float) -> float:
        """Calculate dividend yield."""
        if stock_price == 0:
            return 0.0
        return (dividend / stock_price) * 100
    
    @staticmethod
    def calculate_pe_ratio(price: float, earnings_per_share: float) -> float:
        """Calculate price-to-earnings ratio."""
        if earnings_per_share == 0:
            return 0.0
        return price / earnings_per_share
    
    @staticmethod
    def calculate_pbr_ratio(price: float, book_value_per_share: float) -> float:
        """Calculate price-to-book ratio."""
        if book_value_per_share == 0:
            return 0.0
        return price / book_value_per_share
    
    @staticmethod
    def calculate_dcf_value(future_cash_flows: List[float], discount_rate: float) -> float:
        """Calculate discounted cash flow (DCF) value."""
        present_value = 0.0
        
        for i, cash_flow in enumerate(future_cash_flows):
            pv = cash_flow / ((1 + discount_rate) ** (i + 1))
            present_value += pv
        
        return present_value
    
    @staticmethod
    def calculate_macaulay_duration(cash_flows: List[float], 
                                    times: List[float], 
                                    yield_rate: float) -> float:
        """Calculate Macaulay duration for bonds."""
        total_pv = 0.0
        weighted_time = 0.0
        
        for cash_flow, time in zip(cash_flows, times):
            pv = cash_flow / ((1 + yield_rate) ** time)
            total_pv += pv
            weighted_time += time * pv
        
        if total_pv == 0:
            return 0.0
        
        duration = weighted_time / total_pv
        return duration


def demonstrate_financial_utils():
    """Demonstrate financial utilities functionality."""
    print("=== Financial Utilities Demonstration ===\n")
    
    # Financial Calculations
    print("1. Financial Calculations:")
    principal = 10000
    rate = 0.05
    periods = 10
    
    compound_interest = FinancialCalculator.compound_interest(principal, rate, periods)
    print(f"   Compound interest: ${compound_interest:.2f}")
    
    simple_interest = FinancialCalculator.simple_interest(principal, rate, periods)
    print(f"   Simple interest: ${simple_interest:.2f}")
    
    loan_payment = FinancialCalculator.loan_payment(200000, 0.06, 360)
    print(f"   Monthly loan payment: ${loan_payment:.2f}")
    
    roi = FinancialCalculator.calculate_roi(1000, 1500)
    print(f"   ROI: {roi:.2f}%")
    
    cagr = FinancialCalculator.calculate_cagr(1000, 2000, 5)
    print(f"   CAGR: {cagr:.2f}%")
    
    # Currency Conversion
    print("\n2. Currency Conversion:")
    if REQUESTS_AVAILABLE:
        converted = CurrencyConverter.convert(100, "USD", "EUR")
        print(f"   100 USD = {converted:.2f} EUR")
        
        rates = CurrencyConverter.get_exchange_rates("USD")
        if rates:
            print(f"   Available currencies: {len(rates)}")
    else:
        print("   Install requests: pip install requests")
    
    # Portfolio Management
    print("\n3. Portfolio Management:")
    portfolio_manager = PortfolioManager()
    portfolio = portfolio_manager.create_portfolio("My Portfolio", 10000)
    
    investment1 = Investment(
        symbol="AAPL",
        name="Apple Inc.",
        type=InvestmentType.STOCK,
        quantity=10,
        purchase_price=150.0,
        current_price=175.0,
        purchase_date=datetime.now(),
        risk_level=RiskLevel.MEDIUM
    )
    
    investment2 = Investment(
        symbol="GOOGL",
        name="Alphabet Inc.",
        type=InvestmentType.STOCK,
        quantity=5,
        purchase_price=120.0,
        current_price=140.0,
        purchase_date=datetime.now(),
        risk_level=RiskLevel.MEDIUM
    )
    
    portfolio_manager.add_investment("My Portfolio", investment1)
    portfolio_manager.add_investment("My Portfolio", investment2)
    
    portfolio_value = portfolio_manager.get_portfolio_value("My Portfolio")
    print(f"   Portfolio value: ${portfolio_value:.2f}")
    
    allocation = portfolio_manager.get_portfolio_allocation("My Portfolio")
    print(f"   Allocation: {allocation}")
    
    portfolio_return = portfolio_manager.calculate_portfolio_return("My Portfolio")
    print(f"   Portfolio return: {portfolio_return:.2f}%")
    
    # Risk Analysis
    print("\n4. Risk Analysis:")
    prices = [100, 102, 98, 105, 103, 108, 106, 110, 109, 112]
    
    volatility = RiskAnalyzer.calculate_volatility(prices)
    print(f"   Volatility: {volatility:.4f}")
    
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    sharpe_ratio = RiskAnalyzer.calculate_sharpe_ratio(returns)
    print(f"   Sharpe ratio: {sharpe_ratio:.4f}")
    
    var = RiskAnalyzer.calculate_var(prices)
    print(f"   Value at Risk (95%): {var:.4f}")
    
    # Tax Calculations
    print("\n5. Tax Calculations:")
    tax_brackets = [
        (10000, 0.10),
        (40000, 0.15),
        (85000, 0.25),
        (170000, 0.28),
        (float('inf'), 0.33)
    ]
    
    income_tax = TaxCalculator.calculate_income_tax(50000, tax_brackets)
    print(f"   Income tax on $50,000: ${income_tax:.2f}")
    
    capital_gains_tax = TaxCalculator.calculate_capital_gains_tax(5000, 400)
    print(f"   Capital gains tax (long-term): ${capital_gains_tax:.2f}")
    
    # Budget Management
    print("\n6. Budget Management:")
    budget_manager = BudgetManager()
    
    budget_manager.add_income("Salary", 5000, "monthly")
    budget_manager.add_income("Freelance", 1000, "monthly")
    
    budget_manager.add_expense("Rent", 1500, "Monthly rent")
    budget_manager.add_expense("Food", 500, "Groceries")
    budget_manager.add_expense("Transportation", 300, "Gas and parking")
    
    budget_manager.set_category_budget("Rent", 1500)
    budget_manager.set_category_budget("Food", 600)
    
    total_income = budget_manager.get_total_income()
    total_expenses = budget_manager.get_total_expenses()
    print(f"   Total income: ${total_income:.2f}")
    print(f"   Total expenses: ${total_expenses:.2f}")
    print(f"   Net savings: ${total_income - total_expenses:.2f}")
    
    budget_status = budget_manager.get_budget_status()
    print(f"   Budget status: {list(budget_status.keys())}")
    
    # Investment Analysis
    print("\n7. Investment Analysis:")
    dividend_yield = InvestmentAnalyzer.calculate_dividend_yield(2.0, 50.0)
    print(f"   Dividend yield: {dividend_yield:.2f}%")
    
    pe_ratio = InvestmentAnalyzer.calculate_pe_ratio(100.0, 5.0)
    print(f"   P/E ratio: {pe_ratio:.2f}")
    
    pbr_ratio = InvestmentAnalyzer.calculate_pbr_ratio(80.0, 40.0)
    print(f"   P/B ratio: {pbr_ratio:.2f}")
    
    cash_flows = [100, 110, 120, 130, 140]
    dcf_value = InvestmentAnalyzer.calculate_dcf_value(cash_flows, 0.10)
    print(f"   DCF value: ${dcf_value:.2f}")
    
    # Financial Reporting
    print("\n8. Financial Reporting:")
    income = [
        {"source": "Sales", "amount": 100000},
        {"source": "Services", "amount": 25000}
    ]
    
    expenses = [
        {"category": "Cost of Goods", "amount": 40000},
        {"category": "Operating", "amount": 30000},
        {"category": "Marketing", "amount": 10000}
    ]
    
    income_statement = FinancialReporter.generate_income_statement(income, expenses)
    print(f"   Net income: ${income_statement['net_income']:.2f}")
    print(f"   Profit margin: {income_statement['profit_margin']:.2f}%")
    
    assets = {"Cash": 50000, "Inventory": 30000, "Equipment": 70000}
    liabilities = {"Accounts Payable": 20000, "Loans": 40000}
    
    balance_sheet = FinancialReporter.generate_balance_sheet(assets, liabilities)
    print(f"   Total equity: ${balance_sheet['equity']:.2f}")
    print(f"   Debt-to-equity: {balance_sheet['debt_to_equity']:.2f}")
    
    print("\n=== Demonstration Complete ===")
    print("\nFinancial Best Practices:")
    print("- Diversify investments to manage risk")
    print("- Understand your risk tolerance before investing")
    print("- Maintain an emergency fund (3-6 months expenses)")
    print("- Pay off high-interest debt before investing")
    print("- Use tax-advantaged accounts when possible")
    print("- Rebalance portfolio periodically")
    print("- Monitor fees and expenses")
    print("- Keep long-term perspective for investments")
    print("- Consult financial advisors for complex situations")
    print("- Stay informed about market conditions")


if __name__ == "__main__":
    demonstrate_financial_utils()