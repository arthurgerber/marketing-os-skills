---
name: record-replay
description: >
  Plataforma que OBSERVA o humano trabalhando (conversas, telas, cliques), APRENDE o padrao
  e REPLICA o trabalho junto com a pessoa — sem enviar nada sozinho. Serve qualquer empresa e
  modelo (CS, vendas, suporte, operacoes), nao so gerentes de conta. Acione SEMPRE que o pedido
  envolver: automatizar atendimento, rascunhar/simular mensagens, resumir contas, detectar risco
  de churn/reembolso, replicar o que um bom operador faz, ou escalar um trabalho repetitivo com IA.
  Isolamento de dados por cliente; aprendizado por padrao anonimizado (compartilhado).
---

# Record & Replay — plataforma de observar, aprender e replicar

Comeca no CS (primeiro caso de uso), mas a arquitetura e agnostica: qualquer trabalho onde um
humano opera em conversas/telas de forma repetitiva. **Record** grava o humano bom; **Replay**
repete a jogada certa — com o humano sempre no controle do envio.

## O que ela acessa (deixar liberado conforme o caso)
"Tudo que a pessoa ve", com consentimento e escopo: export de conversas, tela (screenshot/OCR),
DOM do navegador, arvore de acessibilidade, CRM/NPS/pagamento. Ver `agents/observador.md`.

## Organizacao (NAO travada em 6 agentes)
Um `registro` dinamico (`scripts/registro.py`) permite plugar quantos subagentes quiser sem
reescrever o orquestrador. Para escala (100–1000+ clientes), roda como frota: uma fila alimenta
workers que pegam contas por prioridade de risco (`scripts/batch.py`).

| Papel | Modulo | Funcao |
|---|---|---|
| Orquestrador | `scripts/orquestrador.py` | Pipeline por cliente + travas. |
| Observador | `scripts/observador.py` | RECORD: grava conversa/tela/cliques. |
| Ingestor | `scripts/ingestor.py` | Normaliza historico + sinais; isola por cliente. |
| Analista | `scripts/analista.py` | Resumo + score de risco. |
| Gatilhos | `scripts/gatilhos.py` | Alertas por evento (dedup, prioriza parcelado). |
| Redator | `scripts/redator.py` | REPLAY: rascunha no tom das jogadas. |
| Executor | `scripts/executor.py` | Navega e simula mensagem — so envia com aprovacao humana. |
| Curador | `scripts/curador.py` | Aprende: edicao humana -> jogada (sem PII). |
| Batch | `scripts/batch.py` | Segundo plano: fila por risco, sem interromper ninguem. |
| Registro | `scripts/registro.py` | Pluga novos subagentes dinamicamente. |
| Agente QA | `agents/qa.md` | Barreira de qualidade automatica. |
| Agente Dev | `agents/dev.md` | Evolui a plataforma sem quebrar. |

## Isolamento NAO trava o aprendizado
Isolamento de DADOS (nao misturar a conversa do cliente A no contexto do B) e diferente de
isolamento de APRENDIZADO. O Curador extrai o PADRAO anonimizado (PII removido) para a
biblioteca COMPARTILHADA — e assim que ele aprende com um e replica no outro.

## Modo segundo plano
`scripts/batch.py` roda agendado (cron) e monta `fila_de_trabalho.json` ordenada por risco.
A IA prepara em background; a pessoa abre quando quiser e ataca do pior ao melhor.

## Como usar / testar
```
python scripts/orquestrador.py --cliente <id> --export <export.txt>   # 1 cliente
python scripts/batch.py --raiz <pasta_com_1_subpasta_por_cliente>     # frota
python scripts/smoke_test.py                                          # 10 checagens
```

## Integracoes para producao
1. `llm.py::_provedor` -> Claude (Agent SDK/API).
2. `ingestor.py::puxar_sinais` -> CRM (pagamento, NPS, contrato).
3. `observador.py::capturar` -> screenshot/OCR/DOM (computer-use/navegador).
4. `executor.py` -> automacao de UI (envio sempre humano).
5. Export diario do WhatsApp por cliente.

## Regras de seguranca
Ver `references/regras.md` e `agents/*`: isolamento de dados; humano envia; nunca inventar
preco/prazo; PII removido antes de guardar jogada; consentimento/escopo/LGPD na observacao.

## Rollout em dias (nao meses)
Dia 1: ligar observacao em modo leitura e comecar a gravar o humano. Dia 2–3: montar a 1a
biblioteca de jogadas e ligar o rascunho (Replay) com envio humano. Dia 3–5: gatilhos + batch
em segundo plano numa leva, com o Agente QA rodando. O resultado (queda de churn) se mede nas
semanas seguintes — mas o ship e em dias, nao se espera para lancar.

## Handoff / evolucao
Pode virar projeto/plataforma independente e depois plugar num sistema maior: cada camada e
modular (registro de agentes), com QA e Dev embutidos para auto-melhoria.
