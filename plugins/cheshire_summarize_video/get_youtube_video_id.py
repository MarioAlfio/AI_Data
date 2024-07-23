import re
from urllib.parse import parse_qs, urlparse

def get_youtube_video_id(url):
    """
    Extract the video ID from a YouTube URL.

    Parameters:
    url (str): The URL of the YouTube video.

    Returns:
    str: The video ID if found, None otherwise.
    """

    # might not work if the id isn't 11 caracters
    video_id_regex = re.compile(r'^[a-zA-Z0-9_-]{11}$') 
    if video_id_regex.match(url):
        return url
    
    # Check if URL is in the standard format
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return query_params['v'][0].split('?')[0]
    
    # Check if URL is in the shortened format
    match = re.match(r'^(https?://)?(www\.)?(youtu\.be/)([^&?/]+)', url)
    if match:
        return match.group(4)
    
    return None

if __name__ == "__main__":
    # Example usage:
    examples = [
        "https://www.youtube.com/watch?v=e0Qp-AOBj54",
        "https://youtu.be/e0Qp-AOBj54?si=GQ6VTIIyS1Qq9aqk",
        "e0Qp-AOBj54",
        "https://www.youtube.com/watch?v=e0Qp-AOBj54?si=GQ6VTIIyS1Qq9aqk"
    ]

    for url in examples:
        video_id = get_youtube_video_id(url)
        print(f"Input: {url} -> Video ID: {video_id}")