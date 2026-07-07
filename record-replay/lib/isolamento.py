#!/usr/bin/env python3
"""Isolamento por cliente: um cliente = um namespace. Barra vazamento entre contas."""
from datetime import datetime, timezone

class VazamentoDeContexto(Exception):
    """Disparada quando aparece dado de outra conta no contexto de um cliente."""

def carregar_contexto(cliente_id: str) -> dict:
    if not cliente_id or not str(cliente_id).strip():
        raise ValueError("cliente_id vazio")
    return {"cliente_id": str(cliente_id), "carregado_em": datetime.now(timezone.utc).isoformat(),
            "mensagens": [], "sinais": {}}

def checar_vazamento(contexto: dict, cliente_id: str) -> None:
    """Garante que nada no contexto pertence a outro cliente. Falha fechado."""
    alvo = str(cliente_id)
    if contexto.get("cliente_id") != alvo:
        raise VazamentoDeContexto(f"contexto e do cliente {contexto.get('cliente_id')}, esperado {alvo}")
    for msg in contexto.get("mensagens", []):
        dono = msg.get("cliente_id", alvo)
        if str(dono) != alvo:
            raise VazamentoDeContexto(f"mensagem de outra conta ({dono}) no contexto de {alvo}")

def esta_desatualizado(carimbo_iso: str, stale_horas: int) -> bool:
    try:
        t = datetime.fromisoformat(carimbo_iso)
    except (ValueError, TypeError):
        return True
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - t
    return delta.total_seconds() > stale_horas * 3600
