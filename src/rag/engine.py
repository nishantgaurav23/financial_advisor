# src/rag/engine.py
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Dict, List, Optional
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from src.models.embeddings import EmbeddingModel
from src.services.financial_services import FinancialService as fs
from src.services.calculator_services import FinancialCalculator as fc
from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
from langchain_core.prompts import PromptTemplate
from src.services.visualization_service import VisualizationService
from src.services.report_service import ReportService
# Add at the top of engine.py
import logging
from typing import Dict, Optional
from functools import wraps
from src.models.llm import FinancialLLM
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

######################### Imports added on Nov 15, 2024 #########################
from langchain.chains import (
    create_history_aware_retriever, 
    create_retrieval_chain,
    StuffDocumentsChain, 
    LLMChain, 
    ConversationalRetrievalChain
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
import json
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='financial_advisor.log'
)
logger = logging.getLogger(__name__)

# Add error handling decorator
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

class RAGEngine:
    def __init__(self, llm):
        """Initialize RAG engine with a language model"""
        self.llm = llm
        self.embedding_model = EmbeddingModel()
        self.embedding_model.load_embeddings()
        self.memory = self._initialize_memory()
        self.qa_chain = self._create_qa_chain()
        self.financial_service = fs()
        self.financial_calculator = fc()
        self.llm = FinancialLLM()
        self.visualization_service = VisualizationService()
        self.report_service = ReportService()

    
    ######### Added on Nov 15, 2024 #########
    def _initialize_memory(self) -> ConversationBufferMemory:
        """Initialize memory with proper configuration"""
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
            input_key="question"
        )

    # 
    # def _create_qa_chain(self) -> ConversationalRetrievalChain:
    #     """Create the QA chain with custom prompt"""
    #     combine_docs_prompt_template = """You are a professional financial advisor. Use the following information to provide detailed financial advice.

    #     Context: {context}
    #     Chat History: {chat_history}
    #     Question: {question}
    #     Calculations: {calculations}

    #     When providing your response:
    #     1. Start with a brief summary of the situation
    #     2. Reference specific numbers and calculations when available
    #     3. Explain financial concepts in simple terms
    #     4. Consider both short-term and long-term implications
    #     5. Provide actionable next steps
    #     6. If visuals are available, reference them to support your explanation
        
    #     Key points to address:
    #     - Risk factors and considerations
    #     - Tax implications if applicable
    #     - Alternative scenarios or strategies
    #     - Specific recommendations with rationale
    #     - Timeline for implementation
        
    #     Remember to:
    #     - Be conversational but professional
    #     - Explain your reasoning
    #     - Highlight both opportunities and risks
    #     - Suggest follow-up considerations

    #     Response:"""

    #     return ConversationalRetrievalChain.from_llm(
    #         llm=self.llm,
    #         retriever=self.embedding_model.vector_store.as_retriever(),
    #         memory=self.memory,
    #         combine_docs_chain_kwargs={
    #             "prompt": PromptTemplate(
    #                 input_variables=["context", "chat_history", "question", "calculations"],
    #                 template=combine_docs_prompt_template
    #             ),
    #             "document_prompt": PromptTemplate(
    #                 input_variables=["page_content"],
    #                 template="{page_content}"
    #             )
    #         },
    #         return_source_documents=True
    #     )

    # def _create_qa_chain(self) -> ConversationalRetrievalChain:

    #     # Define the template for combining all information
    #     combine_docs_template = """You are a professional financial advisor. Use the following pieces of information to provide detailed financial advice.

    #     Question: {question}
    #     Context Information: {context}

    #     When providing your response:
    #     1. Start with a brief summary of the situation
    #     2. Reference specific numbers and calculations when available
    #     3. Explain financial concepts in simple terms
    #     4. Consider both short-term and long-term implications
    #     5. Provide actionable next steps
        
    #     Key points to address:
    #     - Risk factors and considerations
    #     - Tax implications if applicable
    #     - Alternative scenarios or strategies
    #     - Specific recommendations with rationale
    #     - Timeline for implementation
        
    #     Remember to:
    #     - Be conversational but professional
    #     - Explain your reasoning
    #     - Highlight both opportunities and risks
    #     - Suggest follow-up considerations

    #     Response:"""

    #     # Create the chain
    #     return ConversationalRetrievalChain.from_llm(
    #         llm=self.llm,
    #         retriever=self.embedding_model.vector_store.as_retriever(),
    #         memory=self.memory,
    #         combine_docs_chain_kwargs={
    #             "prompt": PromptTemplate(
    #                 input_variables=["question"],
    #                 template=combine_docs_template
    #             )
    #         },
    #         return_source_documents=True
    #     )

    # @handle_errors
    # def query(self, question: str, context: Dict = None) -> Dict:
    #     """Process a query with error handling and logging"""
    #     logger.info(f"Processing query: {question[:100]}...")
        
    #     # Detect scenario
    #     scenario_type = self.financial_service._detect_financial_scenario(question)
    #     enhanced_context = self.financial_service._get_enhanced_context(scenario_type)
    #     logger.info(f"Detected scenario: {scenario_type}")
        
    #     try:
    #         # Initialize calculations
    #         calculations = {}
    #         calculations_text = ""
            
    #         if context:
    #             if scenario_type in ["retirement", "investment", "debt", 
    #                             "budgeting", "estate_planning", "tax_planning",
    #                             "insurance", "business_finance", "real_estate"]:
    #                 calc_method = getattr(self.financial_calculator, f"calculate_{scenario_type}", None)
    #                 if calc_method:
    #                     calculations = calc_method(**context)
    #                     calculations_text = self._format_calculations(calculations)

    #         # Get LLM response
    #         chain_input = {
    #             "question": question,
    #             "context": enhanced_context,
    #             "chat_history": self.memory.chat_memory.messages,
    #             "calculations": calculations_text or "No specific calculations available."
    #         }

    #         result = self.qa_chain.invoke(chain_input)

    #         response = {
    #             "answer": result["answer"],
    #             "sources": result["source_documents"],
    #             "scenario_type": scenario_type,
    #             "calculations": calculations,
    #             "chat_history": self.memory.chat_memory.messages
    #         }

    #         return response

    #     except Exception as e:
    #         logger.error(f"Error processing query: {str(e)}", exc_info=True)
    #         raise

    # @handle_errors
    # def query(self, question: str, context: Dict = None) -> Dict:
    #     """Process a query with error handling and logging"""
    #     try:
    #         # Detect scenario
    #         scenario_type = self.financial_service._detect_financial_scenario(question)
    #         enhanced_context = self.financial_service._get_enhanced_context(scenario_type)
            
    #         # Get calculations if context exists
    #         calculations_text = ""
    #         calculations = {}
    #         if context:
    #             if scenario_type in ["retirement", "investment", "debt", 
    #                             "budgeting", "estate_planning", "tax_planning",
    #                             "insurance", "business_finance", "real_estate"]:
    #                 calc_method = getattr(self.financial_calculator, f"calculate_{scenario_type}", None)
    #                 if calc_method:
    #                     calculations = calc_method(**context)
    #                     calculations_text = self._format_calculations(calculations)

    #         # Combine context with calculations
    #         # Combine all context information
    #         full_context = f"{enhanced_context}\n\n"
    #         if calculations_text:
    #             full_context += f"Financial Analysis:\n{calculations_text}\n\n"
    #         if self.memory.chat_memory.messages:
    #             full_context += f"Chat History:\n{str(self.memory.chat_memory.messages)}\n\n"

    #         # Get LLM response
    #         result = self.qa_chain({
    #             "question": question
    #             })
            

    #         return {
    #             "answer": result["answer"],
    #             "sources": result["source_documents"],
    #             "scenario_type": scenario_type,
    #             "calculations": calculations,
    #             "chat_history": self.memory.chat_memory.messages
    #         }

    #     except Exception as e:
    #         logger.error(f"Error processing query: {str(e)}", exc_info=True)
    #         raise
    ##### Added new varition########
    ######### Commented on Nov 15, 2024 : Workable code#########
    # def _create_qa_chain(self) -> ConversationalRetrievalChain:
    #     """Create the QA chain with custom prompt"""
        
    #     # Original question prompt
    #     original_question_template = """Based on the following context and original question, provide detailed financial advice.

    #     Context Information: {context}
    #     Original Question: {question}
    #     Chat History: {chat_history}

    #     Please ensure your response:
    #     1. Directly addresses the original question
    #     2. References specific numbers and calculations
    #     3. Provides clear actionable advice
    #     4. Explains any complex terms used
    #     """

    #     # Follow-up question generator prompt
    #     followup_template = """Given the chat history and follow-up question, create a standalone question that captures the full context.

    #     Previous Chat History: {chat_history}
    #     Follow-up Question: {question}

    #     Standalone question:"""
        
    #     # Create the follow-up question generator
    #     question_generator = LLMChain(
    #         llm=self.llm,
    #         prompt=PromptTemplate(
    #             input_variables=["chat_history", "question"],
    #             template=followup_template
    #         )
    #     )

    #     # Document combining prompt for both original and follow-up questions
    #     combine_docs_template = """You are a professional financial advisor. Provide detailed financial advice based on the following information.

    #     Context Information: {context}
    #     Question: {question}

    #     When providing your response:
    #     1. Start with a brief summary of the situation
    #     2. Reference specific numbers and calculations when available
    #     3. Explain financial concepts in simple terms
    #     4. Consider both short-term and long-term implications
    #     5. Provide actionable next steps
        
    #     Key points to address:
    #     - Risk factors and considerations
    #     - Tax implications if applicable
    #     - Alternative scenarios or strategies
    #     - Specific recommendations with rationale
    #     - Timeline for implementation
        
    #     Remember to:
    #     - Be conversational but professional
    #     - Explain your reasoning
    #     - Highlight both opportunities and risks
    #     - Suggest follow-up considerations

    #     Response:"""

    #     # Create the combination chain
    #     combine_docs_chain = StuffDocumentsChain(
    #         llm_chain=LLMChain(
    #             llm=self.llm,
    #             prompt=PromptTemplate(
    #                 input_variables=["context", "question"],
    #                 template=combine_docs_template
    #             )
    #         ),
    #         document_variable_name="context"
    #     )

    #     return ConversationalRetrievalChain(
    #         question_generator=question_generator,
    #         combine_docs_chain=combine_docs_chain,
    #         retriever=self.embedding_model.vector_store.as_retriever(),
    #         memory=self.memory,
    #         return_source_documents=True,
    #         rephrase_question=False  # Don't rephrase original questions
    #     )
    ######### Added on Nov 15, 2024 #########
    def _create_qa_chain(self) -> ConversationalRetrievalChain:
        """Create enhanced QA chain with history awareness"""
        
        # Create a basic prompt that doesn't rely on chat history formatting
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an expert financial advisor. Use the following information to provide detailed financial advice.

            Context: {context}
            Question: {question}

            Provide financial advice that:
            1. References the available context
            2. Explains concepts clearly
            3. Gives specific recommendations
            4. Considers both short and long-term implications

            Response:"""
        )

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.embedding_model.vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 5}
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={
                "prompt": prompt,
            },
            return_source_documents=True,
            chain_type="stuff"
        )

    
    ######### Added on Nov 15, 2024 #########
    def _get_enhanced_prompt_template(self) -> ChatPromptTemplate:
        """Create enhanced prompt template with contextual awareness"""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert financial advisor with deep knowledge of various financial domains.
                        Analyze the user's questions in the context of their previous interactions and financial situation."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{question}"),
            ("system", """Context Information:
                        {context}
                        
                        When providing your response:
                        1. Reference relevant information from previous conversations
                        2. Build upon earlier discussions
                        3. Maintain consistency with previous advice
                        4. Consider both immediate and long-term implications
                        5. Provide practical, actionable recommendations"""),
        ])
    
    def _prepare_enhanced_input(
    self,
    question: str,
    scenario_type: str,
    conversation_context: Dict,
    calculations_text: str,
    is_followup: bool
) -> str:
        """Prepare enhanced input with conversation awareness"""
        
        # Get relevant history if it's a follow-up
        history_context = self._get_relevant_history(scenario_type) if is_followup else ""
        
        # Create separator
        separator = "=" * 40
        
        enhanced_input = f"""
        Financial Advisory {('Follow-up ' if is_followup else '')}Query
        {separator}
        Question: {question}

        {f'Previous Context:{history_context}' if history_context else ''}
        
        Scenario Analysis
        {'-' * 20}
        Type: {scenario_type}
        {conversation_context['enhanced_context']}

        Financial Calculations
        {'-' * 20}
        {calculations_text if calculations_text else 'No specific calculations available for this query.'}

        Please provide {('an updated' if is_followup else 'a')} comprehensive financial analysis that:
        1. {('Builds upon previous discussions and ' if is_followup else '')}Directly answers the question
        2. References specific calculations when available
        3. Explains key financial concepts clearly
        4. Provides actionable recommendations
        5. Highlights potential risks and considerations
        """
        return enhanced_input



    ###################### Workable code: Commented on Nov 15, 2024 ###################  Date : Nov 06, 2024
    # @handle_errors
    # def query(self, question: str, context: Dict = None) -> Dict:
    #     """Process a query with error handling and logging"""
    #     try:
    #         # Detect scenario
    #         scenario_type = self.financial_service._detect_financial_scenario(question)
    #         enhanced_context = self.financial_service._get_enhanced_context(scenario_type)
    #         logger.info(f"Detected scenario: {scenario_type}")
            
    #         # Get calculations if context exists
    #         calculations_text = ""
    #         calculations = {}
    #         if context:
    #             if scenario_type in ["retirement", "investment", "debt", "tax_calculation_scenarios",
    #                             "budgeting", "estate_planning",
    #                             "insurance", "business_finance", "real_estate"]:
    #                 calc_method = getattr(self.financial_calculator, f"calculate_{scenario_type}", None)
    #                 if calc_method:
    #                     calculations = calc_method(**context)
    #                     calculations_text = self._format_calculations(calculations)
    #                     logger.info(f"Calculations performed for {scenario_type}")

    #         # Format input with clear sections
    #         combined_input = f"""
    #         Financial Advisory Query
    #         ======================
    #         Question: {question}

    #         Scenario Analysis
    #         ===============
    #         Type: {scenario_type}
    #         {enhanced_context}

    #         Financial Calculations
    #         ====================
    #         {calculations_text if calculations_text else 'No specific calculations available for this query.'}

    #         Previous Discussion Context
    #         =========================
    #         {str(self.memory.chat_memory.messages) if self.memory.chat_memory.messages else 'No previous conversation history.'}

    #         Please provide a comprehensive financial analysis that:
    #         1. Directly answers the question
    #         2. References specific calculations when available
    #         3. Explains key financial concepts clearly
    #         4. Provides actionable recommendations
    #         5. Highlights potential risks and considerations
    #         """

    #         # Get LLM response
    #         logger.info("Generating response from LLM")
    #         result = self.qa_chain.invoke({"question": combined_input})

    #         # Generate visualizations if calculations exist
    #         visualizations = None
    #         if calculations:
    #             try:
    #                 visualizations = self.visualization_service.create_visualizations(
    #                     scenario_type,
    #                     calculations
    #                 )
    #                 logger.info("Visualizations created successfully")
    #             except Exception as e:
    #                 logger.error(f"Error creating visualizations: {str(e)}")

    #         # Generate follow-up questions
    #         follow_up_questions = self._generate_follow_up_questions(
    #             scenario_type=scenario_type,
    #             original_question=question,
    #             calculations=calculations
    #         )

    #         # Generate report if needed
    #         report_path = None
    #         if calculations or visualizations:
    #             try:
    #                 # Ensure proper dictionary structure for visualizations
    #                 viz_for_report = {
    #                     "figures": visualizations
    #                 } if visualizations else None
                    
    #                 report_path = self.report_service.generate_report(
    #                     scenario_type=scenario_type,
    #                     question=question,
    #                     answer=result["answer"],
    #                     calculations=calculations,
    #                     visualizations=viz_for_report
    #                 )
    #                 logger.info(f"Report generated: {report_path}")
    #             except Exception as e:
    #                 logger.error(f"Error generating report: {str(e)}")

    #         # Prepare enhanced response
    #         response = {
    #             "answer": result["answer"],
    #             "sources": result["source_documents"],
    #             "scenario_type": scenario_type,
    #             "calculations": calculations,
    #             "chat_history": self.memory.chat_memory.messages,
    #             "follow_up_questions": follow_up_questions,
    #             "visualizations": visualizations,
    #             "report_path": report_path
    #         }

    #         logger.info("Query processed successfully")
    #         return response

    #     except Exception as e:
    #         logger.error(f"Error processing query: {str(e)}", exc_info=True)
    #         raise
    ######### Added on Nov 15, 2024: Start #########
    from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

    def _get_chat_history(self) -> List[BaseMessage]:
        """Retrieve chat history as a list of BaseMessage objects"""
        messages = []
        try:
            for msg in self.memory.chat_memory.messages:
                if isinstance(msg, (HumanMessage, AIMessage, BaseMessage)):
                    messages.append(msg)
                elif isinstance(msg, dict):
                    if msg.get("type") == "human":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg.get("type") == "ai":
                        messages.append(AIMessage(content=msg["content"]))
                elif isinstance(msg, str):
                    # Attempt to parse as JSON if it's a string
                    try:
                        msg_dict = json.loads(msg)
                        if msg_dict.get("type") == "human":
                            messages.append(HumanMessage(content=msg_dict["content"]))
                        elif msg_dict.get("type") == "ai":
                            messages.append(AIMessage(content=msg_dict["content"]))
                    except json.JSONDecodeError:
                        # If not JSON, skip this message
                        continue
                
            logger.info(f"Processed chat history messages: {len(messages)}")
            return messages
        except Exception as e:
            logger.error(f"Error processing chat history: {str(e)}")
            return []



    @handle_errors
    def query(self, question: str, context: Dict = None) -> Dict:
        """Process query with enhanced context awareness"""
        try:
            # Detect scenario and get context
            scenario_type = self.financial_service._detect_financial_scenario(question)
            print(f">>>>>>>>>>>>>>>>> Scenario Type: {scenario_type}")
            enhanced_context = self.financial_service._get_enhanced_context(scenario_type)
            print(f">>>>>>>>>>>>>>>>> Enhanced Context: {enhanced_context}")
            # Get calculations if context exists
            calculations_text = ""
            calculations = {}
            if context:
                calc_method = getattr(self.financial_calculator, f"calculate_{scenario_type}", None)
                print(f">>>>>>>>>>>>>>>>> Calc Method: {calc_method}")
                if calc_method:
                    calculations = calc_method(**context)
                    calculations_text = self._format_calculations(calculations)
                    print(f">>>>>>>>>>>>>>>>> Calculations: {calculations_text}")

            # Combine all context into a single string
            combined_context = f"""
            Scenario Type: {scenario_type}
            Enhanced Context: {enhanced_context}
            Calculations: {calculations_text}
            """

            # Prepare input for the chain
            chain_input = {
                "question": question,
                "context": combined_context
            }
            
            # Get LLM response
            result = self.qa_chain(chain_input)
            
            # Update memory
            self.memory.save_context(
                {"question": question},
                {"answer": result["answer"]}
            )
            
            # Process additional features
            visualizations = self._generate_visualizations(scenario_type, calculations)
            report_path = self._generate_report(
                scenario_type,
                question,
                result["answer"],
                calculations,
                visualizations
            )
            
            return {
                "answer": result["answer"],
                "sources": result.get("source_documents", []),
                "scenario_type": scenario_type,
                "calculations": calculations,
                "chat_history": self.memory.load_memory_variables({}),
                "follow_up_questions": self._generate_follow_up_questions(
                    scenario_type,
                    question,
                    calculations
                ),
                "visualizations": visualizations,
                "report_path": report_path,
                "is_followup": bool(self.memory.chat_memory.messages)
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            raise
    ######### Added on Nov 15, 2024: End #########
    ######### Added on Nov 15, 2024: Start #########
    def _manage_conversation_context(self, scenario_type: str, question: str, previous_context: Dict = None) -> Dict:
        """Manage conversation context across interactions"""
        context = {
            "current_scenario": scenario_type,
            "previous_context": previous_context or {},
            "scenario_history": self._get_relevant_history(scenario_type),
            "enhanced_context": self.financial_service._get_enhanced_context(scenario_type)
        }
        
        # Update scenario history
        self._update_scenario_history(scenario_type, question)
        
        return context

    def _get_relevant_history(self, scenario_type: str) -> str:
        """Get relevant conversation history for the current scenario"""
        history = []
        messages = self.memory.chat_memory.messages
        
        # Get last few relevant messages
        for msg in messages[-4:]:  # Get last 2 exchanges (4 messages)
            if hasattr(msg, 'content'):
                history.append(f"{'Q:' if len(history) % 2 == 0 else 'A:'} {msg.content}")
        
        return "\n".join(history) if history else ""

    def _update_scenario_history(self, scenario_type: str, question: str):
        """Update scenario-specific history"""
        self.memory.chat_memory.add_user_message(
            question,
            #additional_kwargs={"scenario_type": scenario_type}
        )
    ######### Added on Nov 15, 2024: End #########
    # @handle_errors
    def _format_calculations(self, calculations: Dict) -> str:
        """Format calculations with error handling"""
        try:
            if not calculations:
                return ""
            
            text = "\nFinancial Analysis:\n"
            for key, value in calculations.items():
                if isinstance(value, (int, float)):
                    text += f"{key}: ₹{value:,.2f}\n"
                elif isinstance(value, dict):
                    text += f"\n{key}:\n"
                    for k, v in value.items():
                        formatted_value = f"₹{v:,.2f}" if isinstance(v, (int, float)) else str(v)
                        text += f"  {k}: {formatted_value}\n"
            
            return text
        except Exception as e:
            logger.error(f"Error formatting calculations: {str(e)}")
            return "Error formatting calculations"
        
    def _generate_follow_up_questions(
    self,
    scenario_type: str,
    original_question: str,
    calculations: Dict
) -> List[str]:
        """Generate contextual follow-up questions"""
        
        base_questions = {
            "retirement": [
                "Would you like to explore how changing your retirement age affects these calculations?",
                "Should we analyze different investment risk levels for your retirement portfolio?",
                "Would you like to see how inflation might impact your retirement savings?"
            ],
            "investment": [
                "Would you like to see how different asset allocations might affect your returns?",
                "Should we analyze the tax implications of these investments?",
                "Would you like to explore different investment timeframes?"
            ],
            "debt": [
                "Would you like to see how accelerated payments would affect your debt payoff timeline?",
                "Should we compare different debt repayment strategies?",
                "Would you like to analyze debt consolidation options?"
            ],
            "tax": [
                "Would you like to explore potential tax deductions you might be eligible for?",
                "Should we analyze different tax-advantaged investment options?",
                "Would you like to see how changes in income might affect your tax situation?"
            ],
            "insurance": [
                "Would you like to compare different insurance coverage levels?",
                "Should we analyze how your insurance needs might change over time?",
                "Would you like to explore other types of insurance coverage?"
            ],
            "estate_planning": [
                "Would you like to explore different trust options?",
                "Should we analyze the tax implications of your estate plan?",
                "Would you like to review beneficiary designation strategies?"
            ]
        }

        # Get default questions for the scenario
        follow_ups = base_questions.get(scenario_type, [
            "Would you like more detailed analysis?",
            "Should we explore specific aspects of this topic?",
            "Would you like to see additional calculations?"
        ])

        # Add calculation-specific questions if available
        if calculations:
            if "total_amount" in calculations:
                follow_ups.append(f"Would you like to see a breakdown of the {scenario_type} calculations?")
            if "projected_values" in calculations:
                follow_ups.append("Would you like to explore different projection scenarios?")

        return follow_ups[:3]  # Return top 3 most relevant questions
    
    def _generate_visualizations(self, scenario_type: str, calculations: Dict) -> Optional[Dict]:
        """Generate visualizations for the scenario"""
        if not calculations:
            return None
            
        try:
            return self.visualization_service.create_visualizations(
                scenario_type,
                calculations
            )
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")
            return None
        
    def _generate_report(
        self,
        scenario_type: str,
        question: str,
        answer: str,
        calculations: Dict,
        visualizations: Dict
    ) -> Optional[str]:
        """Generate PDF report"""
        if not (calculations or visualizations):
            return None
            
        try:
            report_path = self.report_service.generate_report(
                scenario_type=scenario_type,
                question=question,
                answer=answer,
                calculations=calculations,
                visualizations=visualizations
            )
            return report_path
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return None

    def reset_memory(self):
        """Reset the conversation memory"""
        self.memory.clear()