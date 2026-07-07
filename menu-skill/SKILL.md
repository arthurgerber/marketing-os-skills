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
