"""
Módulo de configuração da aplicação.

Carrega as variáveis de ambiente necessárias para conexão
com Supabase e Z-API.
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@dataclass
class ConfiguracaoSupabase:
    """Configurações de conexão com o Supabase."""
    
    url: str
    chave: str


@dataclass
class ConfiguracaoZAPI:
    """Configurações de conexão com a Z-API."""
    
    instancia_id: str
    token: str
    client_token: str
    
    @property
    def url_base(self) -> str:
        """Retorna a URL base para requisições."""
        return f"https://api.z-api.io/instances/{self.instancia_id}/token/{self.token}"


@dataclass
class Configuracao:
    """Configuração completa da aplicação."""
    
    supabase: ConfiguracaoSupabase
    zapi: ConfiguracaoZAPI


def carregar_configuracao() -> Configuracao:
    """
    Carrega a configuração a partir das variáveis de ambiente.
    
    Procura por um arquivo .env na raiz do projeto.
    
    Returns:
        Configuracao: Objeto com todas as configurações carregadas.
        
    Raises:
        ValueError: Se alguma variável obrigatória não estiver definida.
    """
    # Carrega .env da raiz do projeto
    caminho_env = Path(__file__).parent.parent / ".env"
    
    if caminho_env.exists():
        load_dotenv(caminho_env)
        logger.info("Arquivo .env carregado com sucesso")
    else:
        logger.warning("Arquivo .env não encontrado, usando variáveis do sistema")
    
    # Variáveis obrigatórias
    variaveis_obrigatorias = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "ZAPI_INSTANCE_ID",
        "ZAPI_TOKEN",
        "ZAPI_CLIENT_TOKEN",
    ]
    
    # Verifica se todas as variáveis estão definidas
    variaveis_faltando = [
        var for var in variaveis_obrigatorias 
        if not os.getenv(var)
    ]
    
    if variaveis_faltando:
        raise ValueError(
            f"Variáveis de ambiente obrigatórias não definidas: {', '.join(variaveis_faltando)}"
        )
    
    return Configuracao(
        supabase=ConfiguracaoSupabase(
            url=os.getenv("SUPABASE_URL"),
            chave=os.getenv("SUPABASE_KEY"),
        ),
        zapi=ConfiguracaoZAPI(
            instancia_id=os.getenv("ZAPI_INSTANCE_ID"),
            token=os.getenv("ZAPI_TOKEN"),
            client_token=os.getenv("ZAPI_CLIENT_TOKEN"),
        ),
    )
