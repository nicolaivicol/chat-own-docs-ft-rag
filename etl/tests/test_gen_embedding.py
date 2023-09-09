import unittest
import json

from etl.gen_doc_embeddings import gen_embedding


class TestAll(unittest.TestCase):

    def test_costs_to_txt(self):
        code_service = '003000100'
        embedding = gen_embedding(code_service)
        print(f'embedding of size {len(embedding)} created: {embedding}')
