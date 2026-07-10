# PLATAFORMA COMERCIAL — Arquitetura Completa
**Versão:** 1.0 | **Data:** 2026-06-30  
**Referência:** Seven Comercial (Antonio Silva) → nossa versão vai além

---

## VISÃO GERAL

O Seven Comercial avalia transcrições de calls. Nossa plataforma avalia **tudo**:
- ✅ Transcrição (texto, estrutura, processo)
- ✅ Voz (WPM, pitch, nervosismo, energia, hesitação)
- ✅ Vídeo (linguagem corporal, micro-expressões, decisor oculto, temperatura do lead)
- ✅ Score por critério com justificativa
- ✅ Treinamento personalizado por closer (IA gera aula/vídeo para resolver o problema identificado)
- ✅ Multi-grupo: VR, Silva, Lazari (cada um com seu processo customizável)

---

## ARQUITETURA — 4 CAMADAS

```
┌─────────────────────────────────────────────────────────┐
│  CAMADA 1 — COLETA                                      │
│  Google Meet → Drive → Pasta "Analisar/"                │
│  (já funciona via script existente)                     │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  CAMADA 2 — PROCESSAMENTO (analisa-video)               │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────┐  │
│  │ Whisper      │ │ pyannote     │ │ ffmpeg         │  │
│  │ (transcrição)│ │ (speakers)   │ │ (400 frames)   │  │
│  └──────┬───────┘ └──────┬───────┘ └───────┬────────┘  │
│         └────────────────┴─────────────────┘           │
│                          ↓                             │
│         ┌─────────────────────────────────┐            │
│         │  4 Agentes Claude em paralelo   │            │
│         │  (análise visual + score)       │            │
│         └───────────────┬─────────────────┘            │
│                         ↓                              │
│              JSON estruturado completo                 │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  CAMADA 3 — BANCO DE DADOS                              │
│                                                         │
│  Recomendação: SUPABASE                                 │
│  → PostgreSQL gerenciado + Auth + Storage + REST API   │
│  → Tem dashboard próprio (consulta sem código)          │
│  → Escala até milhões de rows sem configuração          │
│  → Plano free até 500MB / 50K requests/mês             │
│                                                         │
│  Tabelas principais:                                    │
│  - calls (id, closer_id, lead_nome, grupo, data, url)  │
│  - analises (call_id, json_completo, score_total, ...)  │
│  - scores_criterios (call_id, criterio, nota, motivo)  │
│  - closers (id, nome, grupo, ativo)                    │
│  - treinamentos (closer_id, problema, aula_url, data)  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  CAMADA 4 — FRONTEND (Dashboard)                        │
│                                                         │
│  Stack: Next.js + Tailwind + Supabase client            │
│  Deploy: Vercel (gratuito, deploy contínuo automático)  │
│                                                         │
│  Páginas:                                               │
│  /login        → Google OAuth (restrito por domínio)   │
│  /dashboard    → métricas gerais, ranking closers       │
│  /calls        → lista de calls com filtros             │
│  /calls/[id]   → análise completa de uma call          │
│  /closers/[id] → histórico + evolução do closer        │
│  /treinamentos → aulas geradas por IA para cada closer  │
│  /grupos/[id]  → visão por grupo (VR/Silva/Lazari)     │
└─────────────────────────────────────────────────────────┘
```

---

## FLUXO COMPLETO — DO MEET AO DASHBOARD

```
[Closer fecha call no Google Meet]
    ↓ (automático)
[Drive salva gravação na pasta configurada]
    ↓ (LaunchAgent detecta novo arquivo)
[analisa-video dispara automaticamente]
    ├── Whisper: transcreve áudio completo
    ├── pyannote: identifica closer vs lead
    ├── ffmpeg: extrai 400 frames
    └── gera_composites.py: 400→20 composites
    ↓ (4 agentes Claude paralelos)
[Análise visual + score por critério + decisor oculto]
    ↓
[JSON completo → POST para Supabase API]
    ↓
[Dashboard atualiza em tempo real]
    ├── Ranking de closers atualizado
    ├── Score da call disponível
    └── Treinamento personalizado gerado
```

---

## DIFERENCIAL vs SEVEN COMERCIAL

| Funcionalidade | Seven Comercial | Nossa Plataforma |
|---|---|---|
| Transcrição | ✅ | ✅ |
| Score por critério | ✅ | ✅ (+ justificativa) |
| Ranking closers | ✅ | ✅ |
| Análise de voz | ❌ | ✅ (WPM, pitch, nervosismo) |
| Análise visual | ❌ | ✅ (400 frames, micro-expressões) |
| Decisor oculto | ❌ | ✅ |
| Temperatura do lead | ❌ | ✅ |
| Treinamento IA por closer | ❌ | ✅ |
| Multi-grupo | ❌ | ✅ (VR/Silva/Lazari) |
| Escala | manual | ✅ (300+ calls/dia automatizado) |

---

## EC2 SPOT — O QUE É E POR QUÊ USAR

**EC2 Spot = servidor AWS alugado "nos buracos de capacidade"**  
É 70-90% mais barato que servidor normal, mas pode ser desligado com 2 min de aviso.

Para processar calls, isso é perfeito:
- A call já foi gravada, não é tempo real
- Se o servidor cair no meio, recomeça do ponto que parou
- Custo: ~$0.03 por call de 60 min processada
- Para 300 calls/dia = ~$9/dia = ~$270/mês

Alternativa sem AWS: Mac Mini dedicado (~$600 uma vez, roda pra sempre)
- Arthur mencionou Mac Mini — para começar, é a melhor opção
- 1 Mac Mini roda ~50 calls/dia facilmente
- 2 Mac Minis = 100+ calls/dia
- Sem custo recorrente, sem configuração de cloud

**Recomendação:** começa com Mac Mini(s), migra pra EC2 quando escalar além.

---

## DATABASE — POR QUÊ SUPABASE

Opções analisadas:

| | Supabase | PostgreSQL próprio | Firebase |
|---|---|---|---|
| Setup | 5 min | 2-4h | 30 min |
| Custo inicial | Grátis | VPS ~$20/mês | Grátis |
| Dashboard | ✅ embutido | ❌ precisa instalar | ✅ |
| SQL real | ✅ | ✅ | ❌ NoSQL |
| Auth Google | ✅ nativo | manual | ✅ |
| Storage (arquivos) | ✅ | manual | ✅ |
| Escala | ✅ | ✅ | limitado |

**Supabase vence em todos os critérios para começar.** Migrar pra PostgreSQL próprio depois se necessário é fácil (é a mesma linguagem SQL).

---

## FRONTEND — CLONAR E MELHORAR vs DO ZERO

**Não faz sentido começar do zero.** O mercado já validou o padrão visual do Seven Comercial (dashboard lateral + cards + tabelas + gráficos de evolução). A estratégia correta é:

1. Pegar um template de dashboard aberto (ex: shadcn/ui dashboard, Tremor, Next.js + Vercel template)
2. Adaptar ao nosso design e dados
3. Adicionar as funcionalidades que o Seven não tem (análise de voz/vídeo, treinamentos IA)

Stack recomendada:
```
Next.js 14 (App Router)
Tailwind CSS
shadcn/ui (componentes prontos, bonitos, gratuitos)
Supabase JS client (conexão direta ao banco)
Recharts (gráficos de evolução)
Vercel (deploy contínuo — push no GitHub → vai pro ar automaticamente)
```

---

## TREINAMENTO IA POR CLOSER

Esta é a funcionalidade mais poderosa e que ninguém tem ainda:

```
[Análise identifica: Marcos não faz minipactos]
    ↓
[Agente de treinamento acessa:]
    ├── Curso de closer (videos internos)
    ├── Playbook do processo
    ├── Exemplos de calls com minipactos bem feitos
    └── PROCESSO_BASE_CLOSER.md
    ↓
[Gera:]
    ├── Aula em texto (script completo)
    ├── Exemplos de como deveria ter sido na call específica
    ├── Exercícios práticos
    └── (futuro) Vídeo narrado por IA com a aula
```

O agente não diz "precisa melhorar minipactos" — ele diz **exatamente como fazer**, com o exemplo da própria call do closer.

---

## ENFORCEMENT — OBRIGATÓRIO EM TODA A PLATAFORMA

Todo componente da plataforma segue o padrão:
- Agente não entrega sem checklist completo
- Output verificável (JSON com todos campos) ou falha visível
- watchdog monitora cada execução
- debugger acionado automaticamente em falha
- auto-qa antes de qualquer dado ir para o banco

---

## PRÓXIMOS PASSOS (ordem)

1. ✅ Arquitetura documentada (este arquivo)
2. ⏳ Criar projeto no Supabase + schema das tabelas
3. ⏳ Adaptar analisa-video para fazer POST ao Supabase após análise
4. ⏳ Template frontend Next.js + shadcn conectado ao Supabase
5. ⏳ Página de login (Google OAuth restrito por domínio)
6. ⏳ Dashboard básico funcionando com dados reais
7. ⏳ Página de análise de call individual
8. ⏳ Módulo de treinamentos IA

*Construção: Claude Code + devstack + agentes paralelos*  
*Deploy: GitHub → Vercel (automático a cada push)*
