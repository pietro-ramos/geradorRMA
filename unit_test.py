import unittest

from contabilidade.hierarquia_contas import hierarquia_contas
from contabilidade.util import construir_contas, encontrar_conta_por_nome
from entidades.BalancoPatrimonial import BalancoPatrimonial


class TestBalancoPatrimonial(unittest.TestCase):

    def setUp(self):
        self.balanco = BalancoPatrimonial()

        # Construir a hierarquia de contas a partir da configuração
        contas_ativo = construir_contas(hierarquia_contas["1"]["subcategorias"])
        contas_passivo = construir_contas(hierarquia_contas["2"]["subcategorias"])

        # Adicionar as contas ao balanço
        for conta in contas_ativo:
            self.balanco.adicionar_conta_ativo(conta)
        for conta in contas_passivo:
            self.balanco.adicionar_conta_passivo(conta)

    def test_validar_balanco(self):
        # Atualizando valores de algumas subcontas
        caixa = encontrar_conta_por_nome(self.balanco.ativo.contas, "Caixa")
        if caixa: caixa.atualizar_valor(1000.0)
        clientes_nacionais = encontrar_conta_por_nome(self.balanco.ativo.contas, "Clientes nacionais")
        if clientes_nacionais: clientes_nacionais.atualizar_valor(2000.0)
        fornecedores = encontrar_conta_por_nome(self.balanco.passivo.contas, "Fornecedores")
        if fornecedores: fornecedores.atualizar_valor(1500.0)
        depositos_judiciais = encontrar_conta_por_nome(self.balanco.ativo.contas, "Depósitos Judiciais")
        if depositos_judiciais: depositos_judiciais.atualizar_valor(3000.0)
        reserva_legal = encontrar_conta_por_nome(self.balanco.passivo.contas, "Reserva Legal")
        if reserva_legal: reserva_legal.atualizar_valor(12000.0)

        # Validando o balanço total
        try:
            self.balanco.validar_balanco()
            total_ativo, total_passivo = self.balanco.calcular_balanco_total()
            self.assertEqual(total_ativo, 6000.0)
            self.assertEqual(total_passivo, 13500.0)
        except ValueError as e:
            self.fail(f"Erro na validação do balanço: {e}")

if __name__ == '__main__':
    unittest.main()
