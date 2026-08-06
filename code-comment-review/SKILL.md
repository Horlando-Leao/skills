---
name: code-comment-review
description: Varre um escopo de código (diff, path ou repo) em busca de comentários grandes, com racional/histórico ou referências a card/ticket, e os enxuga para uma única linha funcional ("recebe X, faz Y, devolve Z"). Use quando o usuário pedir para revisar, limpar, enxugar ou "arrumar" comentários de código, ou remover referências a card/issue de comentários.
---

# Revisão de Comentários de Código

Varredura rápida via `rg` (nunca lendo arquivos inteiros às cegas) + edição pontual, aplicando um critério fixo de comentário: curto, funcional, sem contexto de tarefa.

## Critérios (aplicar em todo comentário encontrado)

1. **Máximo 1 linha** (2 só se genuinamente inevitável). Bloco de várias linhas de prosa é sempre candidato a corte.
2. **Formato funcional, não narrativo**: "recebe X, faz Y (se não óbvio), devolve Z". Descreve o que a função resolve — não como resolve passo a passo, não a história de como chegou nessa forma.
3. **Zero referência a card/ticket/issue** (`OP-123`, `JIRA-456`, `#789`) e zero frases tipo "usado por X", "adicionado para Y", "fix de Z" — isso é conteúdo de commit/PR, nunca de comentário.
4. **Zero racional de decisão** ("antes era X, mudamos para Y porque...", "decidimos fazer assim já que..."). Se a decisão precisa de justificativa, ela vai na descrição do PR, não no código.
5. **Só existe se o "porquê" não for óbvio** (invariante escondido, workaround de bug específico, comportamento que surpreenderia quem lê). Se apagar o comentário não confunde ninguém, apague.
6. **Nunca parafraseia o que o nome já diz** (`// soma os itens` acima de `sumItems()` é sempre lixo).

Isso vale tanto para docblocks (`/** */`, `"""..."""`) quanto para comentários de linha (`//`, `#`).

## Comandos prontos (rg — rápido, sem ler arquivo inteiro)

Troque `<path>` pelo escopo (arquivo, pasta ou `.`). Rode primeiro os de alto sinal (3 e 4) — geralmente já são o essencial da revisão.

```bash
# 1. Comentários de bloco (JSDoc/docstring) em TS/JS
rg -U --multiline -n '/\*\*?[\s\S]*?\*/' --glob '*.{ts,tsx,js,jsx}' <path>

# 2. Docstrings Python (triple-quote)
rg -U --multiline -n '"""[\s\S]*?"""' --glob '*.py' <path>

# 3. ALTO SINAL — referência a card/ticket/issue dentro de qualquer comentário
rg -n -i '\b[A-Z]{2,6}-[0-9]+\b|#[0-9]{3,}\b' --glob '*.{ts,tsx,js,jsx,py}' <path>

# 4. ALTO SINAL — racional/histórico em vez de função (PT + EN)
rg -n -i '(decidimos|motivo|razão|antes era|já que|antes fazia|história|foi adicionado para|usado (por|em|pelo)|used for|added for|because we|used by)' --glob '*.{ts,tsx,js,jsx,py}' <path>

# 5. Blocos "grandes" — heurística: corpo de docblock com mais de ~200 caracteres
rg -U --multiline -n '/\*\*(?:[^*]|\*(?!/)){200,}\*/' --glob '*.{ts,tsx,js,jsx}' <path>

# 6. Comentários de linha simples (TS/JS e Python)
rg -n '^\s*//' --glob '*.{ts,tsx,js,jsx}' <path>
rg -n '^\s*#' --glob '*.py' <path>

# Escopo por diff em vez de path/repo inteiro (revisão de PR)
git diff --name-only <base>... -- '*.ts' '*.tsx' '*.js' '*.jsx' '*.py'
```

## Passo a passo

1. **Escopo**: se o usuário não indicar path/arquivo, use `git diff` contra a branch base (pergunte a base se não for óbvia) em vez do repo inteiro.
2. **Rode os comandos 3 e 4 primeiro** — são os hits que quase certamente violam os critérios. Rode os demais para pegar o resto.
3. **Nunca `cat`/Read o arquivo inteiro por causa de um hit**: leia só a janela ao redor da linha reportada (poucas linhas antes/depois) para decidir a reescrita.
4. **Reescreva cada comentário** para o formato funcional de uma linha (critérios acima) — corte, não parafraseie o corte.
5. **Rode de novo os comandos 3 e 4** no escopo revisado para confirmar zero hits restantes.
6. **Reporte curto**: quantos comentários tocados/removidos, sem listar cada diff linha a linha.
