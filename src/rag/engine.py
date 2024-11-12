# src/rag/engine.py
from typing import Dict, List, Optional
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from src.models.embeddings import EmbeddingModel

class RAGEngine:
    def __init__(self, llm):
        """Initialize RAG engine with a language model"""
        self.llm = llm
        self.embedding_model = EmbeddingModel()
        # Add this line to load existing embeddings
        self.embedding_model.load_embeddings()
        from langchain.memory import ConversationBufferMemory
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer"
            )
        self.qa_chain = self._create_qa_chain()

    def _create_qa_chain(self) -> ConversationalRetrievalChain:
        """Create the QA chain with custom prompt"""
        prompt_template = """You are a professional financial advisor. Use the following information to provide detailed financial advice.

        Context: {context}
        Chat History: {chat_history}
        Question: {question}

        Provide your response in this format:
        1. Key Points
        2. Analysis
        3. Recommendations
        4. Risk Considerations
        5. Next Steps

        Response:"""

        PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=prompt_template
        )

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.embedding_model.vector_store.as_retriever(),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

    def query(self, question: str) -> Dict:
        """Process a query through the RAG system"""
        try:
            result = self.qa_chain({"question": question})
            return {
                "answer": result["answer"],
                "sources": result["source_documents"],
                "chat_history": self.memory.chat_memory.messages
            }
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            raise

    def reset_memory(self):
        """Reset the conversation memory"""
        self.memory.clear()