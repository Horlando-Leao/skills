---
name: pull-request
description: Instructions for writing a good PR description
---

## 📝 Instruções para uma boa PR

Seja direto e visual, eliminando o excesso de campos manuais e focando no que
realmente importa para o revisor de código.

- **Seja conciso:** O revisor deve entender a mudança em menos de 1 minuto.
- **Foque no "Porquê":** O código diz _o que_ foi feito, a descrição deve dizer
  _por que_ foi feito.
- **Use listas:** Facilite o "scanneamento" visual com bullet points.
- **Evidências:** Sempre que possível, anexe um print ou log. Uma imagem vale mais que 100 linhas de código.

## 🚀 Criar PR com GitHub CLI

Use o comando `gh pr create` para criar a PR diretamente via terminal:

```bash
# PR básica (será aberto editor para descrição)
gh pr create

# PR com título e descrição diretos
gh pr create --title "Descrição curta" --body "Descrição detalhada"

# PR para branch específico
gh pr create --base main --head feature/minha-feature

# PR completa com todos os detalhes
gh pr create \
  --title "Novo recurso: autenticação" \
  --body "Implementa autenticação com GitHub OAuth" \
  --base main \
  --assignee @me \
  --reviewer usuario1,usuario2
```

## 📋 Template de Descrição para `gh pr create`

Ao usar o editor (sem `--body`), use este template como guia:

```markdown
## O que foi feito

- Mudança 1
- Mudança 2
- Mudança 3

## Por que foi feito

Contexto e justificativa da implementação.

## Como testar

Passo a passo para validar a mudança.

## Screenshots/Evidências

[Adicione screenshots ou logs aqui]
```

## 📝 Usando Template de Arquivo

Se preferir preparar a descrição em arquivo primeiro, use:

```bash
# Escrever descrição em arquivo
cat > /tmp/pr_description.md << 'EOF'
## O que foi feito
- Implementação X

## Por que
Justificativa

## Testes
Como testar
EOF

# Criar PR lendo do arquivo
gh pr create --body-file /tmp/pr_description.md --title "Sua descrição"
```

Consulte [assets/pull_request_template.md](assets/pull_request_template.md) para um template completo.
