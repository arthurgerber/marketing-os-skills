# MARKETING ESTRATÉGICO & OPERACIONAL — Arquitetura Completa
**Projeto:** Marketing Estratégico & Operacional — Grupo Silva / Lazari / VR  
**Responsável:** Arthur Gerber  
**Última atualização:** 2026-06-29  

> Este arquivo é a memória permanente do projeto. Toda nova sessão deve começar lendo este arquivo.

---

## 🔒 PADRÃO UNIVERSAL DE RECONHECIMENTO — OBRIGATÓRIO EM TODO O SISTEMA

> **Regra permanente.** Aplica-se a TODA skill, TODO agente, TODO script, TODA validação, TODA busca de texto neste projeto. Sem exceção.

### Problema resolvido
Palavras-chave do projeto podem ser escritas de formas diferentes por pessoas diferentes:  
`minipactos` / `mini-pactos` / `Minipactos` / `MINIpactos` / `Mini Pactos` → **todas são a mesma coisa**.

**Nunca usar busca literal exata para palavras do domínio. Sempre usar regex case-insensitive que tolera variações.**

### Padrões regex aprovados (usar em grep -qiE, Python re.search com re.I, etc.)

| Conceito | Regex | Pega |
|----------|-------|------|
| Minipacto | `MINI.?PACTO` | minipacto, mini-pacto, Mini Pacto, MINIpacto, etc. |
| Micro-expressões | `MICRO.?EXPRESS` | micro-expressões, microexpressões, Micro-Expressões, etc. |
| Decisor oculto | `DECISOR.*(OCULTO\|SILENCIOSO\|HIDDEN)` | decisor oculto, Decisor Silencioso, etc. |
| Fechamento | `FECHA(MENTO\|R)` | fechamento, fechar, Fechamento, FECHAMENTO |
| Próximo passo | `PR[OÓ]XIMO.?PASSO` | próximo passo, Proximo Passo, PRÓXIMO PASSO |
| Score/avaliação | `SCORE\|AVALIA` | score, Score, SCORE, avaliação, Avaliação |
| Rapport | `RAPPORT\|CONEXÃO\|CONEXAO` | rapport, Rapport, conexão, conexao |
| Qualificação | `QUALIFICA` | qualificação, qualificar, Qualificação |

### Regra para validações em scripts (bash e Python)

**Bash:**
```bash
grep -qiE "MINI.?PACTO" arquivo.md && echo "encontrado" || echo "ausente"
```

**Python:**
```python
import re
if re.search(r"MINI.?PACTO", texto, re.IGNORECASE):
    print("encontrado")
```

### Regra para Claude (leitura de documentos e análise)

Ao buscar conceitos em transcrições, documentos ou templates:
- Reconhecer TODAS as grafias como equivalentes
- Nunca marcar ausente um conceito só porque a grafia diverge
- Normalizar internamente antes de avaliar presença/ausência

### Como este padrão sobrevive a resets, atualizações e fechamentos

Este padrão está gravado em **3 locais permanentes**:

| Onde | Arquivo | O que protege |
|------|---------|---------------|
| **Downloads (persistente)** | `~/Downloads/MARKETING_OS_ARQUITETURA.md` | Memória permanente do projeto — toda sessão lê este arquivo |
| **Backup da skill** | `~/Downloads/Marketing_OS/skill_backups/SKILL_analisa-video.md` | LaunchAgent restaura isso automaticamente a cada login do Mac |
| **Skill instalada** | `analisa-video.skill` salva no Cowork | Carregada em toda nova sessão Cowork |

**Se o Cowork atualizar:** LaunchAgent restaura os backups (que já têm este padrão) automaticamente.  
**Se fechar e abrir nova sessão:** Cowork carrega a skill salva (que já tem este padrão).  
**Se formatar o Mac:** `~/Downloads/` deve ser mantido — contém toda a base do projeto.

---

---

## VISÃO GERAL

Duas plataformas de automação inteligente que operam como setores de uma empresa real — cada uma independente, com seus próprios agentes e líderes, mas conectadas por infraestrutura compartilhada e um Agente Diretor que coordena decisões cruzadas.

**Duas plataformas Claude Code independentes:**
- **Marketing Estratégico & Operacional** — campanhas, conteúdo, posicionamento, estratégia
- **Avaliação Comercial** — análise de calls, coaching de closers, métricas de vendas

**Como se comunicam:** Via Agente Diretor (tempo real) + AWS RDS PostgreSQL (persistência). Comercial detecta padrão de objeções → Diretor repassa → Marketing cria conteúdo → Comercial aplica → Diretor monitora resultado.

**Escala:** 300 calls/dia (~9.000/mês). Zero custo de transcrição (Whisper local + cache). Claude Haiku para análise (~R$900-1.500/mês).

**Empresas atendidas:** Grupo VR | Grupo Silva | Grupo Lazari (cada uma com processos próprios configurados no banco).

---

## 🚨 AGENTE MONITOR — WATCHDOG DA PLATAFORMA

> **Função:** Detecta falhas em tempo real, aciona os agentes corretores, garante que a plataforma nunca "funciona mas com dados errados".

### Como funciona

```
OUTPUT de qualquer agente
        ↓
[WATCHDOG] valida estrutura + campos obrigatórios
        ↓
    OK? → continua normalmente
    FALHA? → aciona AGENTE DEBUGGER com contexto completo
                ↓
          Debugger investiga causa raiz
                ↓
          Aplica correção automática se possível
                ↓
          Não conseguiu? → escala para Arthur (alerta humano)
```

### Agentes do sistema de monitoramento

| Agente | Papel | Quando aciona |
|--------|-------|---------------|
| **Watchdog** | Valida todo output antes de usar | Após cada análise |
| **Debugger** | Investiga causa raiz do bug | Quando Watchdog detecta falha |
| **Corretor** | Aplica fix e re-valida | Após Debugger identificar causa |
| **Alertador** | Notifica Arthur (Slack/WhatsApp) | Quando Corretor não consegue resolver |

### O que o Watchdog valida em cada análise

```python
VALIDACOES_OBRIGATORIAS = {
    "analisa-video": {
        "speakers": lambda v: v is not None and len(v) > 0,
        "transcricao_segmentos": lambda v: v is not None and len(v) > 10,
        "voz_global": lambda v: v is not None and v.get("wpm", 0) > 0,
        "duracao_s": lambda v: v is not None and v > 0,
    },
    "fup-mensal": {
        "leads": lambda v: v is not None,
        "closer": lambda v: v is not None and len(v) > 0,
    }
    # Adicionar validações para cada agente novo
}

# Se qualquer validação falhar:
# → log detalhado com valores reais
# → aciona Debugger com: agente, input, output, erro esperado vs recebido
# → NUNCA passa output inválido para o próximo agente na cadeia
```

### Fluxo de correção automática

O Debugger ao ser acionado:
1. Roda o `preflight_analisa.py --test-pipeline` para checar dependências
2. Verifica logs de erro no stderr (onde falhas silenciosas aparecem)
3. Tenta re-executar com parâmetros alternativos
4. Se identificar breaking change de lib → aplica fix (como o `fix_diarize.py`)
5. Re-executa a análise que falhou e valida o output
6. Se não resolver em 3 tentativas → alerta Arthur com diagnóstico completo

### Alerta para Arthur (quando humano precisa intervir)

```
🚨 ALERTA — PLATAFORMA

Agente: analisa-video
Call: Marcos Rosa + Milena Almeida (2026-05-28)
Falha: speakers = null (diarização não retornou dados)
Causa identificada: huggingface_hub 0.23 — breaking change em use_auth_token=
Tentativas de correção: 3 (todas falharam)
Arquivo de diagnóstico: ~/Downloads/debug_20260629_0310.json

Ação necessária: aprovação para atualizar diarize.py
```

---

## DECISÃO DE ARQUITETURA — UMA PLATAFORMA, MÚLTIPLOS AGENTES POR EMPRESA

**Decisão (2026-06-29):** Uma única plataforma com agentes dedicados por empresa (VR, Silva, Lazari). Cada empresa tem seu próprio agente coordenador + sub-agentes especializados. Se necessário no futuro, o projeto de cada empresa pode ser extraído e implantado de forma independente.

**Vantagens dessa estrutura:**
- Infraestrutura única — manutenção centralizada
- Agentes podem compartilhar aprendizados entre empresas
- Escalável: adicionar nova empresa = adicionar novo conjunto de agentes
- Portabilidade: qualquer empresa pode virar projeto standalone se o sócio quiser

**Como a call chega ao sistema:**
- **Automático** — sistema monitora pastas do Google Drive por empresa
- Quando nova gravação detectada → agente inicia análise sem intervenção manual
- Resultado vai direto para o dashboard da empresa correspondente
- Zero processo manual ou operacional

---

## ESTRUTURA — UMA PLATAFORMA, AGENTES POR EMPRESA

> **Princípio:** Uma plataforma central com agentes dedicados por empresa. Cada empresa tem coordenador próprio + sub-agentes. Base técnica compartilhada. Portável para deploy independente se necessário.

```
╔══════════════════════════════════════════════════════════════════╗
║              BASE COMPARTILHADA — INFRAESTRUTURA                 ║
║                                                                  ║
║  AGENTES CORE (servem ambas as plataformas):                    ║
║  • analisa-video  → vídeos, calls, áudios, frames               ║
║  • watchdog       → monitora outputs, aciona debugger            ║
║  • debugger       → investiga falhas, aplica correções           ║
║  • alertador      → notifica Arthur quando escala                ║
║                                                                  ║
║  INFRAESTRUTURA:                                                 ║
║  • GitHub privado (código)                                       ║
║  • AWS RDS PostgreSQL São Paulo (dados — LGPD ok)               ║
║  • AWS EC2 Spot São Paulo (processamento pesado)                 ║
╚══════════════╦═══════════════════════════╦═════════════════════╝
               ║                           ║
               ▼                           ▼
╔══════════════════════╗       ╔═══════════════════════════╗
║  PLATAFORMA 1        ║       ║  PLATAFORMA 2             ║
║  Marketing           ║       ║  Avaliação Comercial      ║
║  Estratégico &       ║       ║  (construir depois)       ║
║  Operacional         ║       ║                           ║
║                      ║       ║  Agentes próprios:        ║
║  Agentes próprios:   ║       ║  • Coaching de closers    ║
║  • Estratégia        ║       ║  • FUP de leads           ║
║  • Conteúdo          ║       ║  • Score de performance   ║
║  • Distribuição      ║       ║  • Relatórios gerenciais  ║
║  • Performance       ║       ║                           ║
║  • Webinários        ║       ║  Grupos atendidos:        ║
║                      ║       ║  VR | Silva | Lazari      ║
╚══════════╦═══════════╝       ╚═══════════╦═══════════════╝
           ║                               ║
           ║    COMUNICAÇÃO ENTRE           ║
           ╚═══════ PLATAFORMAS ═══════════╝
                        ║
                        ▼
              ┌─────────────────┐
              │  AWS RDS (SP)   │
              │  Banco único    │
              │  fonte de       │
              │  verdade        │
              └─────────────────┘
```

### Hierarquia de agentes — estrutura de empresa real

```
                        ARTHUR
                    (dono / decisões
                     estratégicas)
                          │
                          │ só aciona quando
                          │ agentes não resolvem
                          ▼
              ┌───────────────────────┐
              │   AGENTE DIRETOR      │
              │   (visão global,      │
              │    prioridades,       │
              │    aprendizados)      │
              └───────────┬───────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  COORDENADOR │  │  COORDENADOR │  │  AGENTE      │
│  Marketing   │  │  Comercial   │  │  SUPORTE     │
│              │  │              │  │  (watchdog   │
│  ↓ delega    │  │  ↓ delega    │  │   debugger   │
│              │  │              │  │   alertador) │
│ • Estratégia │  │ • Coaching   │  └──────────────┘
│ • Conteúdo   │  │ • FUP        │
│ • Performance│  │ • Score      │
│ • Distribuição│ │ • Relatórios │
└──────────────┘  └──────────────┘
          │               │
          └───────┬───────┘
                  ▼
         AGENTES CORE
         (compartilhados)
         • analisa-video
         • fup-mensal
         • outros a contratar
                  │
                  ▼
          AWS RDS (banco)
          persistência e
          memória da empresa
```

### Como funciona na prática (fluxo real)

**Tarefa simples (dentro de um setor):**
```
Arthur → Coordenador Comercial → analisa-video
                                       ↓
                                  JSON com speakers
                                       ↓
                              Coordenador → resultado para Arthur
```
Sem burocracia. Vai direto.

**Tarefa cruzada (dois setores):**
```
Arthur → Agente Diretor
              ↓
    "quais objeções mais comuns essa semana
     e o que Marketing pode criar para isso?"
              ↓
    Diretor → Coordenador Comercial
                    ↓
              analisa 50 calls → extrai objeções
                    ↓
    Diretor → Coordenador Marketing
                    ↓
              cria scripts, posts, VSLs
                    ↓
    Diretor → resultado consolidado para Arthur
```

**Bug ou falha:**
```
analisa-video retorna speakers: null
       ↓
   Watchdog detecta
       ↓
   Debugger investiga → tenta fix automático
       ↓
   Corrigiu? → avisa Coordenador → re-executa
   Não corrigiu? → Alertador → Arthur com diagnóstico
```

**Aprendizado entre plataformas:**
```
Comercial: "objeção de preço aumentou 40% essa semana"
       ↓
   Diretor captura e repassa
       ↓
Marketing: "ajusta ângulo da oferta + cria conteúdo de valor percebido"
       ↓
   Comercial aplica nas próximas calls
       ↓
   Diretor monitora se objeção caiu
```

### Regra anti-burocracia

| Situação | Caminho | Quem NÃO acionar |
|----------|---------|------------------|
| Tarefa simples no setor | Direto ao especialista | Diretor, Arthur |
| Tarefa cruzada | Diretor coordena | Arthur (a menos que seja estratégico) |
| Bug técnico | Watchdog → Debugger → Corretor | Arthur (a menos que 3 tentativas falharam) |
| Decisão estratégica | Arthur | — |

### Modelo de "contratação" de agentes

Começa enxuto. Contrata conforme necessidade real — igual a uma empresa.

**Contratados agora (MVP):**
- analisa-video, fup-mensal, watchdog

**Próximas contratações — Comercial:**
- agente-coaching, agente-score, agente-fup-inteligente, coordenador-comercial

**Próximas contratações — Marketing:**
- agente-conteudo, agente-performance, agente-estrategia, coordenador-marketing

**Regra:** Primeiro faz manual (skill), quando vira rotina cria o agente. Não contrata antes de precisar.

---

## 🔧 STATUS — analisa-video

### Fixes aplicados (permanentes via fix_diarize_v2.py)

| Fix | Problema | Solução aplicada |
|-----|----------|-----------------|
| ✅ cache de transcrição | Re-transcrevia toda call em cada re-run | fix_cache.py aplicado — pula Whisper se cache existe |
| ✅ huggingface_hub ≥ 0.23 | use_auth_token= removido → diarização silenciosamente null | Patch no hf_hub_download: converte use_auth_token → token automaticamente |
| ✅ pyannote 3.1 API | Pipeline.from_pretrained não aceita token= | Chama com use_auth_token= (API correta para v3.1) |
| ✅ torch ≥ 2.6 | weights_only=True quebra carregamento de modelos antigos | Patch torch.serialization.load + auto-descoberta iterativa de safe globals |
| ✅ token HuggingFace | Nunca foi configurado → diarização null sem aviso | Salvo em ~/.config/watch/.env e ~/.huggingface/token |
| ✅ segmentation-3.0 | Modelo dependente também exige aceite de termos | Aceito em huggingface.co/pyannote/segmentation-3.0 |

### Scripts de fix disponíveis

| Script | Função |
|--------|--------|
| `fix_diarize_v2.py` | Patch permanente no diarize.py — todos os fixes acima |
| `fix_cache.py` | Adiciona cache de transcrição ao analisa.py |
| `fix_diarize.py` | Fix inicial use_auth_token (substituído pelo v2) |
| `fix_e_baixa_pyannote.py` | Baixa o modelo pyannote com todos os patches ativos |
| `preflight_analisa.py` | Valida instalação antes de rodar análise |

### Fixes adicionais aplicados (2026-06-29, sessão 2)

| Fix | Problema | Solução aplicada |
|-----|----------|-----------------|
| ✅ patch v3 — ordem de módulo | `_patch_all_version_conflicts()` chamado DEPOIS do import do pyannote → pyannote capturava referência local ANTES do patch → diarização silenciosamente null | Chamada movida para nível do módulo (antes de `def diarizar()`), via `fix_diarize_v3.py` |
| ✅ frames permanentes | Frames iam para `/tmp/analisa_*/frames/` e eram deletados com `shutil.rmtree` ao final | `fix_frames_permanente.py` — frames vão para `~/Downloads/Analises/frames_[titulo]/`, cleanup desabilitado permanentemente |
| ✅ gate de leitura de frames | SKILL.md não bloqueava análise antes de ler frames → Claude produzia análise sem ver os frames | `fix_skill_gate_frames.py` — PASSO 3 virou gate hard no SKILL.md |
| ✅ roles case-sensitivity | `--roles "Speaker_00=Nome"` falhava porque pyannote retorna `SPEAKER_00` (maiúsculas) → lookup falha silenciosamente | SKILL.md corrigido para `SPEAKER_00` maiúsculas |

### Scripts de fix disponíveis

| Script | Localização | Função |
|--------|------------|--------|
| `fix_diarize_v2.py` | ~/Downloads/ e ~/Downloads/Marketing_OS/scripts/ | Patch permanente no diarize.py — fixes de huggingface_hub e torch |
| `fix_diarize_v3.py` | ~/Downloads/ e ~/Downloads/Marketing_OS/scripts/ | Move chamada de patch para nível do módulo (ordem crítica) |
| `fix_frames_permanente.py` | ~/Downloads/ e ~/Downloads/Marketing_OS/scripts/ | Frames permanentes em ~/Downloads/Analises/frames_[titulo]/ |
| `fix_skill_gate_frames.py` | ~/Downloads/ e ~/Downloads/Marketing_OS/scripts/ | Atualiza SKILL.md com gate de leitura obrigatória de frames |
| `fix_frames_taxa.py` | ~/Downloads/ e ~/Downloads/Marketing_OS/scripts/ | Default 400 frames, checklist micro-expressões no aviso |
| `fix_cache.py` | ~/Downloads/ | Adiciona cache de transcrição ao analisa.py |
| `fix_e_baixa_pyannote.py` | ~/Downloads/ | Baixa o modelo pyannote com todos os patches ativos |
| `preflight_analisa.py` | ~/Downloads/ e ~/Downloads/Marketing_OS/scripts/ | Valida instalação antes de rodar análise |

### Sistema de proteção permanente (anti-perda)

**Problema:** Arquivos da skill ficam em `/var/folders/...` (gerenciado pelo Cowork). Update do plugin = reset dos arquivos = todos os fixes perdidos.

**Solução em 3 camadas:**

| Camada | O que protege | Como funciona |
|--------|--------------|---------------|
| **Backup permanente** | Cópias dos arquivos modificados | `~/Downloads/Marketing_OS/skill_backups/` — diarize.py, analisa.py, SKILL.md |
| **Script de restauração** | Reaplica tudo em 1 comando | `~/Downloads/Marketing_OS/scripts/restaurar_tudo.sh` — busca skill dinamicamente, restaura backups, roda fix scripts, valida integridade |
| **LaunchAgent macOS** | Restauração automática no login | `~/Library/LaunchAgents/com.marketingos.restore.plist` — roda restaurar_tudo.sh a cada login, 30s após iniciar (tempo para Cowork carregar) |

**Instalar o LaunchAgent (rodar UMA VEZ no Terminal):**
```bash
bash ~/Downloads/Marketing_OS/scripts/instalar_launchagent.sh
```
Após isso: toda vez que o Mac iniciar, os fixes são replicados automaticamente. Zero ação manual.

**Restaurar manualmente (se necessário):**
```bash
bash ~/Downloads/Marketing_OS/scripts/restaurar_tudo.sh
```

**Atualizar backups após novos fixes:**
```bash
SKILL=$(find /var/folders -path "*/skills/analisa-video" -type d 2>/dev/null | head -1)
cp "$SKILL/SKILL.md" ~/Downloads/Marketing_OS/skill_backups/SKILL_analisa-video.md
cp "$SKILL/scripts/diarize.py" ~/Downloads/Marketing_OS/skill_backups/diarize.py
cp "$SKILL/scripts/analisa.py" ~/Downloads/Marketing_OS/skill_backups/analisa.py
```

**Este padrão se aplica a TODA nova skill e agente:**
- Toda vez que um arquivo de skill/agente for modificado → atualizar o backup em `~/Downloads/Marketing_OS/skill_backups/`
- Toda vez que um fix script novo for criado → adicionar ao `restaurar_tudo.sh`
- O LaunchAgent cobre tudo automaticamente

### Melhorias pendentes

| # | Problema | Fix planejado |
|---|----------|---------------|
| 1 | Re-análise parcial impossível | Flags: --so-frames, --so-voz |
| 2 | Densidade extra automática em momentos-chave | Detectar timestamps de preço/objeção na transcrição → extrair 1 frame/2s nessas janelas |

---

## ⚠️ LIÇÃO DE PROCESSO — incompatibilidades de versão

**Nunca assumir que dependências são compatíveis.** Antes de rodar qualquer skill nova ou após atualização de libs, mapear a matriz de compatibilidade:

```
pyannote.audio 3.1.x:
  - Pipeline.from_pretrained(use_auth_token=)   ← NÃO aceita token=
  - Internamente chama hf_hub_download(use_auth_token=)

huggingface_hub ≥ 0.23:
  - Removeu use_auth_token= de hf_hub_download  ← breaking change

torch ≥ 2.6:
  - torch.load defaults weights_only=True        ← breaking change
  - Modelos antigos do pyannote precisam de weights_only=False

SOLUÇÃO DEFINITIVA:
  Patch _patch_all_version_conflicts() injetado no diarize.py
  Auto-descoberta iterativa de safe globals (funciona com qualquer versão)
```

**Quando criar nova skill que usa pyannote/torch/HF:**
1. Incluir `_patch_all_version_conflicts()` desde o início
2. Rodar `preflight_analisa.py` antes do primeiro uso
3. Verificar termos aceitos em TODOS os modelos dependentes (não só o principal)

---

## MÓDULOS DO MARKETING OS

| # | Módulo | Status | Descrição |
|---|--------|--------|-----------|
| 1 | **analisa-video** | ✅ v3 instalada | Analisa vídeos e áudios: frames, voz, diarização, transcrição |
| 2 | fup-mensal | ✅ instalada | Gera planilhas de FUP por closer (VR, Silva, Lazari) |
| 3-11 | (a definir) | 🔲 pendente | Demais módulos do Marketing OS |

---

## MÓDULO 1 — analisa-video

### Objetivo
Analisar calls de vendas, vídeos de marketing, áudios do WhatsApp, gravações de cursos.  
Extrair: linguagem não-verbal (frames), tonalidade de voz, transcrição, identificação de speakers.

### Localização
```
Skill instalada: Settings → Capabilities → analisa-video (v3)
Scripts: /var/folders/4r/zm09d8k51lgdrrwv6t1yfmsr0000gn/T/claude-hostloop-plugins/ff0de173d7a37fa6/skills/analisa-video/scripts/
```

### Arquitetura técnica
```
analisa.py          → orquestrador principal
local_whisper.py    → transcrição local (faster-whisper, modelo small/medium/large-v3)
diarize.py          → identificação de speakers (pyannote/speaker-diarization-3.1)
voice_features.py   → análise acústica (librosa: pitch, WPM, energia, expressividade)
frames.py           → extração de frames (ffmpeg, para análise visual/linguagem corporal)
download.py         → download com cookies (yt-dlp, qualquer plataforma)
setup.py            → instalação de dependências
```

### Dependências instaladas no Mac
- faster-whisper (transcrição local, zero custo)
- librosa (análise acústica, zero custo)
- pyannote.audio (diarização de speakers, zero custo, HuggingFace gratuito)
- ffmpeg (brew install ffmpeg)
- yt-dlp (brew install yt-dlp)

### Configuração
```
HuggingFace token: ~/.config/watch/.env → HUGGINGFACE_TOKEN=hf_***REDACTED***
Conta HuggingFace: arthurgerber (arthur@ogruposilva.com.br)
```

### Saídas automáticas
```
JSON: ~/Downloads/Analises/analise_[titulo]_[data].json    → para agentes
TXT:  ~/Downloads/Transcricoes/transcricao_[titulo]_[data].txt  → legível
```

### Modo de uso
```bash
# Call de closer (2 speakers)
python3 analisa.py "call.mp4" --speakers 2 --roles "Speaker_00=Closer,Speaker_01=Lead"

# Áudio WhatsApp
python3 analisa.py "audio.ogg" --so-audio

# Curso com login
python3 analisa.py "https://hotmart.com/..." --cookies ~/Downloads/cookies.txt --fast

# Trecho específico
python3 analisa.py "video.mp4" --start 10:00 --end 20:00
```

### Evolução planejada → Chrome-native (sem download)
**Decisão arquitetural (2026-06-29):** Migrar para análise 100% via Chrome, sem download de arquivos.

**Arquitetura nova:**
1. Claude abre vídeo no Chrome (Google Drive, YouTube, qualquer URL)
2. Transcrição nativa: Google Meet já gera transcrição com speakers identificados (botão "Transcrição")
3. Frames: Claude tira screenshots do Chrome enquanto vídeo toca → lê cada frame visualmente
4. Voz: WPM calculado dos timestamps da transcrição nativa + análise qualitativa

**Benefícios:** Zero armazenamento, escalável, funciona para qualquer URL autenticada no Chrome.

---

## AGENTE — analisa-video (futuro Claude Code)

### Papel no sistema
Sub-agente especializado em análise de mídia. Recebe instruções do orquestrador central.

### Ferramentas do agente
- Claude in Chrome MCP → navegar, screenshot, ler transcrições nativas
- Bash → processar áudios locais quando necessário
- Read → ler frames como imagens (multimodal)

### Interface esperada (input)
```json
{
  "url": "https://drive.google.com/...",
  "tipo": "call_closer",
  "speakers": {"closer": "Marcos Rosa", "lead": "Milena Almeida"},
  "foco": "por que não fechou?"
}
```

### Interface esperada (output)
```json
{
  "resultado": "nao_fechou",
  "motivo_principal": "...",
  "score_closer": 7,
  "speakers": {...},
  "transcricao": "...",
  "insights": [...]
}
```

---

## DECISÕES TÉCNICAS IMPORTANTES

| Decisão | Alternativa descartada | Motivo |
|---------|----------------------|--------|
| faster-whisper local | Groq API / OpenAI Whisper API | Custo + limite de uso em escala |
| librosa local | AssemblyAI | Custo por minuto de áudio |
| pyannote local | APIs de diarização | Custo + privacidade das calls |
| Chrome screenshots para frames | Download + ffmpeg | Escalabilidade, zero armazenamento |
| Transcrição nativa do Google Meet | Whisper em calls do Drive | Já tem speaker labels prontos |

---

## GRUPOS / UNIDADES DE NEGÓCIO

- **Grupo VR**
- **Grupo Silva**
- **Grupo Lazari**

Cada grupo tem seus próprios closers. FUP gerado por closer/grupo.

---

## CLOSERS CONHECIDOS

| Nome | Grupo | Observações |
|------|-------|-------------|
| Marcos Rosa | Grupo Lazari | Call avaliada: 28/05/2026 × Milena Almeida + Pedro Moraes. Score 4/10. |
| Camila | Grupo Lazari | Call avaliada por Arthur (doc de avaliações): × Yunes. |
| Ian | Grupo Lazari | Call avaliada por Arthur (doc de avaliações): × Thamyres. |
| Eduarda | Grupo Lazari | Call avaliada por Arthur (doc de avaliações): × Luis. |
| Harisson | Grupo Lazari | Call avaliada por Arthur (doc de avaliações): × Edna. |

### Padrões de erro recorrentes em TODOS os closers (base: doc de avaliações Arthur)

Esses problemas aparecem em todas as calls avaliadas — Camila, Ian, Eduarda, Harisson e Marcos:

1. **Pitch cedo demais** — todos entram na apresentação antes de 5 minutos sem qualificação real
2. **Minipactos ausentes** — nenhum usa as perguntas de comprometimento progressivo
3. **Decisor oculto ignorado** — quando há mais de uma pessoa, a segunda é sistematicamente ignorada
4. **Sem fechamento explícito** — calls terminam sem CTA, sem próximo passo, sem pergunta de decisão
5. **"Tem alguma dúvida?"** — pergunta inútil usada por todos — resposta óbvia é sempre "não"
6. **Vocabulário fraco** — "suporte", "equipe", termos genéricos em vez de "estrategistas, gestores de tráfego"
7. **Não conhece o lead** — não pergunta se já acompanha a Julia, se já tentou o digital, quanto investiu
8. **Câmera e áudio** — olhar para baixo/lado recorrente em vários closers

---

## LOOP DE APRENDIZADO — VISIBILIDADE POR PAPEL

**Como funciona:**
- Após cada análise, padrões recorrentes são extraídos e registrados
- O sistema identifica automaticamente os critérios com score baixo repetido

**Quem vê o quê:**

| Informação | Closer | Líder / Sócio / Diretor |
|-----------|--------|------------------------|
| Análise completa da própria call | ✅ | ✅ |
| Score por critério | ✅ | ✅ |
| Feedback de melhoria | ✅ | ✅ |
| Alertas de padrão recorrente (ex: "3 calls sem minipacto") | ✅ | ✅ |
| Notas de treinamento interno / coaching estratégico | ❌ | ✅ apenas líderes |
| Comparativo entre closers do grupo | ❌ | ✅ |
| Relatório agregado por grupo | ❌ | ✅ |

---

## O QUE O AGENTE DEVE ANALISAR NO VÍDEO (mandatório)

> Esses pontos devem estar na skill analisa-video e no agente avaliador. São os critérios visuais e vocais que o agente deve extrair de toda call.

### Padrão de extração de frames

| Modo | Taxa | Frames para call de 63 min | Quando usar |
|------|------|---------------------------|-------------|
| **Padrão (default)** | 1 frame / 10s | ~380 frames | Toda call de avaliação |
| **Denso (momentos-chave)** | 1 frame / 2s | +frames nas janelas críticas | Preço, objeção, fechamento |
| **Rápido (--fast)** | 1 frame / 38s | ~100 frames | Só quando explicitamente solicitado |

**Janelas de densidade extra (automáticas no futuro, hoje manuais):**
- Abertura: primeiros 2 min
- Revelação de preço: ± 3 min ao redor
- Cada objeção detectada na transcrição: ± 2 min
- Tentativa de fechamento: ± 3 min
- Encerramento: últimos 3 min

### Regra de leitura de frames (Claude)

**100% dos frames devem ser lidos. Sem amostragem. Sem exceção.**

Para cada frame, registrar:

| Elemento | O que observar | Sinais positivos | Sinais negativos |
|----------|---------------|-----------------|-----------------|
| **Olhar do closer** | Direção dos olhos | Câmera = foco no lead | Baixo = script; lado = distração |
| **Olhar do lead** | Direção dos olhos | Câmera = engajado | Cima = 2º monitor; lado = desconexão |
| **Mãos do closer** | Posição e movimento | Gestos ilustrativos | No rosto = tensão; na boca = insegurança |
| **Mãos do lead** | Posição e movimento | Abertas, relaxadas | Cruzadas, na boca, escondidas |
| **Expressão facial** | Toda a face | Aberta, sorriso genuíno | Neutra fechada, tensa, sobrancelha franzida |
| **Micro-expressões** | Mudanças rápidas de <500ms | — | Lábios comprimidos, olho estreitado, maxilar tenso, sorriso forçado, piscar excessivo, nariz franzido |
| **Postura** | Coluna, inclinação | Para frente = engajado | Recostado = desengajado |
| **Terceiros** | Quem mais aparece | — | Decisor ignorado, pessoa desengajada |
| **Câmera do lead** | Status da câmera | Ligada, estável | Apagada: registrar início, duração, reação do closer |
| **Espelhamento** | Closer espelha o lead? | Adapta energia ao estado do lead | Energia alta quando lead está fechado |

### Análise Vocal (áudio)

| Elemento | O que observar | Sinal positivo | Sinal negativo |
|----------|---------------|---------------|----------------|
| **WPM** | Ritmo de fala | 110–160 WPM | <110 (lento/sem energia) ou >170 (ansioso) |
| **Pitch (Hz)** | Frequência da voz | 150–220 Hz (natural) | >220 Hz (ansiedade) |
| **Entonação** | Variação ao longo da fala | Expressivo, varia | Monótono, plano |
| **Energia** | Volume e intensidade | Picos nos momentos de pitch | Queda nos momentos de objeção |
| **Pausas** | Silêncios estratégicos | Pausa após pergunta (técnica) | Silêncio desconfortável, corrida para preencher |
| **Vícios** | Palavras repetidas | Ausentes | "certo", "né", "sem problema", "entende?" |
| **Dicção** | Clareza das palavras | Clara, sem engolir | Engole palavras, prejudica autoridade |

---

## PRÓXIMOS PASSOS

**SKILL analisa-video:**
1. ✅ Análise de frames com critérios de linguagem não-verbal
2. ✅ Diarização de speakers (pyannote)
3. ✅ Frames salvos permanentemente (não mais em /tmp)
4. ✅ Gate obrigatório de leitura de frames antes da análise
5. ✅ Template de saída completo com critérios visuais/vocais — micro-expressões, decisor oculto, score por critério, momento a momento
6. ✅ analisa-video.skill empacotada com todos os fixes (skill-creator) — instalar via "Save skill"
7. ✅ Sistema de persistência permanente: backup em ~/Downloads/Marketing_OS/skill_backups/ + LaunchAgent automático no login
8. 🔲 Aumentar densidade de frames em momentos-chave (revelação de preço, objeções, fechamento) — hoje é manual
9. 🔲 Integrar PROCESSO_BASE_CLOSER.md como gabarito de avaliação dentro da skill
10. 🔲 Passar calls de treinamento interno (minipactos etc) quando disponível — Arthur vai fornecer

**AGENTES:**
9. 🔲 Ver ferramenta do sócio Antonio (Arthur vai passar o link) para referência de dashboard
10. 🔲 Definir estrutura do dashboard — o que aparece para o closer vs o que aparece para o líder
11. 🔲 Criar agente monitor de Drive (detecta nova gravação → dispara análise automaticamente)
12. 🔲 Criar agente coordenador por empresa (VR, Silva, Lazari)
13. 🔲 Criar agente de loop de aprendizado (extrai padrões recorrentes por closer)
14. 🔲 Definir permissões de visibilidade (closer vs líder) no banco

**ARQUITETURA GERAL:**
15. 🔲 Definir os outros módulos do Marketing OS (além de analisa-video e fup-mensal)
16. 🔲 Refinar PROCESSO_BASE_CLOSER.md por sócio/grupo quando processos específicos forem fornecidos
17. 🔲 Infraestrutura AWS (EC2 Spot + RDS) — montar quando escalar para produção

---

## INFRAESTRUTURA DEFINIDA

| Componente | Solução | Custo | Motivo |
|------------|---------|-------|--------|
| Código | GitHub privado | R$0 | Sem dado pessoal, sem risco LGPD |
| Banco de dados | AWS RDS PostgreSQL (São Paulo) | ~R$150/mês | Dado em solo BR, LGPD ok, gerenciado |
| Gravações | Google Drive (já existe) | — | Confirmado ok |
| Análise de texto/voz | Claude Haiku via API | ~R$900-1.500/mês | Melhor custo-benefício |
| Processamento pesado (Whisper, etc) | AWS EC2 Spot (c7g.large, SP) | ~R$10/mês | Mac livre, 10 paralelos, liga/desliga automático |

**✅ APROVADO por Arthur:** usar AWS EC2 spot para qualquer processamento pesado dos agentes. Instância sobe quando tem trabalho, desce quando termina. Mac nunca aquece.

### Supabase schema (Avaliação Comercial)

```sql
calls (id, data_call, duracao_s, grupo, closer_nome, lead_nome,
       resultado, score_closer, probabilidade_fup, motivo_nao_fechou, arquivo_origem)

speakers (call_id, nome, papel, wpm, tempo_fala_s, pct_tempo, tom_predominante, pitch_hz)

segmentos (call_id, speaker, inicio_s, fim_s, texto)

analises_raw (call_id, json_completo, versao_skill)
```

---

## 🔒 LEI DA PLATAFORMA — VALIDAÇÃO É INEGOCIÁVEL EM TODOS OS NÍVEIS

> **Cenário que este padrão evita:** Plataforma rodando 300 calls/dia. Uma atualização de lib muda a API silenciosamente. Todos os agentes continuam "funcionando" mas retornam dados incompletos. Nenhum erro visível. Closers recebem feedback errado por dias. Decisões tomadas com base em dados inválidos.
>
> **Regra:** Todo agente, toda skill, todo script valida antes de executar. Falha visível > falha silenciosa. Sempre.

---

### CAMADA 1 — Skills (uso manual/independente)

Toda skill deve ter no seu SKILL.md uma seção **VALIDAÇÃO** com:
- Lista de dependências + versões mínimas testadas
- Comando de preflight obrigatório antes do primeiro uso
- Instrução de como verificar se a saída está correta (não só se "não deu erro")

**Template obrigatório para toda skill:**
```
## VALIDAÇÃO — rode antes de usar pela primeira vez
python3 ~/Downloads/preflight_analisa.py

Versões testadas e aprovadas:
- pyannote.audio >= 3.1.0
- huggingface_hub >= 0.23.0 (usa token=, não use_auth_token=)
- faster-whisper >= 0.9.0
- torch >= 2.0.0

Sinal de que está funcionando:
- JSON gerado contém speakers com nomes reais (não null)
- TXT contém "Marcos Rosa (Closer):" e "Milena Almeida (Lead):"
- Log mostra: [analisa] 2 speaker(s) detectado(s)
```

---

### CAMADA 2 — Agentes (automação em escala)

Todo agente deve ter um **health check** no início de cada execução. Não é opcional.

```python
# PADRÃO OBRIGATÓRIO — início de todo agente
class AgenteBase:
    def executar(self, input_data):
        # 1. Health check ANTES de qualquer trabalho
        health = self.health_check()
        if not health["ok"]:
            raise RuntimeError(f"[AGENTE] Health check falhou: {health['erros']}")
            # NUNCA continuar com health check falhado

        # 2. Executar a tarefa
        resultado = self._executar_interno(input_data)

        # 3. Validar OUTPUT — não só "não deu erro"
        self._validar_output(resultado)

        return resultado

    def health_check(self) -> dict:
        erros = []
        # Verifica cada dependência com versão
        # Verifica cada credencial
        # Verifica cada recurso externo
        return {"ok": len(erros) == 0, "erros": erros}

    def _validar_output(self, resultado):
        # Campos obrigatórios devem existir e não ser null
        campos_obrigatorios = ["speakers", "transcricao", "voz_global"]
        for campo in campos_obrigatorios:
            if resultado.get(campo) is None:
                raise ValueError(f"[VALIDAÇÃO] Campo '{campo}' é null — análise incompleta")
```

---

### CAMADA 3 — Compatibilidade de versão (breaking changes)

**Regra de código para toda chamada de API externa:**
```python
# PADRÃO: tentar API nova → fallback API antiga → falhar alto se ambas falharem
def chamar_com_compatibilidade(lib, novo_param, antigo_param, valor):
    try:
        return lib.call(**{novo_param: valor})
    except TypeError:
        try:
            return lib.call(**{antigo_param: valor})
        except Exception as e:
            raise RuntimeError(f"API incompatível com ambas as versões: {e}")
```

**Nunca fazer:**
```python
# ERRADO — captura silenciosa
try:
    result = lib.call(use_auth_token=token)
except Exception as e:
    print(f"erro: {e}")
    result = None  # ← continua com resultado nulo. PROIBIDO.
```

---

### CAMADA 4 — Monitoramento contínuo

Quando o AWS EC2 Spot estiver ativo, rodar semanalmente:
```bash
# Verifica se alguma lib atualizou e quebrou compatibilidade
python3 ~/Downloads/preflight_analisa.py --test-pipeline
```

Se o preflight falhar → **parar todos os agentes** + alertar imediatamente.
Não existe "continuar com erro" em produção.

---

### REGRAS DE OURO (não negociáveis para qualquer contribuidor)

1. **Sem falhas silenciosas** — se algo falhou, deve aparecer explicitamente
2. **Validar output, não só ausência de erro** — `speakers: null` é falha, mesmo sem exception
3. **Compatibilidade explícita** — toda lib tem versão mínima documentada
4. **Breaking changes são esperados** — código defende contra eles com try/except versionado
5. **Preflight antes de escalar** — nunca escalar sem confirmar que funciona em 1 call

---

## ⚙️ PADRÃO DE PLATAFORMA — VALIDAÇÃO OBRIGATÓRIA ANTES DE QUALQUER EXECUÇÃO

> **Regra inegociável:** Nenhum agente, skill ou script roda sem validar dependências, versões e compatibilidade de API primeiro. Nunca assumir que está funcionando — versões mudam, APIs quebram silenciosamente.

### Por que existe esse padrão
Em 2026-06-29, a diarização de speakers falhou silenciosamente porque:
- `huggingface_hub >= 0.23` removeu o parâmetro `use_auth_token=` (breaking change)
- O script usava a API antiga → erro capturado internamente → `speakers: null` no JSON
- Nenhum aviso visível → análise rodou como se estivesse ok → resultado incompleto

**Lição:** Nunca confiar que "se não deu erro, funcionou". Validar ativamente.

### Checklist de validação (obrigatório para todo agente/skill)

Antes de construir qualquer agente, responder:

| # | Pergunta | Como validar |
|---|----------|--------------|
| 1 | As bibliotecas estão instaladas? | `import lib` + checar versão |
| 2 | As versões são compatíveis entre si? | Comparar com VERSION_MATRIX |
| 3 | Houve breaking changes recentes? | Checar changelog da lib |
| 4 | As chamadas de API estão atualizadas? | Testar com dado real, não mock |
| 5 | O token/credencial existe e funciona? | Fazer chamada real à API |
| 6 | O modelo/recurso externo está acessível? | Request autenticado |
| 7 | O script falha alto (não silenciosamente)? | Testar caso de erro propositalmente |
| 8 | O output contém os campos esperados? | Validar JSON/estrutura de saída |

### Padrão de código para todo agente

```python
# TODO AGENTE DEVE:
# 1. Tentar API nova primeiro, depois API antiga (compatibilidade futura)
try:
    result = lib.call(new_param=value)
except TypeError:
    result = lib.call(old_param=value)  # fallback para versão antiga

# 2. Falhar alto — nunca capturar erro e continuar silenciosamente
if result.get("erro"):
    raise RuntimeError(f"[AGENTE] Falha crítica: {result['erro']}")
    # NUNCA: print(erro) e continua sem o resultado

# 3. Validar output antes de retornar
assert result.get("speakers") is not None, "Diarização falhou — speakers é null"
```

### Ferramenta de validação padrão
```bash
# Rodar SEMPRE antes de qualquer análise ou deploy
python3 ~/Downloads/preflight_analisa.py

# Com teste completo do pipeline (mais lento, mas garante 100%)
python3 ~/Downloads/preflight_analisa.py --test-pipeline
```

---

## PROTOCOLO DE VERIFICAÇÃO — PRÉ-ANÁLISE OBRIGATÓRIO

**Regra:** Antes de rodar qualquer análise de call ou vídeo, executar o preflight. Sem exceção.

```bash
python3 ~/Downloads/preflight_analisa.py
```

### O que o preflight verifica
| Check | O que faz | Se falhar |
|-------|-----------|-----------|
| Python 3.9+ | Versão mínima | Instalar Python 3.10 via brew |
| ffmpeg | Extração de áudio e frames | `brew install ffmpeg` |
| faster-whisper | Transcrição local | `pip3 install faster-whisper --break-system-packages` |
| librosa | Análise acústica | `pip3 install librosa --break-system-packages` |
| torch | Motor de ML | `pip3 install torch --break-system-packages` |
| pyannote.audio | Diarização de speakers | `pip3 install pyannote.audio --break-system-packages` |
| HUGGINGFACE_TOKEN | Token de acesso | `printf 'HUGGINGFACE_TOKEN=hf_...\n' > ~/.config/watch/.env` |
| Acesso ao modelo | Token válido + termos aceitos | Acessar huggingface.co/pyannote/speaker-diarization-3.1 |
| Modelo Whisper | Cache local | Baixa ~240MB na 1ª execução |

### Lição aprendida (2026-06-29)
O HUGGINGFACE_TOKEN não estava configurado no Mac. O script falhou silenciosamente — continuou sem diarização, sem aviso visível. A análise rodou mas speakers ficou `null`.

**Fix aplicado:** Token salvo em `~/.config/watch/.env`. Preflight criado para detectar isso antes de rodar.

**Regra para a skill:** nunca falhar silenciosamente. Se dependência faltar → parar + mostrar erro claro + instrução de correção.

### Formato de avaliação de calls (padrão Arthur)

Avaliações são narrativas e detalhadas: momento a momento, o que o closer errou, como o lead reagiu, o que deveria ter feito diferente. A skill deve replicar esse formato + adicionar:
- Análise de voz (WPM, pitch, energia, expressividade)
- Identificação de speakers com % de fala
- Frames de linguagem corporal (postura, gestos, contato visual)
- Score do closer + próximo passo recomendado

**Critérios obrigatórios em toda avaliação (extraídos do doc de avaliações de Arthur):**

| Critério | O que avaliar |
|----------|---------------|
| **Apresentação** | Se apresentou com nome + empresa? Não falou idade? |
| **Rapport** | Foi natural ou virou questionário? Se aprofundou na história da pessoa? |
| **Qualificação profunda** | Investigou: vida, família, dores, sonhos, o que já tentou, por que não deu certo, quanto investiu? |
| **Conhece a Julia?** | Perguntou se a pessoa acompanha a Julia antes de apresentá-la? |
| **Decisor oculto** | Tinha mais alguém na call? Esse alguém foi incluído? "Se dependesse só de você, estaria 100% fechado?" |
| **Minipactos** | Usou perguntas de comprometimento progressivo ao longo da call? (não "tem dúvida?" — sim "o que mais fez sentido?") |
| **Adaptação ao lead** | Adaptou o pitch ao perfil e ao objetivo declarado da pessoa? |
| **Vinculação ao objetivo** | Conectou o valor do investimento ao objetivo financeiro que a pessoa revelou? |
| **Linguagem e vocabulário** | Usou "estrategistas, agente de relacionamento, gestor de tráfego"? Evitou "suporte", "produto de IA", "pioneiros"? |
| **Câmera e áudio** | Olhou para a câmera (não para baixo/lado)? Áudio limpo? Sem chiclete? |
| **Contato visual** | Focou na pessoa como se estivesse ao vivo? |
| **Contradições** | Se contradisse em algum momento? (preço, prazo, o que a empresa faz) |
| **Prova social** | Usou casos frescos e com dados reais? |
| **Fechamento explícito** | Pediu decisão? Não terminou a call sem CTA? |
| **Próximo passo** | Saiu com data/hora marcada mesmo sem fechar? |
| **Isolamento de objeção** | "Se dependesse só de você, estaria fechado?" Identificou o fator real que impede? |

**Minipactos (framework central do processo do Marcos):**
- ❌ Nunca: "Tem alguma dúvida?" / "Ficou claro?"
- ✅ Sempre: "Do que passei até aqui, o que mais fez sentido pra você?"
- ✅ "O que menos fez sentido, ou o que faltaria para fazer 100% sentido?"
- ✅ "De 0 a 10, o quanto isso faz sentido para a sua vida?"
- ✅ "Isolando o valor por um segundo — se o financeiro não fosse um problema, você estaria 100% dentro?"

**Decisor oculto (padrão identificado em múltiplas calls):**
Sempre verificar se há mais alguém na call ou que precisará ser consultado. Se houver:
- Cumprimentar pelo nome desde o início
- Direcionar perguntas para essa pessoa também
- Antes do fechamento: "Se dependesse só de vocês dois agora, estariam 100% dentro?"
- Se for consultar alguém ausente: "Você precisa validar com ela, ou apenas comunicar que já decidiu?"

**Vocabulário correto da empresa:**
- ✅ Estrategistas, gestores de tráfego, agentes de produto, agentes de relacionamento, copy
- ❌ Suporte, equipe de suporte, pessoal do CS (usar se falar de função, não de nome do departamento)
- ❌ "Produto construído por IA" (tira autoridade — usar "nosso time desenha e valida os produtos")
- ❌ "Somos pioneiros" (só se for comprovável)
- ❌ Prometer resultado específico no prazo ("ainda neste mês você faz R$2.500") — cuidar com isso

---

## ⚠️ LIÇÃO APRENDIDA — MEMÓRIA E CONTEXTO

**Problema identificado em 2026-06-29:**
O nome original da plataforma de marketing (que surgiu a partir da ideia de webinário e evoluiu para uma estrutura maior) foi perdido na compactação de contexto da conversa. Arthur não lembrava, e o arquivo de memória não tinha essa informação.

**O que melhorar:**
- Toda decisão de naming deve ser registrada imediatamente neste arquivo
- Decisões estratégicas importantes não podem depender apenas da memória da conversa
- A cada sessão, ao tomar uma decisão relevante, atualizar este arquivo antes de continuar

**Nome provisório atual:** Marketing Estratégico & Operacional  
**Nome original perdido:** a recuperar quando Arthur lembrar ou encontrar na conversa anterior

---

## COMO RECUPERAR CONTEXTO EM NOVA SESSÃO

Diga ao Claude: **"leia o arquivo MARKETING_OS_ARQUITETURA.md na minha pasta Downloads e continue o projeto de onde paramos"**

O Claude lê este arquivo e recupera tudo — módulos, decisões, configurações, próximos passos.

---

*Atualizar este arquivo sempre que tomar decisões importantes, criar novos módulos ou mudar arquitetura.*

---

## ARQUITETURA DE SKILLS — PADRÃO DEFINITIVO

### Hierarquia de skills do Marketing OS

```
devstack        ← dev sênior: planejar → codificar → testar → entregar
auto-qa         ← QA obrigatório antes de qualquer entrega
analisa-video   ← análise de calls, vídeos e áudios de vendas
fup-mensal      ← follow-up por closer (VR, Silva, Lazari)
questiona-planeja-age ← postura sênior em qualquer tarefa autônoma
```

### Regra de composição

Todo trabalho técnico segue este pipeline:

```
questiona-planeja-age  →  devstack  →  auto-qa  →  entrega
        ↑                    ↑              ↑
   (postura)          (execução)       (validação)
```

### Padrão obrigatório em toda skill

Cada SKILL.md termina com o bloco:

```markdown
## ANTES DE ENTREGAR — PROTOCOLO OBRIGATÓRIO
1. Rodar auto-qa no que foi criado/modificado
2. Re-testar após qualquer correção
3. Só apresentar a Arthur quando tudo verde
4. Para desenvolvimento técnico: usar skill devstack como guia
```

### PADRÃO UNIVERSAL de reconhecimento de termos

Sempre `grep -qiE` com regex. Nunca busca literal.

| Termo | Regex |
|-------|-------|
| padrão universal | `PADR.O UNIVERSAL` |
| regra absoluta | `REGRA ABSOLUTA` |
| micro-expressões | `MICRO.?EXPRESS` |
| decisor oculto | `DECISOR.{0,20}(OCULTO\|SILENCIOSO)` |
| minipacto | `MINI.?PACTO` |
| speaker (pyannote) | `SPEAKER_\d+` — sempre MAIÚSCULO |

### Scripts de manutenção

| Script | Uso |
|--------|-----|
| `restaurar_tudo.sh` | Roda no login — restaura skill analisa-video do backup |
| `atualizar_skill.sh <nome>` | Atualiza skill nos 3 locais (Downloads + backup + GitHub) |
| `preflight.py` | Verifica dependências antes de rodar análise de call |

### Três locais de persistência

1. `~/Downloads/.claude/skills/<nome>/` — Cowork lê direto (principal)
2. `~/Downloads/Marketing_OS/skill_backups/` — backup local (restauração)
3. GitHub `arthurgerber/marketing-os-skills` — versão remota (recovery total)

---

## ERROS ENCONTRADOS NO TESTE DE ESCALA — 29/06/2026

### Problema 1 — Leitura de 400 frames individualmente = inviável
**Sintoma:** Subagente levou ~50 minutos para ler 400 frames. Mac aqueceu. Inescalável.
**Causa:** Cada Read de imagem = 1 chamada de API. 400 chamadas sequenciais = demora.
**Solução implementada:** Script `gera_composites.py` agrupa 400 frames em 20 grades compostas.
- 400 leituras → 20 leituras
- ~50 minutos → ~3 minutos
- Script: `~/Downloads/Marketing_OS/scripts/gera_composites.py`
- Também em: `~/Downloads/.claude/skills/analisa-video/scripts/gera_composites.py`

### Problema 2 — Labels de speaker invertidos na diarização
**Sintoma:** JSON rotulou o Closer como "Lead" e o Lead como "Closer".
**Causa:** `--roles` mapping foi aplicado ao SPEAKER_ID errado.
**Solução:** Verificar via conteúdo do texto, não só pelo label:
- Quem apresenta o produto/serviço = Closer
- Quem revela objetivos pessoais e faz perguntas de compra = Lead
**Fix no script:** Adicionar validação pós-diarização que verifica % de fala (Closer > 70% = sinal correto).

### Problema 3 — Botão "Transcrição" bloqueado para usuários externos no Drive
**Sintoma:** Usuário com tag "Externos" não consegue abrir painel de transcrição nativa do Google Meet.
**Solução de escala:** Usar conta interna do Grupo (não conta pessoal) para acessar gravações. OU usar Drive API com service account para baixar o arquivo de transcrição diretamente.

### Problema 4 — JavaScript bloqueado no player do Google Drive
**Sintoma:** `document.querySelector('video')` retorna BLOCKED: Cookie/query string data.
**Causa:** Restrição de segurança para usuários externos.
**Solução:** Não depender de JS para controle do player. Usar cliques no timeline (funcional via Chrome MCP) ou Drive API para download.

### Problema 5 — Chrome approach não escala para 300 calls/dia
**Sintoma:** Capturar 400 frames via clicks no timeline do Chrome levaria ~26 minutos por vídeo.
**Decisão arquitetural:** Chrome é APENAS para casos manuais/spot-check. Escala real = pipeline abaixo:

```
PIPELINE DE ESCALA (target: 5-10 min por call, 300/dia):

1. Fonte chega (Drive link ou arquivo local)
   ↓
2. EC2 Spot inicializa (spin-up: ~90s)
   ↓
3. EC2 processa em paralelo:
   - yt-dlp baixa só o áudio (não vídeo inteiro) → ~1 min
   - Whisper transcreve → ~3-5 min para 60min de áudio (modelo small)
   - pyannote diariza speakers → ~2 min
   - ffmpeg extrai 400 frames do vídeo → ~30s
   - gera_composites.py cria 20 grades → ~10s
   ↓
4. EC2 salva JSON + composites + TXT em S3 ou volta para ~/Downloads/Analises/
   EC2 desliga (custo ~$0.02 por call)
   ↓
5. Claude lê JSON (transcrição completa) → ~30s
   Claude lê 20 composites → ~2 min
   Claude gera relatório → ~2 min
   TOTAL CLAUDE: ~5 min
   ↓
6. Relatório entregue. TOTAL PIPELINE: ~8-10 min por call
```

### Padrão de enforcement — Como garantir que agente siga o processo

O problema de agentes "pulando etapas" é resolvido convertendo instruções em scripts executáveis:
- Se o passo É um script = agente executa ou falha (não tem como improvisar)
- Se o passo É texto descritivo = agente pode ignorar ou abreviar

**Regra:** Todo passo crítico da skill deve ter um script correspondente no /scripts/.
Scripts obrigatórios na skill analisa-video:
- `analisa.py` → extração + transcrição + diarização (STEP 2)
- `gera_composites.py` → grades visuais (STEP 3) — NOVO
- Output esperado verificável: se composites não existem, STEP 3 não foi executado

---

## PADRÃO DE AGENTES — DECISÕES ARQUITETURAIS (2026-06-29)

### Enforcement: Skills com Scripts Obrigatórios

**Problema resolvido:** instruções em texto são ignoradas por agentes. Script executável não.

**Padrão aplicado a partir de 29/06/2026:**
- Toda skill crítica tem `scripts/check.py` — roda antes de qualquer entrega
- O checklist OBRIGATÓRIO está no final de TODA skill — bloco padrão
- Passos que podem ser improvisados viram scripts que ou rodam ou falham visivelmente
- Skills afetadas: analisa-video, devstack, auto-qa, fup-mensal, watchdog, debugger (todas)

### Multi-agentes Paralelos (padrão de escala)

**Para análise visual de 400 frames:**
- ❌ 1 agente sequencial = 50 min (inaceitável)
- ✅ 4 agentes paralelos, cada um lendo 5 composites = ~3 min

**Fórmula:** N frames → `gera_composites.py` → 20 composites → 4 agentes paralelos × 5 composites

**Aplicar este padrão em todo agente que processa volume alto de dados:**
- Análise de calls: 4 agentes paralelos por bloco de tempo
- Análise de plataformas de curso: dividir aulas por agente
- FUP em massa: dividir leads por agente

### analisa-video como Base Multi-Agente

A skill analisa-video é a base técnica para:

| Agente futuro | O que usa da analisa-video |
|--------------|---------------------------|
| Agente de Copy | Replica voz/estilo do speaker (perfil vocal) |
| Agente de Tráfego | Analisa criativos em vídeo, frames de ads |
| Agente de Funil | Assiste aulas em plataformas, extrai frameworks/metodologias |
| Agente de Avaliação Comercial | Avalia calls de closers (já em uso) |

**Capacidade já implementada:** qualquer URL autenticada no Chrome → Chrome MCP → screenshots + transcrição

**Para plataformas de curso (Hotmart, Kiwify, Teachable, etc.):**
- Chrome com cookies da sessão logada
- Screenshots dos slides/apresentações durante o vídeo
- Áudio transcrito via Whisper OU transcrição nativa da plataforma
- Extração de frameworks, metodologias, técnicas → base de conhecimento do agente

### Watchdog + Debugger — Agentes de Qualidade

Implementados como skills em 29/06/2026:

```
watchdog → monitora execuções → detecta desvios → aciona debugger
debugger → recebe contexto → reproduz problema → corrige → confirma
```

Localização: `~/Downloads/.claude/skills/watchdog/` e `/debugger/`

**Integração futura:** quando agentes rodarem em pipeline automático, watchdog verifica cada output antes de passar para o próximo agente.

### Solução Chrome-Native — Erros e Status

**Objetivo:** análise 100% via Chrome, zero processamento local, zero download.

| Passo | Status | Solução |
|-------|--------|---------|
| Abrir vídeo no Drive | ✅ Funciona | Chrome MCP + link do Drive |
| Transcrição nativa do Meet | ⚠️ Bloqueada para externos | **Solução:** usar conta interna do Grupo (não conta pessoal). OU: Drive API com service account para download direto do arquivo de transcrição |
| JS para controlar player | ❌ Bloqueado para externos | **Solução:** usar cliques no timeline via Chrome MCP (funcional). Não usar JS. |
| Screenshots durante playback | ✅ Funciona (com vídeo mudo) | Clicar no ícone de som → mudo → clicar no timeline → screenshot |
| 400 frames via Chrome | ⚠️ Lento (26min) | **Solução de escala:** EC2 extrai frames com ffmpeg (~30s). Chrome só para spot-check. |
| gera_composites.py pós-extração | ✅ Implementado | 400 frames → 20 composites em segundos |

**Decisão final de arquitetura de escala (300 calls/dia):**
1. Drive API (service account) → download só do áudio (não vídeo completo)
2. EC2 Spot SP: Whisper + pyannote + ffmpeg → JSON + frames em ~5min
3. gera_composites.py → 20 composites
4. Claude: 4 agentes paralelos leem JSON + composites → relatório em ~3min
5. **Total: ~8-10min por call | Custo: ~$0.03 por call**

