# main.py
import os
import sys
from dotenv import load_dotenv

# Force add the current root to path for local & docker consistency
current_root = os.path.dirname(os.path.abspath(__file__))
if current_root not in sys.path:
    sys.path.insert(0, current_root)

load_dotenv()

from langgraph.graph import StateGraph, END, START
from app.agents.supervisor import supervisor_node, route_from_supervisor, AgentState
from app.agents.nodes import answer_agent_node, quiz_agent_node, summary_agent_node

def create_isa_app():
    builder = StateGraph(AgentState)

    # 1. Add Nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("answer_agent", answer_agent_node)
    builder.add_node("quiz_agent", quiz_agent_node)
    builder.add_node("summary_agent", summary_agent_node)

    # 2. Define Edges
    builder.add_edge(START, "supervisor")
    
    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "answer_agent": "answer_agent",
            "quiz_agent": "quiz_agent",
            "summary_agent": "summary_agent",
            END: END
        }
    )

    builder.add_edge("answer_agent", END)
    builder.add_edge("quiz_agent", END)
    builder.add_edge("summary_agent", END)

    return builder.compile()

# This part only runs during local manual testing
if __name__ == "__main__":
    app = create_isa_app()
    print("ISA Graph compiled successfully.")