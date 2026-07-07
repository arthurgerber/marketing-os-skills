#!/usr/bin/env python3
"""Camada de OBSERVACAO. Grava o que a pessoa ve e faz para virar jogada (RECORD).
Fontes: export de conversa, tela (screenshot/OCR), DOM do navegador, arvore de acessibilidade.
Stub com a interface pronta — a captura real pluga computer-use / navegador."""
from datetime import datetime, timezone

FONTES = ("conversa", "tela", "dom", "acessibilidade")

def capturar(fonte: str = "conversa", payload=None) -> dict:
    if fonte not in FONTES:
        raise ValueError(f"fonte invalida: {fonte}")
    # INTEGRACAO: aqui entra screenshot/OCR, DOM ou export. Stub retorna estrutura.
    return {"fonte": fonte, "capturado_em": datetime.now(timezone.utc).isoformat(),
            "eventos": payload or []}

def gravar_sessao_humana(cliente_id: str, eventos: list) -> dict:
    """RECORD: registra a sequencia de acoes do humano (cliques, mensagens, telas)."""
    return {"cliente_id": str(cliente_id), "n_eventos": len(eventos or []), "eventos": eventos or []}
