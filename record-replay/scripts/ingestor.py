#!/usr/bin/env python3
"""Ingestao diaria: le export do WhatsApp + sinais de CRM/NPS/pagamento, isola por cliente."""
import re
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.isolamento import carregar_contexto

_LINHA = re.compile(r"^\[?(?P<ts>[\d/.: ,-]+)\]?\s*[-]?\s*(?P<autor>[^:]{1,40}):\s*(?P<texto>.*)$")

def ler_export_whatsapp(caminho: str, cliente_id: str) -> list:
    msgs = []
    p = Path(caminho)
    if not p.exists():
        return msgs
    for linha in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = _LINHA.match(linha.strip())
        if m:
            msgs.append({"cliente_id": str(cliente_id), "ts": m.group("ts").strip(),
                         "autor": m.group("autor").strip(), "texto": m.group("texto").strip()})
    return msgs

def puxar_sinais(cliente_id: str) -> dict:
    # INTEGRACAO: puxar do CRM. Stub: estrutura esperada.
    return {"pagamento": "ok", "nps": None, "ultima_interacao_dias": 0,
            "tipo_pagamento": "a_vista", "dias_de_contrato": 0}

def ingerir(cliente_id: str, export_path: str) -> dict:
    ctx = carregar_contexto(cliente_id)
    ctx["mensagens"] = ler_export_whatsapp(export_path, cliente_id)
    ctx["sinais"] = puxar_sinais(cliente_id)
    ctx["atualizado_em"] = datetime.now(timezone.utc).isoformat()
    return ctx
