import streamlit as st

from contabilidade.util import importar_dados_excel, converter_para_datetime


def pagina_upload_dados():
    st.header("Upload de Dados")
    st.write("Faça o upload do arquivo Excel contendo os dados financeiros.")
    arquivo = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

    if arquivo is not None:
        df = importar_dados_excel(arquivo)

        # Converte a coluna 'Mes' para datetime no formato padrão %Y-%m
        try:
            df = converter_para_datetime(df, 'Mes', '%Y-%m')
        except ValueError as e:
            st.error(f"Erro ao converter a coluna 'Mes' para datetime: {e}")
            return

        st.session_state["df"] = df
        st.write("Dados importados do Excel:")
        st.dataframe(df.head())
