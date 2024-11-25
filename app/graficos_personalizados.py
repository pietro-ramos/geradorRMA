import streamlit as st
import os
from graficos.graficos import carregar_modelo_grafico, listar_modelos_disponiveis
from graficos.extracao import extrair_contas_para_modelo, extrair_indicadores_para_modelo
from graficos.exportacao import exportar_modelo_para_excel


def pagina_exportar_graficos():
    st.header("Exportar Gráficos para Excel")

    caminho_pasta_modelos = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/modelos"))
    caminho_arquivo = st.text_input("Caminho do arquivo Excel", os.path.join(caminho_pasta_modelos, "modelos_graficos.xlsx"))
    modelos_disponiveis = listar_modelos_disponiveis()
    nome_modelo = st.selectbox("Selecione o Modelo de Gráfico", modelos_disponiveis)

    if "consolidados" not in st.session_state or len(st.session_state["consolidados"]) == 0:
        st.warning("Nenhum dado consolidado. Por favor, faça a filtragem e consolidação primeiro.")
        return

    planos_selecionados = st.multiselect("Selecione os Planos de Contas para Exportação",
                                         options=st.session_state["consolidados"].keys())

    if st.button("Exportar para Excel"):
        modelo = carregar_modelo_grafico(nome_modelo)
        for plano in planos_selecionados:
            balanco = st.session_state["consolidados"][plano]
            df_filtrado = st.session_state["df_filtrado"]

            # Extrair dados de acordo com o modelo
            df_contas = extrair_contas_para_modelo(balanco, df_filtrado, modelo)
            df_indicadores = extrair_indicadores_para_modelo(balanco, modelo)

            # Exportar para Excel
            exportar_modelo_para_excel(caminho_arquivo, modelo, df_contas, df_indicadores)

        st.success("Dados exportados com sucesso para os modelos de gráficos!")
