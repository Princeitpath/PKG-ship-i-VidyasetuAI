
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.config import settings
from googleapiclient.discovery import build

def get_youtube_transcript(video_url: str):
    video_id = video_url.split("v=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript

def format_transcript_with_timestamps(transcript: list):
    formatted_transcript = ""
    for entry in transcript:
        start_time = entry['start']
        text = entry['text']
        formatted_transcript += f"[{start_time}] {text}\n"
    return formatted_transcript

def get_video_recommendations(topic: str, num_recommendations: int = 5):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=f"{topic} tutorial",
        part="snippet",
        type="video",
        maxResults=num_recommendations
    )
    response = request.execute()

    recommendations = []
    for item in response.get("items", []) :
        recommendations.append({
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })

    return recommendations
