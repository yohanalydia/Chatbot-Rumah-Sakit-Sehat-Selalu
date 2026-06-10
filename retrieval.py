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

def search_documents(
    client,
    question,
    top_k=10
):
    """
    Melakukan pencarian vector similarity
    ke OpenSearch.
    """
    question = question.lower()
    query_embedding = model.encode(
        question
    ).tolist()

    response = client.search(
        index=INDEX_NAME,
        body={
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding,
                        "k": top_k
                    }
                }
            }
        }
    )

    return response["hits"]["hits"]

# ==================================
# Retrieve Context
# ==================================
def retrieve_context(
    question,
    top_k=10
):

    client = connect_opensearch()

    results = search_documents(
        client,
        question,
        top_k
    )

    contexts = []

    for hit in results:

        contexts.append(
            hit["_source"]["content"]
        )

    return contexts

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