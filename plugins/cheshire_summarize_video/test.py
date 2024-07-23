from youtube_transcript_api import YouTubeTranscriptApi, Transcript
from .get_youtube_video_id import get_youtube_video_id

if __name__ == "__main__":
    id = get_youtube_video_id("https://www.youtube.com/watch?v=hJWXIy_bNsQ")

    transcript_list = YouTubeTranscriptApi.list_transcripts(id)
    transcript:Transcript = transcript_list.find_transcript(['en', 'fr'])

    print(" ".join([x['text'] for x in transcript.fetch()]))
    # transcript = YouTubeTranscriptApi.get_transcript(id)
    # print(transcript)