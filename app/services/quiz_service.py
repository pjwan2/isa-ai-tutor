from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.schemas.quiz import QuizResponse
import os

class QuizService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.structured_llm = self.llm.with_structured_output(QuizResponse)
        self._load_template()

    def _load_template(self):
        path = os.path.join(os.path.dirname(__file__), "../prompts/quiz_agent_prompt.xml")
        with open(path, "r", encoding="utf-8") as f:
            self.template = f.read()

    def generate_exam(self, topic: str, num_questions: int = 1):
        prompt = PromptTemplate(
            input_variables=["topic_summary", "num_questions"],
            template=self.template
        ).format(topic_summary=topic, num_questions=num_questions)
        
        return self.structured_llm.invoke(prompt)

quiz_service = QuizService()