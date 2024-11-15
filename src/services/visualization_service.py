import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd

class VisualizationService:
    def create_visualizations(self, scenario_type: str, data: Dict) -> Dict:
        """Create scenario-specific visualizations"""
        viz_methods = {
            "retirement": self._create_retirement_viz,
            "investment": self._create_investment_viz,
            "budget": self._create_budget_viz,
            "insurance": self._create_insurance_viz,
            "real_estate": self._create_real_estate_viz,
            "tax_calculation_scenarios": self._create_tax_calculation_viz
        }
        
        method = viz_methods.get(scenario_type)
        return method(data) if method and data else None

    def _create_retirement_viz(self, data: Dict) -> Dict:
        if 'yearly_projection' not in data:
            return None
            
        df = pd.DataFrame(data['yearly_projection'])
        
        # Portfolio Growth
        growth_fig = go.Figure()
        growth_fig.add_trace(go.Scatter(
            x=df['year'],
            y=df['balance'],
            mode='lines+markers',
            name='Portfolio Balance'
        ))
        growth_fig.update_layout(
            title='Retirement Portfolio Growth',
            xaxis_title='Year',
            yaxis_title='Balance (₹)',
            template='plotly_white'
        )

        return {
            "portfolio_growth": growth_fig,
            "type": "line",
            "description": "Retirement portfolio growth over time"
        }

    def _create_investment_viz(self, data: Dict) -> Dict:
        figs = {}
        
        # Portfolio Allocation
        if 'asset_breakdown' in data:
            figs['allocation'] = px.pie(
                values=list(data['asset_breakdown'].values()),
                names=list(data['asset_breakdown'].keys()),
                title='Portfolio Allocation'
            )
        
        # Return Projection
        if 'yearly_projection' in data:
            df = pd.DataFrame(data['yearly_projection'])
            figs['returns'] = px.line(
                df, 
                x='year', 
                y='value',
                title=f"Investment Growth ({data.get('risk_profile', 'Moderate')} Risk)"
            )
        
        return {
            "figures": figs,
            "type": "multi",
            "description": "Investment portfolio analysis"
        }

    def _create_budget_viz(self, data: Dict) -> Dict:
        figs = {}
        
        # Expense Breakdown
        if 'expense_breakdown' in data:
            figs['expenses'] = px.pie(
                values=list(data['expense_breakdown'].values()),
                names=list(data['expense_breakdown'].keys()),
                title='Expense Distribution'
            )

        # Monthly Cash Flow
        if 'income_summary' in data:
            summary = data['income_summary']
            figs['cash_flow'] = go.Figure(data=[
                go.Bar(name='Income', x=['Monthly Flow'], y=[summary['monthly_income']]),
                go.Bar(name='Expenses', x=['Monthly Flow'], y=[summary['total_expenses']])
            ])
            figs['cash_flow'].update_layout(title='Monthly Cash Flow')

        return {
            "figures": figs,
            "type": "multi",
            "description": "Budget analysis visualizations"
        }

    def _create_insurance_viz(self, data: Dict) -> Dict:
        figs = {}
        
        # Coverage Analysis
        if 'life_insurance' in data:
            life = data['life_insurance']
            coverage_data = {
                'Current': life['current_coverage'],
                'Recommended': life['recommended_coverage'],
                'Gap': life['coverage_gap']
            }
            figs['coverage'] = px.bar(
                x=list(coverage_data.keys()),
                y=list(coverage_data.values()),
                title='Insurance Coverage Analysis'
            )

        # Premium Breakdown
        if 'total_monthly_premium_estimate' in data:
            premiums = data['total_monthly_premium_estimate']
            figs['premiums'] = px.pie(
                values=list(premiums.values()),
                names=list(premiums.keys()),
                title='Monthly Premium Breakdown'
            )

        return {
            "figures": figs,
            "type": "multi",
            "description": "Insurance analysis visualizations"
        }

    def _create_real_estate_viz(self, data: Dict) -> Dict:
        figs = {}
        
        # Equity Buildup
        if 'equity_buildup' in data:
            df = pd.DataFrame(data['equity_buildup'])
            figs['equity'] = px.line(
                df,
                x='year',
                y=['property_value', 'loan_balance', 'equity'],
                title='Property Equity Buildup Over Time'
            )

        # Cost Breakdown
        if all(k in data for k in ['monthly_payment', 'annual_property_tax', 'annual_maintenance']):
            costs = {
                'Monthly Payment': data['monthly_payment'] * 12,
                'Property Tax': data['annual_property_tax'],
                'Maintenance': data['annual_maintenance']
            }
            figs['costs'] = px.pie(
                values=list(costs.values()),
                names=list(costs.keys()),
                title='Annual Cost Breakdown'
            )

        return {
            "figures": figs,
            "type": "multi",
            "description": "Real estate analysis visualizations"
        }

    def _create_tax_calculation_viz(self, data: Dict) -> Dict:
        if not any(k in data for k in ['tax_breakdown', 'deductions_breakdown']):
            return None
            
        figs = {}
        
        # Income Components
        if 'income_components' in data:
            income = data['income_components']
            figs['income'] = px.pie(
                values=list(income.values()),
                names=list(income.keys()),
                title='Income Distribution'
            )

        # Deductions Breakdown
        if 'deductions_breakdown' in data:
            deductions = data['deductions_breakdown']
            figs['deductions'] = px.bar(
                x=list(deductions.keys()),
                y=list(deductions.values()),
                title='Tax Deductions'
            )

        return {
            "figures": figs,
            "type": "multi",
            "description": "Tax calculation visualizations"
        }