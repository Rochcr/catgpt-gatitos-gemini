import streamlit as st
from google import genai

# ======================================
# CONFIG API KEY
# ======================================

API_KEY = (
    st.secrets.get("GEMINI_API_KEY")
    or st.secrets.get("GOOGLE_API_KEY")
    or None
)

DEFAULT_MODEL = "gemini-2.5-flash"


def _get_client():
    """Devuelve el cliente de Gemini o None si no hay API key."""
    if not API_KEY:
        return None
    return genai.Client(api_key=API_KEY)


# ======================================
# FUNCIÓN QUE LLAMA EL DASHBOARD
# ======================================

def generar_respuesta(
    prompt: str,
    temperature: float = 0.9,
    max_tokens: int = 512,
    model: str | None = None,
    **kwargs,   # ← CLAVE: acepta cualquier argumento extra
):
    """
    Función robusta que acepta 'model' y cualquier otro parámetro adicional.
    Compatible con el UI de CatGPT.
    """

    client = _get_client()

    if client is None:
        return "⚠️ No hay API KEY configurada. Agrega GEMINI_API_KEY en tus secrets."

    used_model = model or DEFAULT_MODEL

    try:
        response = client.models.generate_content(
            model=used_model,
            contents=prompt,
            config={
                "temperature": float(temperature),
                "max_output_tokens": int(max_tokens),
            },
        )
        return (response.text or "").strip()

    except Exception as e:
        return f"⚠️ Error al llamar a Gemini: {e}"
