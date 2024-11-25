import streamlit as st

from contabilidade.indicadores import calcular_todos_indicadores
from contabilidade.util import montar_df_plano_contas, calcular_variacoes


def pagina_comparacao_variacoes():
    st.header("Comparação de Variações")
    if "consolidados" not in st.session_state or len(st.session_state["consolidados"]) < 2:
        st.warning("Consolide pelo menos dois planos de contas para realizar a comparação.")
        return

    subpaginas = ["Comparar Planos de Contas", "Comparar Variações e Valores Principais", "Comparar Indicadores"]
    subpagina_escolhida = st.selectbox("Escolha a Subpágina de Comparação", subpaginas)

    planos = list(st.session_state["consolidados"].keys())
    plano_1 = st.selectbox("Selecione o Primeiro Plano", options=planos, key="plano_1")
    plano_2 = st.selectbox("Selecione o Segundo Plano", options=[p for p in planos if p != plano_1], key="plano_2")

    balanco_1 = st.session_state["consolidados"][plano_1]
    balanco_2 = st.session_state["consolidados"][plano_2]

    if subpagina_escolhida == "Comparar Planos de Contas":
        comparar_planos_contas(balanco_1, balanco_2, plano_1, plano_2)

    elif subpagina_escolhida == "Comparar Variações e Valores Principais":
        comparar_variacoes_valores_principais(balanco_1, balanco_2, plano_1, plano_2)

    elif subpagina_escolhida == "Comparar Indicadores":
        comparar_indicadores(balanco_1, balanco_2, plano_1, plano_2)


def comparar_planos_contas(balanco_1, balanco_2, plano_1, plano_2):
    st.subheader(f"Plano de Contas - {plano_1}")

    # Obter o DataFrame filtrado da sessão de estado
    df_filtrado_1 = st.session_state["df_filtrado"]
    df_plano_1 = montar_df_plano_contas(balanco_1, df_filtrado_1)

    # Exibir apenas as contas com valores diferentes de zero
    df_visualizacao_1 = df_plano_1[df_plano_1['Valor'] != 0]
    st.dataframe(df_visualizacao_1)

    st.subheader(f"Plano de Contas - {plano_2}")

    # Obter o DataFrame filtrado para o segundo balanço
    df_filtrado_2 = st.session_state["df_filtrado"]
    df_plano_2 = montar_df_plano_contas(balanco_2, df_filtrado_2)

    # Exibir apenas as contas com valores diferentes de zero
    df_visualizacao_2 = df_plano_2[df_plano_2['Valor'] != 0]
    st.dataframe(df_visualizacao_2)


def comparar_variacoes_valores_principais(balanco_1, balanco_2, plano_1, plano_2):
    st.subheader("Variações entre os Planos de Contas")

    df_filtrado_1 = st.session_state["df_filtrado"]
    df_filtrado_2 = st.session_state["df_filtrado"]

    df_variacoes = calcular_variacoes(balanco_1, balanco_2, plano_1, plano_2)

    # Filtrar variações onde ambos os valores não são zero ou nulos
    df_variacoes_visualizacao = df_variacoes[
        (df_variacoes[f'Valor ({plano_1})'] != 0) | (df_variacoes[f'Valor ({plano_2})'] != 0)
    ]
    st.dataframe(df_variacoes_visualizacao)

    # Exibir a comparação dos valores totais de Ativo e Passivo
    total_ativo_1, total_passivo_1 = balanco_1.calcular_balanco_total()
    total_ativo_2, total_passivo_2 = balanco_2.calcular_balanco_total()

    st.write(f"**Ativo Total ({plano_1}):** {total_ativo_1}")
    st.write(f"**Ativo Total ({plano_2}):** {total_ativo_2}")
    st.write(f"**Variação Absoluta Ativo Total:** {total_ativo_2 - total_ativo_1}")
    st.write(f"**Variação Percentual Ativo Total (%):** {((total_ativo_2 - total_ativo_1) / total_ativo_1) * 100:.2f}%")

    st.write(f"**Passivo Total ({plano_1}):** {total_passivo_1}")
    st.write(f"**Passivo Total ({plano_2}):** {total_passivo_2}")
    st.write(f"**Variação Absoluta Passivo Total:** {total_passivo_2 - total_passivo_1}")
    st.write(f"**Variação Percentual Passivo Total (%):** {((total_passivo_2 - total_passivo_1) / total_passivo_1) * 100:.2f}%")



def comparar_indicadores(balanco_1, balanco_2, plano_1, plano_2):
    st.subheader("Comparação de Indicadores")
    indicadores_1 = calcular_todos_indicadores(balanco_1)
    indicadores_2 = calcular_todos_indicadores(balanco_2)

    # Exibe indicadores para ambos os planos
    st.write(f"**Indicadores - {plano_1}**")
    st.dataframe(indicadores_1)

    st.write(f"**Indicadores - {plano_2}**")
    st.dataframe(indicadores_2)

    # Calcula e exibe as variações de indicadores
    indicadores_variacoes = indicadores_2 - indicadores_1
    indicadores_variacoes_percentuais = ((indicadores_2 - indicadores_1) / indicadores_1.replace(0, float("nan"))) * 100

    st.write("**Variação Absoluta dos Indicadores:**")
    st.dataframe(indicadores_variacoes)

    st.write("**Variação Percentual dos Indicadores (%):**")
    st.dataframe(indicadores_variacoes_percentuais.round(2))
