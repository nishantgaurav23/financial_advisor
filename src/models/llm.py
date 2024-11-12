# src/models/llm.py
from typing import Optional, List, Any
import requests
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from pydantic import BaseModel, Field

class FinancialLLM(LLM, BaseModel):
    """Custom LLM implementation using Ollama"""
    
    base_url: str = Field(default="http://localhost:11434")
    model: str = Field(default="mistral")
    temperature: float = Field(default=0.7)
    num_predict: int = Field(default=512)
    
    class Config:
        arbitrary_types_allowed = True
        
    def _call(self,prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any,) -> str:
        """Call the LLM with the given prompt"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.num_predict,
                    }
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Error calling LLM: {str(e)}")
            raise

    @property
    def _llm_type(self) -> str:
        """Return identifier for LLM"""
        return "financial_advisor_llm"