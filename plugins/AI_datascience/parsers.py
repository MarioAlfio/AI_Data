import json
import pandas as pd

from abc import ABC
from typing import Iterator

from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseBlobParser
from langchain.document_loaders.blob_loaders.schema import Blob

class YoutubeParser(BaseBlobParser, ABC):
    def __init__(self):
        self.formatter = TextFormatter()

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        video_id = extract.video_id(blob.source)
        print(video_id)

        transcript = YouTubeTranscriptApi.get_transcripts([video_id], languages=["it"], preserve_formatting=True)
        text = self.formatter.format_transcript(transcript[0][video_id])

        yield Document(page_content=text, metadata={"video_id":video_id})


class TableParser(BaseBlobParser, ABC):

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:

        with blob.as_bytes_io() as file:
            if blob.mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                content = pd.read_excel(file, index_col=0)
            elif blob.mimetype == "text/csv":
                content = pd.read_csv(file, index_col=0)

        content = content.to_dict()

        yield Document(page_content=json.dumps(content), metadata={})


class JSONParser(BaseBlobParser, ABC):

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:

        with blob.as_bytes_io() as file:
            text = json.load(file)

        yield Document(page_content=text, metadata={})