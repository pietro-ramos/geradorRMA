from entidades.GrupoContas import GrupoContas


class BalancoPatrimonial:
    """
    Representa o balanço patrimonial com ativo e passivo.
    """

    def __init__(self):
        """
        Inicializa o balanço patrimonial com grupos de contas.
        """
        self.ativo = GrupoContas("Ativo")
        self.passivo = GrupoContas("Passivo")

    def adicionar_conta_ativo(self, conta):
        """
        Adiciona uma conta ao grupo de Ativo.
        """
        self.ativo.adicionar_conta(conta)

    def adicionar_conta_passivo(self, conta):
        """
        Adiciona uma conta ao grupo de Passivo.
        """
        self.passivo.adicionar_conta(conta)

    def calcular_balanco_total(self):
        """
        Calcula o valor total de Ativo, Passivo e Patrimônio Líquido.
        """
        total_ativo = self.ativo.calcular_valor_total()
        total_passivo = self.passivo.calcular_valor_total()
        return total_ativo, total_passivo

    def validar_balanco(self):
        """
        Valida se todos os valores das contas no balanço são positivos.
        """
        self.ativo.validar_valores()
        self.passivo.validar_valores()

def print_balanco(balanco):
    def imprimir_contas(grupo_contas, nivel=0):
        for conta in grupo_contas:
            indentacao = '  ' * nivel
            print(f"{indentacao}{conta.nome} (Código: {conta.codigo}) - Valor: {conta.calcular_valor_total()}")
            if conta.subcontas:
                imprimir_contas(conta.subcontas, nivel + 1)

    print("Ativo:")
    imprimir_contas(balanco.ativo.contas)

    print("\nPassivo:")
    imprimir_contas(balanco.passivo.contas)
