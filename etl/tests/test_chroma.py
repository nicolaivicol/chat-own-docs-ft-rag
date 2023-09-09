import unittest
import json
import chromadb
from chromadb.utils import embedding_functions

import config
from vdb.chroma import search


class TestAll(unittest.TestCase):

    def setUp(self) -> None:
        self.client = chromadb.PersistentClient(path=config.CHROMA_DB)
        emb_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=config.OPENAI_API_KEY, model_name=config.MODEL_EMBEDDING)
        self.collection = self.client.get_collection(name=config.CHROMA_COLLECTION, embedding_function=emb_fn)


    def test_search_keywords(self):
        searches = [
            'certificat',
            'certificat de nastere',
            'permis',
            'permis auto',
            'licenta',
            'licenta notariat',
            'alocatie',
            'livret',
            'livret militar',
            'document militar',
            'autorizatie',
            'autorizatie de constructie',
            'permis arma',
            'cum sa obtin un permis de arma',
            'buletin',
            'buletin de identitate',
            'la cat timp se face buletinul de identitate',
            'pasaport',
            'pasaport strain',
            'permis de sedere',
            'imobil',
            'document pe casa',
        ]

        for q in searches:
            results = search(query=q, collection=self.collection, as_df=True)
            print(f'search: "{q}"')
            print('results: \n', results, '\n')

    def test_search_question(self):
        searches = [
            'cat costa certificat de nastere',
            'cum sa obtin un permis de arma',
            'la cat timp se face buletinul de identitate',
            'cum sa obtin cetatenia',
            'cum sa fac certificat pe albini',
            'extras de la cadastru pentru imobil',
            'vreau sa imi schimb adresa de resedinta',
            'inregistrare la adresa de resedinta',
            'vreau sa imi schimb inregistrarea de domiciliu',
            'cat costa schimbarea permisului de conducere',
        ]

        for q in searches:
            results = search(query=q, k=10, collection=self.collection, as_df=True)
            print(f'search: "{q}"')
            print('results: \n', results, '\n')
