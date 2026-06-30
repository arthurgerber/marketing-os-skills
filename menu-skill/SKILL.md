---
name: menu-skill
description: >
  Mostra todas as skills disponíveis para o usuário de forma clara e organizada.
  Acionar SEMPRE que o usuário disser: "menu", "menu skill", "menu skills",
  "skill disponivel", "skills disponiveis", "skill disponíveis", "skills disponíveis",
  "skill disponveis", "skills disponveis", "o que você sabe fazer",
  "o que posso pedir", "quais skills tenho", "lista de skills", "o que tenho disponível",
  "me mostra as skills", "minhas skills", ou qualquer variação indicando que quer
  ver o que está disponível. Aciona com palavras curtas como "menu" ou "skills" sozinhas.
---

# Menu de Skills

Quando esta skill for acionada, ler a lista de skills disponíveis no contexto
(seção `<available_skills>`) e apresentar ao usuário de forma clara.

## Como apresentar

Montar uma resposta no seguinte formato:

```
## Suas skills disponíveis

**[Nome da skill]**
[Uma linha explicando o que faz]
Como chamar: "[exemplo de frase natural]"

**[Nome da skill]**
...
```

Regras:
- Listar TODAS as skills presentes em `<available_skills>` — nunca omitir
- Para cada skill, extrair o nome e escrever uma linha curta e direta do que ela faz
- Inventar um exemplo de frase natural que o usuário pode digitar para acioná-la
- Não incluir esta própria skill (menu-skills) na lista — ela é transparente
- Não usar jargão técnico — escrever como se fosse explicar para alguém que nunca usou
- Se não houver nenhuma skill além desta, informar: "Você não tem outras skills instaladas ainda."

## Tom

Direto, sem enrolação. O objetivo é que o usuário olhe, entenda e saiba o que digitar.


---

## ANTES DE ENTREGAR — PROTOCOLO OBRIGATÓRIO

1. Rodar **auto-qa** no que foi criado/modificado
2. Re-testar após qualquer correção
3. Só apresentar a Arthur quando tudo verde
4. Para desenvolvimento técnico: usar skill **devstack** como guia de arquitetura


---

## 🤖 PADRÃO DE AGENTES — INTEGRAÇÃO OBRIGATÓRIA

Esta skill suporta e incentiva execução multi-agente paralela.

### Coordenadores disponíveis (usar sempre que aplicável):
- **devstack** → spawnar quando a tarefa envolver criação/edição de código, scripts, integrações
- **auto-qa** → spawnar SEMPRE no final, antes de entregar qualquer output
- **watchdog** → spawnar se output parecer incompleto, rápido demais, ou suspeito
- **debugger** → spawnar quando encontrar erro — recebe contexto completo e resolve

### Como chamar subagentes desta skill:
```
[SKILL COORDENADORA] executa a tarefa principal
  ├── Subagente devstack: cria/corrige qualquer código necessário
  ├── Subagente auto-qa: valida o output antes de entregar
  └── Subagente watchdog: monitora se o processo foi seguido corretamente
[SKILL COORDENADORA] integra resultados e entrega para Arthur
```

### Regras de paralelização:
- Se a tarefa tem partes independentes → dividir em subagentes simultâneos, nunca sequencial
- Nunca fazer em 1 agente o que 3 podem fazer ao mesmo tempo mais rápido
- O subagente auto-qa é OBRIGATÓRIO antes de qualquer entrega final


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
