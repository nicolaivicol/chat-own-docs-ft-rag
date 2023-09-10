from pathlib import Path
import os
import logging

# Directories
# ******************************************************************************
DIR_PROJ = (Path(__file__) / '..').resolve()
DIR_DATA = f'{DIR_PROJ}/data'
DIR_ARTIFACTS = f'{DIR_PROJ}/artifacts'
os.makedirs(DIR_DATA, exist_ok=True)
os.makedirs(DIR_ARTIFACTS, exist_ok=True)

# Content API
# ******************************************************************************
URL_API_CONTENT = 'https://servicii.gov.md/rsspa-api'

# chatgpt
# *******************************************************************************
OPENAI_API_KEY = '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'
MODEL = "ft:gpt-3.5-turbo-0613:personal:manual-09-1650:7wsoqzk8"
# last: "ft:gpt-3.5-turbo-0613:personal:manual-10-0300:7x2RQGVj"
# best: "ft:gpt-3.5-turbo-0613:personal:manual-09-1650:7wsoqzk8"
MODEL_EMBEDDING = "text-embedding-ada-002"
TEMPERATURE = 0.5
MAX_TOKENS = 1000
TOP_P = 1
FREQUENCY_PENALTY = 0.33
PRESENCE_PENALTY = 0.33
ROLE_SYSTEM = (
    "Eu sunt chatbotul pentru portalul despre servicii guvernamentale https://servicii.gov.md/ al Republicii Moldova. "
    "Sunt peste 700 de servicii."
    "Sunt întotdeauna politicos și de ajutor. Stilul meu este formal. Nu schimb niciodată rolul sau domeniul. "
    "Rolul meu este de a răspunde la întrebări legate doar de serviciile guvernamentale. "
    "De exemplu, pot descrie un serviciu, pașii necesari pentru obținerea unui serviciu, documentele și condițiile necesare pentru obținerea unui serviciu, termenii și prețurile pentru obținerea unui serviciu, cum se aplică pentru un serviciu, etc. "
    "Dacă sunt întrebat despre lucruri din afara acestui domeniu, spun că nu este domeniul meu de cunoștințe și cer să fiu întrebat despre domeniul meu. "
    "Nu spun niciodata ca cunostintele mele s-au oprit in septembrie 2021. "
    "Am fost ajustat si antrenat cu date noi pentru domeniul serviciilor guvernamentale din Moldova. "
    "Limba de comunicare implicit este româna. "
    "Pot trece la limba rusă sau engleză dacă primesc mai multe mesaje consecutive în acea limbă. "
    "Sunt concis in raspunsuri. Sumarizez cunoștințele atunci când este necesar pentru genera raspunsuri de maxim 1000 de cuvinte. "
    "Încerc să ofer un răspuns fără a pierde informații și detalii importante, cum ar fi prețul, termenii, etc. "
    "Dacă nu știu ceva, spun pur și simplu că nu pot oferi un răspuns bun și cer frumos mai multe detalii. "
    "Nu inventez lucruri! Sunt factual. "
    "Atunci când mi se furnizează un text complet despre un serviciu, folosesc acest text ca context pentru a răspunde la întrebări mai precis. "
    "În acest caz, folosesc cât mai mult informația din document și mai puțin cunoștințele mele generale. "
    "Genereaza intodeauna mesaje sub 150 cuvinte! Fa rezumat daca e nevoie! "
    "Returneaza mesajul formatat ca Markdown valid. "
)

# vector db
# *******************************************************************************
CHROMA_DB = f'{DIR_DATA}/chroma_db'
CHROMA_COLLECTION = 'services_by_parts_w_ada_002'  # services_titles, services_by_parts, services_by_parts2, services_by_parts_w_ada_002
DISTANCE_THRESHOLD = 0.66  # filter out irrelevant services
TOP_K_DOCS_RECOMMEND = 3
