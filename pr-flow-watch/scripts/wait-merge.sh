#!/usr/bin/env bash
# wait-merge.sh — espera a PR ser mergeada (ou fechada sem merge).
# Uso: wait-merge.sh <pr_number> [interval_seconds=20]
# Saída (única, no final):
#   MERGE_RESULT=merged
#   MERGE_SHA=<sha do merge commit>
#   MERGE_BRANCH=<branch base>
#   ou
#   MERGE_RESULT=closed_unmerged
# Exit code: 0 se mergeada, 1 se fechada sem merge.

set -euo pipefail

PR="${1:-}"
INTERVAL="${2:-20}"
if [[ -z "${PR}" ]]; then
  echo "Uso: $0 <pr_number> [interval_seconds]" >&2
  exit 2
fi

while true; do
  INFO="$(gh pr view "${PR}" --json state,mergeCommit,baseRefName)"
  STATE="$(echo "${INFO}" | jq -r '.state')"

  if [[ "${STATE}" == "MERGED" ]]; then
    SHA="$(echo "${INFO}" | jq -r '.mergeCommit.oid')"
    BRANCH="$(echo "${INFO}" | jq -r '.baseRefName')"
    echo "MERGE_RESULT=merged"
    echo "MERGE_SHA=${SHA}"
    echo "MERGE_BRANCH=${BRANCH}"
    exit 0
  fi
  if [[ "${STATE}" == "CLOSED" ]]; then
    echo "MERGE_RESULT=closed_unmerged"
    exit 1
  fi
  sleep "${INTERVAL}"
done
