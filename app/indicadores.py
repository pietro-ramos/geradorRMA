import streamlit as st

from contabilidade.indicadores import calcular_todos_indicadores


def pagina_indicadores():
    st.header("Indicadores Financeiros")
    if "consolidados" not in st.session_state or len(st.session_state["consolidados"]) == 0:
        st.warning("Nenhum dado consolidado. Por favor, faça a filtragem e consolidação primeiro.")
        return

    planos = list(st.session_state["consolidados"].keys())
    plano_selecionado = st.selectbox("Selecione o Plano de Contas para Indicadores", options=planos)

    balanco = st.session_state["consolidados"][plano_selecionado]
    indicadores = calcular_todos_indicadores(balanco)
    st.write("Indicadores Financeiros Calculados:")
    st.dataframe(indicadores)
