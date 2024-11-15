# main.py
from src.models.llm import FinancialLLM
from src.rag.engine import RAGEngine
from src.ui.interface import FinancialAdvisorUI

def main():
    llm = FinancialLLM()
    rag_engine = RAGEngine(llm)
    ui = FinancialAdvisorUI(rag_engine)
    ui.launch()

if __name__ == "__main__":
    main()