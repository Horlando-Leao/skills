#!/usr/bin/env bash
# wait-approval.sh — espera a PR ser aprovada (ou fechada/mergeada sem aprovação).
# Uso: wait-approval.sh <pr_number> [interval_seconds=30]
# Saída (única, no final):
#   APPROVAL_RESULT=approved
#   ou
#   APPROVAL_RESULT=closed_without_approval
# Exit code: 0 se aprovada, 1 caso contrário.

set -euo pipefail

PR="${1:-}"
INTERVAL="${2:-30}"
if [[ -z "${PR}" ]]; then
  echo "Uso: $0 <pr_number> [interval_seconds]" >&2
  exit 2
fi

while true; do
  INFO="$(gh pr view "${PR}" --json state,reviewDecision)"
  STATE="$(echo "${INFO}" | jq -r '.state')"
  DECISION="$(echo "${INFO}" | jq -r '.reviewDecision')"

  if [[ "${DECISION}" == "APPROVED" ]]; then
    echo "APPROVAL_RESULT=approved"
    exit 0
  fi
  if [[ "${STATE}" != "OPEN" ]]; then
    echo "APPROVAL_RESULT=closed_without_approval"
    exit 1
  fi
  sleep "${INTERVAL}"
done
