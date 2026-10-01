import os
import streamlit as st
from openai import OpenAI


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Agente IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CLIENTE GEMINI
# ============================================================

modelo = OpenAI(api_key="AIzaSyBU-MW_oxHitDV1pkYuyG5fBJka41uBZIs",
                   base_url="https://generativelanguage.googleapis.com/v1beta/openai")


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

    /* =========================
       CONFIGURAÇÃO GERAL
       ========================= */

    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }

    .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background-color: #080c14;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] h1 {
        color: #ffffff;
    }

    .sidebar-logo {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .sidebar-logo .icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .sidebar-logo .title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
    }

    .sidebar-logo .subtitle {
        color: #64748b;
        font-size: 13px;
    }


    /* =========================
       HEADER
       ========================= */

    .chat-header {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 18px 22px;
        margin-bottom: 25px;

        background: linear-gradient(
            135deg,
            #111827,
            #0f172a
        );

        border: 1px solid #1e293b;
        border-radius: 18px;

        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
    }

    .header-icon {
        width: 52px;
        height: 52px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 15px;

        background: linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        );

        font-size: 27px;

        box-shadow:
            0 0 25px rgba(99, 102, 241, 0.25);
    }

    .header-title {
        font-size: 23px;
        font-weight: 700;
        color: #ffffff;
    }

    .header-status {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 3px;
    }

    .status-dot {
        color: #22c55e;
        font-size: 10px;
    }


    /* =========================
       WELCOME
       ========================= */

    .welcome {
        text-align: center;
        padding: 65px 20px 40px 20px;
    }

    .welcome-icon {
        font-size: 65px;
        margin-bottom: 15px;
    }

    .welcome-title {
        font-size: 31px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .welcome-text {
        font-size: 15px;
        color: #64748b;
        max-width: 550px;
        margin: auto;
        line-height: 1.6;
    }


    /* =========================
       MENSAGENS
       ========================= */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 12px 0;
    }

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        font-size: 15px;
        line-height: 1.65;
    }


    /* =========================
    INPUT DO CHAT
    ========================= */

    [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Caixa principal */
    [data-testid="stChatInput"] > div {
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s ease !important;
    }

    /* Efeito ao clicar */
    [data-testid="stChatInput"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow:
            0 0 0 1px #6366f1,
            0 8px 30px rgba(99, 102, 241, 0.15) !important;
    }

    /* Campo de texto */
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #f8fafc !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;

        font-size: 15px !important;
        line-height: 1.5 !important;
        padding: 14px 50px 14px 16px !important;
    }

    /* Placeholder */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* Botão de enviar */
    [data-testid="stChatInput"] button {
        background: #6366f1 !important;
        border: none !important;
        border-radius: 10px !important;
        width: 36px !important;
        height: 36px !important;

        transition: all 0.2s ease !important;
    }

    /* Hover do botão */
    [data-testid="stChatInput"] button:hover {
        background: #818cf8 !important;
        transform: scale(1.05);
    }

    /* Ícone do botão */
    [data-testid="stChatInput"] button svg {
        color: white !important;
    }


    /* =========================
       BOTÕES
       ========================= */

    .stButton button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #1e293b;
        background-color: #111827;
        color: #cbd5e1;
        transition: 0.2s;
    }

    .stButton button:hover {
        border-color: #6366f1;
        color: #ffffff;
        background-color: #151c2c;
    }


    /* =========================
       CARDS DA SIDEBAR
       ========================= */

    .info-card {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;

        padding: 14px;
        margin-top: 12px;

        color: #94a3b8;
        font-size: 13px;
        line-height: 1.6;
    }

    .info-card strong {
        color: #e2e8f0;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 12px;
        padding-top: 25px;
    }


    /* =========================
       ESCONDER ELEMENTOS
       ========================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
        <div class="sidebar-logo">
            <div class="icon">🤖</div>
            <div class="title">Agente IA</div>
            <div class="subtitle">Seu assistente inteligente</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️  Nova conversa"):
        st.session_state["lista_mensagens"] = []
        st.rerun()

    st.markdown("""
        <div class="info-card">
            <strong>🤖 Modelo</strong><br>
            Gemini Flash Lite
        </div>

        <div class="info-card">
            <strong>💬 Conversa</strong><br>
            O histórico permanece durante a sessão.
        </div>

        <div class="info-card">
            <strong>⚡ Status</strong><br>
            <span style="color:#22c55e;">●</span>
            Sistema online
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Desenvolvido com Python + Streamlit + Gemini
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
    <div class="chat-header">

        <div class="header-icon">
            🤖
        </div>

        <div>
            <div class="header-title">
                Agente IA
            </div>

            <div class="header-status">
                <span class="status-dot">●</span>
                Gemini Flash Lite • Online
            </div>
        </div>

    </div>
""", unsafe_allow_html=True)


# ============================================================
# TELA INICIAL
# ============================================================

if len(st.session_state["lista_mensagens"]) == 0:

    st.markdown("""
        <div class="welcome">

            <div class="welcome-icon">
                ✨
            </div>

            <div class="welcome-title">
                Olá! Como posso ajudar?
            </div>

            <div class="welcome-text">
                Converse com seu assistente de IA.
                Faça perguntas, peça explicações,
                gere ideias ou simplesmente comece uma conversa.
            </div>

        </div>
    """, unsafe_allow_html=True)


# ============================================================
# HISTÓRICO
# ============================================================

for mensagem in st.session_state["lista_mensagens"]:

    role = mensagem["role"]
    content = mensagem["content"]

    with st.chat_message(
        role,
        avatar="👤" if role == "user" else "🤖"
    ):
        st.markdown(content)


# ============================================================
# INPUT
# ============================================================

mensagem_usuario = st.chat_input(
    "Digite sua mensagem..."
)


# ============================================================
# PROCESSAMENTO DA MENSAGEM
# ============================================================

if mensagem_usuario:

    # -----------------------------------------
    # Mensagem do usuário
    # -----------------------------------------

    mensagem = {
        "role": "user",
        "content": mensagem_usuario
    }

    st.session_state["lista_mensagens"].append(mensagem)

    with st.chat_message("user", avatar="👤"):
        st.markdown(mensagem_usuario)


    # -----------------------------------------
    # Resposta da IA
    # -----------------------------------------

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Pensando..."):

            resposta_modelo = modelo.chat.completions.create(
                messages=st.session_state["lista_mensagens"],
                model="gemini-flash-lite-latest"
            )

            resposta_ia = resposta_modelo.choices[0].message.content

        st.markdown(resposta_ia)


    # -----------------------------------------
    # Salvar resposta
    # -----------------------------------------

    mensagem_ia = {
        "role": "assistant",
        "content": resposta_ia
    }

    st.session_state["lista_mensagens"].append(mensagem_ia)