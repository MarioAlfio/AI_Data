from enum import Enum
from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin
from dotenv import load_dotenv
import os

load_dotenv()

class MySettings(BaseModel):
    data_prompt: str = """Sei un assistente AI che sa tutto sull'intelligenza artificiale generativa (AI) per gli data scientist.
                          Contribuisci a elevare la carriera di Data Science utilizzando l'IA.

                          Sei un'assistente in grado di parlare di temi riguardati la data scientist con AI, per esempio argomenti riguardati i modelli e gli approcci di AI discriminativa e di AI generativa.
                          
                        """
    summarization_prompt: str = """Crea un riassunto della trascrizione di seguito riportata su un video.
                                Ti verrà caricata una lista di capitoli di video educativi sui temi riguardati la data scientist con AI, per esempio 'La differenza tra AI discriminativa e AI generativa'.

                                Ogni capitolo della lista è formattato in questo modo: timestamp | Titolo
                                Dato il seguente riassunto del video, ritorna il capitolo corretto abbinato al riassunto.
                                """
    group_size: int = 5
    supabase_url : str = os.getenv("supabase_url")
    supabase_key: str = os.getenv("supabase_key")

    class Config:
        env_file = ".env"
        extra = "ignore"

@plugin
def settings_model():
    return MySettings


