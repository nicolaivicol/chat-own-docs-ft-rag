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

log = logging.getLogger(os.path.basename(__file__))


def truncate_txt(s: str, max_n=2000):
    s = s.split(' ')
    s = s[:max_n]
    s = ' '.join(s)
    return s


def clean_txt(txt: str) -> str:
    if txt is None:
        return ''
    txt = txt.lstrip()
    txt = txt.rstrip()
    txt = txt.rstrip('\n')
    txt = txt.rstrip()
    return txt

def steps_to_txt(raw_json, sep='   \n') -> str:
    title = raw_json['title']['ro']
    title_steps = f'## Descrierea procesului de obținere a serviciului "{title}" și a pașilor necesari   '
    steps = sorted(raw_json.get('steps', []), key=lambda x: x['order'])
    steps_txt = []
    for step in steps:
        step_txt = []

        step_title = ('' if step.get('title', {}).get('ro', '') is None else step.get('title', {}).get('ro', ''))
        step_title = clean_txt(step_title)
        if step_title != '':
            step_txt.append(step_title)

        step_descr = ('' if step.get('description', {}).get('ro', '') is None else step.get('description', {}).get('ro', ''))
        step_descr = clean_txt(step_descr)
        if step_descr != '':
            step_txt.append(step_descr)

        step_channel = ('' if step.get('channelUrl', '') is None else step.get('channelUrl', ''))
        step_channel = clean_txt(step_channel)
        if step_channel != '':
            step_txt.append('Link: ' + step_channel)

        step_txt = '### ' + sep.join(step_txt)
        step_txt += '  \n'
        steps_txt.append(step_txt)

    if len(steps_txt) > 0:
        steps_txt = sep.join([title_steps + '  \n'] + steps_txt)
    else:
        steps_txt = ''
    return steps_txt


def capitalize_first(s):
    return s[0].upper() + s[1:]


def has_digits(s):
    return any(char.isdigit() for char in s)


def price_int(cost):
    cost_price = cost.get('price')
    if cost_price is None:
        cost_price = 0
    else:
        try:
            cost_price = int(cost_price)
        except ValueError:
            if has_digits(cost_price):
                cost_price = 1
            else:
                cost_price = 0
    return cost_price


def costs_to_txt(raw_json, sep=' \n') -> str:
    dict_duration_unit = {
        'Day': 'zile',
        'WorkDay': 'zile lucrătoare',
        'CalendarDay': 'zile calendaristice',
        'Hour': 'ore',
    }

    title = title_to_txt(raw_json)
    title_costs = f'## Tarifele și termenii prestării serviciului "{title}"'

    costs = raw_json.get('costs', [])
    costs = sorted(costs, key=lambda x: price_int(x))

    costs_txt = []

    for cost in costs:
        # cost = costs[0]
        duration = cost.get('durationValue')
        duration_txt = ''
        if duration is None:
            duration_txt = ''
        # elif duration == 0:
        #     duration_txt = 'Prestarea serviciului în aceeași zi'
        elif duration > 0:
            duration_unit = dict_duration_unit.get(cost.get('durationUnit', 'Day'))
            if duration_unit is None:
                duration_txt = ''
            else:
                duration_txt = f'Termenul de prestare a serviciului este de {duration} {duration_unit}'

        cost_txt = ''
        cost_price = cost.get('price')
        if cost_price is None:
            cost_txt = 'Prețul serviciului nu este specificat.'
        else:
            if cost_price == '0':
                cost_txt = 'Serviciu gratuit.'
            elif has_digits(cost_price):
                currency = cost.get('currency', 'MDL').upper()
                if duration_txt != '':
                    cost_txt = f'la achitarea prețului de {cost_price} {currency}.'
                else:
                    cost_txt = f'Prețul serviciului este de {cost_price} {currency}.'

        cost_duration_txt = ''
        if duration_txt != '' and cost_txt != '':
            if 'gratuit' in cost_txt.lower():
                cost_duration_txt = f'{cost_txt} {duration_txt}'
            else:
                cost_duration_txt = f'{duration_txt} {cost_txt}'
        elif duration_txt != '' and cost_txt == '':
            cost_duration_txt = f'{duration_txt}.'
        elif duration_txt == '' and cost_txt != '':
            cost_duration_txt = f'{cost_txt}'

        commentary = cost.get('commentary')
        if commentary is not None:
            commentary = clean_txt(commentary)
            if commentary != '':
                if commentary[-1] != '.':
                    commentary += '.'
                if cost_duration_txt[-1] != '.':
                    cost_duration_txt += '.'

                commentary = capitalize_first(commentary)
                commentary = commentary.replace('\n-', '\n\t-')
                cost_duration_txt += f' {commentary}'

        costs_txt.append(cost_duration_txt)

    if len(costs_txt) == 0:
        txt = f'{title_costs} nu sunt specificate.  '
    else:
        txt = (sep + ' - ').join([f'{title_costs}   '] + costs_txt)

    return txt


def is_valid_doc(doc):
    is_required = doc.get('type', '').lower() == 'required'
    doc_title = doc.get('title', {}).get('ro', '')
    has_title = doc_title is not None and doc_title != ''
    return is_required and has_title


def documents_to_txt(raw_json, sep=' \n') -> str:
    title = title_to_txt(raw_json)
    title_docs = f'## Documentele (actele) necesare pentru prestarea serviciului "{title}"'

    docs = raw_json.get('documents', [])
    docs = [doc for doc in docs if is_valid_doc(doc)]

    docs_txt = []
    for doc in docs:
        doc_title = doc.get('title', {}).get('ro', '')
        doc_url = doc.get('url', '')
        doc_details = doc.get('details', '')
        doc_txt = f'{clean_txt(doc_title)}'
        if doc_details is not None and doc_details != '':
            doc_txt += f' \n {clean_txt(doc_details)}'
        if doc_url is not None and doc_url != '':
            doc_txt += f' \n url: {clean_txt(doc_url)}'
        docs_txt.append(doc_txt)

    if len(docs_txt) == 0:
        txt = f'{title_docs} nu sunt specificate.   '
    else:
        txt = (sep + ' - ').join([f'{title_docs}  '] + docs_txt)

    return txt


def title_to_txt(raw_json) -> str:
    txt = raw_json['title']['ro']
    txt = clean_txt(txt)
    if txt == '':
        txt = 'Denumirea serviciului nu este specificata.'
    return txt


def objective_to_txt(raw_json) -> str:
    txt = raw_json['objective']['ro']
    txt = clean_txt(txt)
    if txt == '':
        txt = title_to_txt(raw_json)
    return txt


def flatten_raw_json(raw_json: Union[str, Dict]) -> Dict[str, str]:
    if type(raw_json) == str:
        raw_json = json.loads(raw_json)

    doc_simplified = {
        'id': raw_json['id'],
        'code': raw_json['code'],
        'title': title_to_txt(raw_json),
        'objective': objective_to_txt(raw_json),
        'category_id': raw_json['categories'][0]['id'],
        'category_title': raw_json['categories'][0]['title']['ro'],
        'steps': steps_to_txt(raw_json),
        'costs': costs_to_txt(raw_json),
        'documents': documents_to_txt(raw_json),
    }

    return doc_simplified


def gen_doc_from_simple_json(doc: Union[str, Dict]) -> Tuple[str, str, str]:
    doc_txt = (
        f"# Serviciul: {doc['title']} \n\n"
        f"## Categoria serviciului  \n{doc['category_title']}   \n\n"
        f"## Descrierea serviciului  \n{doc['objective']}   \n\n"
        f"{doc['steps']} \n\n"
        f"{doc['costs']} \n\n"
        f"{doc['documents']}"
        f"\n"
    )
    return doc['id'], doc['code'], doc_txt


def gen_doc_from_raw_json(raw_json: Union[str, Dict]) -> Tuple[str, str, str]:
    """
    Generate readable text of document from raw json.
    :param raw_json: raw json of service, as string or dict
    :return: tuple of (id, code, text)
    """

    if type(raw_json) == str:
        raw_json = json.loads(raw_json)

    doc = flatten_raw_json(raw_json)
    doc_txt = (
        f"# Serviciul: {doc['title']} \n\n"
        f"## Categoria serviciului  \n{doc['category_title']}   \n\n"
        f"## Descrierea serviciului  \n{doc['objective']}   \n\n"
        f"{doc['steps']} \n\n"
        f"{doc['costs']} \n\n"
        f"{doc['documents']}"
        f"\n"
    )

    return doc['id'], doc['code'], doc_txt


def load_doc_from_simple_json(code: str) -> Dict[str, str]:
    with open(f'{config.DIR_DATA}/services_simple_json/{code}.json', 'r') as f:
        doc = json.load(f)
    return doc


def load_summarized_doc(code: str) -> Dict[str, str]:
    if os.path.exists(f'{config.DIR_DATA}/services_summarized_simple_json/{code}.json'):
        with open(f'{config.DIR_DATA}/services_summarized_simple_json/{code}.json', 'r') as f:
            doc = json.load(f)
    else:
        with open(f'{config.DIR_DATA}/services_simple_json/{code}.json', 'r') as f:
            doc = json.load(f)
    return doc


def load_summarized_doc_as_txt(code: str) -> str:
    doc = load_summarized_doc(code)
    _, _, doc_txt = gen_doc_from_simple_json(doc)
    return doc_txt

def list_all_codes_simple_json() -> List[str]:
    codes = [code.replace('.json', '') for code in os.listdir(f'{config.DIR_DATA}/services_simple_json')]
    return codes


if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')

    raw_jsons = load_all_services_raw_jsons()
    docs_txt = []

    # create dir for txt files
    if not os.path.exists(f'{config.DIR_DATA}/services_txt'):
        os.makedirs(f'{config.DIR_DATA}/services_txt')

    if not os.path.exists(f'{config.DIR_DATA}/services_simple_json'):
        os.makedirs(f'{config.DIR_DATA}/services_simple_json')

    if not os.path.exists(f'{config.DIR_DATA}/services_txt_json'):
        os.makedirs(f'{config.DIR_DATA}/services_txt_json')

    for raw_json in tqdm(raw_jsons):
        # print(raw_json['code'])
        doc_simple_json = flatten_raw_json(raw_json)
        id, code, text = gen_doc_from_raw_json(raw_json)

        with open(f'{config.DIR_DATA}/services_simple_json/{code}.json', 'w') as f:
            json.dump(doc_simple_json, f, indent=2, ensure_ascii=False)

        with open(f'{config.DIR_DATA}/services_txt/{code}.txt', 'w') as f:
            f.write(text)

        with open(f'{config.DIR_DATA}/services_txt_json/{code}.json', 'w') as f:
            json.dump({'code': code, 'text': text}, f, indent=2, ensure_ascii=False)

    log.info('Done.')
