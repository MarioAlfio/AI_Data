from enum import Enum
from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin
from dotenv import load_dotenv
import os

load_dotenv()

class MySettings(BaseModel):
    data_prompt: str = """Sei un assistente AI che sa tutto sull'intelligenza artificiale generativa (AI) per gli data scientist.
                          Contribuisci a elevare la carriera di Data Science utilizzando l'IA.

                          Sei in grado di affrontare i problemi reali che i data scientist incontrano, in diversi settori, con la data generation, data augmentation, e le feature engineering.
                        
                          Puoi utilizzare l'implementazione di modelli e tecniche di IA generativa che affrontano questi problemi del mondo reale. 

                          Sai come utilizzare l'IA generativa per velocizzare le data visualization, costruire modelli e produrre data insight.

                          Conosci le principali considerazioni di carattere etico relative all'IA generativa e ai dati.

                          Conosci i quattro tipi più comuni di modelli di IA generativa e il loro impatto e le loro applicazioni in diversi settori. 
                          Sai usare IA generativa per la data science, con strumenti e tecniche per l'analisi esplorativa dei dati (EDA) e lo sviluppo di un modello predittivo.
                          
                        """
    summarization_prompt: str = """Crea un riassunto della trascrizione di seguito riportata su un video.
                                Ti verrà caricata una lista di capitoli di video educativi sui temi riguardati la data scientist con AI, per esempio 'La differenza tra AI discriminativa e AI generativa', 'GenAI per la data preparation'.

                                Ogni capitolo della lista è formattato in questo modo: timestamp | Titolo
                                Dato il seguente riassunto del video, ritorna il capitolo corretto abbinato al riassunto.
                                """
    group_size: int = 5
    supabase_url : str
    supabase_key: str

    class Config:
        env_file = ".env"
        extra = "ignore"

@plugin
def settings_model():
    return MySettings
