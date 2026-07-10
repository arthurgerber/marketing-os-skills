# ÍNDICE DE PROJETOS — Marketing OS
**Atualizado:** 2026-07-08

---

## PROJETOS ATIVOS

| Projeto | Pasta | Arquitetura | Status |
|---|---|---|---|
| **CS** | `Projetos/CS/` | `CS/PROJETO_CS_ARQUITETURA.md` | 🟡 Iniciando |
| **Comercial** | `Projetos/Comercial/` | `Comercial/PLATAFORMA_COMERCIAL_ARQUITETURA.md` | 🟢 Em desenvolvimento |
| **Marketing** | `Projetos/Marketing/` | `Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md` | 🟢 Em desenvolvimento |
| **Empresa Hub** | `Projetos/Empresa/` | `Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md` | 🟡 Arquitetura pronta |

> **PENDÊNCIA (Marketing):** recuperar/consolidar o fluxo de **agentes e sub-agentes** (mkt, tráfego, copy, webinário, produto, funil) — provavelmente esboçado em `MARKETING_OS_ARQUITETURA.md` / `Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md` (Mac + GitHub). Ver OBS no topo de `Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md`.

---

## ARQUIVO GLOBAL (referência técnica de todas as skills e infra)

`~/Downloads/MARKETING_OS_ARQUITETURA.md` — ground truth técnico global

---

## SKILLS (compartilhadas entre todos os projetos)

Instaladas automaticamente via plugin Cowork. Disponíveis em qualquer sessão:

- **analisa-video** → análise de calls, cursos, conteúdo
- **devstack** → cria sistemas + segurança/RLS (roda automático quando há código)
- **auto-qa** → valida antes de entregar (roda automático no final de tudo)
- **watchdog** → monitora execuções (roda automático se output suspeito)
- **debugger** → resolve bugs (roda automático em falha)
- **fup-mensal** → planilhas follow-up por closer
- **docx / pptx / xlsx / pdf** → documentos e relatórios

---

## COMO INICIAR NOVA SESSÃO — QUALQUER PROJETO

Cole isso no início da conversa:

```
Contexto do projeto [NOME]:
- Leia: ~/Downloads/Projetos/[PASTA]/[ARQUIVO_ARQUITETURA].md
- Skills disponíveis: analisa-video, devstack, auto-qa, watchdog, debugger, fup-mensal
- Stack: Supabase + N8N + Next.js + Vercel
- Infra inicial: EC2 Spot (Arthur) + Mac Mini (sócios)
- Repo: github.com/arthurgerber/marketing-os-skills
```

---

## ESTRUTURA DE PASTAS

```
~/Downloads/
├── MARKETING_OS_ARQUITETURA.md   ← ground truth global (skills, infra, padrões)
│
└── Projetos/
    ├── INDICE_PROJETOS.md         ← este arquivo
    ├── CS/
    │   └── PROJETO_CS_ARQUITETURA.md
    ├── Comercial/
    │   ├── PLATAFORMA_COMERCIAL_ARQUITETURA.md
    │   └── PROCESSO_BASE_CLOSER.md
    ├── Marketing/
    │   ├── PLATAFORMA_MARKETING_ARQUITETURA.md
    │   └── FRAMEWORK_ANALISE_COPY_LIVES.md
    └── Empresa/
        └── MARKETING_OS_EMPRESA_AUTOMATIZADA.md
```

---

## GITHUB — REPOS (planejado por fase)

```
github.com/arthurgerber/
├── marketing-os-skills/     ← skills (JÁ EXISTE ✅)
├── plataforma-comercial/    ← criar ao entrar em código
├── plataforma-marketing/    ← criar ao entrar em código
├── empresa-hub/             ← criar ao entrar em código (dados sigilosos)
└── plataforma-cs/           ← criar ao entrar em código
```

---

## INFRA COMPARTILHADA

- **EC2 Spot:** Arthur (inicial, ~$0.03/call)
- **Mac Mini:** Sócios (já têm) — Arthur migra pra Mac Mini quando escalar
- **Supabase:** 1 projeto por plataforma (isolamento total)
- **Vercel:** 1 deploy por frontend
- **N8N:** 1 instância
