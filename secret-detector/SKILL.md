---
name: secret-detector
description: Analisa diretórios inteiros procurando por segredos, tokens, chaves privadas e credenciais expostas usando padrões regex avançados. Identifica exposições de segurança como API keys, senhas, tokens de GitHub, AWS credentials e chaves SSH antes de fazer commit ou deploy.
license: MIT
compatibility: Requires Python 3.9+ with re, json, argparse modules (built-in)
metadata:
  version: "1.0"
  category: security
  keywords: secret-detection, security-scanning, credential-finder, leaked-secrets
---

# Secret Detector - Detecção de Credenciais Expostas

Analise diretórios completos e identifique segredos, tokens, chaves privadas e credenciais expostas antes que sejam commitados ao git.

## Quando Usar

- ✅ Antes de fazer commit em um repositório
- ✅ Ao revisar código novo ou integração de dependências
- ✅ Em pipelines CI/CD como verificação de segurança
- ✅ Auditoria de repositórios existentes
- ✅ Análise pré-deployment

## Funcionalidades Principais

- **Detecção Multip padrões:** API keys, tokens, senhas, chaves SSH/RSA
- **Relatórios Detalhados:** Mostra caminho exato, linha, conteúdo parcial
- **Filtros Inteligentes:** Ignora placeholders (`<TOKEN>`, `example`, `test`)
- **Saída Formatada:** JSON, CSV ou relatório de texto estruturado
- **Ignorar Arquivos:** Configurável via `.secretignore` ou argumentos
- **Sem Falsos Positivos:** Validação contextual para reduzir alertas

## Uso Rápido

```bash
# Escanear diretório atual
python scripts/secret_scanner.py .

# Escanear com filtros específicos
python scripts/secret_scanner.py /path/to/dir --patterns api-keys,github,aws

# Saída em JSON
python scripts/secret_scanner.py . --format json > secrets_report.json

# Ignorar diretórios
python scripts/secret_scanner.py . --exclude node_modules,dist,.git
```

## Exemplos de Detecção

### API Keys Detectadas
```
[CRITICAL] Stripe Live Key
  Arquivo: config/production.js:42
  Padrão: sk_live_[A-Za-z0-9]{24,}
  Valor: sk_live_4eC39HqLyjWDarhtT657...
```

### Tokens GitHub
```
[CRITICAL] GitHub Personal Access Token
  Arquivo: .env.local:5
  Padrão: ghp_[A-Za-z0-9]{36}
  Valor: ghp_16C7e42F292c6912E7...
```

### Credenciais AWS
```
[CRITICAL] AWS Secret Access Key
  Arquivo: credentials:3
  Padrão: aws_secret_access_key = [A-Za-z0-9/+=]{40}
  Valor: wJalrXUtnFEMI/K7MDENG/bPxRfiCyE...
```

## Estrutura de Saída

Veja [scripts/secret_scanner.py](scripts/secret_scanner.py) para documentação técnica completa e opcções avançadas.

Consulte [references/PATTERNS.md](references/PATTERNS.md) para lista detalhada de todos os padrões regex de detecção.

Use [assets/config_template.json](assets/config_template.json) para criar configuração personalizada.

## Filtrar Falsos Positivos

A skill automaticamente ignora:
- Strings de exemplo (`example`, `test`, `sample`)
- Placeholders (`<TOKEN>`, `[PASSWORD]`, `***`)
- Comentários de documentação em arquivos `.md`
- Linhas em arquivos de configuração de exemplo

## Integração com CI/CD

```bash
# Falha se encontrar segredos críticos
python scripts/secret_scanner.py . --fail-on-critical

# Retorna exit code 1 se encontrar qualquer segredo
python scripts/secret_scanner.py . --strict
```

## Próximas Leituras

1. [PATTERNS.md](references/PATTERNS.md) - Padrões regex completos
2. [secret_scanner.py](scripts/secret_scanner.py) - Documentação técnica
3. [config_template.json](assets/config_template.json) - Configurações
