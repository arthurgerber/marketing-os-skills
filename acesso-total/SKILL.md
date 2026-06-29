---
name: acesso-total
description: >
  Solicitar acesso completo à máquina do Arthur automaticamente em uma única chamada. Use SEMPRE que o usuário disser "acesso total", "iniciar", "iniciar sessão", "começa", "libera acesso", "libera tudo", "permissão total", "acessa minha máquina", "me dá acesso", "quero acesso", "prepara tudo", "conecta tudo", ou qualquer variação que indique querer liberar o controle do computador. Não peça confirmação — execute diretamente.
---

# Acesso Total — Máquina do Arthur

Quando esta skill for ativada, siga exatamente estes passos **sem pedir confirmação**.

---

## Passo 1 — Ler a lista dinâmica de apps instalados

A ferramenta `request_access` contém no seu schema uma tag `<installed-apps>` com todos os apps instalados na máquina em tempo real. Use essa lista como fonte.

## Passo 2 — Filtrar apps bloqueados por política

Remova silenciosamente antes de chamar `request_access`:
- **Spotify, Livros, Podcasts, TV** → bloqueados por política, ignorar sem mencionar.

Qualquer outro app que retorne `policyDenied` também deve ser ignorado silenciosamente.

## Passo 3 — Chamar request_access com tudo

Passe a lista completa filtrada com:
- `clipboardRead: true`
- `clipboardWrite: true`
- `systemKeyCombos: true`
- `reason`: "Acesso completo à máquina do Arthur para executar qualquer tarefa sem interrupções."

## Passo 3.5 — Montar pasta Downloads (OBRIGATÓRIO)

Chame `mcp__cowork__request_cowork_directory` com `path: "~/Downloads"` para montar a pasta de downloads diretamente no ambiente de trabalho.

Isso evita interrupções no meio de tarefas — qualquer arquivo baixado ou gerado fica imediatamente acessível para leitura e escrita sem precisar pedir permissão separada.

## Passo 4 — Verificar Live Captions do macOS

Tire um screenshot e verifique se a janela flutuante de Live Captions está visível na tela. Não bloqueie o fluxo — apenas registre o status na confirmação final:
- Ativo → confirmar normalmente
- Não detectado → informar: "Live Captions não detectado — para ativar: Ajustes > Acessibilidade > Live Captions."

## Passo 5 — Conectar ao Chrome via extensão (OBRIGATÓRIO)

**Chrome e Safari não permitem cliques via computer-use** — isso é uma limitação do sistema operacional que não pode ser alterada. O equivalente a "100% de acesso ao browser" é feito via extensão Claude in Chrome.

Execute os seguintes passos para conectar todos os Chromes disponíveis:

1. Chame `mcp__Claude_in_Chrome__list_connected_browsers` para ver quantas janelas estão conectadas
2. Para cada browser conectado, chame `mcp__Claude_in_Chrome__select_browser` com o deviceId dele
3. Chame `mcp__Claude_in_Chrome__tabs_context_mcp` para ver os tabs ativos em cada janela
4. Se nenhum Chrome estiver conectado, informe Arthur: "Clique no ícone da extensão Claude na janela do Chrome que quer controlar"

Com a extensão conectada, tenho **acesso total** ao browser:
- Navegar URLs → `navigate`
- Clicar em qualquer elemento → `read_page` + `left_click`
- Digitar em campos → `form_input`
- Ler conteúdo de qualquer página → `get_page_text` / `javascript_tool`
- Executar JavaScript arbitrário → `javascript_tool`

**Regra:** Só pedir autorização de Arthur para ações financeiras (transferências, compras, trades) ou ações irreversíveis de alto risco. Para tudo mais — navegar, clicar, ler, preencher — agir diretamente.

## Passo 6 — Confirmar de forma compacta

Após tudo, informe em até 5 linhas:
- Quantos apps foram liberados
- Se a pasta Downloads foi montada com sucesso
- Status do Live Captions (ativo / não detectado)
- Quantas janelas Chrome conectadas e quais tabs estão ativos
- "Pronto. O que quer fazer?"

---

## Contexto desta máquina

- **Chrome/Safari via extensão** → acesso 100%: clicar, navegar, ler, preencher, executar JS
- **Chrome/Safari via computer-use** → somente screenshot (limitação de SO, não de permissão)
- **Terminal, Atalhos, Automator** → tier "click" via computer-use; comandos shell → usar Bash diretamente
- **Todos os outros apps** → controle total via computer-use
- **~/Downloads** → montado automaticamente no Passo 3.5 para leitura/escrita direta de arquivos

## Perfil do usuário

Arthur Gerber Amaro — COO do Grupo Silva, sócio/diretor do Grupo Lazari e Grupo VR. Usa o Claude como analista sênior operacional com acesso total à máquina. Agir sempre com autonomia máxima — sem questionamentos desnecessários, sem pedir confirmação para ações do dia a dia.


---

## ANTES DE ENTREGAR — PROTOCOLO OBRIGATÓRIO

1. Rodar **auto-qa** no que foi criado/modificado
2. Re-testar após qualquer correção
3. Só apresentar a Arthur quando tudo verde
4. Para desenvolvimento técnico: usar skill **devstack** como guia de arquitetura


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
