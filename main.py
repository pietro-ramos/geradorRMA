import pandas as pd

from entidades.BalancoPatrimonial import BalancoPatrimonial, print_balanco
from contabilidade.util import construir_contas, encontrar_conta_por_codigo, importar_dados_excel, registrar_valores, \
    filtrar_dados
from contabilidade.hierarquia_contas import hierarquia_contas
from contabilidade.indicadores import calcular_todos_indicadores
from graficos.graficos import grafico_indicadores


def main():
    # Caminho do arquivo Excel
    caminho_arquivo = 'data/input_test2.xlsx'

    # Importar dados do Excel
    df = importar_dados_excel(caminho_arquivo)

    # Verificando se o DataFrame foi importado corretamente
    print("Dados importados do Excel:")
    print(df.head())

    # Filtros de exemplo (ajustando o formato para string)
    mes = '2024-05'  # Formato compatível com o que estamos convertendo na função de filtro
    cnpj = '00.369.161/0001-57'  # Garantir que o CNPJ está no formato string

    # Filtrar dados com base no mês e no CNPJ
    df_filtrado = filtrar_dados(df, mes, cnpj)
    print(f"Dados filtrados para o mês {mes} e CNPJ {cnpj}:")
    print(df_filtrado)

    # Construir a hierarquia de contas a partir da configuração
    contas_ativo = construir_contas(hierarquia_contas["1"]["subcategorias"])
    contas_passivo = construir_contas(hierarquia_contas["2"]["subcategorias"])

    # Criar o balanço patrimonial
    balanco = BalancoPatrimonial()

    # Adicionar as contas ao balanço
    for conta in contas_ativo:
        balanco.adicionar_conta_ativo(conta)
    for conta in contas_passivo:
        balanco.adicionar_conta_passivo(conta)

    # Registrar os valores no balanço patrimonial com base nos dados filtrados
    balanco = registrar_valores(df_filtrado, balanco, encontrar_conta_por_codigo)

    # Validar e exibir o balanço total
    try:
        balanco.validar_balanco()
        total_ativo, total_passivo = balanco.calcular_balanco_total()
        print(f"Total Ativo: {total_ativo}")
        print(f"Total Passivo: {total_passivo}")
    except ValueError as e:
        print(f"Erro na validação do balanço: {e}")

    # Calcular todos os indicadores financeiros
    indicadores = calcular_todos_indicadores(balanco)
    print("Indicadores Financeiros Calculados:")
    pd.set_option('display.max_columns', None)
    print(indicadores)

    # Gerar gráficos para os indicadores financeiros
    grafico_indicadores(indicadores)


if __name__ == "__main__":
    main()
