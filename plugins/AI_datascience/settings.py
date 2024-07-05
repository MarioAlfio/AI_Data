from enum import Enum
from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin


class MySettings(BaseModel):
    data_prompt: str = """You are an AI assistant who knows all about Generative Artificial Intelligence (AI) for data scientists.
                            Help elevate Data Science Career by using AI.
                        
                        """
    summarization_prompt: str = """Crea un riassunto della trascrizione di seguito riportata su un video. Di seguito la trascrizione:
                        """
    group_size: int = 5



@plugin
def settings_model():
    return MySettings
