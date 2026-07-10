# MARKETING OS — Empresa Automatizada
**Versão:** 1.0 | **Data:** 2026-06-30  
**Visão:** Uma empresa que roda sozinha — produto, tráfego, vendas, conteúdo, operação.

---

## A IDEIA CENTRAL

Não é um "chatbot" nem um "assistente". É uma **empresa operada por agentes de IA**, onde cada setor tem sua equipe de agentes especializados que estudam, executam, testam e melhoram continuamente.

Arthur é o CEO. Confere os resultados. Define a direção. A empresa executa.

**Meta de validação:** R$5.000–20.000/dia em receita digital, 100% automatizado, mercado brasileiro, com possibilidade de expansão para outros mercados.

---

## ORGANOGRAMA — SETORES E AGENTES

```
ARTHUR (CEO/Sócio)
│
├── 🏢 OPERAÇÃO COMERCIAL (já em desenvolvimento)
│   └── Ver: PLATAFORMA_COMERCIAL_ARQUITETURA.md
│
├── 📣 MARKETING (este documento)
│   │
│   ├── 🖊️  COPY
│   │   ├── Agente Copy Principal (VSL, email, texto longo)
│   │   ├── Agente Copy Criativo (headlines, ganchos, ângulos)
│   │   ├── Agente Copy SDR/Prospecting (mensagens, scripts)
│   │   └── Subagente Swipe File (garimpador de copies que funcionam)
│   │
│   ├── 🎬 VÍDEO / CRIATIVO
│   │   ├── Agente Roteiro (VSL, Reels, UGC, ADs)
│   │   ├── Agente Editor Brief (instrui editor humano ou IA)
│   │   ├── Agente Thumbnail/Imagem (prompt para DALL-E/Midjourney)
│   │   └── Subagente Trend Watcher (monitora tendências no nicho)
│   │
│   ├── 📊 TRÁFEGO
│   │   ├── Agente Media Buyer (estratégia de campanhas Meta/Google)
│   │   ├── Agente Criativo Tráfego (gera variações de criativos para testar)
│   │   ├── Agente Análise de Dados (lê resultados, aponta otimizações)
│   │   └── Subagente Spy (garimpador de anúncios concorrentes que funcionam)
│   │
│   ├── 🎯 PRODUTO / OFERTA
│   │   ├── Agente Produto (define oferta, precificação, posicionamento)
│   │   ├── Agente Garantia/Bônus (estrutura o que aumenta conversão)
│   │   └── Subagente Research (pesquisa mercado, avatar, objeções)
│   │
│   ├── 🔀 FUNIS
│   │   ├── Agente Funil Comercial (qualificação → call → fechamento)
│   │   ├── Agente Funil de Vendas (lançamento, evergreen, webinário)
│   │   ├── Agente Funil Estratégico (escada de valor completa)
│   │   └── Subagente Order Bump / Upsell / Downsell
│   │
│   ├── 🧠 ESTRATÉGIA
│   │   ├── Agente Estrategista Principal (visão macro, trimestral)
│   │   ├── Agente Posicionamento (diferenciação, branding)
│   │   └── Subagente Análise de Concorrentes
│   │
│   └── 🤖 OPERAÇÃO / AUTOMAÇÃO
│       ├── Agente N8N (cria automações, workflows)
│       ├── Agente Plataforma (sobe produto no Hotmart/Kiwify, cria links)
│       └── Subagente Monitor (verifica métricas diárias, alerta anomalias)
```

---

## COMO FUNCIONA NA PRÁTICA

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

---

## COMO OS AGENTES "ESTUDAM"

Os agentes do Marketing OS não partem do zero. Eles têm:

### Base de conhecimento:
- Cursos internos de comercial (analisa-video lê e aprende)
- Swipe file de copies que funcionam (garimpado pelo subagente)
- Anúncios concorrentes (subagente Spy)
- Resultados históricos das próprias campanhas (banco de dados)
- Playbooks e processos documentados

### Ciclo de aprendizado:
```
Executa → Coleta resultado → Compara com histórico → Identifica padrão → 
Atualiza base de conhecimento → Executa melhor na próxima vez
```

Isso é o analisa-video aplicado a marketing: assim como ele estuda calls de closers e treina os closers, os agentes de marketing estudam o que converte e replicam.

---

## INFRA TÉCNICA

### Componentes necessários:
```
Mac Mini(s) × 2          → processamento local (Whisper, análise, automações)
Supabase                  → banco de dados central (todas as métricas, resultados)
N8N (self-hosted)         → orquestração de automações (webhooks, triggers, APIs)
GitHub                    → código versionado + CI/CD
Vercel                    → deploy frontend (gratuito, automático)
Claude API (Sonnet/Haiku) → agentes executando as tarefas
Make/Zapier (backup)      → automações simples quando N8N for overkill
```

### Custo estimado de operação:
- Mac Mini M4 (~R$7.000) × 2 = R$14.000 (uma vez)
- Claude API: ~$50-200/mês dependendo do volume
- Supabase: grátis → $25/mês quando escalar
- Vercel: grátis → $20/mês quando escalar
- N8N self-hosted: grátis (roda no Mac Mini)
- **Total recorrente: ~$100-250/mês (~R$500-1.300)**

---

## ENFORCEMENT — PADRÃO EM TUDO

Cada agente, subagente, automação e processo da empresa automatizada segue:

```
ANTES de executar:
  □ Entendeu o objetivo de negócio (não só a tarefa técnica)?
  □ Tem todos os inputs necessários?
  □ Verificou se existe algo já feito para reaproveitar?

DURANTE a execução:
  □ Está seguindo o processo definido (sem atalhos)?
  □ watchdog está monitorando?
  □ Cada etapa produz output verificável?

ANTES de entregar:
  □ auto-qa rodou e aprovou?
  □ Output está completo (não parcial)?
  □ Próximo passo está definido?
```

---

## SEPARAÇÃO POR ARQUITETURAS (documentos)

Para manter organizado, cada "braço" da empresa tem sua arquitetura própria:

| Documento | Conteúdo |
|---|---|
| `MARKETING_OS_ARQUITETURA.md` | Ground truth técnico — skills, agentes, infra |
| `PLATAFORMA_COMERCIAL_ARQUITETURA.md` | App de avaliação de calls (este) |
| `MARKETING_OS_EMPRESA_AUTOMATIZADA.md` | A empresa como organismo (este) |
| `PROCESSO_BASE_CLOSER.md` | Processo e critérios de avaliação comercial |
| `PLATAFORMA_MARKETING_ARQUITETURA.md` | *(a criar)* App de marketing + tráfego |
| `AGENTES_COPY_VSL.md` | *(a criar)* Especificação dos agentes de copy |
| `AGENTES_TRAFEGO.md` | *(a criar)* Especificação dos agentes de tráfego |

---

## PRIMEIRO PRODUTO A VALIDAR

Recomendação para testar a máquina inteira:

**Produto:** Mini-curso de fechamento (R$97–197)  
**Por quê:** baixo ticket = mais vendas = dados mais rápidos; usa o processo do closer que já documentamos  
**Tráfego:** Meta Ads com 3 criativos em ângulos diferentes  
**Funil:** Page de vendas simples + order bump (checklist de fechamento)  
**Meta de validação:** 30 dias, R$3k-5k/dia  
**Se validar:** escala agressiva + upsell para programa maior

Os agentes montam tudo. Arthur confere e aprova. Go.

---

## SOBRE CHROME-NATIVE (analisa-video)

Status atual:
- ✅ Arquitetura definida: Drive → Chrome → frames + transcrição sem processar no Mac
- ✅ Erros documentados (JS bloqueado, transcrição bloqueada para externos)
- ⏳ Funciona com conta interna @ogruposilva.com.br / @grupolazari etc.
- ⏳ Para conta externa: usar Drive API com service account (próximo desenvolvimento)

O analisa-video rodando via Chrome = base para todos os agentes que aprendem assistindo aulas em plataformas (Hotmart, Kiwify, etc.).

---

*Empresa automatizada v1.0 — Marketing OS*  
*Foco: validar, escalar, expandir. Arthur comanda. Agentes executam.*

---

## CORREÇÃO ARQUITETURAL — 3 SISTEMAS SEPARADOS

A empresa não é uma plataforma única. São **3 sistemas que se comunicam**:

```
┌──────────────────────────────────────────────────────────────────┐
│  EMPRESA (Hub Central)                                           │
│  Dados sigilosos: financeiro, contratos, operação interna       │
│  Agentes: Financeiro, Suporte, WhatsApp, Orchestrador           │
│  NUNCA expõe dados internos para as plataformas                 │
└──────────┬───────────────────────────────┬───────────────────────┘
           │ recebe resultados             │ recebe resultados
           │ direciona ações               │ direciona ações
           ↓                               ↓
┌──────────────────────┐     ┌─────────────────────────────────┐
│ PLATAFORMA COMERCIAL │     │ PLATAFORMA MARKETING            │
│                      │     │                                 │
│ Calls, closers,      │     │ Copy, VSL, criativos,           │
│ scores, FUP, treina- │     │ tráfego, funis, produto,        │
│ mentos, leads        │     │ lançamentos, automações         │
│                      │     │                                 │
│ Acesso: líderes +    │     │ Acesso: time marketing +        │
│ closers do grupo     │     │ parceiros autorizados           │
└──────────────────────┘     └─────────────────────────────────┘
```

### Regra de ouro de segurança:
- Dados que saem das plataformas → podem ir para a Empresa (resultados, métricas)
- Dados que saem da Empresa → NÃO vão para as plataformas (financeiro, contratos, dados sigilosos)
- As plataformas se comunicam via Empresa (nunca diretamente entre si)

### Por que separar?
- Segurança: terceiros com acesso à Plataforma Comercial não veem o financeiro
- Escalabilidade: cada sistema pode crescer e ser mantido independentemente
- Clareza: cada equipe trabalha no seu sistema sem interferir nos outros
- Dados sensíveis ficam no Hub, nunca nas "pontas"

---

## SECURITY LAYERS — PADRÃO OBRIGATÓRIO EM TODOS OS SISTEMAS

```
Camada 1 — Autenticação
  → Google OAuth restrito por domínio (@ogruposilva.com.br, etc.)
  → Sem conta autorizada = sem acesso (nem a página de login aparece útil)

Camada 2 — Autorização por Row Level Security (RLS)
  → Supabase RLS: usuário do Grupo Silva só vê dados do Grupo Silva
  → Closer X não acessa calls do Closer Y
  → Gestor vê tudo do seu grupo, CEO vê tudo

Camada 3 — API Keys separadas por ambiente
  → Chave pública: somente leitura, exposta no frontend com segurança
  → Chave privada: somente no servidor/backend, nunca no browser
  → Tokens de integração (Drive, HF, etc.) SEMPRE em variáveis de ambiente, NUNCA em código

Camada 4 — Transporte e armazenamento
  → HTTPS/SSL em todas as comunicações
  → Dados em repouso criptografados (Supabase padrão)
  → Backups automáticos diários
```

### Regra de segurança para desenvolvimento:
- NUNCA commitar tokens, senhas, API keys em código
- Usar `.env` local + variáveis de ambiente em produção
- Antes de qualquer push: varredura automática de segredos
- Se acidentalmente commitar: revogar o token IMEDIATAMENTE no serviço

---

## DRIVE API SERVICE ACCOUNT — Chrome-Native Próximo Passo

Problema atual: transcrição via Chrome bloqueada para usuários externos.

Solução planejada:
```
1. Criar Service Account no Google Cloud Console
2. Dar acesso à pasta de gravações do Drive para essa conta
3. analisa-video usa Drive API (não Chrome) para:
   - Listar arquivos na pasta de gravações
   - Baixar só o áudio (não o vídeo inteiro)
   - Acessar arquivo de transcrição .vtt/.srt que o Meet gera automaticamente
4. Resultado: transcrição oficial do Meet + áudio, sem depender de quem está logado
5. Funciona de qualquer máquina, sem Chrome aberto, escala para 300+ calls/dia
```

Vantagens sobre Chrome:
- Não precisa ter Chrome aberto
- Não precisa de conta logada
- Funciona headless (Mac Mini sem monitor)
- Escala linear: quantas calls quanto quiser em paralelo

---

## AGENTES DE INFRAESTRUTURA (não limitados ao organograma inicial)

Além dos setores de negócio, a empresa tem agentes de infraestrutura que sustentam tudo:

```
🔧 INFRAESTRUTURA & DEV
├── Agente Dev Principal (Claude Code — programa novas plataformas e features)
├── Agente N8N (cria e mantém automações, workflows, webhooks)
├── Agente MCP/Conectores (cria conectores para novos sistemas)
├── Agente Monitor de Infra (verifica saúde dos sistemas, alerta falhas)
└── Agente Deploy (CI/CD — testa, valida, faz deploy automático)

🎬 PRODUÇÃO DE CONTEÚDO
├── Agente Editor de Vídeo (roteiro → brief para edição → revisão)
├── Agente Narração IA (gera áudio com voz clonada para cursos/treinamentos)
├── Agente Thumbnail (gera imagens para YT, Reels, Ads)
└── Agente Distribuição (publica em múltiplos canais simultâneos)

📞 ATENDIMENTO & SUPORTE
├── Agente WhatsApp (responde leads, faz qualificação inicial)
├── Agente Suporte (resolve dúvidas de clientes pós-compra)
└── Agente CRM (atualiza dados, classifica leads, define próximos passos)

💰 FINANCEIRO
├── Agente Financeiro (monitora receita, custos, margens)
├── Agente Relatório (gera relatórios financeiros semanais/mensais)
└── Agente Alerta (notifica quando algo está fora do padrão)
```

### N8N como sistema nervoso de automação:

O N8N conecta todos os agentes entre si e com sistemas externos:
```
[Evento: nova call gravada no Drive]
    → N8N detecta via webhook
    → aciona analisa-video
    → resultado vai para Supabase
    → notifica líder no WhatsApp/Slack
    → atualiza ranking no dashboard
```

```
[Evento: nova venda no Hotmart]
    → N8N recebe webhook
    → Agente Suporte envia boas-vindas
    → Cria acesso na plataforma
    → Agenda onboarding
    → Registra no financeiro
```

### MCP e Conectores próprios:

Agentes que criam os conectores que outros agentes usam:
- Conector Drive API (para pegar calls e gravações automaticamente)
- Conector Hotmart/Kiwify (para criar produtos, links, consultar vendas)
- Conector Meta Ads (para subir criativos, ler métricas)
- Conector WhatsApp Business API (para atendimento automatizado)
- Conector Supabase interno (para todos os sistemas lerem/escreverem no banco)

---

## DRIVE API — SOLUÇÃO CHROME-NATIVE (Implementação Completa)

Baseado na arquitetura do Seven Comercial do Antonio:

```
FLUXO:
1. Cada closer tem sua pasta no Drive do grupo
2. Script no Drive (Google Apps Script) monitora essas pastas
3. Quando nova gravação aparece → copia para pasta "mãe" centralizada
4. analisa-video usa Drive API + service account para acessar a pasta mãe
5. Baixa só o áudio (não o vídeo inteiro — muito mais rápido)
6. Acessa arquivo de transcrição .vtt que o Google Meet gera automaticamente
7. Processa: Whisper valida transcrição + pyannote + 400 frames
8. Resultado → Supabase → Dashboard atualiza

VANTAGENS:
- Zero dependência de Chrome ou usuário logado
- Funciona 100% headless (Mac Mini sem monitor)
- Service account tem acesso contínuo (não expira como cookie de browser)
- Escala linear: 1 Mac Mini = 50 calls/dia, 2 Mac Minis = 100+/dia
- Transcrição oficial do Meet (mais precisa que Whisper em português)

IMPLEMENTAÇÃO:
- Google Cloud Console → criar Service Account
- Compartilhar pasta mãe do Drive com o e-mail da service account
- Baixar credentials.json
- analisa-video versão "drive-api" usa googleapiclient para autenticar
- LaunchAgent detecta novo arquivo na pasta mãe → aciona processamento
```

---

## SEGURANÇA — PADRÃO UNIVERSAL

Aplicado em TODOS os sistemas (Empresa + Plataforma Comercial + Plataforma Marketing):

```
Camada 1 — Autenticação
  → Google OAuth restrito por domínio (@ogruposilva.com.br, @grupolazari.com.br, etc.)
  → Sem conta autorizada = nem página de login útil

Camada 2 — Autorização granular (RLS no Supabase)
  → Closer X: só vê suas próprias calls e scores
  → Líder do Grupo Silva: vê tudo do Grupo Silva, nada do Lazari
  → CEO/Arthur: visão total de tudo
  → Log de tudo: quem acessou, quando, o quê, de qual IP

Camada 3 — API Keys por ambiente e função
  → Chave pública (read-only, pode ir no frontend): sem risco se exposta
  → Chave privada (write): só no servidor, NUNCA no browser
  → Tokens de serviço (Drive, Claude API, etc.): variáveis de ambiente, auditados

Camada 4 — Isolamento de dados por sistema
  → Empresa Hub: dados sigilosos nunca saem para as plataformas
  → Plataformas: só recebem o que precisam, nada além
  → Backup diário criptografado automático (Supabase faz isso)

Camada 5 — Auditoria e alertas
  → Qualquer acesso incomum (horário estranho, IP novo) → alerta imediato
  → Agente Monitor de Infra revisa logs diariamente
  → Se vazar: saber quem foi + revogar acesso em < 5 minutos
```

### Regra para desenvolvimento:
**NUNCA** commitar tokens, senhas, API keys em código.
Antes de qualquer git push: varredura automática de segredos (já implementada em `push_seguro.sh`).
Token acidentalmente commitado: revogar IMEDIATAMENTE no serviço + reescrever histórico git.

---

## AUTO-EXPANSÃO — AGENTES QUE CRIAM AGENTES

A empresa não tem um número fixo de agentes. Ela cresce sozinha conforme a necessidade.

### Regra de paralelização (obrigatória em todos os agentes):

```
SEMPRE que uma tarefa tiver partes independentes:
→ NUNCA faz sequencialmente o que pode ser paralelo

Trigger automático de divisão em subagentes:
  □ Tarefa tem 2+ partes que não dependem uma da outra? → paralela
  □ Estimativa > 15 min em 1 agente? → divide em 3-4 agentes
  □ Análise de N arquivos/items? → divide em blocos iguais
  
Exemplo: analisar 40 calls → 4 agentes, 10 cada, entregam juntos em 1/4 do tempo
```

O agente NÃO decide se "aguenta sozinho" — ele SEMPRE paralela o que pode ser paralelado.

### Como novos agentes são criados:

```
[Agente Estrategista detecta: volume de copy aumentou 5x]
    ↓
[Decide: precisa de mais capacidade de copy]
    ↓
[Cria novo agente: Agente Copy Especializado — Email Sequences]
    ↓ (usando devstack + skill-creator)
[Novo agente é testado e validado pelo auto-qa]
    ↓
[Agente entra em produção — agora temos 2 agentes de copy]
    ↓
[Watchdog monitora performance dos dois]
    ↓
[Se o novo agente performa melhor → vira o padrão]
```

### Princípio: a empresa sempre melhora

Cada agente tem 3 responsabilidades além da sua função principal:
1. **Executar** — fazer o trabalho com excelência
2. **Monitorar** — reportar métricas de performance
3. **Melhorar** — sugerir (ou criar) o que precisaria existir para funcionar melhor

### Skills têm que suportar isso:

Toda skill deve incluir a possibilidade de:
- Spawnar subagentes quando a carga aumentar
- Chamar devstack quando precisar de nova funcionalidade
- Chamar skill-creator quando detectar que falta uma skill
- Registrar na arquitetura qualquer novo agente criado

### Limite: Arthur aprova novos agentes que custem recursos

Agentes que só processam informação = criação automática OK.
Agentes que gastam API credits, cloud, ou interagem com externos = aprovação de Arthur primeiro.

---

## DOCUMENTOS — ONDE FICAM E COMO PERSISTEM

```
Tipo            | Mac (Downloads) | GitHub | Drive | Container
----------------|-----------------|--------|-------|----------
Skills (.md)    | ✅ sempre       | ✅     | ❌    | ✅ auto
Docs projeto    | ✅ sempre       | ✅ *   | ❌*   | ❌
Scripts (.py/.sh)| ✅ sempre      | ✅ *   | ❌    | ❌
JSONs de análise| ✅ sempre       | ❌     | ❌    | ❌
Arquivos grandes| ✅ sempre       | ❌     | ✅    | ❌
```

*GitHub: após push manual (ou sync automático quando configurado)
*Drive: Arthur pode subir manualmente ou configurar sync automático

### Acesso em nova sessão:

Quando abrir nova sessão do Cowork:
1. Skills carregam automaticamente (sempre disponíveis)
2. Para continuar um projeto: jogar os docs de arquitetura no contexto
3. Os documentos em ~/Downloads sempre estão lá — só apontar para eles

Para acessar projetos anteriores facilmente:
- Criar pasta `~/Downloads/Marketing_OS/projetos/` com atalhos para cada projeto
- Cada projeto tem seu próprio CLAUDE.md que resume o contexto
- Qualquer sessão nova: "leia Marketing_OS/projetos/[projeto]/CLAUDE.md" → retoma de onde parou

