#!/usr/bin/env bash
# wait-checks.sh — espera os checks de CI de uma PR chegarem a um estado terminal.
# Não usa `gh pr checks --watch` porque a versão do gh CLI disponível não suporta essa flag.
# Uso: wait-checks.sh <pr_number> [interval_seconds=20]
# Saída (única, no final — nada é impresso durante o polling):
#   CI_RESULT=success
#   ou
#   CI_RESULT=failure
#   CHECKS_FAILED:
#   <nome do check 1>
#   <nome do check 2>
# Exit code: 0 se todos os checks passaram, 1 se algum falhou.

set -euo pipefail

PR="${1:-}"
INTERVAL="${2:-20}"
if [[ -z "${PR}" ]]; then
  echo "Uso: $0 <pr_number> [interval_seconds]" >&2
  exit 2
fi

ROLLUP=""
while true; do
  ROLLUP="$(gh pr view "${PR}" --json statusCheckRollup --jq '.statusCheckRollup')"
  PENDING="$(echo "${ROLLUP}" | jq '[.[] | select(
    (.status != "" and .status != "COMPLETED")
    or (.status == "" and (.state == "PENDING" or .state == ""))
  )] | length')"
  [[ "${PENDING}" -eq 0 ]] && break
  sleep "${INTERVAL}"
done

FAILED="$(echo "${ROLLUP}" | jq -r '[.[] | select(
    (.status == "COMPLETED" and (.conclusion != "SUCCESS" and .conclusion != "NEUTRAL" and .conclusion != "SKIPPED"))
    or (.status == "" and .state != "SUCCESS")
  ) | (.name // .context)] | .[]')"

if [[ -z "${FAILED}" ]]; then
  echo "CI_RESULT=success"
  exit 0
else
  echo "CI_RESULT=failure"
  echo "CHECKS_FAILED:"
  echo "${FAILED}"
  exit 1
fi
