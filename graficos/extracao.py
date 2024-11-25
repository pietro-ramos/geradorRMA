from contabilidade.util import encontrar_conta_por_codigo
import pandas as pd


def extrair_contas_para_modelo(balanco, df_filtrado, modelo):
    """
    Extrai contas e valores do balanço patrimonial de acordo com o modelo especificado.

    :param balanco: Objeto BalancoPatrimonial.
    :param df_filtrado: DataFrame filtrado para a competência e empresa selecionadas.
    :param modelo: Dicionário contendo as contas e indicadores a serem extraídos.
    :return: DataFrame com as contas e valores extraídos de acordo com o modelo.
    """
    dados = []
    for conta_config in modelo.get("contas", []):
        codigo = conta_config["codigo"]
        nome = conta_config["nome"]

        conta = encontrar_conta_por_codigo(balanco.ativo.contas, codigo) or \
                encontrar_conta_por_codigo(balanco.passivo.contas, codigo)

        if conta:
            valor = conta.calcular_valor_total()
            linha = {
                "Código": codigo,
                "Nome": nome,
                "Valor": valor,
                "Mes": df_filtrado["Mes"].iloc[0],
                "Empresa": df_filtrado["Empresa"].iloc[0]
            }
            dados.append(linha)

    # Constrói DataFrame com os dados extraídos
    df_contas_extracao = pd.DataFrame(dados)
    return df_contas_extracao


def extrair_indicadores_para_modelo(balanco, modelo):
    """
    Calcula indicadores financeiros com base no modelo especificado.

    :param balanco: Objeto BalancoPatrimonial.
    :param modelo: Dicionário contendo os indicadores a serem calculados.
    :return: DataFrame com os indicadores calculados de acordo com o modelo.
    """
    indicadores = []
    for indicador_config in modelo.get("indicadores", []):
        nome = indicador_config["nome"]
        funcao_calculo = globals()[indicador_config["funcao_calculo"]]  # Pega a função globalmente pelo nome

        valor_indicador = funcao_calculo(balanco)
        indicadores.append({"Indicador": nome, "Valor": valor_indicador})

    df_indicadores = pd.DataFrame(indicadores)
    return df_indicadores
