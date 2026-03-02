import os
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class EvalResult(BaseModel):
    is_hallucinated: bool = Field(..., description="True if the answer contains info NOT in the context.")
    reasoning: str = Field(..., description="Reasoning behind the verdict.")

class EvalService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.structured_judge = self.llm.with_structured_output(EvalResult)

    def check_hallucination(self, question: str, context: str, answer: str) -> EvalResult:
        template = """
        You are a strict technical auditor. Compare the ANSWER against the CONTEXT provided.
        Identify if the ANSWER makes any claims not supported by the CONTEXT.
        
        [QUESTION]: {question}
        [CONTEXT]: {context}
        [ANSWER]: {answer}
        """
        prompt = PromptTemplate.from_template(template)
        formatted_prompt = prompt.format(question=question, context=context, answer=answer)
        
        return self.structured_judge.invoke(formatted_prompt)

eval_service = EvalService()