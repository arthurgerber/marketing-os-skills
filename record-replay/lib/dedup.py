#!/usr/bin/env python3
"""Deduplicacao de alertas: 1 por evento por cliente por janela (evita fadiga)."""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

def _store(estado_dir: Path) -> Path:
    return Path(estado_dir) / "alertas.json"

def _load(estado_dir: Path) -> dict:
    p = _store(estado_dir)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
    return {}

def ja_alertado(estado_dir: Path, cliente_id: str, evento: str, dedup_horas: int, agora=None) -> bool:
    agora = agora or datetime.now(timezone.utc)
    dados = _load(estado_dir)
    chave = f"{cliente_id}:{evento}"
    ts = dados.get(chave)
    if not ts:
        return False
    try:
        t = datetime.fromisoformat(ts)
    except ValueError:
        return False
    return (agora - t) < timedelta(hours=dedup_horas)

def registrar_alerta(estado_dir: Path, cliente_id: str, evento: str, agora=None) -> None:
    agora = agora or datetime.now(timezone.utc)
    p = _store(estado_dir)
    dados = _load(estado_dir)
    dados[f"{cliente_id}:{evento}"] = agora.isoformat()
    p.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
