#!/usr/bin/env bash
# =====================================================================
#  DEPLOY + AUDIT — MARKETING OS  v2.2  (auto-contido)
#  Redundancia: GitHub (origin) + GitLab (gitlab, arthur.ga94-group).  [3 lugares]
#  NOTA 2026-07-10: Drive descontinuado como alvo de sync (so arquivos). Repo detectado por remote.
#  NOTA: docs embutidos (secao 8) atualizados para a versao canonica de 2026-07-10 (consolidada, agentes + politica 3 lugares). Re-rodar 'all' reescreve os canonicos com a versao atual (idempotente).
#  Camadas: snapshot, verificacao pos-escrita, 2o remote, idempotencia, acoes manuais.
#  Uso:  bash deploy_marketing_os.sh [audit|deploy|all]   (default: all)
# =====================================================================
set -uo pipefail
BASE="$HOME/Downloads"; PROJ="$BASE/Projetos"; MKT="$PROJ/Marketing"
MODE="${1:-all}"
banner(){ echo; echo "==================== $* ===================="; }
hashof(){ if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" 2>/dev/null | awk '{print $1}'; else shasum -a 256 "$1" 2>/dev/null | awk '{print $1}'; fi; }

banner "1) AUDIT — ground truth global"
if [ -f "$BASE/MARKETING_OS_ARQUITETURA.md" ]; then
  echo "OK     MARKETING_OS_ARQUITETURA.md ($(wc -c < "$BASE/MARKETING_OS_ARQUITETURA.md") bytes)"
else echo "FALTA  $BASE/MARKETING_OS_ARQUITETURA.md  <-- ground truth ausente local"; fi

banner "2) AUDIT — checklist docs canonicos (local)"
for f in \
  "Projetos/INDICE_PROJETOS.md" "Projetos/GUIA_ORGANIZACAO_PROJETOS.md" \
  "Projetos/POLITICA_SYNC_SEGURANCA.md" \
  "Projetos/CS/PROJETO_CS_ARQUITETURA.md" \
  "Projetos/Comercial/PLATAFORMA_COMERCIAL_ARQUITETURA.md" \
  "Projetos/Comercial/PROCESSO_BASE_CLOSER.md" \
  "Projetos/Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md" \
  "Projetos/Marketing/FRAMEWORK_ANALISE_COPY_LIVES.md" \
  "Projetos/Marketing/MANIFESTO_HANDOFF.md" \
  "Projetos/Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md" ; do
  if [ -f "$BASE/$f" ]; then printf "OK     %-56s %s bytes\n" "$f" "$(wc -c < "$BASE/$f")";
  else printf "FALTA  %-56s\n" "$f"; fi
done

banner "3) AUDIT — repositorio git + remotes (origin=GitHub, gitlab=GitLab)"
REPO=$(find "$HOME/Downloads" -maxdepth 4 -type d -name ".git" 2>/dev/null | while read -r g; do d=$(dirname "$g"); git -C "$d" remote get-url origin 2>/dev/null | grep -q "marketing-os-skills" && { echo "$d"; break; }; done)
if [ -n "${REPO:-}" ]; then
  echo "Repo: $REPO"; git -C "$REPO" remote -v
  git -C "$REPO" remote | grep -q gitlab && echo "2o remote (gitlab): OK" || echo "2o remote (gitlab): AUSENTE — ver SETUP no README (so em maquina nova)"
  echo "-- status --"; git -C "$REPO" status -s | head -20
else echo "FALTA  clone de marketing-os-skills nao encontrado sob \$HOME"; fi

banner "4) AUDIT — skill de enforcement / sync"
grep -rilE "enforcement|auto.?sync|salvar.*(drive|github)|3 lugares|rclone" \
  "$HOME/.claude" "$HOME/Downloads" 2>/dev/null | grep -iE "SKILL\.md|sync|enforce" | head -20 \
  || echo "nenhuma skill de sync/enforcement localizada"

banner "5) AUDIT — CLI de Drive"
command -v rclone >/dev/null && echo "rclone: OK" || echo "rclone: ausente"

banner "6) AUDIT — inventario ~/Downloads (soltos p/ reconciliar nos 3 lugares)"
find "$BASE" -maxdepth 1 -mindepth 1 \( -name "*.md" -o -name "*.zip" -o -name "*.skill" -o -name "*.txt" -o -name "*.sh" -o -name "*.py" -o -type d \) \
  -not -name "Projetos" -not -name ".backups" 2>/dev/null | sort | while read -r i; do
    if [ -d "$i" ]; then printf "DIR    %s\n" "${i#$BASE/}"; else printf "FILE   %s (%s bytes)\n" "${i#$BASE/}" "$(wc -c < "$i" 2>/dev/null)"; fi; done
echo "--> Passo 5/5B do README: reconciliar em LOCAL + GITHUB + GITLAB + DRIVE. NAO apagar sem confirmar."

if [ "$MODE" = "audit" ]; then banner "MODO AUDIT — nada foi escrito. Fim."; exit 0; fi

banner "7) SNAPSHOT de seguranca (antes de sobrescrever)"
TS=$(date +%Y%m%d-%H%M%S); mkdir -p "$BASE/.backups"
if [ -d "$PROJ" ]; then tar czf "$BASE/.backups/Projetos-$TS.tar.gz" -C "$BASE" Projetos 2>/dev/null && echo "backup local: $BASE/.backups/Projetos-$TS.tar.gz"; fi
if [ -n "${REPO:-}" ]; then git -C "$REPO" tag "backup-$TS" 2>/dev/null && echo "git tag: backup-$TS"; fi

banner "8) DEPLOY — escrevendo canonicos (idempotente)"
mkdir -p "$MKT"
cat > "$MKT/PLATAFORMA_MARKETING_ARQUITETURA.md" <<'__ARCH_EOF__'
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
__ARCH_EOF__

cat > "$MKT/FRAMEWORK_ANALISE_COPY_LIVES.md" <<'__FW_EOF__'
# FRAMEWORK — ANÁLISE ESTRATÉGICA DE COPY DE LIVES / WEBINÁRIOS

> Método canônico do Projeto Marketing para engenharia reversa de qualquer live/webinário de vendas.
> Caso de referência (1º analisado): Guilherme Bifi — "O Grande Timing" (DTC / Double CPA).
> Nas seções abaixo, onde se lê "BIFI", entenda "o palestrante analisado".

---

Você é um Diretor Sênior de Marketing e Estratégia Digital com histórico como Chief of Copy em operações de alto volume no mercado digital brasileiro. Domina psicologia de persuasão, copywriting de resposta direta, estrutura de webinários de conversão e narrativa de vendas.

Tenho a transcrição completa de uma live/webinário de vendas. Quero que você faça uma análise estratégica e cirúrgica de tudo que o palestrante utilizou, usando o framework abaixo, seção por seção.

**Palestrante / Live:**
[NOME DO PALESTRANTE + TÍTULO DA LIVE]

**Transcrição:**
[COLE A TRANSCRIÇÃO AQUI]

---

## 1. RESEARCH — O QUE BIFI REVELOU SOBRE O AVATAR

**Insights demográficos**
— Quem é o cliente que ele está falando? Atitudes, esperanças, sonhos, vitórias e falhas que ele sinalizou.
— Quais forças externas o avatar culpa pelo fracasso?
— Quais preconceitos ele mencionou? Crenças fundamentais do avatar sobre vida, dinheiro e mercado.
— Resuma o avatar em 2–3 frases como se fosse um brief de copy.

**Soluções existentes**
— Quais ângulos de mercado ele citou ou rebateu?
— O que ele disse sobre concorrentes e soluções que não funcionam?
— Existem histórias de resultado negativo das soluções existentes que ele usou?
— O mercado acredita que as soluções existentes funcionam? O que ele disse sobre isso?

**Curiosidade e corrupção**
— Existe uma narrativa conspiracionista sobre por que as velhas soluções falham?
— Alguma alternativa original, antiga ou esquecida que ele trouxe como contraste?

---

## 2. MECANISMO ÚNICO

— Qual o mecanismo único do **PROBLEMA**? (o que causa o fracasso da maioria — a lógica que ele usou para explicar por que as pessoas erram)
— Qual o mecanismo único da **SOLUÇÃO**? (o que torna a abordagem dele diferente e superior a tudo que já existe)
— Esse mecanismo é contraintuitivo? Como ele o nomeou?

---

## 3. ESTRATÉGIA GERAL

— Como o webinário foi arquitetado? Qual é o posicionamento central?
— Qual a promessa central (resultado + prazo + esforço)?
— Qual a lógica de construção de autoridade ao longo da apresentação?
— Quem é a audiência exata: quem é e quem **NÃO** é o público-alvo?
— Qual é a nova afirmação / causa primária / surpresa que muda tudo para o avatar?
— Top 5 headlines e frases de posicionamento que ele usou.

---

## 4. LEAD — ESTRUTURA DE ABERTURA

Mapeie os primeiros minutos da live:

— **Chamada de Problema**: como ele nomeou e escalou o problema do avatar?
— **Solução + promessa**: como apresentou o resultado e a economia de tempo/dinheiro?
— **Teaser emocional**: como usou a história de descoberta sem revelar tudo?
— **Teaser do mecanismo único**: como criou curiosidade sem entregar a resposta?
— **Gancho de retenção**: o que ele disse para fazer a pessoa ficar até o fim?
— **Ceticismo**: como antecipou e rebateu dúvidas logo de cara?
— **Credibilidade**: quais construtores de autoridade ele usou na abertura?

---

## 5. HISTÓRIA DE BACKGROUND E NARRATIVA

— Como ele construiu "eu estava na mesma dor que você"? Qual foi o ponto de identificação?
— Quais soluções tradicionais ele descartou — e como fez isso sem atacar diretamente?
— Como escalou o problema até o ponto de virada emocional?
— Qual é a "causa real" contraintuitiva que ele revelou? (o 1% que as pessoas não percebem)
— Existe um sábio sensei na história — alguém que revelou a verdade oculta para ele?
— Qual é o arco narrativo completo: tensão → ruptura → descoberta → resolução?
— Como ele criou identificação com a audiência ao longo da narrativa?

---

## 6. GANCHOS

Liste **todos os ganchos** que ele usou, classificados por função:

**Ganchos de abertura** (para prender nos primeiros minutos)
**Ganchos de retenção** (usados no meio para evitar desistência)
**Ganchos de virada** (para preparar a transição à oferta)

Para cada gancho: cite a frase ou estrutura → onde foi usado (tempo aproximado) → por que funciona psicologicamente.

---

## 7. COPY E FRASES DE IMPACTO

Extraia as frases mais poderosas da live. Classifique por tipo:

— **Escassez / urgência**
— **Prova social**
— **Autoridade**
— **Curiosidade**
— **Dor / medo**
— **Desejo / transformação**
— **Contraintuitivo / surpresa**
— **Analogias e metáforas** (as que ele usou para simplificar conceitos complexos)

Para cada frase: cite a frase exata → explique o mecanismo psicológico por trás dela.

---

## 8. PSICOLOGIA E PERSUASÃO

— Quais gatilhos mentais ele ativou e em que ordem?
— Como ele criou tensão e resolução ao longo do webinário?
— Como gerou antecipação antes da oferta?
— Quais objeções ele antecipou e como as quebrou antes de apresentar o produto?
— Qual foi o estado emocional que ele induziu no avatar antes de fazer a oferta?

---

## 9. ESTRUTURA DO WEBINÁRIO (mapa de tempo)

Reconstrua o webinário em blocos:

| Minuto | O que aconteceu | Técnica usada | Objetivo do bloco |
|--------|----------------|---------------|-------------------|
| 0–X    |                |               |                   |

Identifique: abertura → desenvolvimento → virada → oferta → fechamento.

---

## 10. OFERTA

— Qual foi o produto/serviço apresentado?
— Como e quando a oferta entrou — qual foi a transição da live para a venda?
— Qual foi a estrutura completa da oferta: stack de valor, preço, bônus, garantias?
— Como ele ancorou o preço?
— Quais objeções ele quebrou na apresentação da oferta?
— Qual foi o argumento central para comprar agora (e não depois)?

---

## 11. TÉCNICAS DE FECHAMENTO

— Tudo que ele usou para converter no final: urgência, escassez, repetição da promessa, CTA.
— Como ele fez as chamadas para ação? Quantas vezes? Em que tom?
— Como reforçou a promessa central antes do último CTA?

---

## 12. O QUE REPLICAR

Com base em tudo acima:

— **Top 3 técnicas universais** para copiar diretamente em qualquer webinário
— **Top 3 técnicas específicas** do Bifi que são diferenciais dele (e como adaptar)
— **Top 3 adaptações** para o contexto abaixo:

> **SÓCIO:** [nome do sócio]
> **PRODUTO/SERVIÇO:** [descreva o produto ou serviço]
> **AVATAR:** [quem é o cliente desse sócio]
> **PROMESSA CENTRAL:** [qual resultado o produto entrega]

— Qual é a estrutura mínima de um webinário no mesmo estilo para esse contexto? (esqueleto de 60min)

---

## 13. SCRIPT PRONTO

Com base em tudo analisado, escreva a **abertura completa** (primeiros 10 minutos) de um webinário no mesmo estilo, adaptado para o contexto abaixo:

> **SÓCIO:** [nome do sócio]
> **PRODUTO/SERVIÇO:** [descreva o produto ou serviço]
> **AVATAR:** [quem é o cliente desse sócio]
> **PROMESSA CENTRAL:** [qual resultado o produto entrega]

Inclua:
— Chamada de problema
— Teaser do mecanismo único
— Promessa central
— Primeiro gancho de retenção
— Transição para a história de background

O tom deve replicar o estilo do Bifi: direto, com autoridade, próximo da audiência.
__FW_EOF__

cat > "$MKT/MANIFESTO_HANDOFF.md" <<'__MAN_EOF__'
# MANIFESTO DE HANDOFF — Marketing OS

> **ATUALIZAÇÃO 2026-07-10:** O Drive foi **descontinuado como alvo de sync de docs**. A redundância agora é **Local + GitHub + GitLab** (2 remotes versionados). O Drive permanece só para **arquivos** (vídeos, gravações, planilhas, materiais a compartilhar). As seções abaixo sobre estado/stubs do Drive ficam como **registro histórico**.
**Gerado:** 2026-07-08 · **Origem:** sessão de auditoria (chat web)
**Para:** a próxima conversa (Cowork / Claude Code) que vai auditar + sincronizar.

> Este arquivo é a "foto" do que foi descoberto. As URLs do Drive são reais (verificadas nesta sessão).
> O estado em Local/GitHub está marcado como "a confirmar" — o `deploy_marketing_os.sh audit` confirma.

---

## 1. GITHUB
- Org/usuário: **`github.com/arthurgerber`**
- Repo de skills (existe): **`github.com/arthurgerber/marketing-os-skills`**
- Repos planejados (criar ao entrar em código): `plataforma-marketing`, `plataforma-comercial`, `empresa-hub`, `plataforma-cs`

## 2. ESTRUTURA NO DRIVE (URLs reais — 08/jul)
Guarda-chuva: **Marketing OS › Projetos**

| Item | Tipo | ID | URL |
|---|---|---|---|
| Marketing OS (pasta raiz) | folder | `131DWxPAXhT6LIGBZpy5ojeop8Zynzmvx` | https://drive.google.com/drive/folders/131DWxPAXhT6LIGBZpy5ojeop8Zynzmvx |
| Projetos | folder | `1qnfnrZRrMPUbTVsV6zI0zdzyoYCLxGpd` | https://drive.google.com/drive/folders/1qnfnrZRrMPUbTVsV6zI0zdzyoYCLxGpd |
| Projetos/CS | folder | `112aOIrCPM6WzcTRDYx2avaux_2YEA2QN` | https://drive.google.com/drive/folders/112aOIrCPM6WzcTRDYx2avaux_2YEA2QN |
| Projetos/Comercial | folder | `1FPh4tv8yVgUjUpPVr2D_PbRdM4zRIoBr` | https://drive.google.com/drive/folders/1FPh4tv8yVgUjUpPVr2D_PbRdM4zRIoBr |
| Projetos/Empresa | folder | `1idWNJLnXy4PczO29Y3UwiwLZoVUzoirj` | https://drive.google.com/drive/folders/1idWNJLnXy4PczO29Y3UwiwLZoVUzoirj |
| **Projetos/Marketing** | folder | *(NÃO EXISTE — criar)* | — |
| INDICE_PROJETOS | doc (3009 b) | `1A1rohv-UBF4V_mbqi0hVbNQeZVvVqpLN` | https://drive.google.com/file/d/1A1rohv-UBF4V_mbqi0hVbNQeZVvVqpLN/view |
| GUIA_ORGANIZACAO_PROJETOS | doc (946 b) | `1VkC78f0FdcFJb1DHOayS9kdchMoCOs1i` | https://drive.google.com/file/d/1VkC78f0FdcFJb1DHOayS9kdchMoCOs1i/view |
| PROJETO_CS_ARQUITETURA | doc (3446 b) | `1Bq5zpDBUot1YOD2IjwTeRnKndrCBP9sq` | https://drive.google.com/file/d/1Bq5zpDBUot1YOD2IjwTeRnKndrCBP9sq/view |
| PLATAFORMA_COMERCIAL_ARQUITETURA | doc (269 b · STUB) | `1NSMuZOHj5SNBoedS522FSFwRqGdipjee` | https://drive.google.com/file/d/1NSMuZOHj5SNBoedS522FSFwRqGdipjee/view |
| MARKETING_OS_EMPRESA_AUTOMATIZADA | doc (330 b · STUB) | `1HzGa2SyN42JEjhD2IyTzFnE4TOFZfX66` | https://drive.google.com/file/d/1HzGa2SyN42JEjhD2IyTzFnE4TOFZfX66/view |
| Blueprint_Projetos_Claude.pdf | pdf (445 b) | `1RBU28a2zMe_HL-gxvP5UgvMVKbke2wrm` | https://drive.google.com/file/d/1RBU28a2zMe_HL-gxvP5UgvMVKbke2wrm/view |

Docs de planejamento (contexto, não canônicos):
| Doc | ID | URL |
|---|---|---|
| Planejamento de projetos (síntese de ~9 respostas) | `1rZrT53425Eyyeg69yCpvx1gMN8a4Bt5HGqXLSp5Ag0U` | https://docs.google.com/document/d/1rZrT53425Eyyeg69yCpvx1gMN8a4Bt5HGqXLSp5Ag0U/edit |
| Situação CS (cargos/RH) | `1vk4YCmFNIbnGiRQYnKQ3tP_7bB9lVD2TgnO2vtABvJQ` | https://docs.google.com/document/d/1vk4YCmFNIbnGiRQYnKQ3tP_7bB9lVD2TgnO2vtABvJQ/edit |
| CS_Arquitetura_Record_Replay | `13PQIRa6wxEWZnWK79yWRWiEIIUWsH7BOCfNEQTUJKF0` | https://docs.google.com/document/d/13PQIRa6wxEWZnWK79yWRWiEIIUWsH7BOCfNEQTUJKF0/edit |
| INVENTARIO COMPLETO - Analise de Conteudo | `17UfGnQv9GOQXNor8SCPGDnEAIjIp4Om-MoVRc93n6F8` | https://docs.google.com/document/d/17UfGnQv9GOQXNor8SCPGDnEAIjIp4Om-MoVRc93n6F8/edit |

## 3. FUROS CONFIRMADOS (Drive NÃO é espelho completo)
- **AUSENTE no Drive:** `MARKETING_OS_ARQUITETURA.md` (ground truth global) — busca por título retornou vazio.
- **AUSENTE no Drive:** `PROCESSO_BASE_CLOSER.md`.
- **STUB (270–330 b):** `PLATAFORMA_COMERCIAL_ARQUITETURA`, `MARKETING_OS_EMPRESA_AUTOMATIZADA` (este diz "arquivo completo — ver Mac").
- **Conclusão:** o corpo completo dos docs mora no **Mac** (`~/Downloads/...`) e/ou **GitHub**; o Drive tem só índice + guia + 1 CS + stubs. Enforcement de sync NÃO está segurando.

## 4. CAUSA PROVÁVEL (a confirmar)
A skill de enforcement/sync provavelmente só dispara em ambiente Cowork/terminal; sessões de **chat web** gravam por fora dela → stubs e ausências. Nenhum arquivo de watchdog/auto-sync foi achado no Drive.

## 5. PENDÊNCIAS ABERTAS
1. **Recuperar fluxo de agentes/sub-agentes** (mkt, tráfego, copy, webinário, produto, funil) — provável em `MARKETING_OS_ARQUITETURA.md` / `Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md` (Mac/GitHub). Consolidar em `Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md`.
2. **Auditar e corrigir a skill de enforcement** para gravar nos 3 lugares sempre.
3. **Tornar o Drive espelho real** (subir os ausentes, engordar os stubs) — via rclone ou conector do Drive.

## 6. LIMITE DA ORIGEM
Esta sessão foi **chat web**: sem acesso ao Mac, sem git autenticado, e o conector do Drive travou na escrita ("aprovação não recebida"). Por isso o deploy foi empacotado em script para rodar na sua máquina/Cowork.
__MAN_EOF__

cat > "$PROJ/INDICE_PROJETOS.md" <<'__IDX_EOF__'
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
__IDX_EOF__

cat > "$PROJ/POLITICA_SYNC_SEGURANCA.md" <<'__POL_EOF__'
# POLÍTICA CANÔNICA — Sincronização, Segurança e Redundância
**Marketing OS · v2.2 · 2026-07-10**
**Escopo:** OBRIGATÓRIA para TUDO — skills (atuais e futuras), agentes/sub-agentes (atuais e futuros), arquiteturas de projeto (atuais e futuras) e todo código/doc canônico.

> Toda skill, agente ou projeto novo DEVE referenciar e herdar esta política. Qualquer criação/edição de arquivo canônico segue estas regras. Quem cria um projeto/skill/agente sem apontar para cá está fora do padrão.

---

## 1. TRÊS LUGARES, SEMPRE (fonte de verdade + redundância)
Todo arquivo canônico (arquitetura, código `.sh`/`.py`, skill, framework, índice, ground truth) vive, **completo e idêntico**, em:
1. **Local** (`~/Downloads/Projetos/...`) — cópia de trabalho.
2. **GitHub** (`github.com/arthurgerber/marketing-os-skills`) — versionado (backup primário).
3. **GitLab** (mirror privado — segundo remote) — redundância caso o GitHub falhe. Remote `gitlab` → `https://gitlab.com/arthur.ga94-group/marketing-os-skills.git` (JÁ CONFIGURADO em 2026-07-09).

Regra de bytes: os 3 devem bater. Nenhum arquivo nos remotes pode ter menos conteúdo que a versão canônica.

> **Drive não é mais alvo de sync de docs** (decisão 2026-07-10): serve para arquivos/vídeos/planilhas a compartilhar. A leitura dos canônicos no navegador é via GitHub/GitLab, que renderizam Markdown.

## 2. NUNCA DUPLICAR
Se o arquivo existe, **atualize/mova** — jamais crie versão paralela (`_v2`, `_final`, `copia`). Antes de criar, cheque o `INDICE_PROJETOS.md`.

## 3. VERIFICAÇÃO PÓS-ESCRITA (obrigatória)
Depois de salvar, **provar** que sincronizou:
- **Hash/bytes** iguais nos 3+ lugares (comparar `sha256`/tamanho local × Drive × repos).
- **Push confirmado**: `git rev-parse HEAD` local == `origin/main` == `gitlab/main`.
- Se algo não bater → reportar como FALHA, não como sucesso.

## 4. SNAPSHOT ANTES DE SOBRESCREVER
Antes de qualquer sobrescrita em massa:
- **Tag git** de segurança: `git tag backup-YYYYMMDD-HHMM && git push --tags` (nos dois remotes).
- Cópia timestampada local do que será alterado (`.bak/`), caso precise reverter.
Nunca sobrescreva um canônico mais completo por um menor sem sinalizar.

## 5. IDEMPOTÊNCIA
Rodar o deploy 2x não pode poluir: se o conteúdo já está igual (hash bate), **pular** — "nada a fazer".

## 6. AÇÕES QUE NÃO SÃO AUTOMÁTICAS (parar e pedir aval)
O agente **NUNCA** executa sozinho; **sinaliza** a ação exata para o Arthur fazer/aprovar:
- **Apagar/mover duplicata** → apenas sugere ("duplicata de X, remover?"). Deleção é decisão do Arthur.
- **Token/credencial** (GitHub, GitLab, rclone) → nunca escrever em script, zip, doc ou log. Fica só na máquina, o Arthur autentica na hora.
- **`rclone sync`** (apaga no destino) → proibido. Usar `rclone copy` (atualiza/adiciona, não apaga).
- **Force push, reset --hard, history rewrite** → proibido automático.

## 7. SETUP DE MÁQUINA NOVA (esposa / Mac Mini / outra)
Numa máquina nova, o código vem **da nuvem**, não copiado à mão:
1. `git clone` do GitHub (ou GitLab) → traz tudo versionado.
2. Configurar credencial/token **localmente, uma vez** (fica só naquela máquina).
3. (Opcional) `rclone config` para o Drive, se for espelhar por ali.
4. Rodar o deploy/audit para validar que os 3+ lugares batem.
Nada de token viaja em arquivo — cada máquina autentica a sua.

## 8. HERANÇA (como aplicar em tudo)
- **Ground truth global** (`MARKETING_OS_ARQUITETURA.md`) referencia esta política como regra do sistema.
- **Toda arquitetura de projeto** (`PLATAFORMA_*_ARQUITETURA.md`) inclui a linha: "Segue POLITICA_SYNC_SEGURANCA.md".
- **Toda skill nova** (`SKILL.md`) e **todo agente/sub-agente** nasce com a instrução de salvar nos 3+ lugares + verificação pós-escrita.
- A **skill de enforcement** implementa os itens 1, 3, 4, 5 automaticamente e sinaliza o item 6.
__POL_EOF__

echo "escritos/atualizados em: $MKT  e  $PROJ"

banner "9) VERIFICACAO pos-escrita (local)"
for pair in \
  "$MKT/PLATAFORMA_MARKETING_ARQUITETURA.md" \
  "$MKT/FRAMEWORK_ANALISE_COPY_LIVES.md" \
  "$MKT/MANIFESTO_HANDOFF.md" \
  "$PROJ/INDICE_PROJETOS.md" \
  "$PROJ/POLITICA_SYNC_SEGURANCA.md" ; do
  if [ -f "$pair" ]; then echo "OK  $(basename "$pair")  $(wc -c < "$pair")b  sha:$(hashof "$pair" | cut -c1-12)"; else echo "FALHA  $pair nao escrito"; fi
done

banner "10) GIT — commit + push (GitHub origin + GitLab gitlab) com confirmacao"
if [ -n "${REPO:-}" ]; then
  mkdir -p "$REPO/Projetos"; cp -R "$PROJ/." "$REPO/Projetos/"
  [ -f "$BASE/MARKETING_OS_ARQUITETURA.md" ] && cp "$BASE/MARKETING_OS_ARQUITETURA.md" "$REPO/"
  git -C "$REPO" add -A
  if git -C "$REPO" diff --cached --quiet; then echo "idempotente: nada novo a commitar";
  else git -C "$REPO" commit -m "chore(sync): espelho completo Projetos + politica v2.1 + marketing"; fi
  git -C "$REPO" push --tags 2>/dev/null || true
  for R in origin gitlab; do
    if git -C "$REPO" remote | grep -q "^$R$"; then
      git -C "$REPO" push "$R" HEAD && echo "push $R: OK" || echo "push $R: FALHOU (auth?)"
    fi
  done
  L=$(git -C "$REPO" rev-parse HEAD 2>/dev/null)
  for R in origin gitlab; do
    if git -C "$REPO" remote | grep -q "^$R$"; then
      Rr=$(git -C "$REPO" rev-parse "$R/main" 2>/dev/null || echo "?")
      [ "$L" = "$Rr" ] && echo "confirmacao $R: HEAD bate ($L)" || echo "confirmacao $R: DIVERGENTE (local=$L $R=$Rr) — verifique"
    fi
  done
else echo "repo nao encontrado — clone marketing-os-skills sob \$HOME e rode de novo"; fi

banner "11) DRIVE — desativado como alvo de sync (2026-07-10)"
echo "Drive NAO e mais alvo de sync de docs. Redundancia = Local + GitHub (origin) + GitLab (gitlab)."
echo "Drive permanece so para arquivos (videos, gravacoes, planilhas, materiais a compartilhar)."

banner "12) ACOES MANUAIS (o script NAO faz — pede seu aval)"
echo "[ ] Remover duplicatas sinalizadas na secao 6 (voce decide e apaga)."
echo "[ ] Maquina NOVA: git remote add gitlab https://gitlab.com/arthur.ga94-group/marketing-os-skills.git ; git push -u gitlab main"
echo "[ ] Autenticar git/rclone nesta maquina (token fica LOCAL, nunca em arquivo)."

banner "RESUMO FINAL"
echo "Local:$PROJ | GitHub(origin):${REPO:-<nao>} | GitLab(gitlab):$([ -n "${REPO:-}" ] && git -C "$REPO" remote | grep -q gitlab && echo ok || echo ausente)"
echo "Backup deste run: $BASE/.backups/Projetos-$TS.tar.gz + git tag backup-$TS"
echo "Politica: Projetos/POLITICA_SYNC_SEGURANCA.md | URLs Drive: Marketing/MANIFESTO_HANDOFF.md"
echo "Pendencia: consolidar fluxo de AGENTES (repo record-replay/agents/*) no PLATAFORMA_MARKETING_ARQUITETURA.md"
banner "FIM"
