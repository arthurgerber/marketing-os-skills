#!/usr/bin/env python3
"""Modo SEGUNDO PLANO: roda o pipeline para TODOS os clientes de uma vez (cron/agendado).
Nao interrompe ninguem — prepara uma fila de trabalho ordenada por risco que a gerente
abre quando quiser. A IA trabalha em background; a pessoa so consome o resultado."""
import argparse, json, logging, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.config as cfg
from scripts.orquestrador import rodar

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("record_replay.batch")

def descobrir_clientes(raiz: Path):
    """Cada subpasta = 1 cliente; espera um export.txt dentro."""
    for d in sorted(Path(raiz).glob("*")):
        if d.is_dir() and (d / "export.txt").exists():
            yield d.name, str(d / "export.txt")

def rodar_todos(raiz: Path) -> dict:
    fila, erros = [], []
    for cliente_id, export in descobrir_clientes(raiz):
        try:
            rel = rodar(cliente_id, export)
            fila.append({"cliente_id": cliente_id, "risco": rel["risco_score"],
                         "situacao": rel["situacao"], "alertas": rel["alertas"]})
        except Exception as e:
            erros.append({"cliente_id": cliente_id, "erro": str(e)})
            log.error(f"{cliente_id}: {e}")
    fila.sort(key=lambda x: x["risco"], reverse=True)   # pior primeiro
    saida = cfg.ESTADO_DIR / "fila_de_trabalho.json"
    saida.write_text(json.dumps({"fila": fila, "erros": erros}, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"processados": len(fila), "erros": len(erros), "fila": str(saida)}

def main():
    ap = argparse.ArgumentParser(description="Record & Replay — modo segundo plano (batch)")
    ap.add_argument("--raiz", default=str(cfg.CLIENTES_DIR), help="pasta com 1 subpasta por cliente")
    a = ap.parse_args()
    res = rodar_todos(Path(a.raiz))
    log.info(f"processados={res['processados']} erros={res['erros']} fila={res['fila']}")

if __name__ == "__main__":
    main()
