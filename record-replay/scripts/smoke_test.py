#!/usr/bin/env python3
"""Smoke test: isolamento, classificador, dedup, gatilhos, pipeline e modo segundo plano."""
import os, sys, tempfile
from pathlib import Path
os.environ.setdefault("RECORD_REPLAY_BASE", tempfile.mkdtemp(prefix="rr_"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scripts.config as cfg
from lib.isolamento import carregar_contexto, checar_vazamento, VazamentoDeContexto
from lib.classificador import classificar
from lib.dedup import ja_alertado, registrar_alerta
from scripts.gatilhos import avaliar
from scripts.orquestrador import rodar
from scripts.batch import rodar_todos

ok = 0; fail = 0
def check(cond, nome):
    global ok, fail
    if cond: ok += 1; print(f"  ok  {nome}")
    else: fail += 1; print(f"  XX  {nome}")

ctx = carregar_contexto("A"); ctx["mensagens"] = [{"cliente_id": "B", "texto": "oi"}]
try:
    checar_vazamento(ctx, "A"); check(False, "isolamento deveria falhar")
except VazamentoDeContexto:
    check(True, "isolamento barra dado de outra conta")

t, c = classificar("Quero cancelar e pedir reembolso")
check(t == "reembolso" and c >= 0.7, "classificador detecta reembolso")

registrar_alerta(cfg.ESTADO_DIR, "A", "nps_baixo")
check(ja_alertado(cfg.ESTADO_DIR, "A", "nps_baixo", cfg.DEDUP_HORAS), "dedup registra alerta")

al = avaliar("Z", {"pagamento": "falha", "tipo_pagamento": "parcelado"}, cfg)
check(any(a["evento"] == "pagamento_falha" and a["prioridade"] == "alta" for a in al), "gatilho parcelado = alta")

exp = Path(cfg.BASE) / "wa.txt"
exp.write_text("[01/01 10:00] Cliente: Achei caro, nao sei se vale\n", encoding="utf-8")
rel = rodar("cliente_123", str(exp))
check(rel["enviado_automaticamente"] is False, "nada e enviado automaticamente")
check(rel["situacao"] in ("objecao", "check_in", "reembolso"), "pipeline classifica situacao")

# modo segundo plano: roda varias contas e ordena por risco (pior primeiro)
for cid in ("c_alto", "c_baixo"):
    d = Path(cfg.CLIENTES_DIR) / cid; d.mkdir(parents=True, exist_ok=True)
    (d / "export.txt").write_text("[01/01 10:00] Cliente: oi\n", encoding="utf-8")
res_b = rodar_todos(Path(cfg.CLIENTES_DIR))
check(res_b["processados"] >= 2, "batch (segundo plano) processa varias contas")

# 8 registro dinamico (org nao travada em 6)
from scripts.registro import registrar, obter, listar
registrar("teste", lambda x: x, "agente de teste")
check(obter("teste") is not None and "teste" in listar(), "registro dinamico de agentes")

# 9 executor bloqueia envio sem aprovacao humana
from scripts.executor import preparar_acao, executar_com_aprovacao, EnvioBloqueado
acao = preparar_acao("mensagem", "grupo_x", "ola")
try:
    executar_com_aprovacao(acao, aprovado_por_humano=False); check(False, "executor deveria bloquear")
except EnvioBloqueado:
    check(True, "executor bloqueia envio sem aprovacao humana")
check(executar_com_aprovacao(acao, True)["executado"] is True, "executor envia so com aprovacao")

print(f"\nRESULTADO: {ok} ok / {fail} falhas")
sys.exit(0 if fail == 0 else 1)
