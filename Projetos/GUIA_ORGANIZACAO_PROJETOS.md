# GUIA DE ORGANIZAÇÃO DE PROJETOS — Marketing OS
**Versão:** 1.0 | **Síntese de 9 respostas Claude** | **Data:** 2026-07-06
**Autor:** Arthur Gerber | **Owner:** Marketing OS

> Este guia é a fonte única de verdade sobre como organizar projetos, conversas, documentos e ferramentas no Marketing OS. Toda nova sessão deve ler este arquivo antes de criar qualquer coisa.

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
4. Drive:          Criar pasta Marketing OS/Projetos/[NOME]/ no Drive
5. GitHub:         sync_watcher sincroniza automaticamente
```

Nunca criar projeto sem antes registrar no INDICE_PROJETOS.md. O índice é o roteador de tudo.

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
| Documentos de arquitetura | **GitHub** (marketing-os-skills) | Versionado, histórico, merge |
| Skills | **GitHub** + plugin Cowork | Auto-sync via LaunchAgent |
| Docs de negócio (compartilhar) | **Drive** Marketing OS/ | Colaborativo, fácil de acessar |
| Mac local | **~/Downloads/Projetos/** | Fonte para sync automático |
| Contexto de sessão | **Claude** (lê dos docs acima) | Executor, não repositório |

**Regra de ouro:** Claude executa. GitHub/Drive guardam. Conversa é descartável. Doc é permanente.

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
  └── GitHub: sync_watcher faz push automático ✅
  └── Drive: Claude atualiza via MCP ✅
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

## 10. O QUE AS 9 RESPOSTAS CONCORDARAM (síntese final)

Todas as 9 respostas, independente do contexto de cada conversa, chegaram às mesmas 4 conclusões:

1. **Conversa = executor. Doc = memória.** A conversa é descartável. O documento é permanente.
2. **Uma fonte de verdade por projeto.** GitHub para código/docs técnicos. Drive para docs de negócio. Nunca os dois como fonte primária.
3. **INDICE_PROJETOS.md como roteador.** Toda sessão começa lendo o índice. Toda sessão termina atualizando o doc canônico.
4. **Regra anti-duplicação na origem.** Antes de criar → checar. Se existe → atualizar. Nunca criar paralelo.

---

*Gerado em: 2026-07-06 | Fonte: síntese de 9 respostas Claude | Marketing OS*
