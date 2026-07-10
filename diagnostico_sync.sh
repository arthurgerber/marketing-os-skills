#!/usr/bin/env bash
# DIAGNÓSTICO DE SINCRONIZAÇÃO — Marketing OS (SOMENTE LEITURA, não altera nada)
# Rode no Mac:  bash diagnostico_sync.sh
set -uo pipefail

echo "======================================================"
echo " DIAGNÓSTICO MARKETING OS — $(date '+%Y-%m-%d %H:%M')"
echo "======================================================"

BASE="$HOME/Downloads"
PROJ="$BASE/Projetos"

echo
echo "### 1. GROUND TRUTH GLOBAL"
if [ -f "$BASE/MARKETING_OS_ARQUITETURA.md" ]; then
  echo "OK   MARKETING_OS_ARQUITETURA.md  ($(wc -c < "$BASE/MARKETING_OS_ARQUITETURA.md") bytes)"
else
  echo "FALTA  $BASE/MARKETING_OS_ARQUITETURA.md  <-- ausente local"
fi

echo
echo "### 2. ÁRVORE DE PROJETOS (local, com tamanhos)"
if [ -d "$PROJ" ]; then
  find "$PROJ" -type f \( -name "*.md" -o -name "*.sh" \) -print0 \
    | while IFS= read -r -d '' f; do printf "%8s  %s\n" "$(wc -c < "$f")" "${f#$BASE/}"; done
else
  echo "FALTA  $PROJ  <-- pasta de projetos não existe local"
fi

echo
echo "### 3. CHECKLIST DOCS CANÔNICOS (local)"
for f in \
  "Projetos/INDICE_PROJETOS.md" \
  "Projetos/GUIA_ORGANIZACAO_PROJETOS.md" \
  "Projetos/CS/PROJETO_CS_ARQUITETURA.md" \
  "Projetos/Comercial/PLATAFORMA_COMERCIAL_ARQUITETURA.md" \
  "Projetos/Comercial/PROCESSO_BASE_CLOSER.md" \
  "Projetos/Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md" \
  "Projetos/Marketing/FRAMEWORK_ANALISE_COPY_LIVES.md" \
  "Projetos/Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md" ; do
  if [ -f "$BASE/$f" ]; then printf "OK     %-60s %s bytes\n" "$f" "$(wc -c < "$BASE/$f")";
  else printf "FALTA  %-60s\n" "$f"; fi
done

echo
echo "### 4. REPOSITÓRIO GIT (marketing-os-skills)"
REPO=$(find "$HOME" -maxdepth 4 -type d -name "marketing-os-skills" 2>/dev/null | head -1)
if [ -n "${REPO:-}" ]; then
  echo "Repo local: $REPO"
  git -C "$REPO" remote -v | head -2
  echo "-- status --"; git -C "$REPO" status -s | head -20
  echo "-- último commit --"; git -C "$REPO" log -1 --oneline 2>/dev/null
  echo "-- arquivos versionados em Projetos/ --"
  git -C "$REPO" ls-files "Projetos/*" 2>/dev/null | head -40
else
  echo "FALTA  clone local de marketing-os-skills não encontrado sob \$HOME"
fi

echo
echo "### 5. SKILL DE ENFORCEMENT / SYNC (procurando)"
grep -rilE "enforcement|auto.?sync|salvar.*(drive|github)|3 lugares|rclone|gdrive" \
  "$HOME/.claude" "$HOME/Downloads" 2>/dev/null | grep -iE "SKILL\.md|sync|enforce" | head -20 \
  || echo "nenhuma skill de sync/enforcement localizada nesses caminhos"

echo
echo "### 6. FERRAMENTA DE DRIVE NO TERMINAL (rclone/gdrive?)"
command -v rclone >/dev/null && echo "rclone: $(command -v rclone)" || echo "rclone: não instalado"
command -v gdrive >/dev/null && echo "gdrive: $(command -v gdrive)" || echo "gdrive: não instalado"

echo
echo "======================================================"
echo " FIM. Cole a saída inteira de volta no chat."
echo "======================================================"
