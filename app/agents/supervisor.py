import os
from typing import Literal, TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from pydantic import BaseModel, Field

# 1. Structured Output Schema (Internal Use Only)
class RouteDecision(BaseModel):
    """Decide which agent to call next based on the conversation history."""
    next_node: Literal["answer_agent", "quiz_agent", "summary_agent", "FINISH"] = Field(
        description="Select the next specialist or finish the task."
    )
    reasoning: str = Field(description="Explanation for the routing choice.")

# 2. State Definition (Ensuring it matches your main.py)
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The chat history"]
    next_node: str # We store this as a string to avoid serialization issues

# 3. The Supervisor Node
def supervisor_node(state: AgentState):
    """
    Analyzes intent and routes the user. 
    Strictly returns a string to ensure API compatibility.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # Force the LLM to provide a structured JSON response
    structured_llm = llm.with_structured_output(RouteDecision)
    
    system_prompt = """
    You are the Lead Dispatcher for the ISA (Intelligent Study Assistant).
    
    DEPARTMENTS:
    - answer_agent: Technical questions, 'How-to' explanations, or architectural concepts.
    - quiz_agent: Requests for practice questions or knowledge testing.
    - summary_agent: High-level overviews of specific books or the whole library.
    - FINISH: If the user is saying goodbye or the query is fully answered.

    EXAMPLES:
    - "What is a Fencing Token?" -> answer_agent
    - "Test me on CAP theorem." -> quiz_agent
    - "Summarize DDIA." -> summary_agent
    - "Thanks, bye!" -> FINISH
    """

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    # Invoke the structured LLM
    decision = structured_llm.invoke(messages)
    
    # Log the internal reasoning for debugging
    print(f"[Supervisor] Routing to: {decision.next_node} | Reason: {decision.reasoning}")
    
    # 🌟 Staff Fix: Convert to string explicitly to prevent 500 Errors
    return {"next_node": str(decision.next_node)}

# 4. Routing Function
def route_from_supervisor(state: AgentState):
    """Helper for LangGraph conditional edges."""
    return state.get("next_node", "FINISH")