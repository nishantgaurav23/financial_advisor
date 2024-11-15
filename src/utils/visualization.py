# src/utils/visualization.py
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import pandas as pd
import json

class VisualizationManager:
    @staticmethod
    def create_line_chart(data: dict, title: str, x_label: str, y_label: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(data.keys()), y=list(data.values())))
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label
        )
        return fig
    
    @staticmethod
    def create_pie_chart(data: dict, title: str) -> go.Figure:
        fig = go.Figure(data=[go.Pie(labels=list(data.keys()), values=list(data.values()))])
        fig.update_layout(title=title)
        return fig
        
    # Add more visualization methods as needed

class ReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        
    def generate_pdf_report(self, content: dict, filename: str):
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        
        # Add content to PDF
        # Implementation details...
        
        self.pdf.output(filename)
    
    def generate_excel_report(self, data: dict, filename: str):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)