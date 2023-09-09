import pandas as pd
import requests
import os
import time
import random
from pathlib import Path
import logging
from tqdm import tqdm
import json
from typing import List, Dict, Any, Union, Tuple
import openai

import config
from etl.extract_raw_jsons_from_api import get_service, load_all_services_raw_jsons
from etl.gen_docs_from_raw_jsons import list_all_codes_simple_json, load_doc_from_simple_json

log = logging.getLogger(os.path.basename(__file__))


def gen_embedding(code, use_title=True):
    doc = load_doc_from_simple_json(code)

    input = ''
    if use_title:
        input += doc['title']

    response = openai.Embedding.create(
        input=input,
        model=config.MODEL_EMBEDDING,
    )

    embedding = response["data"][0]["embedding"]
    len(embedding)

    return embedding



if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')
    doc_codes = list_all_codes_simple_json()

    for code in tqdm(doc_codes[:10]):
        doc = load_doc_from_simple_json(code)
        title = doc['title']
        openai.Embedding()


    f = open(f'{config.DIR_DATA}/qa/qa_from_templates_20230908_2300.jsonl', 'w')
    with open(f'{config.DIR_DATA}/qa/qa_from_templates_20230908_2300.jsonl', 'w') as f:
        for code in tqdm(doc_codes[:100]):
            doc = load_doc_from_simple_json(code)
            qa_pairs = gen_qa_pairs_from_templates(doc)
            for qa_pair in qa_pairs:
                f.write(json.dumps(qa_pair, ensure_ascii=False) + '\n')
    log.info('Done.')



