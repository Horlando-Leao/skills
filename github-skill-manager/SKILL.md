---
name: github-skill-manager
description: Gerencia o ciclo de vida de Agent Skills usando os comandos oficiais 'gh skill' da GitHub CLI. Valida, inspeciona e publica pacotes de habilidades diretamente em repositórios do GitHub.
---

# GitHub Agent Skills Manager

Este guia orienta o agente na execução e automação de rotinas de gerenciamento de habilidades utilizando a extensão integrada da CLI oficial do GitHub (`gh skill`).

## Diretrizes de Uso

Sempre que o usuário solicitar para pesquisar, testar, validar ou subir uma nova habilidade (skill) para o GitHub, utilize os comandos estruturados abaixo por meio do terminal.

## Fluxos de Trabalho Automatizados

### 1. Pesquisa e Descoberta de Habilidades
Para encontrar habilidades existentes criadas pela comunidade no GitHub antes de iniciar um novo projeto:
```bash
gh skill search <palavra-chave>
```
*Exemplo:* `gh skill search react` ou `gh skill search docker`

### 2. Inspeção Segura (Preview)
Antes de instalar qualquer skill de terceiros no ambiente, é obrigatório inspecionar seu manifesto e instruções para evitar injeções de prompt ou scripts maliciosos:
```bash
gh skill preview <usuario>/<repositorio> <nome-da-skill>
```

### 3. Validação e Publicação Local
Ao desenvolver uma skill própria para disponibilizar no seu repositório do GitHub:

1. **Pré-requisito do Repositório:** Certifique-se de que a estrutura possui uma pasta contendo o arquivo `SKILL.md` (ex: `skills/minha-skill/SKILL.md`) com o frontmatter YAML (`name` e `description`) preenchido.
2. **Validar Localmente (Dry-Run):** Execute o comando de teste para verificar se os metadados estão em conformidade com as regras de nomenclatura do `agentskills.io`:
   ```bash
   gh skill publish --dry-run
   ```
3. **Publicar no GitHub:** Após passar na validação, execute o comando para criar uma release imutável indexada ao Git Tree SHA do repositório:
   ```bash
   gh skill publish <seu-usuario>/<seu-repositorio>
   ```

### 4. Distribuição para Usuários (Instalação)
Para documentar ou orientar como outras pessoas baixam a skill publicada diretamente para os agentes locais delas:
* **Escopo Global (Geral):** `gh skill install <usuario>/<repositorio>`
* **Direcionado ao Claude Code:** `gh skill install <usuario>/<repositorio> --agent claude-code`

## Tratamento de Erros Comuns

* **Erro de Validação de Nome:** Se o CLI acusar erro ao rodar `publish`, certifique-se de que o nome definido na tag `name:` do YAML corresponde exatamente ao nome da pasta onde o arquivo `SKILL.md` está inserido.
* **Autenticação Pendente:** Se o comando falhar por falta de permissões, execute primeiro `gh auth login` para revalidar os escopos do token do GitHub.
