import gradio as gr
from typing import List
import pandas as pd
from pathlib import Path
import logging
from src.models.llm import FinancialLLM
from src.services.financial_services import FinancialService
from src.rag.engine import RAGEngine
from src.services.visualization_service import VisualizationService
from src.services.report_service import ReportService

logger = logging.getLogger(__name__)

class FinancialAdvisorUI:
    def __init__(self, rag_engine):
        #self.llm = FinancialLLM()
        self.rag_engine = rag_engine
        self.create_interface()
        
        # self.financial_services = FinancialService()
        # self.visualization_service = VisualizationService()
        # self.report_service = ReportService()

    def create_interface(self):
        with gr.Blocks(theme=gr.themes.Soft()) as self.interface:
            with gr.Row():
                gr.Markdown(
                """
                # 💰 AI Financial Advisor
                Get expert financial advice powered by AI. Upload documents and ask questions about:
                - Tax calculations (Indian tax regimes)
                - Investment planning
                - Retirement planning
                - Insurance and risk management
                """
                )

            with gr.Row():
                # Left Column - Input Section
                with gr.Column(scale=2):
                    # Document Upload Section
                    gr.Markdown("### 📄 Upload Financial Documents")
                    file_upload = gr.File(
                        label="Upload relevant documents (PDF, Excel, CSV)",
                        file_count="multiple",
                        file_types=[".pdf", ".csv", ".xlsx", ".txt"]
                    )

                    # Query Input Section
                    gr.Markdown("### ❓ Ask Your Question")
                    query_input = gr.Textbox(
                        label="What would you like to know?",
                        placeholder="Example: Calculate my tax liability under new regime, or Analyze my retirement savings",
                        lines=3
                    )
                    with gr.Row():
                        with gr.Column(scale=3):
                            submit_btn = gr.Button("🚀 Get Advice", variant="primary")
                        with gr.Column(scale=1):
                            stop_btn = gr.Button("⏹️ Stop", variant="secondary")
                        with gr.Column(scale=1):
                            clear_btn = gr.Button("🔄 Clear", variant="secondary")

                # Right Column - Output Section
                with gr.Column(scale=3):
                    with gr.Tabs():
                        with gr.TabItem("Analysis"):
                            response_box = gr.Markdown()
                            with gr.Row():
                                download_report = gr.Button("📑 Download Report")
                                download_excel = gr.Button("📊 Download Calculations")
                            follow_up_box = gr.CheckboxGroup(
                                label="Suggested Follow-up Questions",
                                choices=[]
                            )

                        with gr.TabItem("Visualizations"):
                            plot_output = gr.Plot()

                        with gr.TabItem("Calculations"):
                            calculations_output = gr.DataFrame()

            # Event handlers
            submit_event = submit_btn.click(
                fn=self.process_query,
                inputs=[query_input, file_upload],
                outputs=[response_box, calculations_output, plot_output, follow_up_box]
            )
            # Add cancel functionality
            stop_btn.click(
                fn=None,
                #inputs=None,
                #outputs=None,
                cancels=[submit_event]
            )

            clear_btn.click(fn=self.clear_inputs)
            download_report.click(
                fn=self.download_pdf_report,
                inputs=[],
                outputs=[gr.File()]
            )

    def process_query(self, query: str, files: List[str] = None):
        """Process query using existing RAG engine"""
        try:
            # Use RAG engine's query method
            response = self.rag_engine.query(query)
            self.last_response = response

            # Format response for UI
            viz = None
            if response.get("visualizations"):
                viz = response["visualizations"]
                if isinstance(viz, dict) and "figures" in viz:
                    viz = next(iter(viz["figures"].values()))

            return (
                gr.Markdown(response["answer"]),
                self._format_calculations_for_display(response.get("calculations", {})),
                viz,
                gr.CheckboxGroup(choices=response.get("follow_up_questions", []))
            )

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return (
                gr.Markdown("Error processing your query. Please try again."),
                pd.DataFrame(),
                None,
                []
            )

    def clear_inputs(self):
        """Clear all input and output fields"""
        return {
            "query_input": "",
            "response_box": "",
            "calculations_output": None,
            "plot_output": None,
            "follow_up_box": []
        }

    def download_pdf_report(self):
        """Download PDF report of analysis"""
        try:
            if hasattr(self, "last_response") and self.last_response.get("report_path"):
                # Return as file object instead of just path
                return gr.File.update(value=self.last_response["report_path"])
        except Exception as e:
            logger.error(f"Error downloading report: {str(e)}") 
            return None

    def _format_calculations_for_display(self, calculations: dict) -> pd.DataFrame:
        """Format calculations for display in DataFrame"""
        rows = []
        for key, value in calculations.items():
            if isinstance(value, (int, float)):
                rows.append({
                    "Metric": key.replace("_", " ").title(),
                    "Value": f"₹ {value:,.2f}" if isinstance(value, float) else value
                })
            elif isinstance(value, dict):
                for k, v in value.items():
                    rows.append({
                        "Metric": f"{key.replace('_', ' ').title()} - {k.replace('_', ' ').title()}",
                        "Value": f"₹ {v:,.2f}" if isinstance(v, float) else v
                    })
        return pd.DataFrame(rows)

    def launch(self, share=False):
        """Launch the Gradio interface"""
        self.interface.launch(share=share)