"""
Modelos de dados da aplicação.

Define as estruturas de dados utilizadas para representar
contatos e resultados de envio.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Contato:
    """Representa um contato do banco de dados."""
    
    id: str
    nome: str
    telefone: str
    
    def __post_init__(self):
        """Valida e normaliza os dados do contato."""
        # Remove espaços extras do nome
        self.nome = self.nome.strip()
        
        # Normaliza telefone (remove tudo que não é número)
        self.telefone = "".join(c for c in self.telefone if c.isdigit())
    
    @property
    def telefone_valido(self) -> bool:
        """
        Verifica se o telefone está no formato válido.
        
        Formato esperado: DDI + DDD + número (ex: 5511999999999)
        Mínimo 12 dígitos (DDI 2 + DDD 2 + número 8)
        Máximo 13 dígitos (DDI 2 + DDD 2 + número 9)
        """
        return 12 <= len(self.telefone) <= 13
    
    def gerar_mensagem(self) -> str:
        """Gera a mensagem personalizada para o contato."""
        return f"Olá, {self.nome} tudo bem com você?"


@dataclass
class ResultadoEnvio:
    """Representa o resultado de um envio de mensagem."""
    
    contato: Contato
    sucesso: bool
    mensagem_id: Optional[str] = None
    erro: Optional[str] = None
