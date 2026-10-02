import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Sistema de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS PERSONALIZADO
# ============================================================

st.markdown("""
<style>

    /* Fundo principal */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Título principal */
    .titulo {
        font-size: 38px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 5px;
    }

    .subtitulo {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    /* Cards */
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    }

    .card-titulo {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .card-valor {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }

    .card-icone {
        font-size: 28px;
    }

    /* Seções */
    .secao {
        font-size: 23px;
        font-weight: 650;
        color: #111827;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Botão */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 10px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# ARQUIVO CSV
# ============================================================

pasta_projeto = Path(__file__).parent

arquivo_vendas = pasta_projeto / "vendas.csv"


# ============================================================
# CARREGAR DADOS
# ============================================================

if arquivo_vendas.exists():

    tabela = pd.read_csv(arquivo_vendas)

else:

    tabela = pd.DataFrame(
        columns=[
            "data",
            "vendedor",
            "produto",
            "quantidade",
            "valor"
        ]
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📊 Sistema de Vendas")

    st.markdown("---")

    st.markdown("### 🛒 Nova venda")

    data = st.date_input(
        "Data"
    )

    vendedor = st.selectbox(
        "Vendedor",
        ["Ana", "Bruno", "Carla"]
    )

    produto = st.selectbox(
        "Produto",
        ["Notebook", "Celular", "Fone"]
    )

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        step=1
    )

    valor = st.number_input(
        "Valor da venda",
        min_value=0.0,
        step=0.01
    )

    st.write("")

    botao = st.button(
        "➕ Cadastrar venda"
    )

    st.markdown("---")

    st.caption(
        "Sistema de Gestão de Vendas"
    )

    st.caption(
        "Desenvolvido com Python + Streamlit"
    )


# ============================================================
# CADASTRAR VENDA
# ============================================================

if botao:

    nova_venda = {
        "data": data,
        "vendedor": vendedor,
        "produto": produto,
        "quantidade": quantidade,
        "valor": valor
    }

    tabela.loc[len(tabela)] = nova_venda

    tabela.to_csv(
        arquivo_vendas,
        index=False
    )

    st.success("Venda cadastrada com sucesso!")

    st.rerun()


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo">📊 Dashboard de Vendas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Acompanhe o desempenho das vendas em tempo real.</div>',
    unsafe_allow_html=True
)


# ============================================================
# MÉTRICAS
# ============================================================

faturamento = tabela["valor"].sum()

quantidade_vendas = len(tabela)

produtos_vendidos = tabela["quantidade"].sum()

ticket_medio = (
    faturamento / quantidade_vendas
    if quantidade_vendas > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-icone">💰</div>
            <div class="card-titulo">Faturamento total</div>
            <div class="card-valor">R$ {faturamento:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-icone">🛒</div>
            <div class="card-titulo">Total de vendas</div>
            <div class="card-valor">{quantidade_vendas}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-icone">📦</div>
            <div class="card-titulo">Produtos vendidos</div>
            <div class="card-valor">{produtos_vendidos}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-icone">🎯</div>
            <div class="card-titulo">Ticket médio</div>
            <div class="card-valor">R$ {ticket_medio:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABELA DE VENDAS
# ============================================================

st.markdown(
    '<div class="secao">📋 Vendas cadastradas</div>',
    unsafe_allow_html=True
)

st.dataframe(
    tabela,
    width="stretch",
    hide_index=True
)


# ============================================================
# GRÁFICOS
# ============================================================

st.markdown(
    '<div class="secao">📈 Análise de vendas</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# GRÁFICO DE BARRAS
# ============================================================

with col1:

    grafico = px.bar(
        tabela,
        x="vendedor",
        y="valor",
        color="produto",
        title="Faturamento por vendedor",
        labels={
            "vendedor": "Vendedor",
            "valor": "Faturamento",
            "produto": "Produto"
        },
        template="plotly_white"
    )

    grafico.update_layout(
        legend_title="Produto",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        grafico,
        width="stretch"
    )


# ============================================================
# GRÁFICO DE PIZZA
# ============================================================

with col2:

    grafico2 = px.pie(
        tabela,
        names="produto",
        values="valor",
        title="Faturamento por produto",
        hole=0.45,
        template="plotly_white"
    )

    grafico2.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        grafico2,
        width="stretch"
    )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

st.caption(
    "📊 Sistema de Gestão de Vendas • Python + Pandas + Streamlit + Plotly"
)
