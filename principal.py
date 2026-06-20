"""
Script principal para envio de mensagens WhatsApp.

Lê contatos do Supabase e envia mensagens personalizadas via Z-API.
"""

import argparse
import logging
import sys
from typing import List

from aplicacao.configuracao import carregar_configuracao
from aplicacao.cliente_supabase import ClienteSupabase
from aplicacao.cliente_zapi import ClienteZAPI
from aplicacao.modelos import Contato, ResultadoEnvio

logger = logging.getLogger(__name__)

MAXIMO_CONTATOS = 3


def processar_contatos(
    contatos: List[Contato],
    cliente_zapi: ClienteZAPI,
    modo_teste: bool = False,
) -> List[ResultadoEnvio]:
    """
    Processa uma lista de contatos enviando mensagens.
    
    Args:
        contatos: Lista de contatos para enviar mensagens.
        cliente_zapi: Cliente Z-API configurado.
        modo_teste: Se True, não envia mensagens realmente.
        
    Returns:
        Lista de resultados de envio.
    """
    resultados = []
    
    for contato in contatos:
        if modo_teste:
            logger.info(f"[TESTE] Simulando envio para {contato.nome} ({contato.telefone})")
            logger.info(f"[TESTE] Mensagem: {contato.gerar_mensagem()}")
            resultado = ResultadoEnvio(
                contato=contato,
                sucesso=True,
                mensagem_id="TESTE-123",
            )
        else:
            resultado = cliente_zapi.enviar_mensagem(contato)
        
        resultados.append(resultado)
    
    return resultados


def exibir_resumo(resultados: List[ResultadoEnvio]):
    """Exibe um resumo dos resultados de envio."""
    total = len(resultados)
    sucesso = sum(1 for r in resultados if r.sucesso)
    falha = total - sucesso
    
    print("\n" + "=" * 50)
    print("RESUMO DO ENVIO")
    print("=" * 50)
    print(f"Total de contatos: {total}")
    print(f"Enviados com sucesso: {sucesso}")
    print(f"Falhas: {falha}")
    print("=" * 50)
    
    if falha > 0:
        print("\nDetalhes das falhas:")
        for resultado in resultados:
            if not resultado.sucesso:
                print(f"  - {resultado.contato.nome}: {resultado.erro}")
    
    print()


def main():
    """Função principal da aplicação."""
    parser = argparse.ArgumentParser(
        description="Envia mensagens WhatsApp para contatos do Supabase via Z-API"
    )
    parser.add_argument(
        "--teste",
        action="store_true",
        help="Executa em modo de teste (não envia mensagens realmente)",
    )
    parser.add_argument(
        "--limite",
        type=int,
        choices=range(1, MAXIMO_CONTATOS + 1),
        default=MAXIMO_CONTATOS,
        metavar="{1,2,3}",
        help="Número máximo de contatos a processar (1 a 3; padrão: 3)",
    )
    
    args = parser.parse_args()
    
    logger.info("Iniciando aplicação de envio de mensagens")
    
    if args.teste:
        logger.info("*** MODO DE TESTE ATIVADO - Mensagens não serão enviadas ***")
    
    try:
        # Carrega configuração
        config = carregar_configuracao()
        
        # Busca contatos do Supabase
        cliente_supabase = ClienteSupabase(config.supabase)
        contatos = cliente_supabase.buscar_contatos(limite=args.limite)
        
        if not contatos:
            logger.warning("Nenhum contato encontrado no banco de dados")
            print("Nenhum contato encontrado para enviar mensagens.")
            return 0
        
        logger.info(f"Encontrados {len(contatos)} contatos para processar")
        
        # Processa contatos
        with ClienteZAPI(config.zapi) as cliente_zapi:
            resultados = processar_contatos(
                contatos=contatos,
                cliente_zapi=cliente_zapi,
                modo_teste=args.teste,
            )
        
        # Exibe resumo
        exibir_resumo(resultados)
        
        # Retorna código de erro se houver falhas
        falhas = sum(1 for r in resultados if not r.sucesso)
        return 1 if falhas > 0 else 0
        
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        print(f"Erro: {e}")
        return 1
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
