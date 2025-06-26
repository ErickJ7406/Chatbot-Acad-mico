import streamlit as st
from search_engine import BuscadorSemantico
import html

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Buscador del Libro de IA", layout="wide", page_icon="📚")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .stChatMessage[data-testid="chat-message-container-user"] {
        background-color: #E1F5FE;
    }
    .stChatMessage[data-testid="chat-message-container-assistant"] {
        background-color: #F0F2F6;
    }
    .result-container {
        background-color: #262730; /* <-- CORRECCIÓN: Fondo oscuro */
        color: #FAFAFA; /* <-- CORRECCIÓN: Texto claro */
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        border-left: 4px solid #4F8BF9;
        font-size: 0.95em;
    }
    .result-container b {
        color: #4F8BF9;
    }
    .result-container span {
        font-size: 0.85em;
        color: #B0B0B0; /* <-- CORRECCIÓN: Gris más claro */
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO Y DESCRIPCIÓN ---
st.markdown("<h1 style='text-align: center; color: #4F8BF9;'>📚 Chatbot Académico: Buscador del Libro de IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Haz una pregunta sobre el contenido del libro y el asistente te mostrará los fragmentos más relevantes.</p>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("ℹ️ Instrucciones")
    st.markdown("""
    - Usa la caja de chat para hacer tus preguntas.
    - El asistente recordará el historial de tu conversación.
    - Puedes usar las preguntas de ejemplo para empezar.
    """)
    st.markdown("---")
    st.info("Desarrollado por: Erick - Danilo - Elvis - Kevin - Fercho ❤ | Chatbot académico", icon="🤖")

# --- CARGA DEL BUSCADOR (CACHEADO) ---
@st.cache_resource
def cargar_buscador():
    return BuscadorSemantico(
        ruta_index="data/faiss.index",
        ruta_chunks="data/embeddings.pkl",
        top_k=3,
        umbral_similitud=0.60
    )
buscador = cargar_buscador()

# --- INICIALIZACIÓN DEL HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNCIÓN AUXILIAR PARA MOSTRAR RESPUESTAS ---
def display_assistant_response(resultados):
    if resultados and resultados[0].get("id") is not None:
        st.markdown("<p>He encontrado estos fragmentos que podrían ser relevantes:</p>", unsafe_allow_html=True)
        # CORRECCIÓN: Renderizar cada resultado individualmente
        for res in resultados:
            chunk_text = html.escape(res.get("chunk", ""))
            response_html = f"""
            <div class='result-container'>
                <b>Fragmento ID: {res.get('id')}</b> <span>(Similitud: {int(res.get('similitud', 0)*100)}%)</span>
                <p>{chunk_text}</p>
            </div>
            """
            st.markdown(response_html, unsafe_allow_html=True)
    else:
        st.markdown("<p>🤖 Lo siento, no encontré información suficientemente relevante. Intenta reformular tu pregunta.</p>", unsafe_allow_html=True)

# --- MOSTRAR MENSAJES DEL HISTORIAL ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else: # Assistant
            # El contenido es la lista de resultados
            display_assistant_response(message["content"])

# --- LÓGICA DE PREGUNTAS DE EJEMPLO ---
def hacer_pregunta_ejemplo(pregunta):
    st.session_state.pregunta_ejemplo = pregunta

st.markdown("**O prueba con una de estas preguntas:**")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("¿Qué es un agente racional?", on_click=hacer_pregunta_ejemplo, args=("¿Qué es un agente racional?",), use_container_width=True)
with col2:
    st.button("¿En qué consiste el aprendizaje por refuerzo?", on_click=hacer_pregunta_ejemplo, args=("¿En qué consiste el aprendizaje por refuerzo?",), use_container_width=True)
with col3:
    st.button("Explica la diferencia entre búsqueda informada y no informada", on_click=hacer_pregunta_ejemplo, args=("Explica la diferencia entre búsqueda informada y no informada",), use_container_width=True)

# --- ENTRADA DE CHAT DEL USUARIO ---
if prompt := st.chat_input("Escribe tu pregunta aquí...") or st.session_state.get("pregunta_ejemplo"):
    st.session_state.pregunta_ejemplo = None

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando información relevante..."):
            resultados = buscador.buscar(prompt)
            display_assistant_response(resultados)
    
    st.session_state.messages.append({"role": "assistant", "content": resultados})
