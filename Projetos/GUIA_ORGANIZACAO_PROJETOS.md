# GUIA DE ORGANIZAÇÃO DE PROJETOS — Marketing OS
**Versão:** 1.1 | **Síntese de 9 respostas Claude (+ consolidação 2026-07-10)** | **Data:** 2026-07-06 (rev. 2026-07-10)
**Autor:** Arthur Gerber | **Owner:** Marketing OS

> Este guia é a fonte única de verdade sobre como organizar projetos, conversas, documentos e ferramentas no Marketing OS. Toda nova sessão deve ler este arquivo antes de criar qualquer coisa.

---

## PRINCÍPIOS (valem para 1, 3, 5, 10 projetos — qualquer número)

1. **Claude executa. GitHub/GitLab guardam.** Conversa é descartável. Documento é permanente.
2. **1 projeto = 1 documento canônico.** Nunca cópias paralelas. Se existe, atualiza. Nunca cria outro.
3. **Antes de criar qualquer doc → consultar o `INDICE_PROJETOS.md`.** Se o tema já tem dono, editar em vez de criar.
4. **Conversa nova = lê o contexto do projeto antes de começar.** Nada de reexplicar do zero.
5. **Fonte de verdade única por tipo:** GitHub/GitLab = código, arquitetura, skills e agentes. Drive = só arquivos/materiais de negócio a compartilhar.

---

## 1. ESTRUTURA DE PROJETOS (escalável de 1 a N)

### Projetos fixos (núcleo)

| # | Projeto | Doc canônico | Tema |
|---|---|---|---|
| 1 | **IA / Infra / Skills** | `MARKETING_OS_ARQUITETURA.md` | Skills, agentes, sync, padrões técnicos |
| 2 | **Comercial** | `Projetos/Comercial/PLATAFORMA_COMERCIAL_ARQUITETURA.md` | Calls, closers, FUP, dashboard, scoring |
| 3 | **CS** | `Projetos/CS/PROJETO_CS_ARQUITETURA.md` | Retenção, onboarding, anti-churn, NPS |
| 4 | **Empresa Hub** | `Projetos/Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md` | Agentes, copy, tráfego, funis, produto |
| 5 | **Marketing** | `Projetos/Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md` | Campanhas, criativos, tráfego pago, conteúdo |

### Como adicionar projetos novos (6, 7, 8...)

Regra simples — cada novo projeto segue este padrão:

```
1. Criar pasta:    ~/Downloads/Projetos/[NOME]/
2. Criar doc:      ~/Downloads/Projetos/[NOME]/PROJETO_[NOME]_ARQUITETURA.md
3. Registrar:      Adicionar entrada no INDICE_PROJETOS.md
4. GitHub:         commit + push origin (marketing-os-skills)
5. GitLab:         push gitlab (mirror de redundância)
```

Nunca criar projeto sem antes registrar no INDICE_PROJETOS.md. O índice é o roteador de tudo.

---

## 1B. ESBOÇO ESCALÁVEL — quantos projetos criar (1 → 10)

Mesma taxonomia sempre; você só **colapsa ou desmembra**. Comece pequeno e expanda quando um tema ficar grande demais pra ser um *documento* dentro de outro projeto. Cada nível abaixo é a divisão recomendada para aquela quantidade.

### 1 projeto (começando)
`Marketing OS` — tudo dentro, subdividido por documentos. Doc-mãe: `MARKETING_OS_ARQUITETURA.md`.

### 3 projetos (visão macro)
1. **Negócio** (Comercial + CS + OPS/Gestão)
2. **Marketing & Conteúdo**
3. **IA / Infra / Skills & Agentes**

### 5 projetos (RECOMENDADO — o núcleo, já é o da seção 1)
1. Comercial · 2. CS · 3. Marketing · 4. Empresa Hub / OPS · 5. IA / Infra / Skills

### 7 projetos (operação madura — desmembra o técnico)
6. **Análise de Calls & Mídia** → `Projetos/Midia/ANALISE_CALLS.md` (skill analisa-video, transcrições, scores)
7. **Automação & DevStack** → `Projetos/Dev/DEVSTACK.md` (scripts, APIs, bots, pipelines, integrações)

### 8 projetos (entra o produto de conteúdo)
8. **Base de Conteúdo & Ensino de IA** → `Projetos/Conteudo/BASE_CONTEUDO_IA.md` (curadoria de reels/hooks/copys, biblioteca)

### 10 projetos (portfólio completo)
9. **Empresa Automatizada (produto)** → `Projetos/Empresa/AGENTES_EMPRESA.md` (agentes de copy/tráfego/funil como produto vendável)
10. **Conhecimento & Mentor** → `Projetos/Conhecimento/INDICE_CONHECIMENTO.md` (bases de eventos/G4, frameworks, liderança/desenvolvimento)

> **Regra de desmembramento:** um sub-tema nasce como `.md` dentro do projeto-pai. Só vira projeto próprio quando (a) tem doc canônico grande demais, ou (b) vira produto/plataforma com roadmap. Ex.: "WhatsApp near-real-time" começa dentro do CS; vira projeto quando for pro PoC.

**Diversificação por eixo** (pra não concentrar tudo em "operação"):
- Eixo **Negócio**: Comercial, CS, Marketing, OPS/Empresa
- Eixo **Técnico**: IA/Infra/Skills, Mídia, DevStack
- Eixo **Produto/Conhecimento**: Conteúdo & Ensino, Empresa Automatizada, Mentor/Conhecimento

---

## 1C. ESTRUTURA INTERNA DE CADA PROJETO (padrão de arquivos)

Cada projeto pode seguir este padrão de 4 itens — do mais lido ao entregável:

```
[PROJETO]/
├── MEMORIA.md            ← O que Claude lê primeiro. Contexto, regras, estado atual.
├── [DOC]_ARQUITETURA.md  ← Como funciona. Decisões técnicas/negócio. Evolui com o projeto.
├── STATUS.md             ← Feito | Em andamento | Pendente. Atualizado a cada sessão.
└── docs/                 ← Entregáveis: PDFs, planilhas, scripts, specs. Nunca fonte de verdade.
```

**Convenção de nome:** `[PROJETO]_[TIPO]_[TEMA].md` (ex.: `COMERCIAL_playbook_abordagem-objecao.md`). Nome igual + pasta igual = mesmo arquivo versionado. Nunca `_v2`, nunca `_final`.

**1 conversa Claude fixa por projeto** (com o nome exato do projeto) — evita espalhar contexto. Ex.: "Comercial — FUP & Closers", "Análise de Calls & Vídeos", "IA & Infra — Skills & Arquitetura".

---

## 2. REGRA ANTI-DUPLICAÇÃO (o problema real das 9 conversas)

### Por que os documentos duplicam?

Cada conversa cria arquivo do zero sem saber que outra conversa já criou algo similar. Em 2 semanas você tem 3 versões do mesmo arquivo e nenhuma é a verdade.

### A solução (definitiva)

```
ANTES de criar qualquer documento:
  1. Ler INDICE_PROJETOS.md
  2. Verificar se já existe doc para aquele tema
  3. Se existir → ATUALIZAR o doc existente
  4. Se não existir → criar com nome padrão + registrar no índice

NUNCA:
  ❌ Criar "v2", "final", "revisado", "novo"
  ❌ Criar doc sem registrar no índice
  ❌ Guardar decisões só dentro da conversa
```

### Convenção de nomes (obrigatória)

```
[PROJETO]_[TIPO]_[TEMA].md

Exemplos:
  COMERCIAL_ARQUITETURA_PLATAFORMA.md   ✅
  CS_PROCESSO_ONBOARDING.md             ✅
  plataforma_comercial_v2_final.md      ❌
  novo_doc_cs.md                        ❌
```

---

## 3. ONDE VIVE CADA COISA (fonte de verdade única)

| O quê | Onde vive | Por quê |
|---|---|---|
| Documentos de arquitetura | **GitHub + GitLab** (marketing-os-skills) | Versionado, histórico, redundância |
| Skills | **GitHub** + plugin Cowork | Auto-sync via LaunchAgent |
| Docs de negócio (compartilhar) | **Drive** Marketing OS/ | Colaborativo, fácil de acessar |
| Mac local | **~/Downloads/Projetos/** | Fonte para sync automático |
| Contexto de sessão | **Claude** (lê dos docs acima) | Executor, não repositório |

**Regra de ouro:** Claude executa. GitHub/GitLab guardam (Drive só para arquivos a compartilhar). Conversa é descartável. Doc é permanente.

---

## 4. COMO INICIAR QUALQUER CONVERSA NOVA

Cole isso no início de TODA nova conversa, trocando apenas o tema:

```
Projeto: [NOME DO PROJETO]
Leia: ~/Downloads/Projetos/INDICE_PROJETOS.md
Depois leia: ~/Downloads/Projetos/[PASTA]/[DOC_CANONICO].md

Regras desta sessão:
- Não criar documento novo sem checar o índice
- Se o doc já existe → atualizar, não criar paralelo
- Ao finalizar → atualizar o doc canônico do projeto
- Skills disponíveis: analisa-video, devstack, auto-qa, watchdog, debugger
```

---

## 5. CLAUDE.md POR PROJETO (lean — ~50 linhas)

Cada projeto tem um CLAUDE.md enxuto com apenas:

```markdown
# [NOME DO PROJETO] — Contexto

## O que é
[2 linhas descrevendo o projeto]

## Doc canônico
~/Downloads/Projetos/[PASTA]/[DOC].md

## Stack
[3-4 linhas: Supabase + N8N + Next.js + Vercel]

## Skills ativas
devstack (auto), auto-qa (auto), watchdog (auto), debugger (auto)

## Regra
Antes de criar qualquer arquivo: ler INDICE_PROJETOS.md.
Atualizar doc existente, nunca criar paralelo.
```

**Por que lean?** Carregar 1.200 linhas toda sessão gasta tokens desnecessariamente. 50 linhas de contexto real valem mais que 1.200 linhas de histórico.

---

**Bloco recomendado "O que nunca perguntar"** no CLAUDE.md de cada projeto (evita reexplicar o óbvio a cada sessão):

```
## O que nunca perguntar
- Quem são os grupos (VR, Silva, Lazari)
- O que é FUP
- Como funciona o atualizar_skill.sh
- [adicionar o que for específico do projeto]
```

---

## 6. COMO RESOLVER AS 9 CONVERSAS ABERTAS AGORA

Mande para cada uma:

> *"Responda em 3 linhas: (1) qual o tema central desta conversa, (2) o que foi produzido/decidido, (3) o que ficou pendente."*

Depois:
1. Mapeia cada resposta para um dos 5 projetos fixos
2. Migra o conteúdo útil para o doc canônico daquele projeto
3. Encerra ou renomeia as conversas duplicadas
4. Mantém ativa apenas 1 conversa por projeto

---

## 7. WORKFLOW COMPLETO — DO INÍCIO AO FIM DE CADA SESSÃO

```
ABRE SESSÃO
  └── Cola contexto: tema + "leia INDICE_PROJETOS.md + doc canônico"
  
DURANTE A SESSÃO
  └── Executa tarefas
  └── Antes de criar doc → checa índice
  └── Atualiza doc existente OU cria novo com nome padrão + registra no índice
  
FECHA SESSÃO
  └── Doc canônico atualizado ✅
  └── INDICE_PROJETOS.md atualizado ✅
  └── GitHub: commit + push origin ✅
  └── GitLab: push gitlab (redundância) ✅
```

---

## 8. PADRÃO DE AGENTES (em todo projeto)

```
AGENTES QUE RODAM AUTOMATICAMENTE (sem precisar chamar):
  devstack  → quando há código
  auto-qa   → antes de qualquer entrega
  watchdog  → se output parecer suspeito
  debugger  → quando encontrar erro

AGENTES QUE VOCÊ CHAMA:
  analisa-video → análise de calls, cursos, conteúdo
  fup-mensal    → planilhas de follow-up
  skill-creator → criar/melhorar skills
```

---

## 9. IDs DO DRIVE (para Claude usar diretamente)

```
Marketing OS (raiz): 131DWxPAXhT6LIGBZpy5ojeop8Zynzmvx
Projetos/:           1qnfnrZRrMPUbTVsV6zI0zdzyoYCLxGpd
Projetos/CS/:        112aOIrCPM6WzcTRDYx2avaux_2YEA2QN
Projetos/Comercial/: 1FPh4tv8yVgUjUpPVr2D_PbRdM4zRIoBr
Projetos/Empresa/:   1idWNJLnXy4PczO29Y3UwiwLZoVUzoirj
Skills/:             1G9G33mTjZGdrOtQDpx_qH35vYYXegy_5
```

---

## O QUE NÃO FAZER (erros comuns)

- ❌ Usar conversas como repositório de decisões (conversa é descartável)
- ❌ Criar doc novo sem checar o `INDICE_PROJETOS.md`
- ❌ Espalhar o mesmo doc sem fonte única — a fonte é o canônico em **Local + GitHub + GitLab**
- ❌ Nomear arquivos com `_v2`, `_final`, `_novo`, `_atualizado`
- ❌ Abrir conversa sem declarar o projeto
- ❌ Pedir ao Claude para "votar" na estrutura — estrutura se decide uma vez, não por N respostas

---

## 10. O QUE AS 9 RESPOSTAS CONCORDARAM (síntese final)

Todas as 9 respostas, independente do contexto de cada conversa, chegaram às mesmas 4 conclusões:

1. **Conversa = executor. Doc = memória.** A conversa é descartável. O documento é permanente.
2. **Uma fonte de verdade por projeto.** GitHub/GitLab para código, arquitetura, skills e agentes (versionado). Drive só para arquivos/planilhas de negócio a compartilhar. Nunca dois como fonte primária do mesmo doc.
3. **INDICE_PROJETOS.md como roteador.** Toda sessão começa lendo o índice. Toda sessão termina atualizando o doc canônico.
4. **Regra anti-duplicação na origem.** Antes de criar → checar. Se existe → atualizar. Nunca criar paralelo.

---

*Gerado em: 2026-07-06 · Revisado/consolidado em 2026-07-10 (incorporada a versão avulsa da raiz + padronização 3 lugares) | Marketing OS*
