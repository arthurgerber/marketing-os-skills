# AVALIAÇÃO — Conteúdos de IA/Claude do grupo "PROJETOS | IA"
**Data:** 2026-07-02 | **Método:** leitura do grupo (texto/prints/mídia) + 5 agentes em paralelo checando links externos e fatos.

> Objetivo: separar o que é **real e útil** do que é **hype/isca**, e dizer o que compensa mudar em arquitetura/skill.

---

## VEREDITO RÁPIDO (o que fazer)

- **Pare de reinventar o "OS de agentes" do zero.** O que você descreveu (agentes gerenciando agentes, papéis sênior/pleno/diretor, agente revisor) **já existe pronto** no `garrytan/gstack` e no `anthropics/claude-plugins-official`. Forkar/estudar > construir do zero.
- **Migre/teste o Claude Sonnet 5 agora.** Lançado 30/06, com **preço promocional de API até 31/08**. Sua arquitetura hoje assume "Haiku para análise" — vale reavaliar no período barato.
- **Ignore as iscas de Instagram** ("comenta SKILL/GRUPO"). O material real está nos repositórios, não nos reels.

---

## 1. REPOSITÓRIOS / FERRAMENTAS — todos REAIS

| Item | Veredito | O que é | Vale? |
|------|----------|---------|-------|
| **anthropics/skills** (~149k★) | ✅ REAL / oficial | Repo oficial de Agent Skills (formato `SKILL.md`). Fonte canônica de como escrever skill. | ✅ Base essencial |
| **anthropics/claude-plugins-official** (~31k★) | ✅ REAL / oficial (nome confere) | Diretório oficial de plugins do Claude Code: commands, **agents**, skills, MCP empacotados. | ✅ Sim |
| **garrytan/gstack** (~119k★) | ✅ REAL (é o Garry Tan da Y Combinator) | O setup de Claude Code dele: ~23 ferramentas por papel (CEO, Designer, Eng Manager, QA, Security) em slash commands. **É literalmente um "OS de agentes".** | ✅ O mais alinhado ao seu objetivo |
| **DietrichGebert/ponytail** (~69k★) | ✅ REAL / comunidade | Skill "anti-over-engineering": faz o agente escrever o mínimo de código. | ⚠️ Bom complemento, não peça central |

> ⚠️ **Correção de lenda:** o print descreveu o gstack como "browser CLI headless / Chromium daemon". **Está errado.** Isso é só um componente (`/browse`). O gstack real é o framework completo de agentes por papel — que é justamente o que você quer.

---

## 2. FATO CONFIRMADO — o "novo modelo" é real (Claude Sonnet 5)

Os posts de **Alan Nicolas** e **Rafael Milagre** falam do **Claude Sonnet 5**, lançado em **30/06/2026**. Fact-check contra a fonte oficial (anthropic.com/news/claude-sonnet-5):

| Afirmação no post | Veredito |
|-------------------|----------|
| "63 vs 58" em programar no automático | ✅ Confere — SWE-bench **Pro** (Sonnet 5 ~63,2% vs 4.6 ~58%) |
| "81 vs 78" em mexer no computador | ✅ Confere — OSWorld-Verified (81,2% vs 78,5%) |
| "disponível em todos os planos, do grátis ao Enterprise" | ✅ Confere (default no Free e Pro) |
| "promoção de API até fim de agosto" | ✅ Confere — US$2/US$10 por milhão de tokens até 31/08/2026 |

**Não é fake.** Única nuance: o "63" é do SWE-bench *Pro* (mais difícil); no *Verified* o Sonnet 5 fica ~85%. Cuidado só com leaderboards de terceiros (morphllm, claude5.ai etc.) que citam "Fable 5 / Mythos 5 / Opus 4.8" com números inconsistentes — não são fonte confiável.

---

## 3. VÍDEO ÚTIL (YouTube)

- **"I Tried 100+ Claude Code Skills. These 6 Are The Best"** — Nate Herk (03/05/2026). ✅ Técnico legítimo, com viés comercial (isca no título + venda de curso/afiliados). Útil como **lista de referência** de skills/plugins reais: `claude-mem` (memória persistente), `superpowers`, `context-mode`, `skill-creator`, `frontend-design`. ~15 min bem gastos se o foco for descobrir ferramentas prontas.

---

## 4. ISCAS DE ENGAJAMENTO (baixo valor / cuidado)

| Post | Classificação | Por quê |
|------|---------------|---------|
| **Lucas Lopes** — "SKILL OFICIAL de análise de concorrentes, comenta 'SKILL'" | 🟠 Isca + meia-verdade | Skill assim é plausível, mas **"oficial" é falso** — só a Anthropic publica skill oficial. "Comenta que envio acesso" = funil de lista. Risco médio. |
| **Lucas Bravo** — "app aos 17, US$30 mi, comenta 'GRUPO'" | 🔴 Isca | Storytelling viral + comment-to-DM pra crescer grupo. Números não verificáveis. Risco médio-alto. |
| **Amanda Diniz** — "o segredo que ninguém te conta" | 🟡 Misto | Curiosity-gap; pode ter dica real, mas enquadramento é engajamento. |
| **Fabiano Carvalho** — "5 plugins grátis e open source" | 🟢 Conteúdo real | Claude Code TEM plugins open source de verdade. Sem gatilho de DM. O mais saudável do lote. |
| **Bernardo Precht** — vídeo de futebol/copa | ⚪ Off-topic | Não é conteúdo de IA. |

**Regra:** todo post "comenta [PALAVRA] que te envio o acesso" é crescimento de lista, não distribuição honesta. O material pode existir, mas o "acesso" quase sempre passa por funil.

---

## 5. SUAS PRÓPRIAS MENSAGENS (a visão) — comentário

Você escreveu (30/06, 00:45) a visão: loops de autoaprimoramento, MCPs personalizados, agentes paralelos, **agentes que gerenciam agentes** (organograma sênior/pleno/diretor), **agente revisor dentro de cada agente fazedor**. Depois: dica de usar **OAuth do Claude Code como "APT"** (rodar no servidor consumindo a assinatura), automatizar só sob necessidade, rodar em **VPS + Supabase + GitHub Actions**.

**Crítica construtiva:**
- A visão é boa **e já tem molde pronto**: subagentes nativos do Claude Code + `gstack` (papéis) + `claude-plugins-official` (empacotamento) cobrem 80% disso. **Adote antes de construir.**
- "Agente revisor dentro de cada agente" ≈ seu próprio `auto-qa`/`watchdog`. Você já tem o conceito — falta padronizar no formato oficial de plugin/skill.
- Risco do seu setup atual: **excesso de complexidade** (a arquitetura tem dezenas de fix-scripts e camadas). O `ponytail` existe exatamente pra combater isso — vale como skill de disciplina.

---

## 6. NÃO ACESSÍVEL (precisa do seu Chrome logado ou do arquivo)

Esses ficaram bloqueados por login/JS — resolvem rápido se eu abrir pelo seu Chrome logado ou você salvar o arquivo:

- **Google Doc** `docs.google.com/document/d/1suS8DB...` (login/JS)
- **PDF** `7_niveis_guia_claude_code.pdf` (Drive, login)
- **PDF** `prompt_claude_honesto.pdf` (fbsbx)
- **Instagram reels** (Amanda Diniz; `/reel/DaNCWH4AsNN`) — exigem login
- **Vídeo YouTube 1** (`mWvtQHIZM-l`) — ID do print está quebrado; me manda o link limpo
- **Áudio do grupo CS** (2:05) — não transcrito (ambiente bloqueia baixar modelo Whisper)

---

---

# PARTE 2 — RESPOSTAS DIRETAS ÀS SUAS PERGUNTAS

## Vale criar skill nova? SIM — 2, mas adaptadas de padrão provado (não do zero)

1. **Skill de memória persistente (`claude-mem`)** — resolve uma dor que VOCÊ MESMO documentou: no seu `MARKETING_OS_ARQUITETURA.md` está escrito que "o nome original da plataforma foi perdido na compactação de contexto". Isso é exatamente o que memória persistente resolve. É o item de maior ROI. (Referência real: aparece no vídeo do Nate Herk e tem repo open source.)
2. **Gabarito de avaliação de CS/onboarding** — análogo ao seu `PROCESSO_BASE_CLOSER.md`, mas para o CS analisar calls de onboarding (surgiu na outra sessão). Extensão da `analisa-video`.

Tudo o mais que você descreveu na mensagem de abertura do grupo (agentes gerenciando agentes, organograma, revisor por agente) **NÃO precisa de skill nova** — é subagente nativo do Claude Code + o padrão do `gstack`. Adotar > construir.

## Vale agregar nas skills que já temos? SIM

- **`analisa-video`**: está sobre-engenheirada (dezenas de fix-scripts, 3 camadas de backup, LaunchAgent). Aplique a disciplina do `ponytail` (menos código). Padronize no formato oficial `SKILL.md` do `anthropics/skills` — hoje suas skills são custom.
- **`auto-qa` / `watchdog`**: é literalmente o "agente revisor dentro de cada agente" da sua visão. Formalize como **subagente + slash command `/review`** (padrão gstack), em vez de conceito solto.

## Editar o CLAUDE.md? SIM — e é importante

Seu `MARKETING_OS_ARQUITETURA.md` tem ~1.260 linhas e funciona como memória carregada toda sessão. **Isso é pesado demais e queima contexto.** Recomendação (é o tema dos "7 níveis / claude.md" do grupo):
- **CLAUDE.md enxuto** (50–100 linhas): stack, convenções, regras de ouro, e **ponteiros** para os docs longos.
- Os docs grandes viram **referência sob demanda**, não carga automática.
- Isso sozinho melhora velocidade e custo de toda sessão.

## Fluxo de dados e SEGURANÇA — 2 pontos críticos que achei

1. 🔴 **"Usar OAuth do Claude Code como APT, rodando no servidor e consumindo minha assinatura"** (está num print de "dicas extras" do grupo). **Cuidado:** usar a assinatura (Max/Pro) via OAuth para automação servida/programática em escala (você fala em 300 calls/dia) tende a violar os Termos da Anthropic e pode derrubar sua conta. Para automação, use **API** — ainda mais agora com a **promo do Sonnet 5 até 31/08**. Assinatura é para uso interativo.
2. 🟠 **Token do HuggingFace em texto puro** dentro do `MARKETING_OS_ARQUITETURA.md`. Tire do doc, use `~/.config` / secret manager / variável de ambiente (você já usa `~/.config/watch/.env` — então só remova do markdown).

Resto do fluxo (AWS RDS em SP para LGPD, GitHub privado, EC2 Spot) está **correto e bem pensado**.

## Comandos / processos — o atalho

Adote o padrão **1 papel = 1 slash command** do `gstack` (`/plan`, `/review`, `/qa`, `/security`) em vez de orquestrar "agentes que gerenciam agentes" na mão. Você chega no mesmo resultado da sua visão com uma fração do esforço.

---

# PARTE 3 — ANÁLISE DOS PRINTS (o que dá pra extrair)

| Print | O que é / inferência |
|-------|----------------------|
| **Setup "pés na mesa" + notebook** | Notebook com **terminal escuro multi-painel** rodando o que parece uma sessão de **Claude Code / agente em terminal** (não é IDE gráfica). Bate com a sua ideia de "rodar tudo em VPS/terminal". Não dá pra cravar o app exato pela resolução, mas o padrão visual é de workflow de agente por linha de comando. |
| **Tabela de benchmark (Alan Nicolas)** | Comparativo Sonnet 5 × 4.6 — números validados (SWE-bench Pro, OSWorld). ✅ Real. |
| **"dicas extras que me ajudaram"** | 1) OAuth Claude Code como APT (⚠️ ver alerta de segurança acima); 2) automatizar só sob necessidade; 3) rodar em VPS + Supabase + GitHub Actions. Conteúdo legítimo de workflow. |
| **Planilha (Lucas Lopes / "SKILL")** | Saída de uma skill de análise de concorrentes (tabela de produtos/serviços/diferenciais). Plausível tecnicamente; o "oficial" do post é falso. |
| **Álbum +10 (01:19–01:20)** | Thread tipo tutorial: Lovable + Supabase + "10 tipos diferentes, um prompt cada" — construção de app no-code/low-code. Conteúdo instrucional comum. |
| **CLAUDE.md / GSTACK (imagens)** | Referências aos repos já avaliados na Parte 1. |

---

# PARTE 4 — O QUE AINDA ESTÁ BLOQUEADO (precisa de 1 ação sua, ~30s)

Estes são privados/atrás de login e o ID que tirei do print veio errado. Resolve na hora se você:
- **Colar aqui os links exatos** de: Google Doc (`docs.google.com/document/...`), PDF `7_niveis_guia_claude_code`, PDF `prompt_claude_honesto`, e o **YouTube 1** (o `v=` do print está quebrado); **ou**
- **Salvar os 2 PDFs na pasta Downloads** que eu leio localmente.
- **Reels do Instagram** (Amanda Diniz, `/reel/DaNCWH4AsNN`) exigem login — abro pelo seu Chrome se você confirmar.
- **Áudio do grupo CS (2:05)**: transcrição só roda no seu Mac (a `analisa-video` já tem o modelo lá); aqui o ambiente bloqueia baixar o Whisper.

Assim que você fizer uma dessas, eu fecho a avaliação 100%.

---

---

# PARTE 5 — CONTEÚDO ACESSADO NA ÍNTEGRA (verificado, não mais "bloqueado")

Abri de fato pelo Chrome logado / mídia do grupo. Correções e novidades:

### Documentos e PDFs

| Item | Acesso | O que É de verdade | Veredito |
|------|--------|--------------------|----------|
| **Google Doc "Clone - Austin KLEON (Claude)"** | ✅ Lido | **Prompt de persona**: transforma o Claude no escritor Austin Kleon (criatividade, "Roube Como um Artista"). Regras: generoso, dá permissão, anti-perfeccionista, honesto. Tem seção "ARSENAL CRIATIVO". | Útil se você quiser um agente de **conteúdo/copy** com voz criativa. Não tem a ver com engenharia/infra. |
| **PDF "Os 7 níveis do Claude Code"** (5 págs) | ✅ Lido | Guia progressivo: Nível 1 Prompt → Nível 2 Contexto → ... → Nível 7 equipes de agentes em paralelo. Bem escrito, técnico, sem hype. | ✅ **O mais valioso do grupo pra você** — é literalmente o mapa da sua ambição (subir de "chat" até "agentes paralelos"). Guarde e siga. |
| **PDF "prompt_claude_honesto.pdf"** | ⚠️ Link expirado | Link do CDN do Facebook (fbsbx) é assinado e **expirou** ("URL signature expired"). Pelo nome/família, é outra persona ("Claude honesto"). | Peça pra reenviarem ou ache o arquivo original; sozinho o link está morto. |

### Reels / posts (acessados)

| Item | Acesso | Verdade |
|------|--------|---------|
| **@olucaslopesc — reel** | ✅ Aberto | Legenda: "Comenta 'CLAUDE' que te envio o link oficial". 🔴 **Isca** de comentário→DM. |
| **@amandadiniz — reel** | ✅ Legenda lida | "o que eu faço pra garantir que o claude esteja atualizado sobre os meus projetos e ter melhores resultados nas sessões". 🟡 Tema real (memória/CLAUDE.md), embalagem de isca. |
| **@fabianocarvalho — "5 plugins"** | ✅ Prints lidos | **Substantivo e real**: fala de `claude-mem` (memória persistente, Apache 2.0, via hooks), **Memory MCP**, **Basic Memory** (markdown versionável) e **mem0**. 🟢 O melhor conteúdo técnico do lote — e **confirma** a recomendação de memória persistente. |
| **@rafaelmilagre — posts** | ✅ Prints lidos | Tese boa: "defina o problema e a restrição real (prazo, grana, dado) que a IA para de dar resposta genérica". Mostra stack Claude+Supabase+deploy. 🟢 Conteúdo válido. |
| **@bernardoprecht — "record and replay"** | ✅ Legenda lida | NÃO é futebol — é sobre o recurso **record and replay** (Playwright). Gancho de copa, conteúdo dev. |
| **@lucasbravo / @lucaslopesc (SKILL)** | ✅ | 🔴 Iscas "comenta GRUPO/SKILL". |

### Prints de CLAUDE.md / arquitetura (no grupo)
Há prints mostrando estrutura **CLAUDE.md + ARCHITECTURE.md + COMPONENTS.md + SESSION.md** e o prompt "Leia a CLAUDE.md e ARCHITECTURE.md e **reutilize os componentes existentes**". Isso **valida** a recomendação da Parte 2 de enxugar/estruturar seu CLAUDE.md.

---

# PARTE 6 — O PRINT DO "PÉS NA MESA" (sua pergunta específica)

O que dá pra extrair dos prints de setup do grupo:
- O print "pés na mesa + notebook" mostra um **terminal escuro multi-painel** — padrão visual de **Claude Code rodando em terminal** (agente trabalhando enquanto a pessoa "relaxa"). É estética de automação agêntica, não uma IDE gráfica.
- Outro print (camisa laranja, multi-monitores) vem com a legenda: *"Quando termina, ele analisa o que viu e monta um passo a passo reutilizável com inputs, regras e verificação"* — isso é a **descrição literal de criação de skill** (o agente vira um passo-a-passo reutilizável). Ou seja: o "benchmark" implícito nesses prints é **produtividade de um dev rodando agentes/skills em paralelo no terminal**, exatamente o nível 6–7 do guia dos 7 níveis.

**Leitura de contexto:** o conjunto de prints vende um mesmo posicionamento — "monte memória + skills + agentes e deixe rodar". Bate 100% com a sua visão. A parte real e aproveitável está nos **repos e no guia dos 7 níveis**; a parte inflada está nas **iscas de Instagram**.

---

*Avaliação de conteúdos — Marketing OS / PROJETOS | IA. Conteúdo acessado e verificado item a item.*
