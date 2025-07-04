
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QuizGenerationRequest(BaseModel):
    source_type: str = Field(..., description="Type of source: 'youtube', 'text', or 'document'")
    source: str = Field(..., description="URL for youtube, text content, or file path for document")
    num_questions: int = Field(5, description="Number of questions to generate")
    difficulty: Optional[str] = Field("medium", description="Difficulty level of the quiz")
    previous_questions: Optional[List[str]] = Field([], description="A list of previously generated question texts to avoid repetition.")

class Question(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    timestamp: Optional[str] = None

class QuizResponse(BaseModel):
    questions: List[Question]
    summary: Optional[str] = None
    flashcards: Optional[List[Dict[str, str]]] = None

class Flashcard(BaseModel):
    question: str
    answer: str

class RecommendationRequest(BaseModel):
    topic: str
    num_recommendations: int = 5

class VideoRecommendation(BaseModel):
    title: str
    video_id: str
    url: str

class RecommendationResponse(BaseModel):
    recommendations: List[VideoRecommendation]
