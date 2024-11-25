import streamlit as st

from contabilidade.util import montar_df_plano_contas, encontrar_conta_por_codigo


def pagina_plano_contas():
    st.header("Plano de Contas")
    if "consolidados" not in st.session_state or len(st.session_state["consolidados"]) == 0:
        st.warning("Nenhum dado consolidado. Por favor, faça a filtragem e consolidação primeiro.")
        return

    planos = list(st.session_state["consolidados"].keys())
    plano_selecionado = st.selectbox("Selecione o Plano de Contas para Visualização", options=planos)

    balanco = st.session_state["consolidados"][plano_selecionado]

    # Obter o DataFrame filtrado da sessão de estado
    df_filtrado = st.session_state["df_filtrado"]

    df_plano_contas = montar_df_plano_contas(balanco, df_filtrado)

    # Filtrar para mostrar apenas contas com valores não zerados ou não nulos
    df_visualizacao = df_plano_contas[df_plano_contas['Valor'] != 0]

    st.write("Visualização do Plano de Contas (apenas contas com valores relevantes):")
    st.dataframe(df_visualizacao)

    # Exibição dos valores essenciais
    total_ativo, total_passivo = balanco.calcular_balanco_total()
    ativo_circulante = encontrar_conta_por_codigo(balanco.ativo.contas, '1.1').calcular_valor_total()
    ativo_nao_circulante = encontrar_conta_por_codigo(balanco.ativo.contas, '1.2').calcular_valor_total()
    passivo_circulante = encontrar_conta_por_codigo(balanco.passivo.contas, '2.1').calcular_valor_total()
    passivo_nao_circulante = encontrar_conta_por_codigo(balanco.passivo.contas, '2.2').calcular_valor_total()
    patrimonio_liquido = encontrar_conta_por_codigo(balanco.passivo.contas, '2.3').calcular_valor_total()

    st.subheader("Resumo dos Valores Essenciais")
    st.write(f"**Ativo Total:** {total_ativo}")
    st.write(f"**Passivo Total:** {total_passivo}")
    st.write(f"**Ativo Circulante:** {ativo_circulante}")
    st.write(f"**Ativo Não Circulante:** {ativo_nao_circulante}")
    st.write(f"**Passivo Circulante:** {passivo_circulante}")
    st.write(f"**Passivo Não Circulante:** {passivo_nao_circulante}")
    st.write(f"**Patrimônio Líquido:** {patrimonio_liquido}")

