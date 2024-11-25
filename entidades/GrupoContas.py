class GrupoContas:
    """
    Representa um grupo de contas.
    """

    def __init__(self, nome):
        """
        Inicializa um grupo de contas com um nome e uma lista de contas.
        """
        self.nome = nome
        self.contas = []

    def adicionar_conta(self, conta):
        """
        Adiciona uma conta ao grupo de contas.
        """
        self.contas.append(conta)

    def calcular_valor_total(self):
        """
        Calcula o valor total do grupo de contas.
        """
        total = 0.0
        for conta in self.contas:
            total += conta.calcular_valor_total()
        return total

    def validar_valores(self):
        """
        Valida se todos os valores das contas são positivos.
        """
        for conta in self.contas:
            conta.validar_valores()
