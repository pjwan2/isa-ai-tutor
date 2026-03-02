from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    SENIOR = "Senior"
    STAFF = "Staff"
    PRINCIPAL = "Principal"

class QuestionType(str, Enum):
    SYSTEM_DESIGN = "System Design"
    STATE_MANAGEMENT = "State Management"
    ALGORITHM_OPTIMIZATION = "Algorithm Optimization"

class QuizQuestion(BaseModel):
    id: str = Field(..., description="Unique UUID for the question")
    question_type: QuestionType = Field(..., description="Category of the question")
    difficulty: DifficultyLevel = Field(..., description="Target engineering level")
    scenario: str = Field(..., description="Detailed engineering failure or high-concurrency business scenario")
    question: str = Field(..., description="The specific architectural or optimization question based on the scenario")
    expected_architecture_components: List[str] = Field(..., description="Key technical stack or concepts required in a correct answer")
    detailed_explanation: str = Field(..., description="Staff-level explanation of the optimal architecture, trade-offs, and fallback strategies")

class QuizResponse(BaseModel):
    topic: str = Field(..., description="The core topic being tested")
    questions: List[QuizQuestion] = Field(..., description="List of generated questions")