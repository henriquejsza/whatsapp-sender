"""
Cliente para conexão com o Supabase.

Responsável por buscar contatos do banco de dados.
"""

import logging
from typing import List

from supabase import create_client, Client

from aplicacao.configuracao import ConfiguracaoSupabase
from aplicacao.modelos import Contato

logger = logging.getLogger(__name__)


class ClienteSupabase:
    """Cliente para interação com o Supabase."""
    
    def __init__(self, configuracao: ConfiguracaoSupabase):
        """
        Inicializa o cliente Supabase.
        
        Args:
            configuracao: Configurações de conexão com o Supabase.
        """
        self._cliente: Client = create_client(
            configuracao.url,
            configuracao.chave
        )
        logger.info("Cliente Supabase inicializado")
    
    def buscar_contatos(self, limite: int = 3) -> List[Contato]:
        """
        Busca contatos do banco de dados.
        
        Args:
            limite: Número máximo de contatos a retornar (padrão: 3).
            
        Returns:
            Lista de objetos Contato.
            
        Raises:
            Exception: Se houver erro na consulta.
        """
        logger.info(f"Buscando até {limite} contatos...")
        
        try:
            resposta = (
                self._cliente
                .table("contatos")
                .select("id, nome, telefone")
                .order("id")
                .limit(limite)
                .execute()
            )
            
            contatos = [
                Contato(
                    id=str(registro["id"]),
                    nome=registro["nome"],
                    telefone=registro["telefone"]
                )
                for registro in resposta.data
            ]
            
            logger.info(f"Encontrados {len(contatos)} contatos")
            return contatos
            
        except Exception as e:
            logger.error(f"Erro ao buscar contatos: {e}")
            raise
