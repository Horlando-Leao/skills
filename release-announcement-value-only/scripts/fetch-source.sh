#!/usr/bin/env bash
# Extrai o conteúdo bruto de uma entrega para o anúncio de release.
# O modelo usa essa saída para FILTRAR só o que tem valor de produto (não reportar refator/chore/etc.).
#
# Uso:
#   fetch-source.sh tag <vX.Y.Z>
#   fetch-source.sh pr  <numero>
set -euo pipefail

kind="${1:-}"
ref="${2:-}"

if [[ -z "$kind" || -z "$ref" ]]; then
  echo "Uso: $0 tag <vX.Y.Z> | pr <numero>" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh (GitHub CLI) não encontrado." >&2
  exit 1
fi

case "$kind" in
  tag)
    gh release view "$ref" --json tagName,name,body,url \
      --jq '"# Release \(.tagName) — \(.name)\n\(.url)\n\n\(.body)"'
    ;;
  pr)
    gh pr view "$ref" --json number,title,body,url,headRefName \
      --jq '"# PR #\(.number) — \(.title)\nbranch: \(.headRefName)\n\(.url)\n\n\(.body)"'
    ;;
  *)
    echo "Tipo inválido: '$kind' (use 'tag' ou 'pr')." >&2
    exit 1
    ;;
esac
