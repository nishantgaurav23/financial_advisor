# tests/test_rag_engine.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from src.rag.engine import RAGEngine
from src.models.llm import FinancialLLM

@pytest.fixture
def rag_engine():
    llm = FinancialLLM()
    return RAGEngine(llm)

def test_retirement_calculation(rag_engine):
    context = {
        "current_age": 30,
        "retirement_age": 65,
        "current_savings": 50000,
        "monthly_contribution": 1000
    }
    
    result = rag_engine.query(
        "How much will I have at retirement?",
        context=context
    )
    
    assert result["scenario_type"] == "retirement"
    assert "calculations" in result
    assert "total_retirement_savings" in result["calculations"]
    assert result["calculations"]["total_retirement_savings"] > 0

def test_investment_calculation(rag_engine):
    context = {
        "initial_amount": 10000,
        "monthly_contribution": 500,
        "years": 10,
        "risk_profile": "moderate"
    }
    
    result = rag_engine.query(
        "How should I invest my money?",
        context=context
    )
    
    assert result["scenario_type"] == "investment"
    assert "calculations" in result
    assert "future_value" in result["calculations"]

def test_error_handling(rag_engine):
    with pytest.raises(ValueError):
        context = {
            "current_age": -30,  # Invalid age
            "retirement_age": 65
        }
        rag_engine.query("When can I retire?", context=context)

def test_scenario_detection(rag_engine):
    scenarios = [
        ("How much do I need to retire?", "retirement"),
        ("Should I invest in stocks?", "investment"),
        ("How to manage my debt?", "debt"),
        ("Help with tax planning", "tax")
    ]
    
    for query, expected_scenario in scenarios:
        result = rag_engine.query(query)
        assert result["scenario_type"] == expected_scenario