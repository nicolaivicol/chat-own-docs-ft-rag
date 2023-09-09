import unittest
import json

from etl.extract_raw_jsons_from_api import get_service
from etl.gen_docs_from_raw_jsons import costs_to_txt, steps_to_txt, documents_to_txt, flatten_raw_json, \
    gen_doc_from_raw_json


class TestAll(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        code_service = '003000100'
        self.raw_json = get_service(code=code_service, save_to_disk=True)

    def test_costs_to_txt(self):
        costs_txt = costs_to_txt(self.raw_json)
        print(costs_txt)

    def test_steps_to_txt(self):
        steps_txt = steps_to_txt(self.raw_json)
        print(steps_txt)

    def test_documents_to_txt(self):
        txt = documents_to_txt(self.raw_json)
        print(txt)

    def test_flatten_raw_json(self):
        flat_json = flatten_raw_json(self.raw_json)
        print(json.dumps(flat_json, indent=2))

    def test_gen_doc_from_raw_json(self):
        doc_id, doc_code, doc_txt = gen_doc_from_raw_json(self.raw_json)
        print(doc_txt)
