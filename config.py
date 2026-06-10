# ==================================
# OpenSearch Configuration
# ==================================

OPENSEARCH_HOST = "localhost"
OPENSEARCH_PORT = 9200

OPENSEARCH_USER = "admin"
OPENSEARCH_PASSWORD ="YOUR_OPENSEARCH_PASSWORD" # Sesuaikan dengan password yang digunakan di docker-compose.yml

INDEX_NAME = "hospital_knowledge"


# ==================================
# Embedding Model
# ==================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==================================
# GEMINI
# ==================================
GEMINI_MODEL= "gemini-3.1-flash-lite"
GEMINI_API_KEY = "AIzaSyD3g2CdazGBcJMeEMPeLeWbtfaw3dexpfo" # Ganti dengan API key Gemini yang dimiliki
