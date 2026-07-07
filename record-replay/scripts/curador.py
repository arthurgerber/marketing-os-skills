#!/usr/bin/env python3
"""Aprendizado: captura a edicao da gerente e faz a biblioteca crescer (remove PII)."""
from pathlib import Path
from datetime import datetime, timezone
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.pii import scrub

def registrar_edicao(jogadas_dir: Path, tipo: str, rascunho: str, enviado: str) -> bool:
    """Se o humano editou, guarda a versao enviada (sem PII) como nova jogada."""
    if not enviado or enviado.strip() == (rascunho or "").strip():
        return False
    f = Path(jogadas_dir) / f"{tipo}.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    entrada = f"\n\n## jogada capturada {datetime.now(timezone.utc).date()}\n{scrub(enviado).strip()}\n"
    with f.open("a", encoding="utf-8") as fh:
        fh.write(entrada)
    return True
