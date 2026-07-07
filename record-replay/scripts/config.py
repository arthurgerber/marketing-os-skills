#!/usr/bin/env python3
"""Configuracao central do Espelho. Paths via env/Path.home(), nunca hardcoded."""
import os
from pathlib import Path

BASE = Path(os.environ.get("RECORD_REPLAY_BASE", str(Path.home() / "Downloads" / "Marketing_OS" / "record_replay")))
CLIENTES_DIR = BASE / "clientes"     # 1 pasta por cliente (efemera, do dia)
JOGADAS_DIR  = BASE / "jogadas"      # biblioteca de jogadas humanas (curada)
ESTADO_DIR   = BASE / "estado"       # dedup de alertas, timestamps

# Limiares (ajustaveis)
STALE_HORAS      = 18   # dado mais velho que isso => avisar antes de agir
DEDUP_HORAS      = 24   # 1 alerta por evento por cliente nesse intervalo
CONFIANCA_MIN    = 0.60 # abaixo disso, pedir escolha humana da jogada
SILENCIO_DIAS    = 3    # silencio no grupo dispara alerta
NPS_ALERTA       = 6    # NPS <= isso dispara alerta
TETO_ALERTAS_DIA = 15   # teto de alertas por gerente/dia (evita fadiga)

for d in (CLIENTES_DIR, JOGADAS_DIR, ESTADO_DIR):
    d.mkdir(parents=True, exist_ok=True)
