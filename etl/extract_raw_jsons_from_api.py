import pandas as pd
import requests
import os
import time
import random
from pathlib import Path
import logging
from tqdm import tqdm
import json
from typing import List, Dict, Any, Union

import config

log = logging.getLogger(os.path.basename(__file__))


def handle_response(response: requests.Response, load_json=True) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    if response.status_code == 200:
        if load_json:
            return json.loads(response.text)
        else:
            return response.text
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")


def get_categories() -> List[Dict[str, Any]]:
    response = requests.get(f'{config.URL_API_CONTENT}/catalog/categories')
    return handle_response(response)


def get_services_for_category_id(id: int) -> List[Dict[str, Any]]:
    response = requests.get(f'{config.URL_API_CONTENT}/catalog/categories/{id}')
    return handle_response(response)


def get_service(code: str, load_json=True, save_to_disk=False) -> Union[Dict[str, Any], str]:
    response = requests.get(f'{config.URL_API_CONTENT}/public-service/code/{code}')
    r = handle_response(response, load_json=load_json)
    if save_to_disk:
        with open(f'{config.DIR_DATA}/services_raw_json/{code}.json', 'w') as f:
            r_obj = json.loads(r) if type(r) == str else r
            json.dump(r_obj, f, indent=2, ensure_ascii=False)
    return r


def get_categories_as_df(cache=False, file_name='df_categories') -> pd.DataFrame:
    file_path = f'{config.DIR_DATA}/{file_name}.jsonl'

    if cache and Path(file_path).exists():
        return pd.read_json(file_path, orient='records', lines=True)

    cats = get_categories()
    cats_plain = [
        {
            'id': cat['id'],
            'order': cat['order'],
            'name': cat['name']['ro'],
            'description': cat['description']['ro'],
        }
        for cat in cats]
    df = pd.DataFrame(cats_plain)

    if cache:
        df.to_json(file_path, orient='records', lines=True)

    return df


def get_services_as_df(cache=False, file_name='df_services') -> pd.DataFrame:
    file_path = f'{config.DIR_DATA}/{file_name}.jsonl'

    if cache and Path(file_path).exists():
        return pd.read_json(file_path, orient='records', lines=True)

    df_categories = get_categories_as_df(cache=cache)
    all_services = []

    for _, row in tqdm(df_categories.iterrows(), unit='category', total=len(df_categories)):
        time.sleep(random.uniform(1.5, 3))
        cat_id, cat_name = row['id'], row['name']
        log.info(f'{cat_id}: {cat_name}')
        services_in_category = get_services_for_category_id(cat_id).get('publicServices', [])
        services_in_category_flat = [
            {
                'id': service['id'],
                'code': service['code'],
                'title': service['title']['ro'],
                'description': service['description']['ro'],
                'eservice': service['eService'],
                'category_id': cat_id,
            }
            for service in services_in_category
        ]
        all_services.extend(services_in_category_flat)

    df = pd.DataFrame(all_services)
    df.to_json(file_path, orient='records', lines=True)

    return df


def extract_all_services_raw_jsons(file_name='services_raw_json'):
    file_path = f'{config.DIR_DATA}/{file_name}.jsonl'
    df_services = get_services_as_df(cache=True)

    with open(file_path, "w") as file:
        for _, row in tqdm(df_services.iterrows(), unit='service', total=len(df_services)):
            time.sleep(random.uniform(1.0, 2.0))
            code, title, category_id = row['code'], row['title'], row['id']
            log.info(f'{code}: {title}')
            service = get_service(code)
            service['category_id'] = category_id
            file.write(json.dumps(service) + '\n')


def load_all_services_raw_jsons(file_name='services_raw_json') -> List[Dict[str, Any]]:
    file_path = f'{config.DIR_DATA}/{file_name}.jsonl'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]


def read_jsonl_save_nonascii(file_name: str):
    with open(f'{config.DIR_DATA}/{file_name}.jsonl', 'r') as f:
        lines = f.readlines()
        lines = [line.encode('utf-8').decode('unicode-escape') for line in lines]
    with open(f'{config.DIR_DATA}/{file_name}_nonascii.jsonl', 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')
    # extract_all_services_raw_jsons()
    df_services = get_services_as_df(cache=True)
    with open(f'{config.DIR_DATA}/df_services_nonascii.jsonl', 'w') as f:
        df_services[['code', 'title']].to_json(f, orient='records', lines=True, force_ascii=False)
    log.info('Done.')
