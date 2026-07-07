#!/usr/bin/env python3
"""Resumo diario da conta + score de risco (deterministico nos sinais, resumo via LLM)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.llm import gerar

def analisar(contexto: dict) -> dict:
    sinais = contexto.get("sinais", {})
    risco, motivos = 0, []
    if sinais.get("pagamento") == "falha":
        risco += 40; motivos.append("pagamento falhou")
    nps = sinais.get("nps")
    if nps is not None and nps <= 6:
        risco += 25; motivos.append(f"NPS {nps}")
    if (sinais.get("ultima_interacao_dias") or 0) >= 3:
        risco += 20; motivos.append("silencio no grupo")
    if sinais.get("tipo_pagamento") == "parcelado":
        risco += 15; motivos.append("pagador parcelado (recebivel em risco)")
    risco = min(100, risco)
    n = len(contexto.get("mensagens", []))
    resumo = gerar(f"Resuma a conta {contexto.get('cliente_id')} em 2 linhas. {n} mensagens hoje. Sinais: {motivos}")
    return {"resumo": resumo, "risco_score": risco, "sinais_risco": motivos}
