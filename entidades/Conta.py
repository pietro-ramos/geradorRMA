class Conta:
    """
    Representa uma conta no plano de contas.
    """

    def __init__(self, nome, valor=0.0, codigo=""):
        """
        Inicializa uma conta com nome, valor, código e lista de subcontas.
        """
        self.nome = nome
        self.valor = valor
        self.codigo = codigo
        self.subcontas = []

    def adicionar_subconta(self, subconta):
        """
        Adiciona uma subconta à lista de subcontas.
        """
        self.subcontas.append(subconta)

    def atualizar_valor(self, valor):
        """
        Atualiza o valor da conta.
        """
        self.valor += valor

    def calcular_valor_total(self):
        """
        Calcula o valor total da conta, incluindo o valor das subcontas.
        """
        total = self.valor
        for subconta in self.subcontas:
            total += subconta.calcular_valor_total()
        return total

    def validar_valores(self):
        """
        Valida se todos os valores das contas e suas subcontas são consistentes.
        """
        for conta in self.subcontas:
            conta.validar_valores()
            if conta.subcontas:
                total_subcontas = sum(subconta.calcular_valor_total() for subconta in conta.subcontas)
                if conta.valor < total_subcontas:
                    print("Necessario validaçao")
                    # raise ValueError(f"O valor da conta {conta.nome} é menor que o total das suas subcontas")

