import json
import os
import chromadb
import logging
from tqdm import tqdm
import html2text

import config
from chat.chatobj import Chat
from etl.gen_docs_from_raw_jsons import list_all_codes_simple_json, load_doc_from_simple_json

log = logging.getLogger(os.path.basename(__file__))

INSTRUCTIONS_SUMMARY = (
    "Summarize the text below in maximum {n_words} words! Use Romanian language."
    "Text to summarize: \n\n"
)


def truncate_txt(s: str, max_n=2000):
    s = s.split(' ')
    s = s[:max_n]
    s = ' '.join(s)
    return s


def gen_summarized_doc(code, model='gpt-3.5-turbo-0613'):
    doc = load_doc_from_simple_json(code)
    doc['title'] = truncate_txt(doc['title'].replace('\n', ' '))
    doc['objective'] = Chat(model=model, max_tokens=300, temperature=1).ask_gpt(INSTRUCTIONS_SUMMARY.format(n_words=200) + truncate_txt(html2text.html2text(doc['objective']), 1000))
    doc['steps'] = Chat(model=model, max_tokens=400, temperature=1).ask_gpt(INSTRUCTIONS_SUMMARY.format(n_words=200) + truncate_txt(doc['steps']))
    doc['costs'] = Chat(model=model, max_tokens=400, temperature=1).ask_gpt(INSTRUCTIONS_SUMMARY.format(n_words=200) + truncate_txt(doc['costs']))
    doc['documents'] = Chat(model=model, max_tokens=400, temperature=1).ask_gpt(INSTRUCTIONS_SUMMARY.format(n_words=200) + truncate_txt(doc['documents']))
    with open(f'{config.DIR_DATA}/services_summarized_simple_json/{code}.json', 'w') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')
    doc_codes = list_all_codes_simple_json()

    # create dir for txt files
    if not os.path.exists(f'{config.DIR_DATA}/services_summarized_simple_json'):
        os.makedirs(f'{config.DIR_DATA}/services_summarized_simple_json')

    for code in tqdm(doc_codes):
        if not os.path.exists(f'{config.DIR_DATA}/services_summarized_simple_json/{code}.json'):
            try:
                gen_summarized_doc(code)
            except Exception as e:
                log.error(f'Error summarizing {code}: {str(e)}')

    log.info('Done.')
