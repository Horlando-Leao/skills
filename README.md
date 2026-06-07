# Agent Skills Repository

Coleção de skills especializadas para agentes de IA, seguindo a especificação oficial do [agentskills.io](https://agentskills.io).

![GitHub](https://img.shields.io/badge/GitHub-Horlando--Leao/skills-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Skills](https://img.shields.io/badge/Skills-16%2B-brightgreen)

## 📚 Visão Geral

Este repositório contém skills reutilizáveis e modulares que estendem as capacidades de agentes de IA. Cada skill segue a arquitetura de **divulgação progressiva de contexto**, otimizando o uso de tokens e permitindo descoberta automática.

### ✨ Destaques

- **Skills Modulares:** Estrutura completa com scripts, referências e assets
- **Baixo Consumo de Contexto:** Metadados leves, conteúdo carregado sob demanda
- **Pronto para Produção:** Validado contra a especificação oficial
- **Segurança Integrada:** Scanner de credenciais expostas incluído

## 🚀 Skills Disponíveis

### 1. **skill-generator** 🛠️ Meta-Skill
Assistente especializado na criação de novas skills com estrutura modular completa.

- **Descrição:** Guia o usuário na criação e validação de habilidades para agentes IA
- **Uso:** Para estruturar novas skills seguindo melhores práticas
- **Diretório:** [skill-generator/](skill-generator/)

```bash
python skill-generator/scripts/setup_skill.py \
  --name minha-skill \
  --description "Descrição clara"
```

---

### 2. **secret-detector** 🔐 Segurança
Scanner avançado que detecta credenciais e segredos expostos em diretórios.

- **Descrição:** Analisa código procurando tokens, chaves privadas e credenciais expostas
- **Uso:** Pré-deploy, CI/CD, auditoria de segurança
- **Padrões:** 20+ regex patterns (Stripe, GitHub, AWS, SSH, JWT, etc.)
- **Diretório:** [secret-detector/](secret-detector/)

```bash
# Escanear diretório
python secret-detector/scripts/secret_scanner.py .

# Com filtros
python secret-detector/scripts/secret_scanner.py . --patterns github,aws

# Saída JSON
python secret-detector/scripts/secret_scanner.py . --format json > report.json

# Falhar em CI/CD se encontrar secrets críticos
python secret-detector/scripts/secret_scanner.py . --fail-on-critical
```

---

### 3. **bug-resolution-cycle** 🐛
Framework para ciclo estruturado de resolução de bugs com reprodução e validação.

- **Diretório:** [bug-resolution-cycle/](bug-resolution-cycle/)

---

### 4. **mermaid-to-svg** 📊
Converte diagramas Mermaid para SVG com renderização automática.

- **Diretório:** [mermaid-to-svg/](mermaid-to-svg/)

---

### 5. **nestjs-di-patterns** 🏗️
Padrões avançados de injeção de dependência em NestJS.

- **Diretório:** [nestjs-di-patterns/](nestjs-di-patterns/)

---

### 6. **new-migration-typeorm** 📦
Gerador e validador de migrations TypeORM.

- **Diretório:** [new-migration-typeorm/](new-migration-typeorm/)

---

### 7. **pr-with-diagrams** 📈
Integração de diagramas visuais em pull requests.

- **Diretório:** [pr-with-diagrams/](pr-with-diagrams/)

---

### 8. **pull-request** 🔀
Assistente para criação e revisão de pull requests estruturados usando `gh pr create`.

- **Descrição:** Guia prático para criar PRs de qualidade com GitHub CLI
- **Uso:** Criar PRs via terminal com descrições estruturadas
- **Diretório:** [pull-request/](pull-request/)

```bash
# PR básica com editor
gh pr create

# PR com título e descrição diretos
gh pr create --title "Título" --body "Descrição"

# PR completa com detalhes
gh pr create \
  --title "Feature: novo recurso" \
  --body "Implementa..." \
  --base main \
  --assignee @me \
  --reviewer usuario1,usuario2
```

---

### 9. **query-local** 🔍
Ferramenta para executar queries locais em dados estruturados.

- **Diretório:** [query-local/](query-local/)

---

### 10. **review-pr** ✅
Sistema especializado em revisão técnica de pull requests.

- **Diretório:** [review-pr/](review-pr/)

---

### 11. **safe-rename** ♻️
Renomeação segura de variáveis, funções e classes com refactoring.

- **Diretório:** [safe-rename/](safe-rename/)

---

### 12. **task-criteria-review** 📋
Validação de critérios de aceitação e escopo de tarefas.

- **Diretório:** [task-criteria-review/](task-criteria-review/)

---

### 13. **test-api** 🧪
Framework para testes automatizados de APIs REST e GraphQL.

- **Diretório:** [test-api/](test-api/)

---

### 14. **teste-local** 🔧
Utilitário para testes locais rápidos durante desenvolvimento.

- **Diretório:** [teste-local/](teste-local/)

---

## 📖 Estrutura de Diretórios

Cada skill segue este padrão:

```
skill-name/
├── SKILL.md                   # Manifesto e instruções (obrigatório)
├── scripts/                   # Código executável (opcional)
│   └── script.py
├── references/                # Documentação densa (opcional)
│   └── REFERENCE.md
└── assets/                    # Templates e dados estáticos (opcional)
    └── config.json
```

### Princípio de Divulgação Progressiva

1. **~100 tokens:** `name` + `description` carregados para todas as skills
2. **<5000 tokens:** `SKILL.md` completo carregado quando ativado
3. **Sob demanda:** Arquivos em `scripts/`, `references/`, `assets/` acessados quando necessário

## 🔧 Como Usar

### Instalação

```bash
# Clonar repositório
git clone git@github.com:Horlando-Leao/skills.git
cd skills

# Ou com HTTPS
git clone https://github.com/Horlando-Leao/skills.git
cd skills
```

### Usar uma Skill

Cada skill pode ser ativada conforme a necessidade. Exemplo com `secret-detector`:

```bash
# 1. Navegar para o diretório da skill
cd secret-detector

# 2. Executar o script
python scripts/secret_scanner.py /caminho/para/analizar

# 3. Verificar padrões disponíveis
python scripts/secret_scanner.py . --list-patterns

# 4. Usar com opções
python scripts/secret_scanner.py . --format json --fail-on-critical
```

#### Exemplo 2: Criar Pull Request com pull-request skill

```bash
# Criar PR básica (abre editor)
gh pr create

# Criar PR com título e descrição
gh pr create \
  --title "Feature: autenticação OAuth" \
  --body "Implementa login com GitHub\n\n## Mudanças\n- Adicionado module auth\n- Integração OAuth2" \
  --base main

# Criar PR com reviewers
gh pr create \
  --title "Fix: bug no cálculo de preço" \
  --body-file description.md \
  --reviewer @usuario1,@usuario2 \
  --assignee @me
```

### Criar Nova Skill

Use a meta-skill `skill-generator`:

```bash
cd skill-generator

python scripts/setup_skill.py \
  --name minha-skill \
  --description "O que essa skill faz e quando ativar" \
  --license MIT

# Resultado: estrutura completa gerada em ./minha-skill/
```

## ✅ Validação

Valide suas skills contra a especificação oficial:

```bash
# Instalar validador
pip install skills-ref

# Ou usar via npm
npm install -g skills-ref

# Validar skill
skills-ref validate ./skill-name
```

## 🔐 Segurança

### Verificação de Secrets

Antes de fazer commit/push, execute o scanner:

```bash
python secret-detector/scripts/secret_scanner.py . --strict
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Security Check
  run: |
    python secret-detector/scripts/secret_scanner.py . \
      --fail-on-critical \
      --exclude .git,node_modules
```

## 📝 Documentação

- **[specification.md](specification.md)** - Especificação oficial do agentskills.io
- **[skill-generator/SKILL.md](skill-generator/SKILL.md)** - Guia de criação de skills
- **[secret-detector/references/PATTERNS.md](secret-detector/references/PATTERNS.md)** - Padrões de detecção de secrets

## 🤝 Contribuição

Contribuições são bem-vindas! Para adicionar uma nova skill:

1. Clone este repositório
2. Use `skill-generator` para criar estrutura:
   ```bash
   python skill-generator/scripts/setup_skill.py \
     --name sua-skill \
     --description "Descrição clara"
   ```
3. Implemente sua skill seguindo a estrutura modular
4. Valide com `skills-ref validate ./sua-skill`
5. Faça push e abra um Pull Request

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Skills Totais** | 16 |
| **Padrões de Detecção** | 20+ (secret-detector) |
| **Linhas de Código** | 4000+ |
| **Licença** | MIT |

## 🔗 Links Úteis

- 🌐 [agentskills.io](https://agentskills.io) - Especificação oficial
- 📚 [Documentação de Skills](https://agentskills.io/llms.txt)
- 🛠️ [skills-ref Validator](https://github.com/agentskills/agentskills)
- 🔐 [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes

---

## 👤 Autor

**Horlando Leão**

- GitHub: [@Horlando-Leao](https://github.com/Horlando-Leao)
- Email: horlando.leao@example.com

---

## ⭐ Suporte

Se achou útil, considere deixar uma estrela! ⭐

Para dúvidas ou sugestões, abra uma [Issue](https://github.com/Horlando-Leao/skills/issues) ou [Discussion](https://github.com/Horlando-Leao/skills/discussions).

---

**Última atualização:** 7 de junho de 2026
