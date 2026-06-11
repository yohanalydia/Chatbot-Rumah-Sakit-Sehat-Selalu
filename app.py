import streamlit as st

st.set_page_config(
    page_title="Asisten RS Sehat Selalu",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root {
  --primary:#087f73; --primary-dark:#075f58; --soft:#eaf7f5;
  --ink:#173330; --muted:#687d79; --line:#dce9e7; --surface:#fff;
}
html, body, [class*="css"] {
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.stApp {
  color:var(--ink);
  background:radial-gradient(circle at 85% 0%,rgba(31,176,157,.10),transparent 28rem),#f5f9f8;
}
[data-testid="stHeader"] {
  background:rgba(245,249,248,.8);
  backdrop-filter:blur(12px)
}
#MainMenu, footer, [data-testid="stDecoration"] {
  display:none!important
}
.block-container {
  max-width:960px;
  padding-top:2rem;
  padding-bottom:7rem
}
[data-testid="stSidebar"] {
  background:#fafffe;
  border-right:1px solid var(--line)
}
.brand {
  display:flex;
  align-items:center;
  gap:.75rem;
  margin-bottom:1.2rem
}
.brand-mark {
  display:grid;
  place-items:center;
  width:42px;
  height:42px;
  border-radius:13px;
  color:#fff;
  background:linear-gradient(145deg,var(--primary),#27aa97);
  font-size:.78rem;
  font-weight:800;
  box-shadow:0 8px 20px rgba(8,127,115,.2)
}
.brand-title {
  font-size:.98rem;
  font-weight:750;
  line-height:1.2
}
.brand-subtitle {
  margin-top:.1rem;
  color:var(--muted);
  font-size:.76rem
}
.sidebar-label {
  margin:1.15rem 0 .5rem;
  color:#81918e;
  font-size:.68rem;
  font-weight:800;
  letter-spacing:.09em;
  text-transform:uppercase
}
.status-card {
  padding:.85rem;
  border:1px solid var(--line);
  border-radius:14px;
  background:#fff
}
.status-row {
  display:flex;
  align-items:center;
  gap:.55rem;
  font-size:.85rem;
  font-weight:700
}
.status-dot {
  width:9px;
  height:9px;
  border-radius:50%;
  background:#d14343;
  box-shadow:0 0 0 4px #d143431c
}
.status-dot.online {
  background:#18a66f;
  box-shadow:0 0 0 4px #18a66f20
}
.status-detail {
  margin-top:.38rem;
  color:var(--muted);
  font-size:.75rem;
  line-height:1.45
}
.data-tags {
  display:flex;
  flex-wrap:wrap;
  gap:.35rem
}
.data-tag {
  padding:.3rem .52rem;
  border:1px solid #d8ebe8;
  border-radius:999px;
  color:#35645f;
  background:#eff9f7;
  font-size:.69rem;
  font-weight:650
}
.notice {
  margin-top:1rem;
  padding:.72rem .8rem;
  border-left:3px solid #dda63a;
  border-radius:0 10px 10px 0;
  color:#755b26;
  background:#fff9ec;
  font-size:.72rem;
  line-height:1.5
}
.hero {
  position:relative;
  overflow:hidden;
  margin-bottom:1.5rem;
  padding:1.45rem 1.55rem;
  border:1px solid #087f7321;
  border-radius:22px;
  background:linear-gradient(135deg,#fff,#edf9f7);
  box-shadow:0 14px 34px rgba(37,79,73,.07)
}
.hero:after {
  content:"RS";
  position:absolute;
  right:1.2rem;
  top:50%;
  transform:translateY(-50%);
  color:#087f7311;
  font-size:5.5rem;
  font-weight:900;
  letter-spacing:-.08em
}
.eyebrow {
  position:relative;
  z-index:1;
  color:var(--primary);
  font-size:.69rem;
  font-weight:800;
  letter-spacing:.1em;
  text-transform:uppercase
}
.hero h1 {
  position:relative;
  z-index:1;
  margin:.28rem 0 .3rem;
  font-size:clamp(1.7rem,4vw,2.45rem);
  line-height:1.1;
  letter-spacing:-.035em
}
.hero p {
  position:relative;
  z-index:1;
  max-width:650px;
  margin:0;
  color:var(--muted);
  font-size:.9rem;
  line-height:1.58
}
.welcome {
  margin:1.1rem auto .7rem;
  text-align:center
}
.welcome-title {
  font-size:1.1rem;
  font-weight:760
}
.welcome-copy {
  max-width:610px;
  margin:.35rem auto 1.1rem;
  color:var(--muted);
  font-size:.84rem;
  line-height:1.55
}
[data-testid="stChatMessage"] {
  margin-bottom:.7rem;
  padding:.95rem 1rem;
  border:1px solid var(--line);
  border-radius:17px;
  background:rgba(255,255,255,.95);
  box-shadow:0 7px 20px rgba(41,74,69,.045)
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
  line-height:1.65
}
[data-testid="stChatInput"] {
  border:1px solid #cfe2df;
  border-radius:18px;
  background:#fff;
  box-shadow:0 12px 28px rgba(35,76,70,.13)
}
[data-testid="stChatInput"]:focus-within {
  border-color:var(--primary);
  box-shadow:0 0 0 3px #087f731c,0 12px 28px rgba(35,76,70,.13)
}
.stButton>button {
  min-height:2.55rem;
  border:1px solid #d4e5e2;
  border-radius:13px;
  color:#315b56;
  background:#fff;
  font-weight:680;
  transition:.15s ease
}
.stButton>button:hover {
  border-color:#87c8be;
  color:var(--primary-dark);
  background:#eff9f7;
  transform:translateY(-1px)
}
.stButton>button[kind="primary"] {
  border:0;
  color:#fff;
  background:linear-gradient(135deg,var(--primary),#179c8d)
}
[data-testid="stSlider"] [role="slider"] {
  background:var(--primary)!important
}
@media(max-width:700px) {
  .block-container {padding:1rem .8rem 6.5rem}
  .hero {padding:1.15rem;border-radius:17px}
  .hero:after {display:none}
}
</style>
"""

DATA_LABELS = [
    "Pasien", "Dokter", "Departemen", "Tim medis", "Asuransi",
    "Penanggung jawab", "Layanan", "Tagihan", "Pembayaran",
    "Bukti pembayaran",
]

EXAMPLES = [
    "Siapa dokter spesialis kardiologi?",
    "Tampilkan pasien yang tagihannya belum lunas.",
    "Siapa penanggung jawab pasien P002?",
    "Apa layanan dan pembayaran pasien Aldo Pratama?",
]


def init_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("pending_question", None)


def reset_chat():
    st.session_state.messages = []
    st.session_state.pending_question = None


def queue_question(question):
    st.session_state.pending_question = question


@st.cache_resource(show_spinner=False)
def load_backend():
    # Import sekali karena SentenceTransformer cukup berat.
    from config import GEMINI_MODEL, INDEX_NAME
    from rag import answer_question
    from retrieval import connect_opensearch

    return answer_question, connect_opensearch, INDEX_NAME, GEMINI_MODEL


@st.cache_data(ttl=30, show_spinner=False)
def check_backend():
    client = None

    try:
        _, connect, index_name, model_name = load_backend()
        client = connect()
        count = client.count(index=index_name)["count"]

        return (
            True,
            "Sistem siap",
            f"{count} dokumen tersedia. Model: {model_name}.",
        )
    except Exception as exc:
        return (
            False,
            "Sistem belum terhubung",
            f"Periksa OpenSearch dan konfigurasi backend "
            f"({type(exc).__name__}).",
        )
    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
                pass


def ask_backend(question, top_k):
    answer_question, _, _, _ = load_backend()
    answer = answer_question(question, top_k=top_k)

    if not answer or not answer.strip():
        raise RuntimeError("Backend mengembalikan jawaban kosong.")

    return answer.strip()


def friendly_error(exc):
    message = str(exc).lower()

    if "401" in message or "api key" in message or "unauth" in message:
        return "Gemini menolak autentikasi. Periksa API key pada config.py."

    if "429" in message or "quota" in message:
        return "Kuota Gemini sedang habis. Coba kembali beberapa saat lagi."

    if "connection" in message or "opensearch" in message:
        return (
            "OpenSearch tidak dapat dihubungi. "
            "Pastikan Docker dan index rumah sakit aktif."
        )

    return (
        "Terjadi kendala saat memproses pertanyaan. "
        "Periksa terminal untuk detail teknis."
    )


def render_sidebar(online, status_title, status_detail):
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">RS</div>
                <div>
                    <div class="brand-title">RS Sehat Selalu</div>
                    <div class="brand-subtitle">Asisten data internal</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button(
            "New Chat",
            type="primary",
            use_container_width=True,
            on_click=reset_chat,
        )

        st.markdown(
            '<div class="sidebar-label">Status sistem</div>',
            unsafe_allow_html=True,
        )

        status_class = "online" if online else ""

        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-row">
                    <span class="status-dot {status_class}"></span>
                    {status_title}
                </div>
                <div class="status-detail">{status_detail}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Periksa ulang koneksi", use_container_width=True):
            check_backend.clear()
            st.rerun()

        st.markdown(
            '<div class="sidebar-label">Kedalaman pencarian</div>',
            unsafe_allow_html=True,
        )

        top_k = st.slider(
            "Jumlah konteks",
            min_value=3,
            max_value=15,
            value=10,
            help=(
                "Jumlah dokumen yang diberikan kepada Gemini "
                "untuk menyusun jawaban."
            ),
        )

        st.markdown(
            '<div class="sidebar-label">Basis data</div>',
            unsafe_allow_html=True,
        )

        tags = "".join(
            f'<span class="data-tag">{name}</span>'
            for name in DATA_LABELS
        )

        st.markdown(
            f'<div class="data-tags">{tags}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="notice">
                Gunakan untuk kebutuhan operasional internal.
                Selalu verifikasi informasi penting pada sistem rumah sakit.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return top_k


def render_header():
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Hospital Knowledge Assistant</div>
            <h1>Apa yang ingin kamu cari?</h1>
            <p>
                Cari informasi pasien, dokter, tim medis, layanan,
                asuransi, tagihan, dan pembayaran dari basis
                pengetahuan RS Sehat Selalu.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(online):
    st.markdown(
        """
        <div class="welcome">
            <div class="welcome-title">
                Mulai dengan pertanyaan yang spesifik
            </div>
            <div class="welcome-copy">
                Gunakan nama atau ID bila tersedia agar hasil lebih tepat.
                Kamu juga bisa mencari berdasarkan spesialisasi atau
                status pembayaran.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(2, gap="small")

    for index, question in enumerate(EXAMPLES):
        with columns[index % 2]:
            st.button(
                question,
                key=f"example_{index}",
                use_container_width=True,
                disabled=not online,
                on_click=queue_question,
                args=(question,),
            )


def render_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("is_error"):
                st.error(message["content"])
            else:
                st.markdown(message["content"])


def main():
    st.markdown(CSS, unsafe_allow_html=True)
    init_state()

    online, status_title, status_detail = check_backend()
    top_k = render_sidebar(online, status_title, status_detail)

    render_header()

    if not st.session_state.messages:
        render_empty_state(online)

    render_messages()

    typed = st.chat_input(
        "Tanyakan data rumah sakit...",
        disabled=not online,
    )

    queued = st.session_state.pop("pending_question", None)
    question = typed or queued

    if not question:
        if not online:
            st.warning(
                "Question box dinonaktifkan. Aktifkan OpenSearch, "
                "lalu tekan 'Periksa ulang koneksi'."
            )
        return

    question = question.strip()

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Menelusuri basis pengetahuan dan menyusun jawaban..."
        ):
            try:
                answer = ask_backend(question, top_k)
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )
            except Exception as exc:
                error = friendly_error(exc)
                st.error(error)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error,
                        "is_error": True,
                    }
                )

    st.rerun()


if __name__ == "__main__":
    main()