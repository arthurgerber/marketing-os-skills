# POLÍTICA CANÔNICA — Sincronização, Segurança e Redundância
**Marketing OS · v2.0 · 2026-07-08**
**Escopo:** OBRIGATÓRIA para TUDO — skills (atuais e futuras), agentes/sub-agentes (atuais e futuros), arquiteturas de projeto (atuais e futuras) e todo código/doc canônico.

> Toda skill, agente ou projeto novo DEVE referenciar e herdar esta política. Qualquer criação/edição de arquivo canônico segue estas regras. Quem cria um projeto/skill/agente sem apontar para cá está fora do padrão.

---

## 1. TRÊS LUGARES, SEMPRE (fonte de verdade + redundância)
Todo arquivo canônico (arquitetura, código `.sh`/`.py`, skill, framework, índice, ground truth) vive, **completo e idêntico**, em:
1. **Local** (`~/Downloads/Projetos/...`) — cópia de trabalho.
2. **GitHub** (`github.com/arthurgerber/marketing-os-skills`) — versionado (backup primário).
3. **GitLab** (mirror privado — segundo remote) — redundância caso o GitHub falhe. Remote `gitlab` → `https://gitlab.com/arthur.ga94-group/marketing-os-skills.git` (JÁ CONFIGURADO em 2026-07-09).
4. **Drive** (`Marketing OS/Projetos/...`) — **conveniência de leitura no navegador**, com **conteúdo completo** (nunca stub/ponteiro).

Regra de bytes: os 4 devem bater. Nenhum arquivo no Drive/remotes pode ter menos conteúdo que a versão canônica.

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
