from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

# ==================================
# OpenSearch Configuration
# ==================================

from config import (
    OPENSEARCH_HOST,
    OPENSEARCH_PORT,
    OPENSEARCH_USER,
    OPENSEARCH_PASSWORD,
    INDEX_NAME,
    EMBEDDING_MODEL
)

# ==================================
# Load Embedding Model
# ==================================
model = SentenceTransformer(
        EMBEDDING_MODEL
    )

# ==================================
# Connect OpenSearch
# ==================================

def connect_opensearch():

    client = OpenSearch(
        hosts=[
            {
                "host": OPENSEARCH_HOST,
                "port": OPENSEARCH_PORT
            }
        ],
        http_auth=(
            OPENSEARCH_USER,
            OPENSEARCH_PASSWORD
        ),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )

    return client


# ==================================
# Vector Search
# ==================================
import re
def search_documents(client, question, top_k=10):
    question = question.strip()

    # Menangkap ID seperti A002, P001, DR001, TAG001, dan lainnya.
    entity_ids = re.findall(
        r"\b(?:TAG|BYR|PJ|DR|BP|DL|A|P|D|T)\d{3}\b",
        question.upper(),
    )

    collected_hits = []
    seen = set()

    def add_hits(hits):
        for hit in hits:
            source = hit["_source"]
            key = (
                source.get("doc_type"),
                source.get("source_id"),
                source.get("content"),
            )

            if key not in seen:
                seen.add(key)
                collected_hits.append(hit)

    # 1. Prioritaskan pencarian ID exact.
    if entity_ids:
        exact_clauses = []

        for entity_id in entity_ids:
            exact_clauses.extend(
                [
                    {
                        "term": {
                            "source_id": {
                                "value": entity_id,
                                "boost": 20,
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "content": {
                                "query": entity_id,
                                "boost": 8,
                            }
                        }
                    },
                ]
            )

        exact_response = client.search(
            index=INDEX_NAME,
            body={
                "size": top_k,
                "query": {
                    "bool": {
                        "should": exact_clauses,
                        "minimum_should_match": 1,
                    }
                },
            },
        )

        add_hits(exact_response["hits"]["hits"])

    # 2. Cari berdasarkan kata/nama menggunakan BM25.
    lexical_response = client.search(
        index=INDEX_NAME,
        body={
            "size": top_k,
            "query": {
                "match": {
                    "content": {
                        "query": question,
                        "operator": "or",
                    }
                }
            },
        },
    )

    add_hits(lexical_response["hits"]["hits"])

    # 3. Lengkapi dengan semantic vector search.
    query_embedding = model.encode(question.lower()).tolist()

    vector_response = client.search(
        index=INDEX_NAME,
        body={
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding,
                        "k": top_k,
                    }
                }
            },
        },
    )

    add_hits(vector_response["hits"]["hits"])

    return collected_hits[:top_k]

# ==================================
# Retrieve Context
# ==================================
def retrieve_context(question, top_k=10):
    client = connect_opensearch()

    try:
        results = search_documents(client, question, top_k)

        return [
            hit["_source"]["content"]
            for hit in results
        ]
    finally:
        client.close()

# ==================================
# Main
# ==================================

def main():

    client = connect_opensearch()
    
    print(
        f"Jumlah dokumen dalam index: "
        f"{client.count(index=INDEX_NAME)['count']}"
    )

    question = input(
        "Masukkan pertanyaan: "
    )

    results = search_documents(
        client,
        question
    )

    print("\nHASIL PENCARIAN\n")

    for i, hit in enumerate(results, start=1):

        print("=" * 70)

        print(
            f"Ranking : {i}"
        )

        print(
            f"Score   : {hit['_score']}"
        )

        print(
            f"Tipe    : {hit['_source']['doc_type']}"
        )

        print(
            f"ID      : {hit['_source']['source_id']}"
        )

        print("\nCONTENT:")

        print(
            hit["_source"]["content"]
        )

        print()


if __name__ == "__main__":
    main()
