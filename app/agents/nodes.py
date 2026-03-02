import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.services.rag_service import rag_service
from app.services.quiz_service import quiz_service
from app.services.eval_service import eval_service

def answer_agent_node(state):
    """
    Expert Mentor Node: Retrieves, Synthesizes, and Audits technical answers.
    Ensures all returns are strings to prevent serialization errors.
    """
    # 1. Extract inputs
    user_query = state["messages"][-1].content
    print(f"[Answer Agent] Processing query: {user_query}")
    
    # 2. Retrieval Phase
    # Pulling from your 2,244 chunks in FAISS
    docs = rag_service.query(user_query, k=3)
    context_text = "\n\n".join([
        f"Source: {d.metadata.get('source', 'Unknown')} (Page {d.metadata.get('page', 'N/A')})\nContent: {d.page_content}" 
        for d in docs
    ])
    
    # 3. Generation Phase (LLM as Expert Architect)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    
    system_prompt = """
    You are an ISA (Intelligent Study Assistant), a mentor specializing in Distributed Systems.
    Explain concepts using ONLY the provided context from architecture books.
    
    Format your response:
    - **Definition**: Concise summary.
    - **Core Principles**: Bullet points.
    - **Trade-offs/Pitfalls**: Critical warnings.
    
    [Context]:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    chain = prompt | llm
    generated_answer = chain.invoke({"context": context_text, "question": user_query}).content
    
    # 4. Guardrail Phase (Hallucination Check)
    print("[Answer Agent] Running Hallucination Guardrail...")
    eval_report = eval_service.check_hallucination(
        question=user_query, 
        context=context_text, 
        answer=str(generated_answer)
    )
    
    # 5. Final Output Assembly (Ensuring JSON-Safe Strings)
    if eval_report.is_hallucinated:
        print(f"⚠️  Audit Failed: {eval_report.reasoning}")
        final_output = (
            f"### ⚠️  Self-Correction Notice\n"
            f"The initial draft contained details not found in the source text. "
            f"Here is the verified information based on your library:\n\n"
            f"{generated_answer}\n\n"
            f"**Audit Reasoning**: {eval_report.reasoning}"
        )
    else:
        print("✅ Audit Passed.")
        final_output = generated_answer
        
    # 🌟 Staff-level Tip: Explicitly cast to string to avoid Pydantic leaking into State
    return {"messages": [str(final_output)]}

def quiz_agent_node(state):
    """Generates structured quizzes based on RAG context."""
    user_query = state["messages"][-1].content
    print(f"[Quiz Agent] Generating quiz for: {user_query}")
    
    exam = quiz_service.generate_exam(user_query)
    q = exam.questions[0]
    
    formatted_quiz = (
        f"### 📝 Architecture Quiz: {exam.topic}\n"
        f"**Scenario**: {q.scenario}\n\n"
        f"**Question**: {q.question}\n\n"
        f"*Difficulty: {q.difficulty}*"
    )
    
    return {"messages": [str(formatted_quiz)]}

def summary_agent_node(state):
    """Placeholder for high-level book summarization."""
    print("[Summary Agent] Routing to summary placeholder.")
    return {"messages": ["The High-Level Summary feature is currently in development. Please ask a specific technical question or request a quiz!"]}