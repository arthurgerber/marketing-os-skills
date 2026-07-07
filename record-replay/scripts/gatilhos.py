#!/usr/bin/env python3
"""Gatilhos por evento (proativo). Cruza o sinal antes de alertar (evita falso positivo)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.dedup import ja_alertado, registrar_alerta

def avaliar(cliente_id: str, sinais: dict, cfg, agora=None) -> list:
    alertas = []
    def add(evento, msg, prioridade):
        if not ja_alertado(cfg.ESTADO_DIR, cliente_id, evento, cfg.DEDUP_HORAS, agora):
            alertas.append({"evento": evento, "mensagem": msg, "prioridade": prioridade})
            registrar_alerta(cfg.ESTADO_DIR, cliente_id, evento, agora)

    parcelado = sinais.get("tipo_pagamento") == "parcelado"
    # pagamento: so alerta se for FALHA confirmada (nao atraso de sincronizacao)
    if sinais.get("pagamento") == "falha":
        add("pagamento_falha", "Pagamento falhou — risco de reembolso integral.",
            "alta" if parcelado else "media")
    nps = sinais.get("nps")
    if nps is not None and nps <= cfg.NPS_ALERTA:
        add("nps_baixo", f"NPS {nps} — contato de recuperacao.", "alta" if parcelado else "media")
    if (sinais.get("ultima_interacao_dias") or 0) >= cfg.SILENCIO_DIAS:
        add("silencio", "Conta silenciada — reativar contato.", "alta" if parcelado else "media")
    dias = sinais.get("dias_de_contrato") or 0
    for marco in (7, 30, 90):
        if dias == marco:
            add(f"marco_{marco}", f"Marco de {marco} dias — check-in de valor.", "media")
    # prioriza parcelado e corta pelo teto diario
    ordem = {"alta": 0, "media": 1, "baixa": 2}
    alertas.sort(key=lambda a: ordem.get(a["prioridade"], 9))
    return alertas[: cfg.TETO_ALERTAS_DIA]
