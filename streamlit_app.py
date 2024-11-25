import streamlit as st

from app.layout import layout_main

# Configuração da página do Streamlit
st.set_page_config(page_title="Análise Financeira", layout="wide")

if __name__ == "__main__":
    layout_main()
