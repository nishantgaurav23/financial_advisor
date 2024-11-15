from fpdf import FPDF
import plotly
import json
from typing import Dict, List
import os
from datetime import datetime

class ReportService:
    def generate_report(self, 
                       scenario_type: str,
                       question: str,
                       answer: str,
                       calculations: Dict,
                       visualizations: Dict) -> str:
        """Generate PDF report with analysis and visualizations"""
        pdf = FPDF()
        pdf.add_page()
        
        # Add header with timestamp
        self._add_header(pdf, scenario_type)
        
        # Add summary section
        self._add_summary_section(pdf, question, answer)
        
        # Add calculations
        if calculations:
            pdf.add_page()
            self._add_calculations_section(pdf, calculations)
        
        # Add visualizations
        if visualizations:
            pdf.add_page()
            self._add_visualizations(pdf, visualizations)
        
        # Add recommendations if available
        if 'recommendations' in calculations:
            pdf.add_page()
            self._add_recommendations(pdf, calculations['recommendations'])
        
        # Save the report
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{report_dir}/financial_report_{scenario_type}_{timestamp}.pdf'
        pdf.output(filename)
        return filename

    def _add_header(self, pdf: FPDF, scenario_type: str):
        """Add formatted header to report"""
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Financial Analysis Report - {scenario_type.title()}', ln=True)
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
        pdf.ln(10)

    def _add_summary_section(self, pdf: FPDF, question: str, answer: str):
        """Add question and analysis summary"""
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Query Summary', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, f'Question: {question}')
        pdf.ln(5)
        pdf.multi_cell(0, 10, f'Analysis: {answer}')

    def _add_calculations_section(self, pdf: FPDF, calculations: Dict):
        """Add calculations with proper formatting"""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Detailed Calculations', ln=True)
        pdf.ln(5)

        for category, values in calculations.items():
            if isinstance(values, dict):
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, category.replace('_', ' ').title(), ln=True)
                pdf.set_font('Arial', '', 12)
                
                for key, value in values.items():
                    if isinstance(value, (int, float)):
                        pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: ₹{value:,.2f}", ln=True)
                    else:
                        pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
                pdf.ln(5)
            elif isinstance(values, (int, float)):
                pdf.cell(0, 10, f"{category.replace('_', ' ').title()}: ₹{values:,.2f}", ln=True)

    def _add_visualizations(self, pdf: FPDF, visualizations: Dict):
        """Add visualizations to report"""
        if not visualizations or "figures" not in visualizations:
            return
            
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Visual Analysis', ln=True)
        
        for viz_name, viz_fig in visualizations["figures"].items():
            try:
                img_path = f'temp_{viz_name}.png'
                viz_fig.write_image(img_path)
                pdf.image(img_path, x=10, y=None, w=190)
                pdf.ln(10)
                os.remove(img_path)
            except Exception as e:
                logger.error(f"Error adding visualization {viz_name}: {str(e)}")

    def _add_recommendations(self, pdf: FPDF, recommendations: List[str]):
        """Add recommendations section"""
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Recommendations', ln=True)
        pdf.set_font('Arial', '', 12)
        
        for i, rec in enumerate(recommendations, 1):
            pdf.multi_cell(0, 10, f"{i}. {rec}")
        pdf.ln(5)