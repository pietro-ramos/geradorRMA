import json
import os


def carregar_modelo_grafico(nome_modelo):
    """
    Carrega um modelo de gráfico a partir de um arquivo JSON.

    :param nome_modelo: Nome do modelo de gráfico.
    :return: Dicionário com as configurações do modelo.
    """
    # Caminho absoluto para a pasta de modelos
    caminho_pasta_modelos = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/modelos"))
    caminho_modelo = os.path.join(caminho_pasta_modelos, f"{nome_modelo}.json")

    if not os.path.exists(caminho_modelo):
        raise FileNotFoundError(f"Modelo de gráfico '{nome_modelo}' não encontrado em {caminho_modelo}.")

    with open(caminho_modelo, 'r', encoding='utf-8') as arquivo:
        modelo = json.load(arquivo)
    return modelo


def listar_modelos_disponiveis():
    """
    Lista todos os modelos de gráficos disponíveis na pasta de modelos.

    :return: Lista de nomes de modelos disponíveis.
    """
    # Caminho absoluto para a pasta de modelos
    caminho_pasta_modelos = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/modelos"))

    if not os.path.exists(caminho_pasta_modelos):
        raise FileNotFoundError(f"Pasta de modelos '{caminho_pasta_modelos}' não encontrada.")

    # Listar os arquivos JSON na pasta de modelos
    modelos = [arquivo.split(".json")[0] for arquivo in os.listdir(caminho_pasta_modelos) if arquivo.endswith(".json")]
    return modelos
