"""
Cliente para envio de mensagens via Z-API.

Responsável por enviar mensagens de texto pelo WhatsApp.
"""

import logging
from typing import Optional

import httpx

from aplicacao.configuracao import ConfiguracaoZAPI
from aplicacao.modelos import Contato, ResultadoEnvio

logger = logging.getLogger(__name__)


class ClienteZAPI:
    """Cliente para interação com a Z-API."""
    
    def __init__(self, configuracao: ConfiguracaoZAPI):
        """
        Inicializa o cliente Z-API.
        
        Args:
            configuracao: Configurações de conexão com a Z-API.
        """
        self._config = configuracao
        self._cliente = httpx.Client(timeout=30.0)
        logger.info("Cliente Z-API inicializado")
    
    def _obter_headers(self) -> dict:
        """Retorna os headers para requisições à API."""
        return {
            "Content-Type": "application/json",
            "Client-Token": self._config.client_token,
        }
    
    def enviar_mensagem(self, contato: Contato) -> ResultadoEnvio:
        """
        Envia uma mensagem de texto para um contato.
        
        Args:
            contato: O contato que receberá a mensagem.
            
        Returns:
            ResultadoEnvio com o status do envio.
        """
        if not contato.telefone_valido:
            logger.warning(f"Telefone inválido para {contato.nome}: {contato.telefone}")
            return ResultadoEnvio(
                contato=contato,
                sucesso=False,
                erro=f"Telefone inválido: {contato.telefone}"
            )
        
        mensagem = contato.gerar_mensagem()
        url = f"{self._config.url_base}/send-text"
        
        payload = {
            "phone": contato.telefone,
            "message": mensagem,
        }
        
        logger.info(f"Enviando mensagem para {contato.nome} ({contato.telefone})...")
        
        try:
            resposta = self._cliente.post(
                url,
                json=payload,
                headers=self._obter_headers(),
            )
            
            dados = resposta.json()
            mensagem_id = (
                dados.get("messageId")
                or dados.get("id")
                or dados.get("zapiMessageId")
                or dados.get("zaapId")
            )
            
            if resposta.status_code == 200 and mensagem_id:
                logger.info(f"Mensagem enviada com sucesso para {contato.nome} (ID: {mensagem_id})")
                return ResultadoEnvio(
                    contato=contato,
                    sucesso=True,
                    mensagem_id=mensagem_id,
                )
            else:
                erro = (
                    dados.get("error")
                    or dados.get("message")
                    or f"Resposta inesperada da Z-API (status {resposta.status_code})"
                )
                logger.error(f"Falha ao enviar para {contato.nome}: {erro}")
                return ResultadoEnvio(
                    contato=contato,
                    sucesso=False,
                    erro=erro,
                )
                
        except httpx.TimeoutException:
            erro = "Timeout na requisição"
            logger.error(f"Timeout ao enviar para {contato.nome}")
            return ResultadoEnvio(
                contato=contato,
                sucesso=False,
                erro=erro,
            )
        except httpx.RequestError as e:
            erro = f"Erro de conexão: {str(e)}"
            logger.error(f"Erro de conexão ao enviar para {contato.nome}: {e}")
            return ResultadoEnvio(
                contato=contato,
                sucesso=False,
                erro=erro,
            )
        except Exception as e:
            erro = f"Erro inesperado: {str(e)}"
            logger.error(f"Erro inesperado ao enviar para {contato.nome}: {e}")
            return ResultadoEnvio(
                contato=contato,
                sucesso=False,
                erro=erro,
            )
    
    def fechar(self):
        """Fecha o cliente HTTP."""
        self._cliente.close()
        logger.info("Cliente Z-API encerrado")
    
    def __enter__(self):
        """Suporte a context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha o cliente ao sair do context manager."""
        self.fechar()
