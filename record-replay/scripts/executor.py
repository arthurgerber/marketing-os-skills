#!/usr/bin/env python3
"""Camada de EXECUCAO. Navega nas conversas e simula mensagens junto com o humano.
Trava dura: NADA e executado sem aprovacao humana explicita."""

class EnvioBloqueado(Exception):
    """Disparada quando se tenta executar sem aprovacao humana."""

def preparar_acao(tipo: str, alvo: str, conteudo: str) -> dict:
    """Monta a acao (navegar/rascunhar/simular) mas NAO envia."""
    return {"tipo": tipo, "alvo": alvo, "conteudo": conteudo,
            "requer_aprovacao_humana": True, "executado": False}

def executar_com_aprovacao(acao: dict, aprovado_por_humano: bool) -> dict:
    if not aprovado_por_humano:
        raise EnvioBloqueado("acao requer aprovacao humana explicita")
    # INTEGRACAO: automacao de UI (computer-use / navegador) executa aqui, ritmo humano.
    acao = dict(acao); acao["executado"] = True
    return acao
