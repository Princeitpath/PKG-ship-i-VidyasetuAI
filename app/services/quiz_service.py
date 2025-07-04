
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import json

from app.core.config import settings
from app.services.youtube_service import get_youtube_transcript, format_transcript_with_timestamps

# Define the state for our LangGraph
class GraphState(TypedDict):
    source_text: str
    num_questions: int
    difficulty: str
    generated_questions: List[str]
    quiz_json: str

class QuizGenerationService:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-3.5-turbo")
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(GraphState)
        graph.add_node("generate_questions", self._generate_questions_node)
        graph.add_node("format_quiz", self._format_quiz_node)

        graph.set_entry_point("generate_questions")
        graph.add_edge("generate_questions", "format_quiz")
        graph.add_edge("format_quiz", END)

        return graph.compile()

    def _generate_questions_node(self, state: GraphState):
        prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant designed to create educational materials.
            Based on the following text, please generate a comprehensive JSON output that includes:
            1.  A brief summary of the text (about 2-3 sentences).
            2.  A list of {num_questions} multiple-choice questions of {difficulty} difficulty.
            3.  For each question, provide the question text, a list of 4 options, the correct answer, an explanation, and the starting timestamp from the text where the answer is discussed (if available).
            4.  A list of {num_questions} flashcards, each with a question and a concise answer.

            Avoid generating questions you have already generated: {generated_questions}

            Text with Timestamps:
            {source_text}

            Provide the entire output as a single JSON object with the keys: 'summary', 'questions', and 'flashcards'.
            The 'questions' key should be a list of objects, each with 'question_text', 'options', 'correct_answer', 'explanation', and 'timestamp'.
            The 'flashcards' key should be a list of objects, each with 'question' and 'answer'.
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        generated_json = chain.invoke(state)
        
        # This is a simplified approach. In a real scenario, you'd parse the output 
        # and append to the list of generated questions.
        # For now, we will just pass the generated json through
        updated_generated_questions = state['generated_questions'] # In a real app, you'd update this

        return {"generated_questions": updated_generated_questions, "quiz_json": generated_json}

    def _format_quiz_node(self, state: GraphState):
        # The output from the LLM should already be in JSON format.
        # Here you could add validation or further formatting if needed.
        return {"quiz_json": state["quiz_json"]}

    def generate_quiz(self, source_type: str, source: str, num_questions: int, difficulty: str, previous_questions: List[str]):
        if source_type == 'youtube':
            transcript = get_youtube_transcript(source)
            source_text = format_transcript_with_timestamps(transcript)
        elif source_type == 'text':
            source_text = source
        elif source_type == 'document':
            # You would add logic here to read the document content
            with open(source, 'r') as f:
                source_text = f.read()
        else:
            raise ValueError("Unsupported source type")

        initial_state = {
            "source_text": source_text,
            "num_questions": num_questions,
            "difficulty": difficulty,
            "generated_questions": previous_questions,
        }

        final_state = self.graph.invoke(initial_state)
        return json.loads(final_state['quiz_json'])
