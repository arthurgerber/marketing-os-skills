#!/usr/bin/env python3
"""Orquestrador do Espelho (por cliente). Pipeline: ingestao -> analise -> gatilhos -> rascunho.
Humano no controle: NADA e enviado automaticamente. Isolamento por cliente garantido."""
import argparse, json, logging, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.config as cfg
from lib.isolamento import checar_vazamento, esta_desatualizado
from lib.classificador import classificar
from scripts.ingestor import ingerir
from scripts.analista import analisar
from scripts.gatilhos import avaliar
from scripts.redator import rascunhar

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("espelho")

def rodar(cliente_id: str, export_path: str) -> dict:
    ctx = ingerir(cliente_id, export_path)
    checar_vazamento(ctx, cliente_id)                      # trava anti-vazamento
    desatualizado = esta_desatualizado(ctx.get("atualizado_em", ""), cfg.STALE_HORAS)
    analise = analisar(ctx)
    alertas = avaliar(cliente_id, ctx.get("sinais", {}), cfg)
    ultimo = ctx["mensagens"][-1]["texto"] if ctx["mensagens"] else ""
    tipo, conf = classificar(ultimo)
    rascunho = rascunhar(tipo, conf, ctx, cfg.JOGADAS_DIR, cfg)
    return {
        "cliente_id": cliente_id,
        "dado_desatualizado": desatualizado,
        "resumo": analise["resumo"],
        "risco_score": analise["risco_score"],
        "sinais_risco": analise["sinais_risco"],
        "alertas": alertas,
        "situacao": tipo,
        "rascunho": rascunho,
        "enviado_automaticamente": False,   # sempre humano
    }

def main():
    ap = argparse.ArgumentParser(description="Espelho — copiloto de CS por cliente")
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--export", required=True, help="caminho do export do WhatsApp")
    ap.add_argument("--saida", default=None)
    a = ap.parse_args()
    try:
        rel = rodar(a.cliente, a.export)
    except Exception as e:
        log.error(f"falhou: {e}")
        sys.exit(1)
    saida = a.saida or str(cfg.CLIENTES_DIR / f"{a.cliente}_relatorio.json")
    Path(saida).write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(f"relatorio salvo em {saida} | risco={rel['risco_score']} | alertas={len(rel['alertas'])}")

if __name__ == "__main__":
    main()
