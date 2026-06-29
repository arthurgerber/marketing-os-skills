---
name: auto-qa
description: >
  QA automático — testa, detecta bugs e corrige antes de entregar qualquer trabalho a Arthur.
  ACIONAR SEMPRE que Claude terminar de criar ou modificar: scripts bash, scripts Python,
  skills (SKILL.md), planilhas de FUP, documentos, ou qualquer entrega técnica.
  Nunca entregar sem rodar este protocolo. Funciona como uma barreira de qualidade interna
  que age antes que Arthur veja o resultado. Se detectar bug: corrige e re-testa até passar.
  Termos que ativam: "testa antes", "verifica antes de entregar", "roda o QA", "auto-qa",
  "confere antes", "revisa antes de passar", "qa", "validação automática", "bug", "erro".
allowed-tools: Bash, Read, Edit, Write
---

# AUTO-QA — Protocolo de Qualidade Antes de Entregar

Você é a última linha de defesa antes de qualquer entrega a Arthur.
**Nunca entregue trabalho que não passou aqui.**

---

## QUANDO RODAR

Execute este protocolo automaticamente ao terminar:

- Scripts bash (`.sh`) — sempre
- Scripts Python (`.py`) — sempre  
- Skills novas ou modificadas (`SKILL.md`) — sempre
- Qualquer automação ou script de manutenção — sempre

**Regra simples: se tem código ou lógica → passa pelo QA primeiro.**

---

## PASSO 1 — Identificar tipo

```
BASH    → .sh
PYTHON  → .py
SKILL   → SKILL.md
MISTO   → múltiplos arquivos (QA em cada um)
```

---

## PASSO 2 — Verificações automáticas

### BASH
```bash
bash -n "$ARQUIVO" && echo "✅ sintaxe ok" || echo "❌ erro sintaxe"
grep -n "/Users/arthur\|/home/arthur" "$ARQUIVO" && echo "❌ PATH HARDCODED" || echo "✅ sem hardcode"
grep -n "cp \|mv \|rm " "$ARQUIVO" | grep -v "#" | grep -v '|| echo\|&& echo'
# → linhas sem tratamento de erro são risco
```

### PYTHON
```bash
python3 -m py_compile "$ARQUIVO" && echo "✅ compila" || echo "❌ erro de compilação"
grep -n "home()\|expanduser\|Path.home" "$ARQUIVO" || echo "⚠️ checar paths"
grep -n "Speaker_0\b" "$ARQUIVO" && echo "❌ casing errado — deve ser SPEAKER_00" || echo "✅ casing ok"
grep -n "max_frames=100\b" "$ARQUIVO" && echo "❌ default frames baixo" || echo "✅ frames ok"
```

### SKILL.md
```bash
grep -q "^---" "$ARQUIVO"            && echo "✅ frontmatter" || echo "❌ sem frontmatter"
grep -q "^name:"        "$ARQUIVO"   && echo "✅ name"        || echo "❌ sem name"
grep -q "^description:" "$ARQUIVO"   && echo "✅ description" || echo "❌ sem description"
grep -qiE "PADR.O UNIVERSAL" "$ARQUIVO" && echo "✅ padrão universal" || echo "⚠️ sem padrão universal"
```

---

## PASSO 3 — Simular execução

- Bash: `bash -n` (dry run) + rodar com `HOME=/tmp/` se possível
- Python: `python3 script.py --help` para checar imports
- Skill: confirmar que todos os scripts referenciados existem no caminho indicado

---

## PASSO 4 — Corrigir automaticamente

Se encontrar bug claro, **corrige sem perguntar**:

| Problema | Correção |
|----------|----------|
| Sintaxe bash inválida | Corrigir e re-testar |
| Path hardcoded `/Users/arthur` | Substituir por `$HOME` / `Path.home()` |
| `grep` sem `-i` em termos variáveis | Adicionar `-iE` |
| `cp`/`mv` sem tratamento de erro | Adicionar `|| echo "❌ erro"` |
| `mkdir` sem `-p` | Adicionar `-p` |
| `max_frames=100` | Corrigir para `max_frames=400` |
| `Speaker_00` (lowercase s/p) | Corrigir para `SPEAKER_00` |
| SKILL.md sem frontmatter | Adicionar frontmatter mínimo |

Bug ambíguo → reportar problema + opções antes de entregar. Nunca esconder.

---

## PASSO 5 — Re-testar após correção

Se corrigiu → roda PASSO 2 de novo → só entrega quando tudo verde.
Sem exceções.

---

## PASSO 6 — Relatório obrigatório

**Sempre** incluir no início da entrega:

```
╔══════════════════════════════════╗
║  QA ✅  N/N verificações ok      ║
║  Testado: bash -n, py_compile... ║
╚══════════════════════════════════╝
```

Se corrigiu algo:
```
╔════════════════════════════════════════╗
║  QA ✅  N/N ok                         ║
║  🔧 Corrigido automaticamente:         ║
║    • frames.py: default 100 → 400     ║
║    • diarize.py: Speaker → SPEAKER    ║
╚════════════════════════════════════════╝
```

---

## REGRAS ABSOLUTAS

1. **Nunca entregar sem rodar o QA real** (bash, não mental)
2. **Se testou e corrigiu: re-testar até zerar**
3. **Nunca esconder um bug** — reportar claramente se não conseguiu corrigir
4. **Retroativo**: ao modificar skill existente, QA no arquivo inteiro (não só no que mudou)
5. **Após QA: atualizar backup** → `bash ~/Downloads/Marketing_OS/scripts/atualizar_skill.sh <nome>`

---

## PADRÃO UNIVERSAL

Todo matching de termos usa `grep -qiE` com regex. Nunca busca literal.

| Termo | Regex |
|-------|-------|
| padrão universal | `PADR.O UNIVERSAL` |
| micro-expressões | `MICRO.?EXPRESS` |
| decisor oculto | `DECISOR.{0,20}(OCULTO\|SILENCIOSO)` |
| minipacto | `MINI.?PACTO` |
| speaker (pyannote) | `SPEAKER_[0-9]+` — sempre maiúsculo |


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
