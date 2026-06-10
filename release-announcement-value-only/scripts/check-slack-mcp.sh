#!/usr/bin/env bash
# Verificação rápida: o conector/MCP do Slack está disponível para publicar?
# Best-effort — a confirmação real é a presença das tools mcp__*_Slack__* na sessão do agente.
set -uo pipefail

if command -v claude >/dev/null 2>&1; then
  if claude mcp list 2>/dev/null | grep -iq slack; then
    echo "✅ Slack MCP detectado em 'claude mcp list'."
    exit 0
  fi
  echo "⚠️  Slack não apareceu em 'claude mcp list'."
else
  echo "⚠️  CLI 'claude' indisponível — não dá para checar via 'claude mcp list'."
fi

cat <<'TXT'
Antes de publicar, garanta que o Slack está conectado:
  - Conector gerenciado (claude.ai): habilite "Slack" em Integrações/Connectors da conta.
  - MCP local: adicione com `claude mcp add` e reinicie a sessão.
A skill só cria o rascunho se as ferramentas mcp__..._Slack__* estiverem disponíveis nesta sessão.
TXT
exit 1
