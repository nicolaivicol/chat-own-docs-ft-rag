import chromadb
import warnings
import config


client = chromadb.PersistentClient(path=config.CHROMA_DB)

# Suppress all DeprecationWarnings
warnings.filterwarnings('ignore', category=DeprecationWarning)


def create_collection():
    collection = client.create_collection(
        name="services_titles",
        metadata={"hnsw:space": "cosine"},  # l2 is the default
        # embedding_function=emb_fn
    )
    return collection


# def add_documents(collection, documents, metadatas, ids):
#     collection.add(
#         documents=documents,    # ["doc1", "doc2", "doc3", ...],
#         metadatas=metadatas,    # [{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
#         ids=ids,                # ["id1", "id2", "id3"]
#     )


def search(query, collection, k=5, as_df=False):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    if as_df:
        import pandas as pd
        pd.set_option('display.width', 2000)
        pd.set_option('display.max_colwidth', 100)
        pd.set_option('display.max_columns', None)  # Show all columns

        if len(results['ids'][0]) > 0:
            results = pd.DataFrame(
                {'ids': results['ids'][0],
                 'parent_code': [m['parent_doc_id'] for m in results['metadatas'][0]],
                 'parent_title': [m['parent_title'] for m in results['metadatas'][0]],
                 'distances': results['distances'][0],
                 'documents': results['documents'][0]}
            )
        else:
            results = pd.DataFrame(
                {'ids': [],
                 'parent_code': [],
                 'parent_title': [],
                 'distances': [],
                 'documents': []}
            )

    return results
