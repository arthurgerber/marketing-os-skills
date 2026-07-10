#!/usr/bin/env bash
# =====================================================================
#  SETUP 2o REMOTE — GitLab (redundancia)
#  >>> JA CONFIGURADO na maquina do Arthur (2026-07-09). <<<
#  Use este script SO em MAQUINA NOVA (esposa / Mac Mini / outra).
#  Uso:  bash setup_gitlab_remote.sh              (usa grupo padrao arthur.ga94-group)
#        bash setup_gitlab_remote.sh OUTRO_NAMESPACE
# =====================================================================
set -uo pipefail

NS="${1:-arthur.ga94-group}"   # namespace/grupo do GitLab (padrao: grupo real)
URL="https://gitlab.com/${NS}/marketing-os-skills.git"

REPO=$(find "$HOME" -maxdepth 4 -type d -name "marketing-os-skills" 2>/dev/null | head -1)
if [ -z "${REPO:-}" ]; then
  echo "ERRO: repo local marketing-os-skills nao encontrado sob \$HOME."
  echo "Clone primeiro:  git clone https://github.com/arthurgerber/marketing-os-skills.git"
  exit 1
fi
echo "Repo: $REPO"

git config --global credential.helper osxkeychain

if git -C "$REPO" remote | grep -q "^gitlab$"; then
  git -C "$REPO" remote set-url gitlab "$URL"; echo "remote 'gitlab' atualizado -> $URL"
else
  git -C "$REPO" remote add gitlab "$URL"; echo "remote 'gitlab' adicionado -> $URL"
fi
git -C "$REPO" remote -v

echo "-- 1o push (autentique quando pedir) --"
echo "   Username: git-real   |   Password: token glpat-... (GitLab > Settings > Access tokens; escopo write_repository; role Maintainer)"
git -C "$REPO" push -u gitlab main && echo "OK: GitLab configurado. Deploy passa a empurrar nos dois remotes." \
  || echo "push falhou. Verifique: projeto existe no GitLab? token com write_repository + Maintainer? credencial velha? (git credential-osxkeychain erase)"
