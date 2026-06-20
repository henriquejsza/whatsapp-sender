import unittest

from aplicacao.modelos import Contato


class ContatoTestCase(unittest.TestCase):
    def test_normaliza_telefone_e_nome(self):
        contato = Contato(id="1", nome="  Henrique  ", telefone="55 (62) 99164-9963")

        self.assertEqual(contato.nome, "Henrique")
        self.assertEqual(contato.telefone, "5562991649963")
        self.assertTrue(contato.telefone_valido)

    def test_gera_mensagem_exata(self):
        contato = Contato(id="1", nome="Henrique", telefone="5562991649963")

        self.assertEqual(contato.gerar_mensagem(), "Olá, Henrique tudo bem com você?")

    def test_rejeita_telefone_curto(self):
        contato = Contato(id="1", nome="Henrique", telefone="6299999999")

        self.assertFalse(contato.telefone_valido)


if __name__ == "__main__":
    unittest.main()
