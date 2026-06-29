#!/bin/bash
# ============================================================
# instalar_skills.sh — Marketing OS
# ============================================================
# Instala todas as skills do Marketing OS em ~/Downloads/.claude/skills/
# Compatível com Cowork (quando Downloads é a pasta selecionada).
#
# USO:
#   bash instalar_skills.sh            # instala tudo
#   bash instalar_skills.sh analisa-video fup-mensal  # instala específicas
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills_packaged"
SKILLS_DST="$HOME/Downloads/.claude/skills"

echo "============================================"
echo "  Marketing OS — Instalação de Skills"
echo "============================================"
echo ""

# Verificar se os pacotes existem
if [ ! -d "$SKILLS_SRC" ]; then
    echo "❌ Pasta skills_packaged não encontrada em: $SKILLS_SRC"
    echo "   Clone o repositório completo e tente novamente."
    exit 1
fi

mkdir -p "$SKILLS_DST"

# Determinar quais skills instalar
if [ $# -gt 0 ]; then
    SKILLS_TO_INSTALL=("$@")
    echo "Instalando skills específicas: ${SKILLS_TO_INSTALL[*]}"
else
    SKILLS_TO_INSTALL=()
    for f in "$SKILLS_SRC"/*.skill; do
        [ -f "$f" ] && SKILLS_TO_INSTALL+=("$(basename "$f" .skill)")
    done
    echo "Instalando todas as skills (${#SKILLS_TO_INSTALL[@]} encontradas)"
fi

echo ""
INSTALADAS=0
FALHAS=0

for skill in "${SKILLS_TO_INSTALL[@]}"; do
    skill_file="$SKILLS_SRC/${skill}.skill"

    if [ ! -f "$skill_file" ]; then
        echo "  ⚠️  $skill — arquivo .skill não encontrado"
        FALHAS=$((FALHAS + 1))
        continue
    fi

    # Extrair para ~/.claude/skills/
    dest="$SKILLS_DST/$skill"
    mkdir -p "$dest"

    # Unzip mantendo estrutura interna (sem o diretório raiz do zip)
    unzip -qo "$skill_file" -d /tmp/_skill_install_tmp/

    if [ -d "/tmp/_skill_install_tmp/$skill" ]; then
        cp -rf "/tmp/_skill_install_tmp/$skill/." "$dest/"
        rm -rf /tmp/_skill_install_tmp
        echo "  ✅ $skill instalada em $dest"
        INSTALADAS=$((INSTALADAS + 1))
    else
        echo "  ❌ $skill — estrutura inesperada no zip"
        FALHAS=$((FALHAS + 1))
    fi
done

echo ""
echo "============================================"
echo "  Resultado: $INSTALADAS instaladas | $FALHAS falhas"
echo "============================================"
echo ""
echo "Próximo passo:"
echo "  1. Abra o Cowork com sua pasta Downloads selecionada"
echo "  2. As skills já estarão disponíveis automaticamente"
echo ""
echo "Para verificar: ls ~/Downloads/.claude/skills/"
