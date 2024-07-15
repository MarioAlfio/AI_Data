from enum import Enum
from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin


class MySettings(BaseModel):
    data_prompt: str = """Sei un assistente AI che sa tutto sull'intelligenza artificiale generativa (AI) per gli data scientist.
                          Contribuisci a elevare la carriera di Data Science utilizzando l'IA.
                        
                        """
    summarization_prompt: str = """Crea un riassunto della trascrizione di seguito riportata su un video.
                                Ti verrà caricata una lista di capitoli di video educativi sui temi riguardati la data scientist con AI, per esempio 'La differenza tra AI discriminativa e AI generativa'.

                                Ogni capitolo della lista è formattato in questo modo: timestamp | Titolo
                                Dato il seguente riassunto di tutto il video. Nella risposta ritorna il riassunto del capitolo del video che ritieni più rilevante.
                                """
    group_size: int = 3

    supabase_url: str

    supabase_key: str 

class Config:
    env_file = ".env"
    extra = "ignore"

@plugin
def settings_model():
    return MySettings
