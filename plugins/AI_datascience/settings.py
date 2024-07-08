from enum import Enum
from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin


class MySettings(BaseModel):
    data_prompt: str = """Sei un assistente AI che sa tutto sull'intelligenza artificiale generativa (AI) per gli data scientist.
                          Contribuisci a elevare la carriera di Data Science utilizzando l'IA.
                        
                        """
    summarization_prompt: str = """Crea un riassunto della trascrizione di seguito riportata su un video. Di seguito la trascrizione:
                                
                                """
    group_size: int = 3



@plugin
def settings_model():
    return MySettings
