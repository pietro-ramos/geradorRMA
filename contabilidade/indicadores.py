import pandas as pd
import unicodedata

from contabilidade.util import encontrar_conta_por_codigo


def obter_valores(balanco, codigo_categoria, nome_categoria):
    """
    Obtém o valor total para uma categoria específica na hierarquia.
    """
    # Encontra a conta pelo código
    conta_categoria = encontrar_conta_por_codigo(balanco.ativo.contas, codigo_categoria) or \
                      encontrar_conta_por_codigo(balanco.passivo.contas, codigo_categoria)

    if conta_categoria is None:
        raise ValueError(f"Não há dados para '{nome_categoria}' com o código '{codigo_categoria}'")

    if conta_categoria.nome != nome_categoria:
        raise ValueError(f"O nome da categoria '{nome_categoria}' não corresponde ao código '{codigo_categoria}'")

    valor_total = conta_categoria.valor

    # Soma os valores das subcategorias
    for subconta in conta_categoria.subcontas:
        valor_total += obter_valores_para_subconta(subconta, subconta.nome)

    return valor_total


def obter_valores_para_subconta(conta, nome_categoria):
    """
    Obtém o valor total para uma subconta.
    """
    valor_total = conta.valor

    # Soma os valores das subcategorias
    for subconta in conta.subcontas:
        valor_total += obter_valores_para_subconta(subconta, subconta.nome)

    return valor_total


def normalize_string(s):
    """
    Normaliza strings para remover acentos e caracteres especiais.
    """
    if s is None:
        return None
    if isinstance(s, float):
        s = str(s)
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')


def calcular_liquidez_corrente(balanco):
    """
    Calcula o indicador de Liquidez Corrente: Ativo Circulante / Passivo Circulante.
    """
    ativo_circulante = obter_valores(balanco, '1.1', 'Ativo Circulante')
    passivo_circulante = obter_valores(balanco, '2.1', 'Passivo Circulante')
    return ativo_circulante / passivo_circulante


def calcular_liquidez_geral(balanco):
    """
    Calcula o indicador de Liquidez Geral: (Ativo Circulante + Realizável a Longo Prazo) /
    (Passivo Circulante + Passivo Não Circulante).
    """
    ativo_circulante = obter_valores(balanco, '1.1', 'Ativo Circulante')
    realizavel_a_longo_prazo = obter_valores(balanco, '1.2.1', 'Ativo Realizável a Longo Prazo')
    passivo_circulante = obter_valores(balanco, '2.1', 'Passivo Circulante')
    passivo_nao_circulante = obter_valores(balanco, '2.2', 'Passivo Não Circulante')
    return (ativo_circulante + realizavel_a_longo_prazo) / (passivo_circulante + passivo_nao_circulante)


def calcular_grau_endividamento(balanco):
    """
    Calcula o Grau de Endividamento: (Passivo Circulante + Passivo Não Circulante) / Ativo Total.
    """
    passivo_circulante = obter_valores(balanco, '2.1', 'Passivo Circulante')
    passivo_nao_circulante = obter_valores(balanco, '2.2', 'Passivo Não Circulante')
    ativo_total = balanco.ativo.calcular_valor_total()
    return (passivo_circulante + passivo_nao_circulante) / ativo_total


def calcular_composicao_endividamento(balanco):
    """
    Calcula a Composição do Endividamento: Passivo Circulante / (Passivo Circulante + Passivo Não Circulante).
    """
    passivo_circulante = obter_valores(balanco, '2.1', 'Passivo Circulante')
    passivo_nao_circulante = obter_valores(balanco, '2.2', 'Passivo Não Circulante')
    return passivo_circulante / (passivo_circulante + passivo_nao_circulante)


def calcular_liquidez_seca(balanco):
    """
    Calcula o indicador de Liquidez Seca: (Ativo Circulante - (Estoques + Adiantamentos)) / Passivo Circulante.
    """
    ativo_circulante = obter_valores(balanco, '1.1', 'Ativo Circulante')
    estoques = obter_valores(balanco, '1.1.6', 'Estoques')
    adiantamentos = obter_valores(balanco, '1.1.5', 'Adiantamentos')
    passivo_circulante = obter_valores(balanco, '2.1', 'Passivo Circulante')
    return (ativo_circulante - (estoques + adiantamentos)) / passivo_circulante
def calcular_todos_indicadores(balanco):
    """
    Calcula todos os indicadores financeiros e retorna um DataFrame com os resultados.
    """
    balanco.calcular_balanco_total()
    indicadores = {
        'Liquidez Corrente': calcular_liquidez_corrente(balanco),
        'Liquidez Seca': calcular_liquidez_seca(balanco),
        'Liquidez Geral': calcular_liquidez_geral(balanco),
        'Grau de Endividamento': calcular_grau_endividamento(balanco),
        'Composição do Endividamento': calcular_composicao_endividamento(balanco)
    }

    return pd.DataFrame(indicadores, index=[0])
