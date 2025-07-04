
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from app.core.config import settings
from app.services.youtube_service import get_video_recommendations

class RecommendationService:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-3.5-turbo")

    def get_llm_recommendations(self, topic: str, num_recommendations: int = 3):
        prompt = ChatPromptTemplate.from_template(
            """Given the topic '{topic}', what are some related topics or next steps for a learner? 
            Provide a comma-separated list of 3-5 keywords or short phrases.
            For example, if the topic is 'Introduction to Python', you could suggest: 'Python data structures, Python functions, Object-oriented programming in Python'.
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        
        recommended_topics_str = chain.invoke({"topic": topic})
        recommended_topics = [t.strip() for t in recommended_topics_str.split(',')]

        all_recommendations = []
        for rec_topic in recommended_topics:
            # Get 1-2 videos per recommended topic to get a variety
            video_recs = get_video_recommendations(rec_topic, num_recommendations=2)
            all_recommendations.extend(video_recs)
            if len(all_recommendations) >= num_recommendations:
                break
        
        return all_recommendations[:num_recommendations]
