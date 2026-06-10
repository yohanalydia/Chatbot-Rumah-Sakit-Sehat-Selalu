# Hospital QA System

Question Answering System untuk data rumah sakit menggunakan OpenSearch, Sentence Transformers, dan Gemini.

## Fitur

- Vector Search menggunakan OpenSearch
- Semantic Embedding menggunakan Sentence Transformers
- Retrieval Augmented Generation (RAG)
- Jawaban Natural Language menggunakan Gemini
- Mendukung pencarian data pasien, dokter, tagihan, pembayaran, dan layanan rumah sakit

## Struktur Proyek

```text
project/
│
├── config.py
├── setup_opensearch.py
├── retrieval.py
├── rag.py
├── requirements.txt
└── README.md
```

## Instalasi

Clone repository:

```bash
git clone <repository-url>
cd project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Konfigurasi

Sebelum menjalankan aplikasi, sesuaikan terlebih dahulu nilai pada `config.py` dan `docker-compose.yml`.

Pada `config.py` ganti:
* `YOUR_GEMINI_API_KEY` dengan API Key Gemini milik Anda.
* `YOUR_OPENSEARCH_PASSWORD` dengan password OpenSearch yang digunakan pada Docker Compose.

Pada `docker-compose.yml` ganti:
* `OPENSEARCH_INITIAL_ADMIN_PASSWORD` dengan password OpenSearch Anda

## Menjalankan OpenSearch

Pastikan Docker Desktop sudah berjalan.

```bash
docker compose up -d
```

## Membangun Knowledge Base

Jalankan:

```bash
python setup_opensearch.py
```

Proses ini akan:

- Membuat index OpenSearch
- Generate master documents
- Generate join documents
- Generate embeddings
- Upload seluruh dokumen ke OpenSearch

## Menjalankan QA System

```bash
python rag.py
```

Contoh pertanyaan:

- Siapa dokter spesialis kardiologi?
- Pasien yang memiliki tagihan terbesar?
- Tagihan pasien yang belum lunas?
- Siapa penanggung jawab pasien tertentu?

## Teknologi

- Python
- OpenSearch
- Docker
- Sentence Transformers
- Gemini API
