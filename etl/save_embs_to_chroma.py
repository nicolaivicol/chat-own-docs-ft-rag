import os
import chromadb
import logging

import html2text
from chromadb.utils import embedding_functions
from tqdm import tqdm


import config
from etl.gen_docs_from_raw_jsons import list_all_codes_simple_json, load_doc_from_simple_json
from etl.gen_summarized_docs import truncate_txt

log = logging.getLogger(os.path.basename(__file__))


def save_embedding_to_chroma(code, collection: chromadb.Collection):
    doc = load_doc_from_simple_json(code)
    for part_name in ['title', 'objective', 'steps', 'costs', 'documents']:
        doc_part = doc[part_name]
        if part_name == 'objective':
            doc_part = html2text.html2text(doc_part)
        doc_part = truncate_txt(doc_part, 1000)
        id = f'{code}-{part_name}'
        id_res = collection.get([id])
        if id not in id_res['ids']:
            try:
                collection.add(
                    documents=[doc_part],
                    metadatas=[{'parent_doc_id': code, 'parent_title': doc['title'], 'part_name': part_name}],
                    ids=[id]
                )
            except Exception as e:
                log.error(f'Error for id: {id}: {str(e)}')


def get_emb_fn():
    pass


client = chromadb.PersistentClient(path=config.CHROMA_DB)
# client = chromadb.Client()
# client = chromadb.HttpClient(host='localhost', port='8000')

emb_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=config.OPENAI_API_KEY, model_name="text-embedding-ada-002")

collection = client.create_collection(
    name="services_by_parts_w_ada_002",  # services_titles
    metadata={"hnsw:space": "cosine"},  # l2 is the default
    get_or_create=True,
    embedding_function=emb_fn,
)


if __name__ == '__main__':
    log.info(f'Running {os.path.basename(__file__)}')
    doc_codes = list_all_codes_simple_json()

    for code in tqdm(doc_codes):
        save_embedding_to_chroma(code, collection)

    log.info('Done.')


