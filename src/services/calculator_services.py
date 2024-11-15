from typing import Dict, List, Optional
import numpy as np
from functools import wraps 
import logging 

logger = logging.getLogger(__name__)

class FinancialCalculator:
    def validate_inputs(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Basic validation for numeric inputs
                for key, value in kwargs.items():
                    if isinstance(value, (int, float)) and value < 0:
                        raise ValueError(f"{key} cannot be negative")
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Validation error in {func.__name__}: {str(e)}")
                raise
        return wrapper
    @validate_inputs
    def calculate_budgeting(self, income: float, expenses: Dict[str, float], savings_goal: float = 0) -> Dict:
        try:
            total_expenses = sum(expenses.values())
            if total_expenses > income:
                raise ValueError("Expenses exceed income")

            # Enhanced calculations
            monthly_income = income / 12
            monthly_expenses = {k: v/12 for k, v in expenses.items()}
            
            # 50/30/20 rule analysis
            needs = sum(v for k, v in expenses.items() if k in ["housing", "utilities", "food", "healthcare"])
            wants = sum(v for k, v in expenses.items() if k in ["entertainment", "shopping", "dining"])
            savings = income - total_expenses
            
            rule_analysis = {
                "needs_ratio": (needs / income) * 100,
                "wants_ratio": (wants / income) * 100,
                "savings_ratio": (savings / income) * 100
            }

            return {
                "income_analysis": {
                    "annual_income": income,
                    "monthly_income": monthly_income,
                    "total_expenses": total_expenses,
                    "monthly_expenses": sum(monthly_expenses.values()),
                    "savings_potential": savings
                },
                "expense_breakdown": expenses,
                "monthly_breakdown": monthly_expenses,
                "rule_analysis": rule_analysis,
                "health_indicators": {
                    "expense_to_income": (total_expenses / income) * 100,
                    "savings_to_income": (savings / income) * 100,
                    "meets_50_30_20": all([
                        rule_analysis["needs_ratio"] <= 50,
                        rule_analysis["wants_ratio"] <= 30,
                        rule_analysis["savings_ratio"] >= 20
                    ])
                },
                "recommendations": self._generate_budget_recommendations(rule_analysis, savings, savings_goal)
            }
        except Exception as e:
            logger.error(f"Error in budget calculation: {str(e)}")
            raise

    @validate_inputs
    def calculate_retirement(
        self,
        current_age: int,
        retirement_age: int,
        current_savings: float,
        monthly_contribution: float,
        expected_return: float = 7.0,
        inflation_rate: float = 3.0,
        desired_retirement_income: float = None
    ) -> Dict:
        years_to_retirement = retirement_age - current_age
        real_return = (1 + expected_return/100) / (1 + inflation_rate/100) - 1
        
        # Enhanced calculations
        monthly_savings = monthly_contribution * 12
        total_contributions = monthly_savings * years_to_retirement
        future_savings = current_savings * (1 + real_return) ** years_to_retirement
        future_contributions = monthly_savings * (((1 + real_return) ** years_to_retirement - 1) / real_return)
        total_retirement_savings = future_savings + future_contributions

        # Additional metrics
        return {
            "timing": {
                "current_age": current_age,
                "retirement_age": retirement_age,
                "years_to_retirement": years_to_retirement
            },
            "savings_analysis": {
                "current_savings": current_savings,
                "monthly_contribution": monthly_contribution,
                "total_contributions": total_contributions,
                "future_value": total_retirement_savings
            },
            "financial_metrics": {
                "real_return_rate": real_return * 100,
                "inflation_adjusted_return": expected_return - inflation_rate,
                "savings_growth_multiple": total_retirement_savings / (current_savings + total_contributions)
            },
            "monthly_retirement_income": total_retirement_savings / (25 * 12),  # 4% withdrawal rule
            "yearly_projection": self._generate_retirement_projection(
                current_savings,
                monthly_contribution,
                years_to_retirement,
                real_return
            ),
            "retirement_readiness": self._assess_retirement_readiness(
                total_retirement_savings,
                desired_retirement_income,
                years_to_retirement
            )
        }

    def calculate_estate_planning(self,
                                assets: Dict[str, float],
                                liabilities: Dict[str, float],
                                beneficiaries: int) -> Dict:
        """Calculate estate planning metrics"""
        total_assets = sum(assets.values())
        total_liabilities = sum(liabilities.values())
        net_estate = total_assets - total_liabilities
        
        # Calculate estate tax implications
        estate_tax = self._calculate_estate_tax(net_estate)
        
        # Calculate per-beneficiary distribution
        per_beneficiary = (net_estate - estate_tax) / beneficiaries if beneficiaries > 0 else 0
        
        return {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "net_estate": net_estate,
            "estate_tax": estate_tax,
            "per_beneficiary_amount": per_beneficiary,
            "asset_breakdown": assets,
            "liability_breakdown": liabilities
        }

    @validate_inputs
    def calculate_real_estate(
        self,
        property_value: float,
        down_payment: float,
        interest_rate: float,
        term_years: int,
        rental_income: float = 0,
        property_tax_rate: float = 0.01,
        maintenance_rate: float = 0.01,
        appreciation_rate: float = 0.03,
        vacancy_rate: float = 0.08,
        insurance_cost: float = 0
    ) -> Dict:
        loan_amount = property_value - down_payment
        monthly_payment = self._calculate_mortgage_payment(loan_amount, interest_rate, term_years)
        
        # Operating costs
        annual_property_tax = property_value * property_tax_rate
        annual_maintenance = property_value * maintenance_rate
        annual_insurance = insurance_cost
        total_monthly_costs = (annual_property_tax + annual_maintenance + annual_insurance) / 12
        
        # Rental analysis
        effective_rental_income = rental_income * (1 - vacancy_rate)
        net_operating_income = (effective_rental_income * 12) - (annual_property_tax + annual_maintenance + annual_insurance)
        cash_flow = effective_rental_income - (monthly_payment + total_monthly_costs)
        cap_rate = (net_operating_income / property_value) * 100 if property_value > 0 else 0
        
        return {
            "property_metrics": {
                "property_value": property_value,
                "loan_amount": loan_amount,
                "down_payment": down_payment,
                "down_payment_percentage": (down_payment / property_value * 100)
            },
            "monthly_costs": {
                "mortgage_payment": monthly_payment,
                "property_tax": annual_property_tax / 12,
                "maintenance": annual_maintenance / 12,
                "insurance": annual_insurance / 12,
                "total_monthly_cost": monthly_payment + total_monthly_costs
            },
            "investment_metrics": {
                "cap_rate": cap_rate,
                "cash_on_cash_return": (cash_flow * 12 / down_payment * 100) if down_payment > 0 else 0,
                "net_operating_income": net_operating_income,
                "monthly_cash_flow": cash_flow
            },
            "rental_analysis": {
                "gross_rental_income": rental_income * 12,
                "vacancy_loss": rental_income * vacancy_rate * 12,
                "effective_rental_income": effective_rental_income * 12,
                "operating_expenses_ratio": ((annual_property_tax + annual_maintenance + annual_insurance) / 
                                        (effective_rental_income * 12) * 100) if rental_income > 0 else 0
            },
            "equity_analysis": self._calculate_equity_buildup(
                loan_amount, interest_rate, term_years, property_value, appreciation_rate
            ),
            "roi_analysis": {
                "total_return": self._calculate_real_estate_roi(
                    property_value, appreciation_rate, net_operating_income, term_years
                ),
                "appreciation_return": property_value * (1 + appreciation_rate) ** term_years - property_value,
                "cash_flow_return": cash_flow * 12 * term_years
            }
        }

    def _calculate_mortgage_payment(self, principal: float, rate: float, years: int) -> float:
        """Helper method to calculate mortgage payment"""
        monthly_rate = rate / 12 / 100
        num_payments = years * 12
        return (principal * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

    def _calculate_estate_tax(self, net_estate: float) -> float:
        """Helper method to calculate estate tax"""
        # Simplified calculation - replace with actual tax brackets
        exemption = 12920000  # 2023 exemption amount
        if net_estate <= exemption:
            return 0
        return (net_estate - exemption) * 0.40

    def _calculate_equity_buildup(self, 
                                loan_amount: float, 
                                rate: float,
                                years: int,
                                initial_value: float,
                                appreciation_rate: float) -> List[Dict]:
        """Calculate equity buildup over time"""
        monthly_rate = rate / 12 / 100
        monthly_payment = self._calculate_mortgage_payment(loan_amount, rate, years)
        
        equity_timeline = []
        remaining_balance = loan_amount
        property_value = initial_value
        
        for year in range(years + 1):
            property_value = initial_value * (1 + appreciation_rate) ** year
            equity = property_value - remaining_balance
            
            equity_timeline.append({
                "year": year,
                "property_value": property_value,
                "loan_balance": remaining_balance,
                "equity": equity
            })
            
            # Calculate next year's remaining balance
            for _ in range(12):
                interest = remaining_balance * monthly_rate
                principal = monthly_payment - interest
                remaining_balance -= principal
                
        return equity_timeline
    
    @validate_inputs
    def calculate_investment(
        self,
        portfolio_value: float,
        monthly_contribution: float,
        time_horizon: int,
        risk_profile: str = "moderate",
        target_amount: float = None
    ) -> Dict:
        risk_returns = {
            "conservative": {"return": 6.0, "volatility": 8.0, "bond_allocation": 70},
            "moderate": {"return": 8.0, "volatility": 12.0, "bond_allocation": 40},
            "aggressive": {"return": 10.0, "volatility": 16.0, "bond_allocation": 20}
        }

        profile = risk_returns[risk_profile]
        expected_return = profile["return"] / 100
        monthly_rate = expected_return / 12

        future_value = self._calculate_future_value(
            portfolio_value,
            monthly_contribution,
            expected_return,
            time_horizon
        )

        return {
            "current_analysis": {
                "portfolio_value": portfolio_value,
                "monthly_contribution": monthly_contribution,
                "time_horizon": time_horizon,
                "risk_profile": risk_profile
            },
            "projected_returns": {
                "expected_return": profile["return"],
                "expected_volatility": profile["volatility"],
                "future_value": future_value,
                "total_contributions": monthly_contribution * 12 * time_horizon,
                "investment_gain": future_value - portfolio_value - (monthly_contribution * 12 * time_horizon)
            },
            "portfolio_metrics": {
                "sharpe_ratio": (profile["return"] - 3) / profile["volatility"],  # Assuming 3% risk-free rate
                "recommended_allocation": {
                    "stocks": 100 - profile["bond_allocation"],
                    "bonds": profile["bond_allocation"],
                    "cash": 0
                },
                "risk_adjusted_return": profile["return"] / profile["volatility"]
            },
            "goal_analysis": self._analyze_investment_goals(
                future_value,
                target_amount,
                time_horizon
            ),
            "yearly_projection": self._generate_investment_projection(
                portfolio_value,
                monthly_contribution,
                expected_return,
                time_horizon
            )
        }
    def calculate_budget(
    self,
    monthly_income: float,
    expenses: Dict[str, float],
    savings_goals: Dict[str, float] = None,
    debt_payments: Dict[str, float] = None
) -> Dict:
        """Calculate comprehensive budget analysis"""
        
        # Categorize expenses
        expense_categories = {
            "essential": {"housing", "utilities", "food", "healthcare", "insurance"},
            "lifestyle": {"entertainment", "dining", "shopping", "travel"},
            "financial": {"savings", "investments", "debt"}
        }
        
        categorized_expenses = {
            "essential": sum(amt for cat, amt in expenses.items() if cat in expense_categories["essential"]),
            "lifestyle": sum(amt for cat, amt in expenses.items() if cat in expense_categories["lifestyle"]),
            "financial": sum(amt for cat, amt in expenses.items() if cat in expense_categories["financial"])
        }
        
        total_expenses = sum(expenses.values())
        total_debt_payments = sum(debt_payments.values()) if debt_payments else 0
        total_savings_goals = sum(savings_goals.values()) if savings_goals else 0
        
        # Calculate ratios
        income_ratios = {
            "essential_ratio": (categorized_expenses["essential"] / monthly_income * 100),
            "lifestyle_ratio": (categorized_expenses["lifestyle"] / monthly_income * 100),
            "financial_ratio": (categorized_expenses["financial"] / monthly_income * 100),
            "debt_ratio": (total_debt_payments / monthly_income * 100),
            "savings_ratio": (total_savings_goals / monthly_income * 100)
        }
        
        # Calculate discretionary income
        discretionary_income = monthly_income - categorized_expenses["essential"] - total_debt_payments

        return {
            "income_summary": {
                "monthly_income": monthly_income,
                "total_expenses": total_expenses,
                "discretionary_income": discretionary_income
            },
            "expense_breakdown": categorized_expenses,
            "detailed_expenses": expenses,
            "financial_ratios": income_ratios,
            "budget_health": self._assess_budget_health(income_ratios),
            "recommendations": self._generate_budget_recommendations(
                income_ratios,
                discretionary_income,
                total_savings_goals
            )
        }

    # Helper methods
    def _estimate_health_premium(self, age: int, dependents: int) -> float:
        """Estimate monthly health insurance premium"""
        base_premium = 400
        age_factor = max(1, (age - 30) * 0.02 + 1)
        dependent_factor = 1 + (dependents * 0.5)
        return base_premium * age_factor * dependent_factor

    def _recommend_deductible(self, annual_income: float) -> float:
        """Recommend insurance deductible based on income"""
        if annual_income < 30000:
            return 1000
        elif annual_income < 60000:
            return 2000
        else:
            return 4000

    def _estimate_life_premium(self, coverage_amount: float, age: int) -> float:
        """Estimate monthly life insurance premium"""
        base_rate = 0.1  # per $1000 of coverage
        age_factor = max(1, (age - 30) * 0.05 + 1)
        return (coverage_amount / 1000) * base_rate * age_factor

    def _assess_stock_risk(self, beta: float, pe_ratio: float) -> str:
        """Assess stock risk level"""
        if beta > 1.5 or pe_ratio > 30:
            return "High"
        elif beta > 0.8 or pe_ratio > 15:
            return "Moderate"
        else:
            return "Low"

    def _assess_valuation(self, price: float, pe_ratio: float, market_cap: float) -> str:
        """Assess stock valuation"""
        if pe_ratio > 30:
            return "Potentially overvalued"
        elif pe_ratio < 10:
            return "Potentially undervalued"
        return "Fairly valued"

    def _assess_budget_health(self, ratios: Dict[str, float]) -> str:
        """Assess overall budget health"""
        if ratios["essential_ratio"] > 50 or ratios["debt_ratio"] > 40:
            return "Needs Attention"
        elif ratios["savings_ratio"] < 20:
            return "Could Improve"
        return "Healthy"

    def _generate_budget_recommendations(
        self,
        ratios: Dict[str, float],
        discretionary_income: float,
        savings_goals: float
    ) -> List[str]:
        """Generate budget recommendations"""
        recommendations = []
        
        if ratios["essential_ratio"] > 50:
            recommendations.append("Consider reducing essential expenses")
        if ratios["debt_ratio"] > 40:
            recommendations.append("Focus on debt reduction")
        if ratios["savings_ratio"] < 20:
            recommendations.append("Increase savings rate")
            
        return recommendations
    @validate_inputs
    def calculate_tax_calculation_scenarios(
        self,
        annual_income: float,
        tax_regime: str = "new",
        deductions: Dict[str, float] = None,
        investments: Dict[str, float] = None
    ) -> Dict:
        try:
            # Input validation
            if annual_income <= 0:
                raise ValueError("Annual income must be positive")
            if tax_regime not in ["old", "new"]:
                raise ValueError("Invalid tax regime")

            # Enhanced tax calculations with surcharge
            def calculate_surcharge(income: float, tax: float) -> float:
                if income > 5000000 and income <= 10000000:
                    return tax * 0.10
                elif income > 10000000 and income <= 20000000:
                    return tax * 0.15
                elif income > 20000000 and income <= 50000000:
                    return tax * 0.25
                elif income > 50000000:
                    return tax * 0.37
                return 0

            # Calculate tax with existing methods
            result = super().calculate_tax_calculation_scenarios(
                annual_income=annual_income,
                tax_regime=tax_regime,
                deductions=deductions,
                investments=investments
            )

            # Add enhanced analysis
            for regime in ["old", "new"]:
                tax_calc = result[f"{regime}_regime"]
                surcharge = calculate_surcharge(annual_income, tax_calc["tax_before_cess"])
                tax_calc.update({
                    "surcharge": surcharge,
                    "effective_tax_rate": (tax_calc["total_tax"] / annual_income) * 100,
                    "monthly_tax_liability": tax_calc["total_tax"] / 12,
                    "take_home_monthly": (annual_income - tax_calc["total_tax"]) / 12
                })

            # Add tax saving opportunities
            result["tax_saving_opportunities"] = self._identify_tax_savings(
                annual_income, 
                deductions or {}, 
                investments or {}
            )

            return result

        except Exception as e:
            logger.error(f"Error in tax calculation: {str(e)}")
            raise

    @validate_inputs
    def calculate_tax_planning(
        self,
        annual_income: float,
        tax_regime: str = "new",
        deductions: Dict[str, float] = None,
        investments: Dict[str, float] = None
    ) -> Dict:
        try:
            # Input validation
            if annual_income <= 0:
                raise ValueError("Annual income must be positive")
            if tax_regime not in ["old", "new"]:
                raise ValueError("Invalid tax regime")

            # Enhanced tax calculations with surcharge
            def calculate_surcharge(income: float, tax: float) -> float:
                if income > 5000000 and income <= 10000000:
                    return tax * 0.10
                elif income > 10000000 and income <= 20000000:
                    return tax * 0.15
                elif income > 20000000 and income <= 50000000:
                    return tax * 0.25
                elif income > 50000000:
                    return tax * 0.37
                return 0

            # Calculate tax with existing methods
            result = super().calculate_tax_calculation_scenarios(
                annual_income=annual_income,
                tax_regime=tax_regime,
                deductions=deductions,
                investments=investments
            )

            # Add enhanced analysis
            for regime in ["old", "new"]:
                tax_calc = result[f"{regime}_regime"]
                surcharge = calculate_surcharge(annual_income, tax_calc["tax_before_cess"])
                tax_calc.update({
                    "surcharge": surcharge,
                    "effective_tax_rate": (tax_calc["total_tax"] / annual_income) * 100,
                    "monthly_tax_liability": tax_calc["total_tax"] / 12,
                    "take_home_monthly": (annual_income - tax_calc["total_tax"]) / 12
                })

            # Add tax saving opportunities
            result["tax_saving_opportunities"] = self._identify_tax_savings(
                annual_income, 
                deductions or {}, 
                investments or {}
            )

            return result

        except Exception as e:
            logger.error(f"Error in tax calculation: {str(e)}")
            raise

    @validate_inputs
    def calculate_insurance(
        self,
        annual_income: float,
        age: int,
        dependents: int = 0,
        years_income_needed: int = 20,
        current_savings: float = 0,
        total_debt: float = 0,
        education_needs: float = 0,
        medical_history: str = "standard",
        existing_coverage: Dict[str, float] = None
    ) -> Dict:
        existing_coverage = existing_coverage or {}
        
        # Life Insurance
        total_life_needs = (annual_income * years_income_needed) + \
                        total_debt + \
                        (dependents * education_needs) + \
                        15000 - \
                        current_savings  # Final expenses
                        
        life_gap = max(0, total_life_needs - existing_coverage.get('life', 0))
        
        # Disability Insurance
        disability_needs = {
            "short_term": annual_income * 0.60,  # 60% income replacement
            "long_term": annual_income * 0.60 * max(65 - age, 0),
            "elimination_period": "90 days" if age < 50 else "180 days"
        }
        
        # Critical Illness Coverage
        critical_illness_amount = max(annual_income * 2, 50000)
        
        # Health Insurance
        health_insurance = self._calculate_health_insurance_needs(
            age, dependents, medical_history, annual_income
        )

        return {
            "life_insurance": {
                "total_needs": total_life_needs,
                "current_coverage": existing_coverage.get('life', 0),
                "coverage_gap": life_gap,
                "breakdown": {
                    "income_replacement": annual_income * years_income_needed,
                    "debt_coverage": total_debt,
                    "education_needs": dependents * education_needs,
                    "final_expenses": 15000
                },
                "recommended_term": min(80 - age, 30)
            },
            "disability_insurance": {
                "short_term_needs": disability_needs["short_term"],
                "long_term_needs": disability_needs["long_term"],
                "current_coverage": existing_coverage.get('disability', 0),
                "coverage_gap": disability_needs["short_term"] - existing_coverage.get('disability', 0),
                "elimination_period": disability_needs["elimination_period"]
            },
            "health_insurance": health_insurance,
            "critical_illness": {
                "recommended_coverage": critical_illness_amount,
                "current_coverage": existing_coverage.get('critical_illness', 0),
                "coverage_gap": critical_illness_amount - existing_coverage.get('critical_illness', 0)
            },
            "premium_estimates": self._estimate_insurance_premiums(
                age, total_life_needs, disability_needs["short_term"], 
                health_insurance["recommended_coverage"], medical_history
            ),
            "risk_assessment": self._assess_insurance_risk(
                age, medical_history, annual_income, dependents, total_debt
            )
        }

    def _calculate_health_insurance_needs(
        self, age: int, dependents: int, medical_history: str, annual_income: float
    ) -> Dict:
        base_coverage = max(annual_income * 0.3, 50000)
        coverage_adjustments = {
            "standard": 1.0,
            "high_risk": 1.5,
            "low_risk": 0.8
        }
        
        return {
            "recommended_coverage": base_coverage * coverage_adjustments.get(medical_history, 1.0),
            "deductible": self._recommend_deductible(annual_income),
            "out_of_pocket_max": min(annual_income * 0.1, 8000),
            "family_coverage_needed": dependents > 0,
            "hsa_eligible": annual_income > 0
        }

    def _estimate_insurance_premiums(
        self, age: int, life_coverage: float, disability_coverage: float, 
        health_coverage: float, medical_history: str
    ) -> Dict:
        # Premium calculation logic
        life_base_rate = 0.1 # per $1000 of coverage
        health_base_rate = 400
        disability_rate = 0.03
        
        risk_factors = {
            "standard": 1.0,
            "high_risk": 1.5,
            "low_risk": 0.8
        }
        
        age_factor = max(1, (age - 30) * 0.05 + 1)
        risk_factor = risk_factors.get(medical_history, 1.0)
        
        return {
            "life": (life_coverage / 1000) * life_base_rate * age_factor * risk_factor,
            "disability": disability_coverage * disability_rate * age_factor,
            "health": health_base_rate * age_factor * risk_factor
        }