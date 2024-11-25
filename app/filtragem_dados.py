import pandas as pd
import streamlit as st

from contabilidade.hierarquia_contas import hierarquia_contas
from contabilidade.util import filtrar_dados, construir_contas, registrar_valores, encontrar_conta_por_codigo
from entidades.BalancoPatrimonial import BalancoPatrimonial


def pagina_filtragem_dados():
    st.header("Filtragem de Dados")

    if "consolidados" not in st.session_state:
        st.session_state["consolidados"] = {}
    if "df_completo" not in st.session_state:
        st.session_state["df_completo"] = pd.DataFrame()  # Inicializa um DataFrame vazio para consolidar todos os dados

    # Verifica se o DataFrame foi carregado
    if "df" not in st.session_state:
        st.warning("Por favor, faça o upload do arquivo na página de Upload de Dados.")
        return

    df = st.session_state["df"]

    # Converte a coluna 'Mes' para datetime se necessário
    if not pd.api.types.is_datetime64_any_dtype(df['Mes']):
        df['Mes'] = pd.to_datetime(df['Mes'], errors='coerce')

    # Obtenção dos meses disponíveis no formato adequado
    meses_disponiveis = df["Mes"].dt.strftime('%Y-%m').unique()

    # Mapeia CNPJs para Empresas, criando uma lista de empresas únicas com seus respectivos CNPJs
    empresas_cnpjs = df[["CNPJ", "Empresa"]].drop_duplicates().set_index("Empresa")["CNPJ"].to_dict()

    # Seleção de Mês e Empresa
    mes = st.selectbox("Selecione o Mês", options=meses_disponiveis)
    empresa = st.selectbox("Selecione a Empresa", options=empresas_cnpjs.keys())

    # Obtenção do CNPJ com base na empresa selecionada
    cnpj = empresas_cnpjs[empresa]

    # Filtragem dos dados
    df_filtrado = filtrar_dados(df, mes, cnpj)
    st.session_state["df_filtrado"] = df_filtrado
    st.write(f"Dados filtrados para o mês {mes} e Empresa {empresa}:")
    st.dataframe(df_filtrado)

    # Atualiza o DataFrame completo com a nova consolidação
    st.session_state["df_completo"] = pd.concat([st.session_state["df_completo"], df_filtrado]).drop_duplicates()

    # Construção do Balanço Patrimonial
    contas_ativo = construir_contas(hierarquia_contas["1"]["subcategorias"])
    contas_passivo = construir_contas(hierarquia_contas["2"]["subcategorias"])
    balanco = BalancoPatrimonial()

    # Adiciona as contas ao balanço
    for conta in contas_ativo:
        balanco.adicionar_conta_ativo(conta)
    for conta in contas_passivo:
        balanco.adicionar_conta_passivo(conta)

    # Registra os valores no balanço patrimonial
    balanco = registrar_valores(df_filtrado, balanco, encontrar_conta_por_codigo)
    st.session_state["balanco"] = balanco

    # Gera o nome padrão da consolidação como EMPRESA_MES
    nome_consolidacao = f"{empresa}_{mes}"

    # Botão para consolidar os dados
    if st.button("Consolidar Dados"):
        if nome_consolidacao in st.session_state["consolidados"]:
            st.error(f"Os dados já foram consolidados para {nome_consolidacao}.")
        else:
            st.session_state["consolidados"][nome_consolidacao] = balanco
            st.success(f"Dados consolidados com o nome: {nome_consolidacao}")
