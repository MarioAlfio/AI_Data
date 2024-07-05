from cat.mad_hatter.decorators import hook
import langchain
from langchain.docstore.document import Document
from cat.log import log
from enum import Enum
import json

from langchain.document_loaders.parsers.language.language_parser import LanguageParser
from langchain.document_loaders.parsers.msword import MsWordParser

from .parsers import YoutubeParser, TableParser, JSONParser


@hook
def rabbithole_instantiates_parsers(file_handlers: dict, cat) -> dict:

    new_handlers = {
        "application/binary": YoutubeParser(),
        "video/mp4": YoutubeParser(),
        "text/csv": TableParser(),
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": TableParser(),
        "text/x-python": LanguageParser(language="python"),
        "text/javascript": LanguageParser(language="js"),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": MsWordParser(),
        "application/msword": MsWordParser(),
        "application/json": JSONParser()

    }
    file_handlers = file_handlers | new_handlers
    return file_handlers


chaptersList = [
    {
        "timestamp": 0,
        "title": "Introduzione"
    },
    {
        "timestamp": 60,
        "title": "Rappresentazioni: diagramma a torta, a barre, istogramma, grafico"
    },
    {
        "timestamp": 90,
        "title": "Misure di tendenza: media, moda e mediana"
    },
    {
        "timestamp": 236,
         "title": "La gaussiana o normale"
    },
    {
        "timestamp": 270,
         "title": "Misure di dispersione: range, intervallo interquartile, deviazione standard o scarto quadratico medio"
    },
    {
        "timestamp": 440,
         "title": "Come fare la regressione"
    },
    {
        "timestamp": 472,
         "title": "L'indice di correlazione"
    },
    {
        "timestamp": 603,
         "title": "Il lieto fine"
    },

]


@hook
def before_rabbithole_stores_documents(docs, cat):
    # Load settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    group_size = settings["group_size"]
    print(group_size)

    # LLM Chain from Langchain
    summarization_prompt = f"{settings['summarization_prompt']}\n {{text}}"
    summarization_chain = langchain.chains.LLMChain(
        llm=cat._llm,
        verbose=False,
        prompt=langchain.PromptTemplate(template=summarization_prompt,
                                        input_variables=["text"]),
    )

    notification = f"Starting to summarize {len(docs)}",
    log(notification, "INFO")
    cat.send_ws_message(notification, msg_type="notification")

    # we will store iterative summaries all together in a list
    all_summaries = []

    # Compute total summaries for progress notification
    n_summaries = len(docs) // group_size
    print(len(docs))
    print(n_summaries)
    print(group_size)

    # make summaries of groups of docs
    for n, i in enumerate(range(0, len(docs), group_size)):
        if n_summaries==0:
            n_summaries = 1
            # Notify the admin of the progress
            progress = (n * 100) // n_summaries
            print(progress)
            message = f"{progress}% of summarization"
            cat.send_ws_message(message, msg_type="notification")
            log(message, "INFO")

        # Get the text from groups of docs and join to string
        group = docs[i: i + group_size]
        group = list(map(lambda d: d.page_content, group))
        text_to_summarize = "\n".join(group)

        # Summarize and add metadata
        summary = summarization_chain.run(text_to_summarize)
        summary = Document(page_content=summary)
        summary.metadata["is_summary"] = True
        
        print(text_to_summarize)
        print(summary)

        # mi creo la stringa 
        chapters="\n".join("|".join((str(chapter["timestamp"]),chapter["title"])) for chapter in chaptersList)
        # 0 | Come funziona useSTate
        # 123 | Come funziona ....
        prompt = f"""Questa è una lista di capitoli di un video: {chapters}.\n\nOgni capitolo della lista è formattato 
        in questo modo: seconds | Titolo\n\nRispondi dicendo quale di questi capitoli è relativo a questa parte di testo:{summary}. 
        Nella risposta ricopia solo il capitolo che hai scelto.
        """

        res = cat.llm(prompt)

        # risultato di che capitolo capisce di inserire
        summary.metadata["chapter"] = res
        print(res)

        # add summary to list of all summaries
        all_summaries.append(summary)

    docs.extend(all_summaries)

    return docs

@hook
def agent_prompt_prefix(prompt_prefix, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    prompt_prefix = settings["data_prompt"]

    return prompt_prefix

@hook  # default priority = 1
def agent_prompt_suffix(prompt_suffix, cat):
    # tell the LLM to always answer in a specific language
    prompt_suffix = """ 
    # Context

    {episodic_memory}

    {declarative_memory}

    {tools_output}

    ALWAYS answer in Italian. 
    Write the most important words in bold. 

    ## Conversation until now:{chat_history}
     - Human: {input}
       - AI: 
    """
    return prompt_suffix

@hook  # default priority = 1
def agent_fast_reply(fast_reply, cat):

    print(cat.working_memory["declarative_memories"])
    
    if len(cat.working_memory["declarative_memories"]) == 0:
        fast_reply["output"] = "Sorry, I'm afraid I don't know the answer"

    return fast_reply
