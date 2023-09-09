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

import config
from etl.extract_raw_jsons_from_api import get_service, load_all_services_raw_jsons
from etl.gen_docs_from_raw_jsons import load_doc_from_simple_json, list_all_codes_simple_json

log = logging.getLogger(os.path.basename(__file__))

# https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset


def gen_qa_template_title_description(doc_json: Dict[str, str]) -> Dict:
    templates = [
        '{title}',
        # '{title}?',
        # 'ce este {title}?',
        # 'ce e {title}?',
    ]
    template = random.choice(templates)
    title = doc_json['title']
    description = doc_json['objective']
    qa = {"messages": [
        {"role": "system", "content": config.ROLE_SYSTEM},
        {"role": "user", "content": template.format(title=title)},
        {"role": "assistant", "content": description}
    ]}
    return qa


def gen_qa_template_steps(doc_json: Dict[str, str]) -> Dict:
    templates = [
        'cum {title}',
        '{title} cum?',
        'pasii pentru {title}',
        'cum obtin {title}?',
        'cum se face {title}?',
        'cum se obtine {title}?',
        'care e procedura pentru {title}?',
        'procesul pentru {title}?',
    ]
    template = random.choice(templates)
    title = doc_json['title']
    description = doc_json['steps']
    qa = {"messages": [
        {"role": "system", "content": config.ROLE_SYSTEM},
        {"role": "user", "content": template.format(title=title)},
        {"role": "assistant", "content": description}
    ]}
    return qa


def gen_qa_template_terms_price(doc_json: Dict[str, str]) -> Dict:
    templates = [
        'Cât costă {title}',
        'Prețul pentru {title}',
        'Ce preț are {title}',
        'Ce tarif pentru {title}',
        'Care sunt tarifele pentru {title}',
        'Care este prețul pentru {title}',
        'Costul pentru {title}',
        'Cât mă costă {title}',
        'În cât timp se face {title}',
        'Care este termenul {title}',
        'Cât durează {title}',
        'Cât timp durează {title}',
        'Cât de repede se face {title}',
        'La cât timp se face {title} și care este prețul',
        'Prețul și termenul pentru {title}',
    ]
    template = random.choice(templates)
    title = doc_json['title']
    costs = doc_json['costs']
    qa = {"messages": [
        {"role": "system", "content": config.ROLE_SYSTEM},
        {"role": "user", "content": template.format(title=title)},
        {"role": "assistant", "content": costs}
    ]}
    return qa


def gen_qa_template_required_docs(doc_json: Dict[str, str]) -> Dict:
    templates = [
        'Ce acte trebuiesc pentru {title}?',
        'Care documente trebuiesc pentru {title}?',
        'Ce documente sunt necesare pentru {title}?',
        'Ce acte sunt necesare pentru a obține {title}?',
        'Trebuiesc careva documente pentru a obține {title}?',
        'Documente pentru {title}',
    ]
    template = random.choice(templates)
    title = doc_json['title']
    docs = doc_json['documents']
    qa = {"messages": [
        {"role": "system", "content": config.ROLE_SYSTEM},
        {"role": "user", "content": template.format(title=title)},
        {"role": "assistant", "content": docs}
    ]}
    return qa


def gen_qa_pairs_from_templates(doc_json: Dict[str, str]):
    qa_pairs = [
        gen_qa_template_title_description(doc_json),
        gen_qa_template_steps(doc_json),
        gen_qa_template_terms_price(doc_json),
        gen_qa_template_required_docs(doc_json),
    ]
    return qa_pairs


if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')
    doc_codes = list_all_codes_simple_json()
    with open(f'{config.DIR_DATA}/qa/qa_from_templates_20230908_2300.jsonl', 'w') as f:
        for code in tqdm(doc_codes[:100]):
            doc = load_doc_from_simple_json(code)
            qa_pairs = gen_qa_pairs_from_templates(doc)
            for qa_pair in qa_pairs:
                f.write(json.dumps(qa_pair, ensure_ascii=False) + '\n')
    log.info('Done.')
