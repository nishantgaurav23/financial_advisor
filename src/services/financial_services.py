from typing import Dict, Optional
from src.services.calculator_services import FinancialCalculator
from src.services.visualization_service import VisualizationService

class FinancialService:
    def __init__(self):
        self.calculator = FinancialCalculator()
        self.visualizer = VisualizationService()


    def process_financial_query(self, scenario_type: str, context: Dict) -> Dict:
        """Process financial queries and return calculations with visualizations"""
        results = {}
        
        # Get calculations
        calculations = self.calculator.calculate(scenario_type, context)
        if calculations:
            results['calculations'] = calculations
            
            # Add visualizations if applicable
            viz = self.visualizer.create_visualization(scenario_type, calculations)
            if viz:
                results['visualizations'] = viz
                
        return results

    def _get_enhanced_context(self, scenario_type: str) -> str:
            """Get enhanced context for specific financial scenarios"""
            contexts = {
            "retirement": """
                Consider retirement planning factors:
                - Current age and timeline
                - Savings and contributions
                - Investment strategy
                - Risk tolerance
                - Social Security benefits
                - Healthcare costs
                - Required Minimum Distributions
                """,
            "investment": """
                Consider investment factors:
                - Risk tolerance and goals
                - Time horizon
                - Asset allocation
                - Market conditions
                - Diversification needs
                - Tax implications
                """,
            "debt": """
                Consider debt management factors:
                - Outstanding balances
                - Interest rates
                - Minimum payments
                - Debt consolidation options
                - Credit score impact
                - Repayment strategies
                """,
            "budgeting": """
                Consider budgeting factors:
                - Income sources
                - Essential expenses
                - Discretionary spending
                - Savings goals
                - Emergency fund
                - Debt obligations
                """,
            "estate_planning": """
                Consider estate planning factors:
                - Asset inventory
                - Beneficiary designations
                - Will and trusts
                - Tax implications
                - Healthcare directives
                - Power of attorney
                """,
            "insurance": """
                Consider insurance planning factors:
                - Coverage types needed
                - Risk assessment
                - Policy comparison
                - Premium costs
                - Beneficiary designations
                - Claims process
                """,
            "business_finance": """
                Consider business financial factors:
                - Revenue streams
                - Operating costs
                - Cash flow management
                - Business structure
                - Tax considerations
                - Growth planning
                """,
            "real_estate": """
                Consider real estate factors:
                - Property values
                - Mortgage options
                - Rental income
                - Maintenance costs
                - Tax implications
                - Market conditions
                """,
            "tax_calculation_scenarios": """
                Consider the following tax calculation factors:
                - Income sources (salary, business, investments, etc.)
                - Tax deductions (Section 80C, 80D, etc.)
                - Exemptions (HRA, LTA, etc.)
                - Capital gains (short-term, long-term, indexed, non-indexed)
                - Tax slabs and rates for different income brackets
                - Rebates and credits (Section 87A)
                - Tax-saving investments (PPF, ELSS, NSC, etc.)
                - Deductions for interest on home loans (Section 24)
                - Compliance and filing deadlines
                - Surcharge and cess calculations
                - New tax regime (2024-25)
                - Tax implications of new tax regime
                - Old tax regime (2024-25)
                - Tax implications of old tax regime
                - Calculation of tax based on new and old tax regime
                """,
            "tax_planning": """
                Consider tax planning factors:
                - Income sources
                - Tax brackets
                - Deductions and credits
                - Investment tax impact
                - Retirement account strategies
                - Estate tax considerations
                """,
        }
            return contexts.get(scenario_type, "General financial planning considerations")
    
        # Update the _detect_financial_scenario method with new scenarios
    def _detect_financial_scenario(self, query: str) -> str:
        """Detect financial scenario from query"""
        scenario_keywords = {
            "retirement": ["retire", "retirement", "pension", "401k", "ira", "social security"],
            "investment": ["invest", "portfolio", "stocks", "bonds", "market", "returns"],
            "debt": ["debt", "loan", "mortgage", "credit", "payment", "interest"],
            #"budgeting": ["budget", "spending", "expenses", "income", "cash flow"],
            "estate_planning": ["estate", "will", "trust", "inheritance", "beneficiary"],
            "tax_planning": ["tax", "deduction", "credit", "write-off", "ira", "filing"],
            "insurance": ["insurance", "coverage", "policy", "premium", "claim", "risk"],
            "business_finance": ["business", "company", "revenue", "profit", "startup"],
            "real_estate": ["property", "real estate", "mortgage", "rent", "housing"],
            "tax_calculation_scenarios" :{
                "salary_income": ["salary", "basic pay", "HRA", "allowance", "bonus", "gratuity"],
                "investment_income": ["investment", "interest income", "dividends", "capital gains", "FD", "mutual funds", "stocks"],
                "business_income": ["business income", "profits", "turnover", "revenue", "freelance", "consultant"],
                "rental_income": ["rental income", "property rent", "house property", "tenant", "real estate income"],
                "retirement_income": ["pension income", "retirement benefits", "senior citizen income", "EPF", "NPS", "superannuation"],
                "deductions": ["tax deduction", "section 80C", "section 80D", "section 80G", "PPF", "insurance premium", "charity donations"],
                "home_loan_interest": ["home loan interest", "housing loan interest", "mortgage", "property purchase", "section 24"],
                "capital_gains": ["capital gains", "short-term gain", "long-term gain", "indexed gain", "sale of assets", "property sale"],
                "foreign_income": ["foreign income", "NRI income", "overseas income", "global income", "DTAA", "foreign remittance"],
                "tax_compliance": ["income tax filing", "ITR", "tax compliance", "form submission", "filing deadline"],
                "rebates_and_credits": ["rebate", "section 87A", "tax credit", "tax relief", "surcharge", "health and education cess"],
                "inheritance_tax": ["inheritance", "gift tax", "wealth transfer", "estate planning", "property inheritance"]
            }
        }
        
        query_lower = query.lower()
        for scenario, keywords in scenario_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return scenario
        return "general"