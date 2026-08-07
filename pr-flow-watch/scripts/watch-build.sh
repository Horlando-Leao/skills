#!/usr/bin/env bash
# watch-build.sh — localiza o workflow run disparado por um commit (merge ou tag) e assiste
# até ele terminar, usando `gh run watch`, que é bloqueante nativo do gh CLI (sem polling manual).
#
# A versão do gh CLI deste ambiente não suporta `gh run list --commit`/`--branch`, então o
# filtro por SHA/branch é feito no lado do cliente via --json + jq.
#
# Uso: watch-build.sh <commit_sha> [branch] [workflow_name] [interval_seconds=5]
#   branch:        opcional — filtra por headBranch. Vazio = ignora.
#   workflow_name: opcional — filtra por nome do workflow (gh run list -w). Útil quando mais
#                  de um workflow dispara para o mesmo commit (ex.: build/deploy + notificação).
#                  Vazio = considera qualquer workflow, pegando o run mais antigo (o primeiro
#                  disparado diretamente pelo commit, não os que dependem dele via workflow_run).
#
# Saída (única, no final):
#   BUILD_RESULT=success|failure|not_found
#   <url do run>   (se encontrado)
# Exit code: 0 se o run terminou com sucesso, 1 caso contrário/não encontrado.

set -euo pipefail

SHA="${1:-}"
BRANCH="${2:-}"
WORKFLOW="${3:-}"
INTERVAL="${4:-5}"
if [[ -z "${SHA}" ]]; then
  echo "Uso: $0 <commit_sha> [branch] [workflow_name] [interval_seconds]" >&2
  exit 2
fi

RUN_ID=""
for _ in $(seq 1 30); do
  if [[ -n "${WORKFLOW}" ]]; then
    LIST="$(gh run list --workflow "${WORKFLOW}" --limit 30 --json databaseId,headSha,headBranch)"
  else
    LIST="$(gh run list --limit 30 --json databaseId,headSha,headBranch)"
  fi

  RUN_ID="$(echo "${LIST}" | jq -r --arg sha "${SHA}" --arg branch "${BRANCH}" '
    [.[] | select(.headSha == $sha and ($branch == "" or .headBranch == $branch))]
    | sort_by(.databaseId)
    | .[0].databaseId // empty
  ')"

  [[ -n "${RUN_ID}" ]] && break
  sleep 10
done

if [[ -z "${RUN_ID}" ]]; then
  echo "BUILD_RESULT=not_found"
  exit 1
fi

RESULT=0
gh run watch "${RUN_ID}" --exit-status --interval "${INTERVAL}" || RESULT=$?

if [[ "${RESULT}" -eq 0 ]]; then
  echo "BUILD_RESULT=success"
else
  echo "BUILD_RESULT=failure"
fi
gh run view "${RUN_ID}" --json url --jq '.url'
exit "${RESULT}"
