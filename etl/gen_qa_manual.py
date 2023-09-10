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



if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')
    qa_files = [code.replace('.json', '') for code in os.listdir(f'{config.DIR_DATA}/qa/manual')]
    with open(f'{config.DIR_DATA}/qa/qa_manual_20230910_0300.jsonl', 'w') as f:
        for code in tqdm(qa_files):
            print(code)
            qa = json.load(open(f'{config.DIR_DATA}/qa/manual/{code}.json'))
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    log.info('Done.')
