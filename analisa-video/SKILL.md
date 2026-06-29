---
name: analisa-video
description: "Analisa videos E audios — 2-em-1. Identifica quem fala (closer, lead, multiplos speakers), analisa voz (pitch, ritmo, energia, nervosismo, hesitacao), linguagem nao-verbal via frames (micro-expressoes, olhar, maos, postura, decisor oculto, temperatura do lead), transcreve local sem custo. Salva JSON estruturado + TXT. Funciona com URL, arquivo local, WhatsApp (.ogg), ligacao (.mp3), call de closer, curso, YouTube, Reel, qualquer plataforma com cookies. 100% local, zero APIs pagas, escalavel para 500+ videos/dia. Usar SEMPRE que pedir: analisa esse video, analisa essa call, analisa essa ligacao, transcreve esse audio, audio do zap, modo rapido, extrai o conteudo, replica a voz, perfil vocal, quem falou, identifica o closer, identifica o lead, avalia o closer, score da call, temperatura do lead, objecoes, micro-expressoes, decisor oculto."
allowed-tools: Bash, Read, AskUserQuestion
---

# analisa-video v4 — Analista Comercial Completo

Zero APIs pagas. Tudo local. Escalável. Pronto para usar em qualquer projeto.

---

## 🚀 MODO AUTOMÁTICO — SEM TERMINAL (ESCALA REAL)

**A análise roda sem o usuário abrir o terminal:**
1. Jogue o vídeo/áudio em `~/Downloads/Analisar/`
2. LaunchAgent `com.marketingos.video` detecta e dispara análise automaticamente
3. Resultado salvo em `~/Downloads/Analises/` (JSON) + `~/Downloads/Transcricoes/` (TXT)
4. Claude lê o JSON e entrega análise completa sem intervenção manual

**Instalar o watcher (uma única vez no Terminal):**
```bash
bash ~/Downloads/Marketing_OS/scripts/instalar_video_watcher.sh
```

**Terminal só é necessário para:**
- Primeira instalação de dependências (pip3 install ...)
- Análises com flags especiais: --speakers N, --roles, --modelo large-v3
- Debug de erros específicos

**Escala:** 10, 100, 500 vídeos/dia = drop na pasta, análise automática, zero intervenção.

---

## ⚠️ REGRA ABSOLUTA — LER ANTES DE QUALQUER COISA

**Não produza análise nenhuma antes de:**
1. Rodar o script e esperar terminar
2. Ler 100% dos frames com Read (se for vídeo) — nenhum pulado
3. Ler a transcrição completa

Quem pula frames entrega análise errada. A linguagem corporal no frame 312 pode mudar tudo que aconteceu antes.

---

## PADRÃO UNIVERSAL — RECONHECIMENTO DE TERMOS

Todo matching de termos usa `grep -qiE` com regex. Nunca busca literal.

| Como o usuário pode escrever | Regex de reconhecimento |
|------------------------------|------------------------|
| minipacto, mini-pacto, Mini Pacto | `MINI.?PACTO` |
| micro-expressões, microexpressões | `MICRO.?EXPRESS` |
| decisor oculto, decisor silencioso | `DECISOR.{0,20}(OCULTO\|SILENCIOSO)` |
| fechamento, fechar | `FECHA` |
| SPEAKER_00, Speaker_00 | sempre usar `SPEAKER_00` (pyannote = MAIÚSCULO) |

---

## PASSO 0 — Verificação pré-voo

```bash
python3 ~/Downloads/Marketing_OS/scripts/preflight.py
```

Confirma que todas as dependências estão ok antes de rodar.
Se falhar → seguir as instruções de instalação que aparecem.

**HuggingFace Token (necessário para diarização de speakers):**
```bash
cat ~/Downloads/.env | grep HF_TOKEN
# Se não tiver: echo "HF_TOKEN=hf_SEU_TOKEN" >> ~/Downloads/.env
# Token gratuito em: https://huggingface.co/settings/tokens
# Aceitar termos em: https://huggingface.co/pyannote/speaker-diarization-3.1
```

---

## PASSO 1 — Setup (apenas na primeira vez)

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py"
```

Instala: faster-whisper, librosa, pyannote.audio, modelo Whisper.
Tempo: ~5 minutos na primeira vez.

---

## PASSO 2 — Executar análise

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/analisa.py" "<FONTE>" [FLAGS]
```

**FLAGS PRINCIPAIS:**
```
--so-audio                          Áudio puro (.ogg, .mp3, .wav, .m4a)
--speakers N                        Número de speakers (obrigatório para diarização)
--roles "SPEAKER_00=Closer,SPEAKER_01=Lead"   Nomear speakers
  ⚠️  ATENÇÃO: pyannote retorna SPEAKER_00 em MAIÚSCULAS — usar sempre assim
--no-diarizacao                     Pular identificação de speakers
--fast                              Modo rápido (~100 frames, para cursos longos)
--modelo small/medium/large-v3      Precisão da transcrição (default: small)
--max-frames N                      Frames totais (default: 400)
--cookies <path>                    Cookies para plataformas com login
--no-save                           Não salvar arquivos
--start MM:SS --end MM:SS          Analisar só um trecho
```

**EXEMPLOS PRÁTICOS:**
```bash
# Call de closer (caso mais comum)
python3 analisa.py "call.mp3" --so-audio --speakers 2 \
  --roles "SPEAKER_00=Closer,SPEAKER_01=Lead"

# Call com decisor oculto (3 pessoas)
python3 analisa.py "call.mp4" --speakers 3 \
  --roles "SPEAKER_00=Closer,SPEAKER_01=Lead,SPEAKER_02=Decisor"

# Áudio do WhatsApp
python3 analisa.py "audio.ogg" --so-audio

# YouTube / Reel / Vídeo de vendas
python3 analisa.py "https://youtube.com/watch?v=..."

# Plataforma com login (Hotmart, Kiwify, Teachable, etc.)
python3 analisa.py "https://hotmart.com/..." --cookies ~/Downloads/cookies.txt --fast

# Analisar só o trecho do fechamento
python3 analisa.py "call.mp4" --start 45:00 --end 60:00 --speakers 2
```

**Saída do script:**
1. Tabela de speakers: WPM, % de fala, total de palavras
2. Análise acústica: pitch, energia, expressividade
3. Lista de frames extraídos (se vídeo)
4. Transcrição com timestamps e speakers
5. Caminhos dos arquivos salvos

---

## PASSO 3 — Gerar composites e ler (OBRIGATÓRIO — NUNCA ler 400 frames individualmente)

### ❌ PROIBIDO: ler frames um a um → leva 50 minutos, trava o Mac, inescalável
### ✅ CORRETO: script gera 20 composites → Claude lê 20 imagens em ~3 minutos

```bash
# EXECUTAR OBRIGATORIAMENTE antes de qualquer leitura de frame:
SKILL_DIR="$(dirname $(find ~/Downloads/.claude/skills/analisa-video -name SKILL.md 2>/dev/null | head -1))"
python3 "$SKILL_DIR/scripts/gera_composites.py" \
  ~/Downloads/Analises/frames_[titulo]/frames/
```

Saída: `~/Downloads/Analises/frames_[titulo]/composites/composite_001.jpg` … `composite_020.jpg`
Cada composite = 20 frames em grade 4×5 com timestamps visíveis no canto de cada frame.

**Depois de gerar, ler os 20 composites com Read:**
```
Read: ~/Downloads/Analises/frames_[titulo]/composites/composite_001.jpg  (00:00–03:10)
Read: ~/Downloads/Analises/frames_[titulo]/composites/composite_002.jpg  (03:10–06:20)
... até composite_020.jpg (fim da call)
```

**⚠️ VERIFICAÇÃO OBRIGATÓRIA antes de analisar:**
- Confirme que leu TODOS os N composites (número varia com duração da call)
- Não pule nenhum composite — a câmera do lead pode ligar em qualquer momento
- Se composite tiver tela preta: anote timestamp (câmera desligada = dado comportamental)

**Benchmark:** 400 frames → 20 leituras → análise completa em ~3 min (não 50 min)

**Para CADA frame, registrar internamente:**

| O que observar | O que anotar |
|---------------|-------------|
| **OLHAR** | câmera=engajado / baixo=script ou anotações / lado=distração / cima=2º monitor |
| **MÃOS** | abertas=confiança / no rosto=nervoso / entrelaçadas=tensão / punho=determinação |
| **EXPRESSÃO** | aberta / neutra / fechada / tensa |
| **MICRO-EXPRESSÕES** | lábios comprimidos / sobrancelha franzida / olho estreitado / tensão maxilar / sorriso genuíno vs. forçado / desvio súbito de olhar / piscar excessivo |
| **POSTURA** | para frente=engajado / recostado=desengajado / mudança súbita=reação |
| **TERCEIROS** | há mais alguém? quem? qual linguagem corporal? |
| **CÂMERA** | apagou? quando (MM:SS)? quanto tempo? closer parou de falar? |

**Marcos temporais a rastrear:**
- 00:00 — abertura (estado inicial de cada pessoa)
- Revelação do preço — reação imediata (frame exato)
- Primeira objeção — mudança de postura/expressão
- Silêncio após pergunta de fechamento — quem quebrou primeiro?
- Encerramento — estado final de cada pessoa

**Só avançar para PASSO 4 após ler o último frame.**

---

## PASSO 4 — Análise visual com MULTI-AGENTES PARALELOS (padrão de escala)

### ❌ PROIBIDO: 1 subagente lendo composites sequencialmente (~10min ou mais)
### ✅ CORRETO: 4 agentes em paralelo, cada bloco simultâneo (~3min total)

**Spawnar os 4 agentes na MESMA mensagem (simultâneos):**

```
Agente 1: composites 001-005 | 00:00–25:00 | foco: abertura, qualificação, rapport
Agente 2: composites 006-010 | 25:00–47:30 | foco: apresentação, objeções iniciais
Agente 3: composites 011-015 | 47:30–54:00 | foco: câmera apaga/volta, consulta privada ← CRÍTICO
Agente 4: composites 016-020 | 54:00–63:33 | foco: fechamento, sinais de compra ← CRÍTICO
```

**Cada agente recebe:**
- Caminho dos composites: `~/Downloads/Analises/frames_[titulo]/composites/composite_00X.jpg`
- Trecho da transcrição JSON correspondente ao seu período
- Roles confirmados: Closer (lado direito) / Leads (lado esquerdo)
- O que observar: câmera on/off, micro-expressões, mãos, postura, olhar, gestos

**Agente principal depois:**
1. Mescla as 4 análises em ordem cronológica
2. Cruza com a transcrição (timestamps alinhados)
3. Gera o relatório final completo de uma vez

---

## PASSO 5 — Análise estruturada

Escolha o template conforme o tipo de conteúdo.

---

## TEMPLATE A — CALL DE CLOSER

### RESUMO EXECUTIVO (5 linhas)
```
Score geral: [X/10]
Fechou: [sim/não]
Motivo principal: [1 frase]
Maior erro: [1 frase com timestamp]
Próximo passo: [ação específica]
```

---

### DADOS OBJETIVOS DA CALL

| Speaker | Tempo de fala | % | WPM | Papel |
|---------|--------------|---|-----|-------|
| [nome] | [Xmin Ys] | [X%] | [X] | Closer / Lead / Decisor oculto |

⚠️ **ALERTA AUTOMÁTICO:**
- Closer > 70% do tempo → monólogo de vendas (ponto negativo)
- Lead < 20% → não engajou ou foi silenciado
- Decisor oculto identificado nos frames → foi incluído?

---

### ANÁLISE VOCAL SOB PRESSÃO

**Closer:**
- WPM na abertura vs. no momento do preço: [comparar — acelerou = nervoso]
- Tom ao revelar o preço: [confiante / hesitante / defensivo]
- Vocabulário fraco identificado: ["né?", "tipo assim", "então", "basicamente"] — quantas vezes?
- Vocabulário de poder usado: ["estrategistas", "gestores de tráfego", "agente de produto"]
- Silêncio estratégico: usou silêncio após pergunta de fechamento? [sim/não — duração]
- Voz subiu (agudizou) em algum momento de pressão? [sim/não — quando: MM:SS]

**Lead:**
- Tom geral: [receptivo / cético / fechado]
- Mudança de tom após revelar preço: [qual foi]
- Monossilábicos ("sim", "não", "tá") — sinal de desengajamento?

---

### LINGUAGEM NÃO-VERBAL — EVOLUÇÃO POR MOMENTO

**ABERTURA [00:00–MM:SS]**
- Closer: [postura, olhar, energia inicial]
- Lead: [câmera ligada/desligada, expressão inicial, postura]

**RAPPORT [MM:SS–MM:SS]**
- Closer: [gestos, espelhamento com o lead, energia]
- Lead: [engajamento crescente ou queda?]

**REVELAÇÃO DO PREÇO [MM:SS]**
- Closer: [mudança de postura antes de falar o valor? acelerou a fala?]
- Lead: [reação imediata nos primeiros 3s — frame exato]
- Micro-expressão do lead no frame do preço: [específico]

**OBJEÇÕES [MM:SS–MM:SS]**
- Lead: [postura fechou? câmera apagou? olhar desviou?]
- Closer: [recuou? ficou firme? linguagem corporal de defesa?]

**FECHAMENTO [MM:SS–MM:SS]**
- Closer: [fez a pergunta de decisão? ficou em silêncio depois?]
- Lead: [quem quebrou o silêncio? em quanto tempo?]
- Estado final de cada pessoa no último frame

---

### TEMPERATURA DO LEAD (0–10 por momento)

| Momento | Temperatura | O que indicou |
|---------|------------|---------------|
| Abertura | [X]/10 | |
| Pós-rapport | [X]/10 | |
| Durante apresentação | [X]/10 | |
| Revelação do preço | [X]/10 | |
| Pós-objeção | [X]/10 | |
| Fechamento | [X]/10 | |

> 7 = pronto para fechar | 5–6 = precisa de mais aquecimento | < 5 = não qualificado ou mal trabalhado

---

### AVALIAÇÃO PONTO A PONTO

**[1] Abertura [00:00–MM:SS]**
- Se apresentou? (nome + empresa — não revelou idade?) [sim/não]
- Áudio e câmera funcionando desde o início? [sim/não]
- Pediu para o lead abrir a câmera? [sim/não — quando: MM:SS]
- Tom de abertura: [energético / neutro / inseguro]

**[2] Rapport e Investigação [MM:SS–MM:SS]**
- Duração: [X min] — Mínimo esperado: 10–15 min
- O que descobriu: [vida, família, histórico, sonhos, dores reais]
- Foi natural ou virou questionário? [natural / questionário]
- Perguntou se conhece a empresa/Julia antes de apresentar? [sim/não]
- Nível de profundidade: [superficial / médio / profundo]

**[3] Qualificação Profunda [MM:SS–MM:SS]**
- Investigou objetivo financeiro real? [sim/não]
- Identificou a dor principal? [qual foi]
- Perguntou o que já tentou e por que não deu certo? [sim/não]
- Revelou capacidade de investimento? [sim/não — valor mencionado]
- Identificou o decisor real? [sim/não — quem é]

**[4] Decisor Oculto/Silencioso**
- Havia mais alguém na call? [sim/não — quem]
- Foi cumprimentado e incluído desde o início? [sim/não]
- Closer usou isolamento: "Se dependesse só de você, estaria 100%?" [sim/não]
- Câmera de terceiro ligada? [sim/não — reação nos frames quando o preço foi revelado]

**[5] Apresentação [MM:SS–MM:SS]**
- Começou antes de qualificar completamente? [sim/não — quando: MM:SS]
- Vinculou ao objetivo declarado pelo lead? [sim/não — como]
- Adaptou linguagem ao nível do lead? [sim/não]
- Usou vocabulário correto: "estrategistas / gestores de tráfego / agente de produto"? [sim/não]
- Duração da apresentação: [X min] — foi proporcional à qualificação?

**[6] Gatilhos de Compra Ativados**
- Escassez: [usou? quando? MM:SS] — foi crível ou forçado?
- Urgência: [usou? quando? MM:SS]
- Prova social: [depoimentos/resultados mencionados? quais?]
- Autoridade: [como estabeleceu credibilidade?]
- Reciprocidade: [deu algo de valor antes de pedir o fechamento?]

**[7] Minipactos [MM:SS–MM:SS]**
- Usou perguntas de comprometimento progressivo? [sim/não]
- Exemplos reais usados na call: [transcrever as perguntas]
- Usou "tem alguma dúvida?" ou "ficou claro?" (fraco — não compromete)? [sim/não]
- Quantos minipactos conseguiu antes do fechamento? [número]

**[8] Objeções [MM:SS–MM:SS]**

| Objeção | Categoria | Como tratou | Resolveu? |
|---------|-----------|-------------|-----------|
| [texto] | PREÇO / TEMPO / CÔNJUGE / CONFIANÇA / NÃO PRECISA | [resposta] | sim/não |

- Se contradisse em algum momento? [sim/não — o quê e quando]
- Criou mais objeções ao tratar uma? [sim/não]

**[9] Fechamento [MM:SS–MM:SS]**
- Fez pergunta explícita de decisão? [sim/não — qual foi]
- Ficou em silêncio após a pergunta? [sim/não — quem quebrou: MM:SS]
- Como terminou: [fechou / desconectou / próximo passo / sem definição]
- Lead ficou confuso sobre o que fazer em seguida? [sim/não]

**[10] Próximo Passo**
- Saiu com data e hora concretas? [sim/não]
- O que ficou combinado: [específico]
- Script de FUP recomendado: [texto que inclui todos os decisores e a dor revelada]

---

### SCORE POR CRITÉRIO

| Critério | Nota /10 | Maior erro identificado |
|----------|----------|------------------------|
| Abertura e apresentação | | |
| Rapport e investigação | | |
| Qualificação profunda | | |
| Identificação do decisor | | |
| Adaptação da apresentação | | |
| Gatilhos de compra | | |
| Minipactos | | |
| Tratamento de objeções | | |
| Fechamento explícito | | |
| Próximo passo definido | | |
| **SCORE TOTAL** | **/10** | |

---

### RECOMENDAÇÕES DE COACHING
[3–5 pontos específicos com o timestamp exato e o que deveria ter sido feito diferente]

Exemplo de formato:
- **[32:14] Revelação do preço sem silêncio estratégico**: falou o valor e continuou falando imediatamente. Deveria ter dito o valor, fechado a boca e esperado o lead reagir. O silêncio força o lead a processar e revelar objeção real.

---

## TEMPLATE B — VÍDEO DE VENDAS / WEBINÁRIO

### RESUMO EXECUTIVO
- Objetivo do vídeo: [1 frase]
- Público-alvo: [perfil]
- Framework principal: [Perfect Webinar / AIDA / PAS / Story Selling / VSL / outro]
- Score: [/10]

### VOZ E TONALIDADE
- Ritmo médio: [WPM] — [lento < 120 / normal 130-160 / rápido > 170]
- Pitch base: [Hz] — [grave < 150Hz / médio 150-250Hz / agudo > 250Hz]
- Expressividade: [monótona / moderada / expressiva]
- Curva de energia: [descrever o arco — começa alta? cai no meio? sobe no CTA?]
- Momentos de pico de expressividade: [MM:SS — o que disse]
- Perfil vocal em 3 linhas: [para replicação]

### LINGUAGEM NÃO-VERBAL (frames)
- Postura dominante: [ereta / dinâmica / relaxada]
- Padrão de gestos: [ilustrativos / ausentes / defensivos / abertos]
- Contato visual com câmera: [direto / indireto / frequência estimada]
- Enquadramento: [muito fechado / ideal / muito aberto]
- Iluminação: [profissional / amadora / inadequada]
- Elementos de autoridade no ambiente: [livros, diplomas, escritório, outdoor, etc.]
- Micro-expressões recorrentes: [identificar padrão]

### ESTRUTURA DO CONTEÚDO
| Elemento | Timestamp | Duração | Avaliação |
|---------|-----------|---------|-----------|
| Hook | 00:00 | Xs | [forte/fraco — por quê] |
| Big Promise | | | |
| Credencial/Autoridade | | | |
| Problema agitado | | | |
| Solução apresentada | | | |
| Prova social | | | |
| Oferta + preço | | | |
| Bônus/urgência | | | |
| CTA | | | |

### INSIGHTS ESTRATÉGICOS
- 3 ângulos mais fortes do conteúdo:
- 3–5 hooks prontos para testar (baseados no conteúdo):
- Formatos recomendados para recorte: [Reel / carrossel / stories / VSL curto]
- O que o concorrente não faz que este faz:

---

## TEMPLATE C — AULA / CURSO (modo rápido)

- Tema central: [1 frase]
- Frameworks ensinados: [listar com timestamp]
- Cases e exemplos usados: [listar]
- Referências citadas: [listar]
- Vocabulário específico do nicho: [listar termos próprios]
- 5 takeaways imediatos para aplicar:
  1. [timestamp] ...
  2. [timestamp] ...
  3. [timestamp] ...
  4. [timestamp] ...
  5. [timestamp] ...

---

## PERFIL VOCAL PARA REPLICAÇÃO

Usar após analisar 2–3 vídeos/áudios da mesma pessoa:

```
PERFIL VOCAL — [Nome]
════════════════════════════════
Ritmo: [WPM médio] wpm
Pitch: [Hz] — [grave/médio/agudo]
Expressividade: [monótona/moderada/expressiva]

Cadência típica de frase:
  [descrever: começa calmo, acelera no ponto principal, pausa dramática]

Vocabulário característico:
  [lista de palavras/expressões que usa frequentemente]

Abertura padrão:
  [como começa — ex: "Deixa eu te contar uma coisa..."]

Estrutura favorita:
  [como constrói argumento — ex: problema → agitação → solução → prova → CTA]

Tom dominante: [confiante / didático / urgente / empático / desafiador]

Pausas estratégicas: [onde usa — ex: "após revelar resultado, pausa de 2s"]

Para usar: "Escreva [tipo de conteúdo] seguindo este perfil vocal: [colar perfil]"
```

---

## PLATAFORMAS COM LOGIN

Funciona com qualquer plataforma onde você loga no Chrome:
Hotmart, Kiwify, Eduzz, Monetizze, Teachable, Thinkific, Kajabi, Udemy, YouTube privado, membros WordPress, qualquer outra.

**Como exportar cookies:**
1. Chrome: instale "Get cookies.txt LOCALLY"
2. Faça login na plataforma
3. Clique na extensão → Export
4. Salve como `cookies.txt`
5. Use: `--cookies ~/Downloads/cookies.txt`

Se a plataforma bloquear mesmo com cookies:
- Grave a tela com QuickTime enquanto assiste → analise o arquivo gravado

---

## ARQUIVOS SALVOS AUTOMATICAMENTE

```
~/Downloads/Analises/analise_[titulo]_[data].json    ← dados estruturados (JSON)
~/Downloads/Transcricoes/transcricao_[titulo]_[data].txt  ← transcrição legível
~/Downloads/Analises/frames_[titulo]/frame_XXXX.jpg  ← frames (permanentes, nunca deletar)
```

**O JSON contém:** speakers, métricas de voz por speaker, segmentos com timestamps, dados acústicos — pronto para integrar em banco de dados ou leitura por outro agente.

Para desativar JSON/TXT: `--no-save`
Frames sempre salvos quando vídeo — são ativos de análise permanentes.

---

## PADRÃO UNIVERSAL — RECONHECIMENTO DE TERMOS

Todos os termos abaixo são equivalentes e devem ser reconhecidos independente de capitalização ou grafia:

| Conceito | Regex `grep -qiE` |
|----------|-------------------|
| Padrão Universal | `PADR.O UNIVERSAL` |
| Regra Absoluta | `REGRA ABSOLUTA` |
| Micro-expressões | `MICRO.?EXPRESS` |
| Decisor oculto | `DECISOR.{0,20}(OCULTO\|SILENCIOSO)` |
| Mini-pacto | `MINI.?PACTO` |
| Speaker pyannote | `SPEAKER_\d+` — SEMPRE maiúsculo |

---

## ANTES DE ENTREGAR — PROTOCOLO OBRIGATÓRIO

1. Rodar **auto-qa** no que foi criado/modificado
2. Re-testar após qualquer correção
3. Só apresentar quando tudo verde
4. Para desenvolvimento técnico: usar skill **devstack**


---

## ⚡ CHECKLIST OBRIGATÓRIO — ANTES DE QUALQUER ENTREGA

**O agente NÃO entrega sem confirmar todos os itens abaixo:**

- [ ] Todos os passos desta skill foram executados como scripts (não improvisados)
- [ ] Output esperado existe e foi verificado (não apenas gerado)
- [ ] Nenhum passo foi pulado, abreviado ou substituído por "equivalente mais rápido"
- [ ] Erros encontrados foram reportados — nunca suprimidos
- [ ] auto-qa rodou e aprovou antes da entrega

```bash
# Validar antes de entregar:
python3 ~/Downloads/.claude/skills/auto-qa/scripts/check.py 2>/dev/null || \
  echo "Rodar auto-qa manualmente — skill/scripts/check.py"
```

**Por que isso existe:** instruções em texto podem ser ignoradas por agentes. Scripts executados produzem output verificável — ou falham visivelmente. Este checklist converte intenção em obrigação técnica que não pode ser improvisada.
