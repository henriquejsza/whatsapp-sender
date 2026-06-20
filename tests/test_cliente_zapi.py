import unittest
from unittest.mock import Mock

from aplicacao.cliente_zapi import ClienteZAPI
from aplicacao.configuracao import ConfiguracaoZAPI
from aplicacao.modelos import Contato


class ClienteZAPITestCase(unittest.TestCase):
    def test_aceita_message_id_da_resposta_atual(self):
        cliente = ClienteZAPI(
            ConfiguracaoZAPI(
                instancia_id="instancia",
                token="token",
                client_token="client-token",
            )
        )
        resposta = Mock(status_code=200)
        resposta.json.return_value = {
            "zaapId": "zaap-id",
            "messageId": "message-id",
            "id": "message-id",
        }
        cliente._cliente.post = Mock(return_value=resposta)

        try:
            resultado = cliente.enviar_mensagem(
                Contato(id="1", nome="Henrique", telefone="556284085315")
            )
        finally:
            cliente.fechar()

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.mensagem_id, "message-id")


if __name__ == "__main__":
    unittest.main()
