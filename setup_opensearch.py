"""
setup_opensearch.py

Script untuk:
1. Membaca seluruh dataset Rumah Sakit Sehat Selalu
2. Membuat knowledge documents
3. Membuat embedding
4. Membuat index OpenSearch
5. Mengunggah seluruh dokumen ke OpenSearch
6. Jalankan dengan "python setup_opensearch.py"
"""
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
# Import Libraries
# ==================================

import json # Membaca file JSON
import os # Mengelola path file
from tqdm import tqdm # Progress bar
from sentence_transformers import SentenceTransformer # Membuat embedding
from opensearchpy import OpenSearch # Koneksi ke OpenSearch
import uuid # Generate UUID untuk id dokumen (opsional)

def load_json_files():
    """
    Membaca seluruh file JSON Rumah Sakit Sehat Selalu
    dan mengembalikannya dalam bentuk dictionary.

    Returns:
        dict: seluruh dataset yang telah dimuat
    """
    data_folder = "data"
    datasets = {}
    file_mapping = {
        "asuransi": "asuransi_rs_sehat_selalu.json",
        "bukti_pembayaran": "bukti_pembayaran_rs_sehat_selalu.json",
        "departemen": "departemen_rs_sehat_selalu.json",
        "detail_layanan": "detail_layanan_rs_sehat_selalu.json",
        "dokter": "dokter_rs_sehat_selalu.json",
        "pasien": "pasien_rs_sehat_selalu.json",
        "pembayaran": "pembayaran_rs_sehat_selalu.json",
        "penanggung_jawab": "penanggung_jawab_rs_sehat_selalu.json",
        "tagihan": "tagihan_rs_sehat_selalu.json",
        "tim_medis": "tim_medis_rs_sehat_selalu.json"
    }
    for dataset_name, filename in file_mapping.items():

        filepath = os.path.join(data_folder, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            datasets[dataset_name] = json.load(file)

        print(
            f"✓ {dataset_name} loaded "
            f"({len(datasets[dataset_name])} records)"
        )

    return datasets
    
def generate_master_documents(datasets):
    """
    Membuat knowledge documents dari setiap koleksi
    tanpa melakukan join antar entitas.

    Parameters:
        datasets (dict): hasil dari load_json_files()

    Returns:
        list: daftar knowledge documents
    """
    documents = []
    
    # ==========================
    # DOKTER
    # ==========================
    for dokter in datasets["dokter"]:

        documents.append({
            "doc_type": "dokter",
            "source_id": dokter["dokter_id"],
            "content": f"""
            Tipe: Dokter
            ID: {dokter['dokter_id']}
            Nama Dokter: {dokter['nama_dokter']}
            Spesialisasi: {dokter['spesialisasi']}
            """
        })

    # ==========================
    # PASIEN
    # ==========================
    for pasien in datasets["pasien"]:

        documents.append({
            "doc_type": "pasien",
            "source_id": pasien["pasien_id"],
            "content": f"""
            Tipe: Pasien
            ID: {pasien['pasien_id']}
            Nama Pasien: {pasien['nama_pasien']}
            Status VIP: {'Ya' if pasien['vip_status'] else 'Tidak'}
            """
        })

    # ==========================
    # ASURANSI
    # ==========================
    for asuransi in datasets["asuransi"]:

        documents.append({
            "doc_type": "asuransi",
            "source_id": asuransi["asuransi_id"],
            "content": f"""
            Tipe: Asuransi
            ID: {asuransi['asuransi_id']}
            Nama Asuransi: {asuransi['nama_asuransi']}
            Nomor Polis: {asuransi['polis']}
            """
        })

    # ==========================
    # DEPARTEMEN
    # ==========================
    for departemen in datasets["departemen"]:

        documents.append({
            "doc_type": "departemen",
            "source_id": departemen["departemen_id"],
            "content": f"""
            Tipe: Departemen
            ID: {departemen['departemen_id']}
            Nama Departemen: {departemen['nama_departemen']}
            """
        })

    # ==========================
    # PENANGGUNG JAWAB
    # ==========================
    for pj in datasets["penanggung_jawab"]:

        documents.append({
            "doc_type": "penanggung_jawab",
            "source_id": pj["pj_id"],
            "content": f"""
            Tipe: Penanggung Jawab
            ID: {pj['pj_id']}
            Nama: {pj['nama_pj']}
            Hubungan: {pj['hubungan']}
            """
        })

    # ==========================
    # TIM MEDIS
    # ==========================
    for tim in datasets["tim_medis"]:

        documents.append({
            "doc_type": "tim_medis",
            "source_id": tim["tim_id"],
            "content": f"""
            Tipe: Tim Medis
            ID: {tim['tim_id']}
            Nama Tim: {tim['nama_tim']}
            Daftar Dokter: {', '.join(tim['daftar_dokter'])}
            """
        })

    # ==========================
    # TAGIHAN
    # ==========================
    for tagihan in datasets["tagihan"]:

        documents.append({
            "doc_type": "tagihan",
            "source_id": tagihan["tagihan_id"],
            "content": f"""
            Tipe: Tagihan
            ID Tagihan: {tagihan['tagihan_id']}
            ID Pasien: {tagihan['pasien_id']}
            Total Biaya: {tagihan['total_biaya']}
            Status Pembayaran: {tagihan['status_pembayaran']}
            ID Asuransi: {tagihan['asuransi_id']}
            """
        })

    # ==========================
    # PEMBAYARAN
    # ==========================
    for pembayaran in datasets["pembayaran"]:

        documents.append({
            "doc_type": "pembayaran",
            "source_id": pembayaran["pembayaran_id"],
            "content": f"""
            Tipe: Pembayaran
            ID Pembayaran: {pembayaran['pembayaran_id']}
            ID Tagihan: {pembayaran['tagihan_id']}
            Metode Pembayaran: {pembayaran['metode_pembayaran']}
            Jumlah Dibayar: {pembayaran['jumlah_dibayar']}
            Tanggal Pembayaran: {pembayaran['tanggal_pembayaran']}
            """
        })

    # ==========================
    # DETAIL LAYANAN
    # ==========================
    for detail in datasets["detail_layanan"]:

        documents.append({
            "doc_type": "detail_layanan",
            "source_id": detail["detail_id"],
            "content": f"""
            Tipe: Detail Layanan
            ID Detail: {detail['detail_id']}
            ID Tagihan: {detail['tagihan_id']}
            Jenis Layanan: {detail['jenis_layanan']}
            Biaya: {detail['biaya']}
            Deskripsi: {detail['deskripsi']}
            """
        })

    # ==========================
    # BUKTI PEMBAYARAN
    # ==========================
    for bukti in datasets["bukti_pembayaran"]:

        documents.append({
            "doc_type": "bukti_pembayaran",
            "source_id": bukti["bukti_id"],
            "content": f"""
            Tipe: Bukti Pembayaran
            ID Bukti: {bukti['bukti_id']}
            ID Pembayaran: {bukti['pembayaran_id']}
            Nomor Bukti: {bukti['nomor_bukti']}
            Tanggal Terbit: {bukti['tanggal_terbit']}
            """
        })
        
    print(f"✓ Menghasilkan {len(documents)} master documents")

    return documents
    
def generate_join_documents(datasets):
    """
    Membuat knowledge documents hasil join antar koleksi.

    Tujuan:
    - Menambahkan konteks relasional yang tidak dimiliki master documents.
    - Mempermudah OpenSearch dan LLM menjawab pertanyaan lintas entitas.

    Parameters:
        datasets (dict): hasil dari load_json_files()

    Returns:
        list: daftar join documents
    """

    documents = []

    # ==================================================
    # LOOKUP TABLES
    # Mempermudah proses join berdasarkan ID
    # ==================================================

    dokter_lookup = {
        d["dokter_id"]: d
        for d in datasets["dokter"]
    }

    departemen_lookup = {
        d["departemen_id"]: d
        for d in datasets["departemen"]
    }

    pasien_lookup = {
        p["pasien_id"]: p
        for p in datasets["pasien"]
    }

    asuransi_lookup = {
        a["asuransi_id"]: a
        for a in datasets["asuransi"]
    }

    pj_lookup = {
        pj["pj_id"]: pj
        for pj in datasets["penanggung_jawab"]
    }

    tim_lookup = {
        t["tim_id"]: t
        for t in datasets["tim_medis"]
    }

    tagihan_lookup = {
        t["tagihan_id"]: t
        for t in datasets["tagihan"]
    }

    pembayaran_lookup = {
        p["pembayaran_id"]: p
        for p in datasets["pembayaran"]
    }

    # ==================================================
    # DOKTER + DEPARTEMEN
    # ==================================================

    for dokter in datasets["dokter"]:

        departemen = departemen_lookup.get(
            dokter["departemen_id"]
        )

        documents.append({
            "doc_type": "dokter_departemen",
            "source_id": dokter["dokter_id"],
            "content": f"""
            ID Dokter: {dokter['dokter_id']}
            ID Departemen: {dokter['departemen_id']}
            Nama Dokter: {dokter['nama_dokter']}
            Spesialisasi: {dokter['spesialisasi']}
            Departemen: {departemen['nama_departemen']}
            """
        })

    # ==================================================
    # PASIEN + ASURANSI + PJ + TIM
    # ==================================================

    for pasien in datasets["pasien"]:

        asuransi = asuransi_lookup.get(
            pasien["asuransi_id"]
        )

        pj = pj_lookup.get(
            pasien["pj_id"]
        )

        tim = tim_lookup.get(
            pasien["tim_id"]
        )

        nama_asuransi = (
            asuransi["nama_asuransi"]
            if asuransi
            else "Tidak memiliki asuransi"
        )


        documents.append({
            "doc_type": "pasien_profile",
            "source_id": pasien["pasien_id"],
            "content": f"""
            ID Pasien: {pasien['pasien_id']}
            Nama Pasien: {pasien['nama_pasien']}
            Status VIP: {'Ya' if pasien['vip_status'] else 'Tidak'}
            ID Asuransi: {pasien['asuransi_id']}
            Asuransi: {nama_asuransi}
            ID PJ: {pasien['pj_id']}
            Penanggung Jawab: {pj['nama_pj']}
            Hubungan: {pj['hubungan']}
            ID Tim: {pasien['tim_id']}
            Tim Medis: {tim['nama_tim']}
            """
        })

    # ==================================================
    # TIM MEDIS + NAMA DOKTER
    # ==================================================

    for tim in datasets["tim_medis"]:

        dokter_names = []

        for dokter_id in tim["daftar_dokter"]:

            dokter = dokter_lookup.get(
                dokter_id
            )

            if dokter:
                dokter_names.append(
                    dokter["nama_dokter"]
                )

        documents.append({
            "doc_type": "tim_medis_detail",
            "source_id": tim["tim_id"],
            "content": f"""
            ID Tim: {tim['tim_id']}
            Nama Tim: {tim['nama_tim']}
            Anggota Dokter:
            {', '.join(dokter_names)}
            """
        })

    # ==================================================
    # TAGIHAN + PASIEN + ASURANSI
    # ==================================================

    for tagihan in datasets["tagihan"]:

        pasien = pasien_lookup.get(
            tagihan["pasien_id"]
        )

        asuransi = asuransi_lookup.get(
            tagihan["asuransi_id"]
        )

        nama_asuransi = (
            asuransi["nama_asuransi"]
            if asuransi
            else "Tidak memiliki asuransi"
        )
        
        documents.append({
            "doc_type": "tagihan_profile",
            "source_id": tagihan["tagihan_id"],
            "content": f"""
            ID Tagihan: {tagihan['tagihan_id']}
            ID Pasien: {pasien['pasien_id']}
            ID Asuransi: {tagihan['asuransi_id']}
            Nama Pasien: {pasien['nama_pasien']}
            Asuransi: {nama_asuransi}
            Total Biaya: {tagihan['total_biaya']}
            Status Pembayaran: {tagihan['status_pembayaran']}
            """
        })

    # ==================================================
    # PEMBAYARAN + TAGIHAN + PASIEN
    # ==================================================

    for pembayaran in datasets["pembayaran"]:

        tagihan = tagihan_lookup.get(
            pembayaran["tagihan_id"]
        )

        pasien = pasien_lookup.get(
            tagihan["pasien_id"]
        )

        documents.append({
            "doc_type": "pembayaran_profile",
            "source_id": pembayaran["pembayaran_id"],
            "content": f"""
            ID Pembayaran: {pembayaran['pembayaran_id']}
            ID Pasien: {pasien['pasien_id']}
            ID Tagihan: {tagihan['tagihan_id']}
            Nama Pasien: {pasien['nama_pasien']}
            Metode Pembayaran: {pembayaran['metode_pembayaran']}
            Jumlah Dibayar: {pembayaran['jumlah_dibayar']}
            Tanggal Pembayaran: {pembayaran['tanggal_pembayaran']}
            """
        })

    # ==================================================
    # DETAIL LAYANAN + TAGIHAN + PASIEN
    # ==================================================

    for detail in datasets["detail_layanan"]:

        tagihan = tagihan_lookup.get(
            detail["tagihan_id"]
        )

        pasien = pasien_lookup.get(
            tagihan["pasien_id"]
        )

        documents.append({
            "doc_type": "layanan_profile",
            "source_id": detail["detail_id"],
            "content": f"""
            ID Pasien: {pasien['pasien_id']}
            ID Tagihan: {tagihan['tagihan_id']}
            ID Detail: {detail['detail_id']}
            Nama Pasien: {pasien['nama_pasien']}
            Jenis Layanan: {detail['jenis_layanan']}
            Biaya Layanan: {detail['biaya']}
            Deskripsi: {detail['deskripsi']}
            """
        })

    # ==================================================
    # BUKTI PEMBAYARAN + PEMBAYARAN + PASIEN
    # ==================================================

    for bukti in datasets["bukti_pembayaran"]:

        pembayaran = pembayaran_lookup.get(
            bukti["pembayaran_id"]
        )

        tagihan = tagihan_lookup.get(
            pembayaran["tagihan_id"]
        )

        pasien = pasien_lookup.get(
            tagihan["pasien_id"]
        )

        documents.append({
            "doc_type": "bukti_pembayaran_profile",
            "source_id": bukti["bukti_id"],
            "content": f"""
            ID Pasien: {pasien['pasien_id']}
            ID Pembayaran: {pembayaran['pembayaran_id']}
            ID Bukti: {bukti['bukti_id']}
            Nama Pasien: {pasien['nama_pasien']}
            Nomor Bukti: {bukti['nomor_bukti']}
            Tanggal Terbit: {bukti['tanggal_terbit']}
            Metode Pembayaran: {pembayaran['metode_pembayaran']}
            """
        })

    print(
        f"✓ Menghasilkan {len(documents)} join documents"
    )

    return documents
    
def create_embeddings(documents):
    """
    Membuat embedding untuk seluruh knowledge documents
    dan menyimpannya ke file JSON.

    Parameters:
        documents (list): hasil gabungan master_docs dan join_docs

    Returns:
        list: dokumen yang sudah memiliki embedding
    """

    print("Memuat model embedding...")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    embedded_documents = []

    print(
        f"Menghasilkan embeddings untuk {len(documents)} documents..."
    )

    for doc in tqdm(documents):

        embedding = model.encode(
            doc["content"]
        )

        embedded_documents.append({
            **doc,
            "embedding": embedding.tolist()
        })

    # ==================================
    # Simpan hasil embedding ke file
    # ==================================

    output_file = "embedded_documents.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            embedded_documents,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"✓ Menyimpan embeddings ke {output_file}"
    )

    return embedded_documents
    
def connect_opensearch():
    """
    Membuat koneksi ke OpenSearch dan memastikan
    server dapat diakses.

    Returns:
        OpenSearch: client OpenSearch
    """

    try:

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

        info = client.info()

        print(
            f"✓ Berhasil terkoneksi dengan OpenSearch "
            f"{info['version']['number']}"
        )

        return client

    except Exception as error:

        print(
            f"✗ Gagal terkoneksi dengan OpenSearch: {error}"
        )

        raise
    
def create_index(client):
    """
    Membuat index OpenSearch untuk menyimpan
    knowledge documents dan vector embeddings.

    Parameters:
        client (OpenSearch): koneksi OpenSearch
    """

    if client.indices.exists(
        index=INDEX_NAME
    ):

        print(
            f"✓ Index '{INDEX_NAME}' already exists"
        )

        return

    index_body = {
        "settings": {
            "index": {
                "knn": True
            }
        },
        "mappings": {
            "properties": {

                "doc_type": {
                    "type": "keyword"
                },

                "source_id": {
                    "type": "keyword"
                },

                "content": {
                    "type": "text"
                },

                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384
                }
            }
        }
    }

    client.indices.create(
        index=INDEX_NAME,
        body=index_body
    )

    print(
        f"✓ Index '{INDEX_NAME}' berhasil dibuat"
    )
    
def recreate_index(client):
    """
    Menghapus index lama lalu membuat ulang.
    Berguna saat development.
    """

    if client.indices.exists(
        index=INDEX_NAME
    ):

        client.indices.delete(
            index=INDEX_NAME
        )

        print(
            f"✓ Menghapus '{INDEX_NAME}'"
        )

    create_index(client)
    
def upload_documents(client, documents):
    """
    Mengunggah seluruh dokumen ke OpenSearch.
    """

    success_count = 0
    failed_count = 0

    for doc in tqdm(documents):

        try:

            client.index(
                index=INDEX_NAME,
                body=doc
            )

            success_count += 1

        except Exception as error:

            failed_count += 1

            print(
                f"Gagal mengunggah dokumen: {doc['source_id']}"
            )

            print(error)

    print(
        f"✓ Berhasil: {success_count}"
    )

    print(
        f"✗ Gagal: {failed_count}"
    )
    
def load_embedded_documents():
    """
    Membaca embedded documents dari file JSON.
    """

    with open(
        "embedded_documents.json",
        "r",
        encoding="utf-8"
    ) as file:

        documents = json.load(file)

    print(
        f"✓ Memuat {len(documents)} dokumen yang diembed"
    )

    return documents

def main():

    # ==========================
    # LOAD DATASET
    # ==========================

    datasets = load_json_files()

    # ==========================
    # GENERATE DOCUMENTS
    # ==========================

    master_docs = generate_master_documents(
        datasets
    )

    join_docs = generate_join_documents(
        datasets
    )

    all_docs = master_docs + join_docs

    print(
        f"Total documents: {len(all_docs)}"
    )

    # ==========================
    # EMBEDDING
    # ==========================

    embedded_docs = create_embeddings(
        all_docs
    )

    # ==========================
    # CONNECT TO OPENSEARCH
    # ==========================

    client = connect_opensearch()

    # ==========================
    # CREATE INDEX
    # ==========================

    recreate_index(client)

    # ==========================
    # UPLOAD DOCUMENTS
    # ==========================

    upload_documents(
        client,
        embedded_docs
    )

    print(
        "\n✓ Setup berhasil diselesaikan dengan sukses!"
    )
    
if __name__ == "__main__":
    main()