# Marketing OS — Skills para Claude / Cowork

Skills do Marketing OS dos Grupos VR, Silva e Lazari.  
Desenvolvido por Arthur Gerber — COO.

---

## Skills disponíveis

| Skill | Descrição | Tamanho |
|-------|-----------|---------|
| `analisa-video` | Analisa calls, vídeos e áudios de vendas — diarização, frames, micro-expressões, score de closer | 31K |
| `fup-mensal` | Gera planilhas de Follow-Up por closer (VR, Silva, Lazari) | 5K |
| `acesso-total` | Acesso completo ao Mac via Cowork | 2K |
| `questiona-planeja-age` | Postura de execução sênior — questiona, planeja, executa | 2K |
| `menu-skill` | Menu de skills disponíveis | 1K |
| `docx` | Criar e editar documentos Word | 9K |
| `pdf` | Manipular PDFs | 14K |
| `pptx` | Criar e editar apresentações | 16K |
| `xlsx` | Criar e editar planilhas Excel | 6K |
| `schedule` | Agendar tarefas automáticas | 2K |

---

## Como instalar uma skill

### Método 1 — Pelo Cowork (mais fácil)
1. Baixe o arquivo `.skill` que deseja (ex: `analisa-video.skill`)
2. Abra o Cowork
3. Arraste o arquivo para o chat ou clique no ícone de anexo
4. Clique em **"Save skill"**
5. Pronto — a skill fica disponível em todas as sessões futuras

### Método 2 — Via Terminal (para desenvolvedores)
```bash
# Clonar o repositório
git clone https://github.com/SEU_USUARIO/marketing-os-skills.git

# Rodar o instalador
bash marketing-os-skills/instalar_skills.sh
```

---

## Como funciona a persistência

As skills ficam salvas em `~/Downloads/.claude/skills/<nome>/`.  
Esse caminho é:
- ✅ Lido pelo Cowork automaticamente (quando Downloads é a pasta selecionada)
- ✅ Acessível pelo Terminal do Mac
- ✅ Versionável via Git
- ✅ Restaurável via `bash ~/Downloads/Marketing_OS/scripts/restaurar_tudo.sh`

---

## Como criar uma nova skill e salvar neste padrão

1. Crie a pasta: `mkdir -p ~/Downloads/.claude/skills/minha-skill/scripts/`
2. Crie o `SKILL.md` com frontmatter YAML:
   ```yaml
   ---
   name: minha-skill
   description: "Descrição clara do que faz e quando acionar. SEMPRE incluir variações de linguagem."
   allowed-tools: Bash, Read, AskUserQuestion
   ---
   ```
3. Adicione scripts em `scripts/` se necessário
4. No Cowork, peça ao Claude para empacotar:
   > "Empacota a skill em ~/Downloads/.claude/skills/minha-skill/ como minha-skill.skill"
5. Clique **"Save skill"** no arquivo gerado
6. Adicione ao backup: copie o `SKILL.md` para `~/Downloads/Marketing_OS/skill_backups/`

---

## Padrão Universal de Reconhecimento de Termos

Toda skill do Marketing OS usa reconhecimento fuzzy para termos-chave:

| Termo | Regex utilizado |
|-------|----------------|
| minipacto, mini-pacto, Minipacto | `MINI.?PACTO` |
| micro-expressões, microexpressões | `MICRO.?EXPRESS` |
| decisor oculto, decisor silencioso | `DECISOR.*(OCULTO\|SILENCIOSO)` |
| fechamento | `FECHA` |

Usar sempre `grep -qiE` — nunca busca literal.

---

## Restauração automática

O script `restaurar_tudo.sh` roda no login do Mac via LaunchAgent.  
Restaura os arquivos críticos do backup caso sejam perdidos.

```bash
# Rodar manualmente
bash ~/Downloads/Marketing_OS/scripts/restaurar_tudo.sh
```
