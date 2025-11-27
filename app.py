import streamlit as st
from google import genai

# ─────────────────────────────────────
# CONFIG SECRETS Y CLIENTE GEMINI
# ─────────────────────────────────────
API_KEY = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
MODEL = "gemini-2.5-flash"  # puedes cambiarlo si quieres

if not API_KEY:
    st.error("Add GEMINI_API_KEY or GOOGLE_API_KEY to your Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# ─────────────────────────────────────
# CONFIG DE PÁGINA
# ─────────────────────────────────────
st.set_page_config(
    page_title="Gemini + Streamlit",
    layout="centered"
)

st.title("✨ Gemini + Streamlit")
st.write("Escribe un prompt y genera una respuesta con el modelo Gemini.")

# Prompt
prompt = st.text_area("Prompt", "Explain how AI works in a few words.", height=120)

# Parámetros extra
temperature = st.slider("Creatividad (temperature)", 0.0, 1.5, 0.9)
max_tokens = st.slider("Máximo de tokens", 64, 1024, 256, step=64)

# Botón
if st.button("Send to Gemini"):
    if not prompt.strip():
        st.error("Write a prompt first.")
    else:
        with st.spinner("Calling Gemini..."):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                    config={
                        "temperature": float(temperature),
                        "max_output_tokens": int(max_tokens),
                    },
                )
                text = (response.text or "").strip()
            except Exception as e:
                text = f"Error: {e}"

        st.subheader("Response")
        st.write(text or "(empty response)")
