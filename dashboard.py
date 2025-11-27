import streamlit as st
import random
from gemini import generar_respuesta

# ================== CONFIG GLOBAL ==================
st.set_page_config(
    page_title="CatGPT",
    page_icon="🐾",
    layout="wide",
)

# ================== CSS PERSONALIZADO ==================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f172a 0, #020617 40%, #000000 100%);
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

/* Header */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.8rem;
}

.app-title-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.app-title {
    font-size: 2.4rem;
    font-weight: 750;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, #f97316, #ec4899, #a855f7, #22c55e);
    -webkit-background-clip: text;
    color: transparent;
}

.app-subtitle {
    font-size: 0.95rem;
    color: #9ca3af;
}

.badge-stack {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.3rem;
}

.badge-pill {
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    border: 1px solid #4b5563;
    font-size: 0.75rem;
    color: #e5e7eb;
    background: rgba(15, 23, 42, 0.95);
}

/* Cards */
.card {
    background: rgba(15, 23, 42, 0.98);
    border-radius: 1.4rem;
    padding: 1.4rem 1.5rem;
    border: 1px solid #111827;
    box-shadow: 0 22px 55px rgba(0, 0, 0, 0.6);
}

.card-soft {
    background: rgba(15, 23, 42, 0.96);
    border-radius: 1.2rem;
    padding: 1.2rem 1.3rem;
    border: 1px solid #0f172a;
}

/* Textarea */
.stTextArea textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 0.9rem !important;
    border: 1px solid #1f2937 !important;
    font-size: 0.97rem !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ec4899, #a855f7);
    color: white;
    border-radius: 999px;
    border: none;
    font-weight: 600;
    padding: 0.6rem 2.0rem;
    font-size: 0.93rem;
    cursor: pointer;
    box-shadow: 0 14px 40px rgba(236, 72, 153, 0.45);
    transition: transform 0.08s ease, box-shadow 0.08s ease, filter 0.1s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.06);
    box-shadow: 0 18px 55px rgba(236, 72, 153, 0.6);
}

/* Chips */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 0.7rem;
}

.chip {
    font-size: 0.8rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    border: 1px solid #4b5563;
    background: #020617;
    color: #e5e7eb;
}

/* Response */
.response-content {
    font-size: 0.96rem;
    line-height: 1.7;
    color: #e5e7eb;
    white-space: pre-wrap;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #111827;
}

/* Cat image */
.cat-caption {
    font-size: 0.85rem;
    color: #9ca3af;
    margin-top: 0.4rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ================== ESTADO ==================
if "prompt_texto" not in st.session_state:
    st.session_state["prompt_texto"] = ""
if "respuesta_texto" not in st.session_state:   
    st.session_state["respuesta_texto"] = ""
if "respuesta_imagen" not in st.session_state:   
    st.session_state["respuesta_imagen"] = None
if "ejecutar" not in st.session_state:            
    st.session_state["ejecutar"] = False

# Lista de imágenes de gatitos (urls públicas)
CAT_IMAGES = [
    "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg",
    "https://images.pexels.com/photos/617278/pexels-photo-617278.jpeg",
    "https://images.pexels.com/photos/127409/pexels-photo-127409.jpeg",
    "https://images.pexels.com/photos/20787/pexels-photo.jpg",
    "https://images.pexels.com/photos/177809/pexels-photo-177809.jpeg",
]

# ================== SIDEBAR ==================
st.sidebar.markdown("### 🐾 Modo gatuno")

modo = st.sidebar.radio(
    "¿En que nos enfocamos?",
    [
        "Datos",
        "Consejos",
        "Historias",
        "Nombres estéticos",
    ],
)

temperature = st.sidebar.slider(
    "Creatividad",
    0.0, 1.5, 0.9, 0.1,
)

max_tokens = st.sidebar.slider(
    "Máx. tokens",
    64, 1024, 512, 64,
)

if modo == "Datos":
    system_instruction = (
        "Eres un experto en gatos que cuenta datos curiosos, divertidos y adorables "
        "sobre gatos. Explica de forma clara y amigable."
    )
elif modo == "Consejos":
    system_instruction = (
        "Das consejos básicos, responsables y seguros para el cuidado de gatos "
        "domésticos. No des consejos médicos avanzados; para eso siempre recomiendas "
        "consultar a un veterinario."
    )
elif modo == "Historias":
    system_instruction = (
        "Inventas historias cortas y tiernas sobre gatitos, con un tono narrativo "
        "lindo y visual."
    )
else:  # "Nombres estéticos"
    system_instruction = (
        "Generas listas de nombres creativos y estéticos para gatos, con explicaciones "
        "cortas del estilo o significado de cada nombre."
    )

st.sidebar.markdown("---")
st.sidebar.caption("Gemini vía google-genai 🐱")

# ================== PROCESO  ==================
if st.session_state["ejecutar"]:
    with st.spinner("Hablando con CatGPT..."):
        try:
            texto = generar_respuesta(
                prompt=st.session_state["prompt_texto"],
                model="gemini-2.0-flash",
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_instruction,
            )
            st.session_state["respuesta_texto"] = texto
            st.session_state["respuesta_imagen"] = random.choice(CAT_IMAGES)
        except Exception as e:
            st.session_state["respuesta_texto"] = f"Error al llamar a Gemini: {e}"
            st.session_state["respuesta_imagen"] = None

    st.session_state["ejecutar"] = False  

# ================== HEADER ==================
st.markdown(
    """
    <div class="app-header">
        <div class="app-title-group">
            <div class="app-title">CatGPT · Gatitos + Gemini</div>
            <div class="app-subtitle">
                Juega con un modelo de lenguaje tematizado en gatos
            </div>
        </div>
        <div class="badge-stack">
            <div class="badge-pill">🐾 Friendly LLM UI</div>
            <div class="badge-pill">✨ Streamlit + google-genai</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================== LAYOUT DOS COLUMNAS ==================
col_left, col_right = st.columns([0.55, 0.45])

with col_left:
    st.markdown('<div>', unsafe_allow_html=True)

    ejemplos = [
        "Dame los mejores 5 datos extraños sobre gatos.",
        "Explícame cómo son los psicólogos para gatos.",
        "Invéntate una historia corta sobre un gatito astronauta.",
        "Dame 10 nombres estéticos para una gata blanca y tranquila.",
    ]

    st.markdown('<div class="chip-row">', unsafe_allow_html=True)
    for i, texto in enumerate(ejemplos):
        if st.button(texto, key=f"chip_{i}"):
            st.session_state["prompt_texto"] = texto
    st.markdown("</div>", unsafe_allow_html=True)

    prompt = st.text_area(
        "",
        value=st.session_state["prompt_texto"],
        height=180,
        placeholder="Escribe tu prompt gatuno aquí...",
    )

    if st.button("Genera ✨"):                     
        st.session_state["prompt_texto"] = prompt
        st.session_state["ejecutar"] = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div>', unsafe_allow_html=True)

    if st.session_state["respuesta_texto"]:
        st.markdown(
            f"<div class='response-content'>{st.session_state['respuesta_texto']}</div>",
            unsafe_allow_html=True,
        )

    if st.session_state["respuesta_imagen"]:
        st.image(st.session_state["respuesta_imagen"], use_container_width=True)
        st.markdown(
            "<div class='cat-caption'>Gatito aleatorio 🐾</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
