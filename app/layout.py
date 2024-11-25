import streamlit as st

from app.comparacao_variacoes import pagina_comparacao_variacoes
from app.exportar_plano_pptx import pagina_exportar_plano_contas
from app.filtragem_dados import pagina_filtragem_dados
from app.graficos_personalizados import pagina_exportar_graficos
from app.indicadores import pagina_indicadores
from app.plano_contas import pagina_plano_contas
from app.upload_dados import pagina_upload_dados

# Inicialização das variáveis de sessão
if "consolidados" not in st.session_state:
    st.session_state["consolidados"] = {}


def layout_main():
    st.title("Análise Financeira e Indicadores")
    st.sidebar.title("Menu de Navegação")

    opcoes_menu = [
        "Upload de Dados",
        "Filtragem de Dados",
        "Plano de Contas",
        "Indicadores Financeiros",
        "Comparação de Variações",
        "Gráficos Personalizados",
        "Exportar plano de contas para PowerPoint",
    ]
    escolha = st.sidebar.selectbox("Escolha a Página", opcoes_menu)

    if escolha == "Upload de Dados":
        pagina_upload_dados()
    elif escolha == "Filtragem de Dados":
        pagina_filtragem_dados()
    elif escolha == "Plano de Contas":
        pagina_plano_contas()
    elif escolha == "Indicadores Financeiros":
        pagina_indicadores()
    elif escolha == "Comparação de Variações":
        pagina_comparacao_variacoes()
    elif escolha == "Gráficos Personalizados":
        pagina_exportar_graficos()
    elif escolha == "Exportar plano de contas para PowerPoint":
        pagina_exportar_plano_contas()
