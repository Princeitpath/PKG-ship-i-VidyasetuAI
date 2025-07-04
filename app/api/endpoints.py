
from fastapi import APIRouter, HTTPException
from app.models.models import (
    QuizGenerationRequest, 
    QuizResponse, 
    RecommendationRequest, 
    RecommendationResponse
)
from app.services.quiz_service import QuizGenerationService
from app.services.recommendation_service import RecommendationService

router = APIRouter()
quiz_service = QuizGenerationService()
recommendation_service = RecommendationService()

@router.post("/generate_quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizGenerationRequest):
    try:
        quiz_data = quiz_service.generate_quiz(
            source_type=request.source_type,
            source=request.source,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            previous_questions=request.previous_questions
        )
        return QuizResponse(**quiz_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations", response_model=RecommendationResponse)
async def recommendations(request: RecommendationRequest):
    try:
        recommendations = recommendation_service.get_llm_recommendations(
            topic=request.topic,
            num_recommendations=request.num_recommendations
        )
        return RecommendationResponse(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
