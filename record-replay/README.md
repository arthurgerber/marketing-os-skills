# Record & Replay — Copiloto de CS

Estado: **documentado e pronto**, com stubs de integracao. Nao envia mensagem sozinho.

## O que faz
Le o historico do WhatsApp (export diario), resume a conta, pontua risco, dispara
alertas proativos e rascunha respostas no tom das jogadas humanas — 1 cliente por vez.

## Estrutura
- `SKILL.md` — como acionar e operar.
- `scripts/` — orquestrador + subagentes + integracao (llm, pii).
- `lib/` — isolamento, classificador, dedup.
- `references/jogadas/` — biblioteca de jogadas humanas (semente; cresce com o uso).
- `references/regras.md` — regras de seguranca.

## Rodar o teste
```
python scripts/smoke_test.py
```

## Ligar em producao (3 integracoes)
1. `scripts/llm.py` -> chamada real ao Claude.
2. `scripts/ingestor.py::puxar_sinais` -> CRM.
3. Rotina diaria de export do WhatsApp por cliente.

## Ajustes rapidos
`scripts/config.py` — limiares (silencio, NPS, dedup, confianca minima, teto de alertas).
