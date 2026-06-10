from google import genai

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

from retrieval import retrieve_context


# ==================================
# Configure Gemini
# ==================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==================================
# Build Prompt
# ==================================

def build_prompt(
    question,
    context_text
):
    """
    Membuat prompt untuk Gemini.
    """

    prompt = f"""
Anda adalah chatbot Rumah Sakit Sehat Selalu.

Gunakan hanya informasi dari konteks yang diberikan.

Berikan jawaban yang lengkap, jelas, dan informatif.
Jika terdapat beberapa data yang relevan, tampilkan semuanya dalam bentuk daftar.

Jika informasi tidak ditemukan dalam konteks,
jawab:

"Maaf, informasi tersebut tidak tersedia dalam basis pengetahuan."

====================
KONTEKS
====================

{context_text}

====================
PERTANYAAN
====================

{question}

====================
JAWABAN
====================
"""

    return prompt


# ==================================
# Generate Answer
# ==================================

def answer_question(
    question,
    top_k=10
):

    contexts = retrieve_context(
        question,
        top_k
    )
    # Debug: Tampilkan konteks yang diambil
    # print("\n=== RETRIEVED CONTEXT ===\n")

    # for i, context in enumerate(
    #     contexts,
    #     start=1
    # ):
    #     print(f"Context {i}")
    #     print(context)
    #     print("-" * 50)

    context_text = "\n\n".join(
        contexts
    )

    prompt = build_prompt(
        question,
        context_text
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text


# ==================================
# Main
# ==================================

def main():

    while True:

        question = input(
            "\nMasukkan pertanyaan (ketik 'exit' untuk keluar): "
        )
        question = question.lower()
        if question == "exit":
            break

        answer = answer_question(
            question
        )

        print("\nJAWABAN:\n")

        print(answer)

        

if __name__ == "__main__":
    main()