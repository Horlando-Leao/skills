# Padrões de Detecção - Secret Detector

Documentação técnica dos padrões regex usados para detectar segredos expostos.

## Serviços de Pagamento

### Stripe Live Key
- **Padrão:** `sk_live_[A-Za-z0-9]{24,}`
- **Severidade:** CRITICAL
- **Descrição:** Chave de produção Stripe (acesso completo)
- **Exemplo (fictício):** `sk_live_XXXXXXXXXXXXXXXXXXXX...` (formato)

### Stripe Test Key
- **Padrão:** `sk_test_[A-Za-z0-9]{24,}`
- **Severidade:** HIGH
- **Descrição:** Chave de teste Stripe
- **Exemplo (fictício):** `sk_test_XXXXXXXXXXXXXXXXXXXX...` (formato)

### Stripe Restricted Key
- **Padrão:** `rk_live_[A-Za-z0-9]{24,}`
- **Severidade:** CRITICAL
- **Descrição:** Chave restrita de Stripe
- **Exemplo (fictício):** `rk_live_XXXXXXXXXXXXXXXXXXXX...` (formato)

## GitHub Tokens

### GitHub Personal Access Token (PAT)
- **Padrão:** `ghp_[A-Za-z0-9]{36}`
- **Severidade:** CRITICAL
- **Descrição:** Token de Acesso Pessoal GitHub
- **Exemplo (fictício):** `ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXX...` (formato)

### GitHub OAuth Token
- **Padrão:** `gho_[A-Za-z0-9]{36}`
- **Severidade:** CRITICAL
- **Descrição:** Token OAuth do GitHub
- **Exemplo (fictício):** `gho_XXXXXXXXXXXXXXXXXXXXXXXXXXXX...` (formato)

### GitHub App Token
- **Padrão:** `ghu_[A-Za-z0-9]{36}`
- **Severidade:** CRITICAL
- **Descrição:** Token de App GitHub
- **Exemplo (fictício):** `ghu_XXXXXXXXXXXXXXXXXXXXXXXXXXXX...` (formato)

### GitHub Refresh Token
- **Padrão:** `ghr_[A-Za-z0-9]{76}`
- **Severidade:** CRITICAL
- **Descrição:** Token de Refresh GitHub
- **Exemplo (fictício):** `ghr_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...` (formato)

## Credenciais AWS

### AWS Access Key ID
- **Padrão:** `AKIA[0-9A-Z]{16}`
- **Severidade:** CRITICAL
- **Descrição:** ID de Chave de Acesso AWS
- **Exemplo (fictício):** `AKIAXXXXXXXXXXX...` (formato)

### AWS Secret Access Key
- **Padrão:** `aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}`
- **Severidade:** CRITICAL
- **Descrição:** Chave Secreta de Acesso AWS
- **Exemplo (fictício):** `aws_secret_access_key = XXXXXXXXXXXXXXXX/XXXXXXXXXXXXXXX...` (formato)

## Senhas e Credenciais Genéricas

### Atribuição de Senha
- **Padrão:** `password\s*[:=]\s*['\"]([^'\"]{8,})['\"]`
- **Severidade:** CRITICAL
- **Descrição:** Senha em atribuição de variável
- **Exemplo (fictício):** `password = "XXxXXxxXXxXXX"` (formato)

### Atribuição de API Key
- **Padrão:** `api[_-]?key\s*[:=]\s*['\"]([A-Za-z0-9\-._~+/]{20,})['\"]`
- **Severidade:** CRITICAL
- **Descrição:** API Key em atribuição
- **Exemplo (fictício):** `api_key = "XXXXXXXXXXXXXXXXXXXXXXX"` (formato)

## Chaves Privadas

### SSH/RSA Private Key
- **Padrão:** `-----BEGIN (?:RSA|DSA|EC) PRIVATE KEY-----`
- **Severidade:** CRITICAL
- **Descrição:** Chave Privada SSH/RSA
- **Locais Comuns:** `~/.ssh/id_rsa`, `~/.ssh/id_ecdsa`, `config files`

### OpenSSH Private Key
- **Padrão:** `-----BEGIN OPENSSH PRIVATE KEY-----`
- **Severidade:** CRITICAL
- **Descrição:** Chave Privada OpenSSH
- **Locais Comuns:** `~/.ssh/id_ed25519`

### PGP Private Key
- **Padrão:** `-----BEGIN PGP PRIVATE KEY BLOCK-----`
- **Severidade:** CRITICAL
- **Descrição:** Chave Privada PGP
- **Locais Comuns:** `~/.gnupg/privring.gpg`

## URLs com Credenciais

### URL com User:Password
- **Padrão:** `https?://[A-Za-z0-9\-._]+:[A-Za-z0-9\-._@]+@[A-Za-z0-9\-._/]+`
- **Severidade:** CRITICAL
- **Descrição:** URL contendo credenciais embutidas
- **Exemplo (fictício):** `https://user:XXXX@github.com/repo.git` (formato)

## Tokens Genéricos

### Bearer Token
- **Padrão:** `Bearer\s+[A-Za-z0-9\-._~+/=]{20,}`
- **Severidade:** HIGH
- **Descrição:** Bearer token genérico
- **Contexto:** Headers HTTP, Authorization

### JWT Token
- **Padrão:** `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
- **Severidade:** HIGH
- **Descrição:** JSON Web Token (JWT)
- **Exemplo (fictício):** `eyJXXXXXXXXXXXXX.eyJXXXXXXXXXXXXX.XXXXXXXXXXXX` (formato)

## Serviços de Terceiros

### Firebase API Key
- **Padrão:** `AIza[0-9A-Za-z\-_]{35}`
- **Severidade:** HIGH
- **Descrição:** Chave API Firebase/Google
- **Exemplo (fictício):** `AIzaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...` (formato)

### Google OAuth Token
- **Padrão:** `ya29\.[0-9A-Za-z\-_]+`
- **Severidade:** HIGH
- **Descrição:** Token OAuth Google
- **Exemplo (fictício):** `ya29.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...` (formato)

### Slack Token
- **Padrão:** `xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9-]{24,32}`
- **Severidade:** CRITICAL
- **Descrição:** Token ou Webhook Slack
- **Exemplo (fictício):** `xoxb-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXXXXXXXXXX...` (formato)

## Níveis de Severidade

### CRITICAL (🔴)
- Chaves privadas (SSH, PGP)
- Tokens de produção (Stripe Live, AWS, GitHub)
- URLs com credenciais
- Senhas em claro

**Ação:** Revogar imediatamente, fazer rotação de credenciais

### HIGH (🟠)
- Tokens de teste
- Bearer tokens genéricos
- JWT tokens
- API keys de serviços

**Ação:** Investigar contexto, revogar se necessário

### MEDIUM (🟡)
- Possíveis credenciais
- Padrões incertos

**Ação:** Revisar manualmente

### LOW (🟢)
- Informações não sensíveis
- Placeholders

**Ação:** Pode ignorar após revisão

## Filtragem de Falsos Positivos

A ferramenta automaticamente ignora:

```
<TOKEN>          # Placeholders
[PASSWORD]       # Placeholders com colchetes
***              # Asteriscos
example          # Exemplos de documentação
test             # Valores de teste
sample           # Valores de amostra
placeholder      # Explicitamente placeholder
your-            # Prefixo indicando customização
replace-         # Indicação de substituição
change-this      # Indicação de mudança
```

## Customização

Para adicionar novos padrões, edite `SecretPatterns.PATTERNS` no script:

```python
"seu-pattern-aqui": {
    "pattern": r"seu_regex_aqui",
    "severity": "HIGH",
    "description": "Descrição clara"
}
```

Depois rebuild o scanner e teste com:
```bash
python scripts/secret_scanner.py . --list-patterns
```

## Recursos

- [OWASP - Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [TruffleHog - Regex Patterns](https://github.com/trufflesecurity/truffleHog)
- [GitGuardian - Secrets Detection](https://www.gitguardian.com/)
