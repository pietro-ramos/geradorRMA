import streamlit as st

from contabilidade.util import filtrar_contas_ultimos_12_meses, exportar_para_pptx


def pagina_exportar_plano_contas():
    st.header("Exportar Plano de Contas para PowerPoint")

    if "df" not in st.session_state:
        st.warning("Por favor, faça o upload dos dados primeiro.")
        return

    # Filtrar contas dos últimos 12 meses
    df_filtrado = filtrar_contas_ultimos_12_meses(st.session_state["df"])

    if st.button("Exportar para PowerPoint"):
        caminho_pptx = "relatorio_contas.pptx"
        exportar_para_pptx(df_filtrado, caminho_pptx)
        st.success(f"Relatório exportado para {caminho_pptx}")
