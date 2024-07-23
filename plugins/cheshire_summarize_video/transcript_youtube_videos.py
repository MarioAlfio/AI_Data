from cat.mad_hatter.decorators import tool, hook, plugin # type: ignore
from pydantic import BaseModel # type: ignore
from datetime import date
from youtube_transcript_api import YouTubeTranscriptApi, Transcript

from .get_youtube_video_id import get_youtube_video_id

class MySettings(BaseModel):
    required_int: int
    optional_int: int = 69
    required_str: str
    optional_str: str = "meow"
    required_date: date
    optional_date: date = 1679616000 # type: ignore

# @plugin
def settings_model():
    return MySettings

@tool(examples=["Can you summarize this Youtube Video ? https://www.youtube.com/watch?v=GyllRd2E6fg", "Can you explain https://youtu.be/XwL_cRuXM2E ?"])
def get_youtube_transcription(tool_input, cat):
    """Useful for reading the transcription of a YouTube video from an URL. This tool will always be used when a user sends the link.
    For example, a user may ask, "Can you tell me about https://www.youtube.com/watch?v=GyllRd2E6fg ?"
    Input is the youtube video URL that contains youtube.com or youtu.be. Example input: https://youtu.be/GyllRd2E6fg?si=esjbQcs_w3Jz8t7U"""
    print("Input extracted for youtube transcription is", tool_input)
    id = get_youtube_video_id(tool_input)

    transcript_list = YouTubeTranscriptApi.list_transcripts(id)
    transcript:Transcript = transcript_list.find_transcript(['en', 'fr'])

    return " ".join([x['text'] for x in transcript.fetch()])