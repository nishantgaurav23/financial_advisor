FINANCIAL_TEMPLATES = {
    "retirement": {
        "context": """
        Consider the following retirement planning factors:
        - Current age and retirement age
        - Current savings and contributions
        - Expected returns and inflation
        - Risk tolerance level
        - Social security benefits
        """,
        "calculations": ["future_value", "required_savings", "income_replacement"]
    },
    "investment": {
        "context": """
        Analyze investment options considering:
        - Risk tolerance profile
        - Investment horizon
        - Current market conditions
        - Diversification needs
        - Tax implications
        """,
        "calculations": ["portfolio_return", "risk_metrics", "optimal_allocation"]
    }
    # Add more scenarios as needed
}

def calculate_future_value(principal: float, rate: float, years: int, monthly_contribution: float = 0) -> dict:
    # Implementation
    pass

def calculate_loan_payments(principal: float, rate: float, years: int) -> dict:
    # Implementation
    pass

# Add more financial calculation functions