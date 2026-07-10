# PLATAFORMA MARKETING — ARQUITETURA

**Projeto:** Marketing | **Status:** 🟢 Em desenvolvimento | **Atualizado:** 2026-07-10
**Doc canônico do Projeto Marketing** — registrado no `INDICE_PROJETOS.md`
**Segue:** `POLITICA_SYNC_SEGURANCA.md` (3 lugares idênticos — Local + GitHub + GitLab —, verificação pós-escrita, snapshot antes de sobrescrever, ações destrutivas sinalizadas).

---

## ESCOPO DO PROJETO

Tudo que é criação e engenharia de mensagem de marketing dos grupos (VR / Silva / Lazari):

- Copy e copywriting de resposta direta
- Estratégia de posicionamento e mensagem
- Funis (VSL, DTC, quiz, TSL, editorial)
- Webinários e lives de conversão
- Campanhas, criativos e ângulos
- Ofertas (stack de valor, ancoragem, bônus, garantias)

---

## FLUXO DE AGENTES DO PROJETO MARKETING

> **Consolidado em 2026-07-10** a partir de `Projetos/Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md` (organograma de setores/agentes) e de `Marketing_OS/github_skills/record-replay/agents/` (agentes operacionais). Substitui a antiga OBS/HANDOFF ("fluxo a recuperar") — o fluxo abaixo é a versão real e canônica.

### Organograma — setores e agentes de Marketing

```
📣 MARKETING
│
├── 🖊️  COPY
│   ├── Agente Copy Principal (VSL, email, texto longo)
│   ├── Agente Copy Criativo (headlines, ganchos, ângulos)
│   ├── Agente Copy SDR/Prospecting (mensagens, scripts)
│   └── Subagente Swipe File (garimpador de copies que funcionam)
│
├── 🎬 VÍDEO / CRIATIVO
│   ├── Agente Roteiro (VSL, Reels, UGC, ADs)
│   ├── Agente Editor Brief (instrui editor humano ou IA)
│   ├── Agente Thumbnail/Imagem (prompt para DALL-E/Midjourney)
│   └── Subagente Trend Watcher (monitora tendências no nicho)
│
├── 📊 TRÁFEGO
│   ├── Agente Media Buyer (estratégia de campanhas Meta/Google)
│   ├── Agente Criativo Tráfego (gera variações de criativos para testar)
│   ├── Agente Análise de Dados (lê resultados, aponta otimizações)
│   └── Subagente Spy (garimpador de anúncios concorrentes que funcionam)
│
├── 🎯 PRODUTO / OFERTA
│   ├── Agente Produto (define oferta, precificação, posicionamento)
│   ├── Agente Garantia/Bônus (estrutura o que aumenta conversão)
│   └── Subagente Research (pesquisa mercado, avatar, objeções)
│
├── 🔀 FUNIS
│   ├── Agente Funil Comercial (qualificação → call → fechamento)
│   ├── Agente Funil de Vendas (lançamento, evergreen, webinário)
│   ├── Agente Funil Estratégico (escada de valor completa)
│   └── Subagente Order Bump / Upsell / Downsell
│
├── 🧠 ESTRATÉGIA
│   ├── Agente Estrategista Principal (visão macro, trimestral)
│   ├── Agente Posicionamento (diferenciação, branding)
│   └── Subagente Análise de Concorrentes
│
└── 🤖 OPERAÇÃO / AUTOMAÇÃO
    ├── Agente N8N (cria automações, workflows)
    ├── Agente Plataforma (sobe produto no Hotmart/Kiwify, cria links)
    └── Subagente Monitor (verifica métricas diárias, alerta anomalias)
```

### Ciclo de validação de oferta (exemplo)

```
[Arthur define: quero testar oferta de curso de fechamento]
    ↓
[Agente Research]: pesquisa avatar, dores, objeções do mercado
    ↓
[Agente Produto]: monta oferta, preço, garantia, bônus
    ↓
[Agente Copy Principal]: escreve VSL, página de vendas
    ↓
[Agente Criativo Tráfego]: gera 5 ângulos de criativo para testar
    ↓
[Agente Funil]: monta página, order bump, upsell
    ↓
[Agente Plataforma]: sobe no Hotmart, cria links de pagamento
    ↓
[Arthur confere e aprova — 30 min de revisão]
    ↓
[Agente Media Buyer]: sobe campanhas com budget mínimo de teste
    ↓
[Agente Monitor]: acompanha métricas a cada 2h
    ↓
[Agente Análise]: depois de 3 dias, relatório de resultados + próximos passos
```

**Meta:** R$5k/dia validado → escala automática.

### Agentes operacionais da plataforma (base record-replay)

> Todo agente de Marketing acima roda sobre a base operacional da plataforma **record-replay** (`Marketing_OS/github_skills/record-replay/agents/`). São quatro papéis de execução que garantem que a IA aprende observando e replica **junto** com o humano — nunca sozinha.

| Agente | Papel | Regra inegociável |
|---|---|---|
| **Observador** | RECORD: grava o que a pessoa vê e faz (conversas, telas, cliques, navegação). | Sempre com consentimento e escopo definido (LGPD). Saída: sessões humanas que o Curador vira em jogadas. |
| **Executor** | Navega nas conversas e simula/rascunha mensagens JUNTO com o humano. | **Nada é enviado/executado sem aprovação humana explícita.** UI imita ritmo humano; o envio fica no humano. |
| **Dev** | Dev sênior que evolui a plataforma sem quebrar o que funciona. | Entende o objetivo antes de codar; novo subagente registra em `scripts/registro.py`, nunca reescreve o orquestrador; não entrega sem o QA passar. |
| **QA** | Barreira de qualidade antes de qualquer entrega ou mudança de comportamento. | `py_compile` em todo `.py`; `smoke_test.py` verde; jogada nova sem PII; nenhuma ação `executado=True` sem aprovação; isolamento por cliente intacto. |

### Regras herdadas (de POLITICA_SYNC_SEGURANCA.md)

- Nada é publicado/enviado sem aprovação de Arthur (item 6 da política — ações destrutivas/irreversíveis são sinalizadas, nunca automáticas).
- Todo agente/subagente nasce salvando nos 3 lugares (Local + GitHub + GitLab) com verificação pós-escrita.
- Novo agente que consome recurso: Arthur aprova antes de criar.
- Isolamento de dados por cliente/empresa; aprendizado compartilhado só por padrão anonimizado.

---

## METODOLOGIAS DO PROJETO

### 1. Análise de Copy de Lives / Webinários (engenharia reversa)

Método canônico para dissecar qualquer live/webinário de vendas e extrair o que replicar.

- **Framework:** `FRAMEWORK_ANALISE_COPY_LIVES.md` (13 seções)
- **Entrada:** transcrição da live + o framework
- **Saída:** análise seção por seção → técnicas a replicar → script de abertura adaptado ao sócio/produto
- **Casos analisados:**
  - Guilherme Bifi — "O Grande Timing" (DTC / Double CPA) — *1º caso de referência*

*(Próximas metodologias entram aqui: estrutura de VSL, construção de oferta, ângulos DTC, criativos, etc.)*

---

## ARQUIVOS DO PROJETO

- `PLATAFORMA_MARKETING_ARQUITETURA.md` ← este (índice/canônico do projeto)
- `FRAMEWORK_ANALISE_COPY_LIVES.md` ← método de análise de copy de lives
- `MANIFESTO_HANDOFF.md` ← mapa de estado (URLs/IDs do Drive, furos, pendências)
- *(transcrições e casos entram como material de referência na pasta)*

---

## PAPEL DO CLAUDE NESTE PROJETO

Atua como **Diretor Sênior de Marketing / Chief of Copy**.

- Ao receber **transcrição + framework**: executa a análise seção por seção com precisão cirúrgica.
- Quando Arthur disser **"quero aplicar"** ou passar contexto de um sócio (nome, produto, avatar, promessa): gera as adaptações e o **script de abertura** para aquele contexto.
- Perguntas sobre a análise **antes** de aplicar: responde com profundidade estratégica antes de qualquer execução.

---

## COMO INICIAR SESSÃO (Projeto Marketing)

Cole no início da conversa:

```
Projeto: Marketing.
- Leia: ~/Downloads/Projetos/Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md
- Depois o método: FRAMEWORK_ANALISE_COPY_LIVES.md
- Skills: analisa-video, devstack, auto-qa, docx / pptx / xlsx / pdf
- Repo: github.com/arthurgerber/plataforma-marketing (criar ao entrar em código)
```

---

## SINCRONIZAÇÃO (local + GitHub + GitLab)

Padrão do Marketing OS: cada doc vive nos 3 lugares (Local + GitHub + GitLab), sincronizado por terminal/Cowork, com bytes idênticos.
Comandos de referência (rodar no Mac, na raiz do repo — aqui `~/Downloads/Marketing_OS/github_skills`):

```bash
# 1. Local → estrutura
mkdir -p ~/Downloads/Projetos/Marketing
cp PLATAFORMA_MARKETING_ARQUITETURA.md FRAMEWORK_ANALISE_COPY_LIVES.md ~/Downloads/Projetos/Marketing/

# 2. GitHub (origin) + GitLab (gitlab) — fonte de verdade versionada + redundância
cp -R ~/Downloads/Projetos/. ./Projetos/
git add Projetos INDICE_PROJETOS.md
git commit -m "feat(marketing): arquitetura + agentes + framework análise de copy de lives"
git push origin HEAD
git push gitlab HEAD

# (Drive não é mais alvo de sync de docs — fica para arquivos/vídeos. Leitura web dos canônicos: GitHub/GitLab.)
```
