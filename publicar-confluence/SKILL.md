---
name: publicar-confluence
description: Publica um relatório Markdown em uma página do Confluence Cloud via REST API, convertendo para o formato storage e validando antes de escrever. Use quando o usuário pedir para publicar, republicar ou atualizar um documento no Confluence.
---

# Publicar relatório no Confluence

Converte um Markdown para o formato storage (XHTML) do Confluence, valida, e publica como uma nova versão da página. Não usa MCP — fala direto com a REST API v2.

## Script

`scripts/publicar_confluence.py` (depende de `scripts/md_to_confluence.py`, no mesmo diretório). Só stdlib do Python 3 — sem `pip install`.

```bash
# 1. SEMPRE rode o dry-run primeiro
python3 .claude/skills/publicar-confluence/scripts/publicar_confluence.py

# 2. Publique passando a versão que o dry-run reportou
python3 .claude/skills/publicar-confluence/scripts/publicar_confluence.py \
  --apply -m "descreva o que mudou" --expect-version <N>
```

Outra página ou outro arquivo:

```bash
... --page https://superlogica.atlassian.net/wiki/spaces/OP/pages/123456/Titulo --file docs/outro.md
```

| Flag | Efeito |
|---|---|
| *(nenhuma)* | Dry-run: converte, valida, mostra versão atual e o que faria. Não escreve. |
| `--apply` | Publica. Exige `-m`. |
| `-m/--message` | Mensagem da versão, aparece no histórico da página. |
| `--expect-version N` | Aborta se a página não estiver na versão N. |
| `--page` | Id ou URL da página. Default: 4256497705 (OP-631). |
| `--file` | Markdown. Default: procura `analise/relatorio.md`, `relatorio.md`, `../relatorio.md`. |
| `--site` / `--email` / `--token-file` | Sobrescrevem os defaults. Também leem `CONFLUENCE_SITE`, `CONFLUENCE_EMAIL`, `CONFLUENCE_TOKEN_FILE`. |

Exit 0 = ok. Exit 1 = qualquer falha.

## Procedimento

1. **Dry-run.** Nunca chame `--apply` direto. O dry-run reporta a versão atual, a mensagem da última versão e o resultado da validação.
2. **Compare a versão com o esperado.** Se a página estiver numa versão mais alta do que a última publicação registrada nesta conversa, **pare e investigue** antes de sobrescrever — pode haver edição manual pelo navegador. Cheque o histórico:
   ```bash
   curl -s -u "$EMAIL:$(cat ~/token_confluence_jira_atlassian.txt)" \
     "https://superlogica.atlassian.net/wiki/api/v2/pages/<id>/versions" | python3 -m json.tool
   ```
   O Confluence às vezes cria versões sozinho só reformatando o HTML (adiciona atributos `local-id`). Para distinguir isso de uma edição real, compare o **texto sem tags** das duas versões, não o XHTML cru.
3. **Publique** com `--apply -m "..." --expect-version <N>`, onde N é o que o dry-run mostrou.
4. **Relate ao usuário** a versão publicada e o que a verificação confirmou.

## Regras que não devem ser violadas

- **Nunca imprima, ecoe ou cole o token** em comando, log ou resposta. O script lê o arquivo direto; não passe o token por argumento nem por `python3 -c`.
- **Nunca use `--apply` sem dry-run antes.** Publicar sobrescreve a página inteira; não há merge.
- **Se a validação falhar, corrija o Markdown** — não contorne a validação. Ela existe porque cada checagem corresponde a um bug que já foi para a página publicada.

## Armadilhas conhecidas (todas já custaram uma versão errada)

**Acentos vêm como entidades HTML.** O storage format devolve `Análise` como `An&aacute;lise`. Comparar texto acentuado literal contra o corpo cru **sempre** dá falso negativo. Passe por `html.unescape()` antes de qualquer comparação.

**Pipe escapado em tabela.** `\|` dentro de célula era tratado como separador de coluna e quebrava a tabela. Já corrigido em `md_to_confluence.py` (só divide em pipes não escapados), e a validação de colunas inconsistentes pega uma regressão.

**Links relativos quebram.** Um `href` relativo numa página do Confluence resolve contra a URL da página. `md_to_confluence.py` renderiza caminhos locais como `<code>` em vez de `<a>` — de propósito. Não "conserte" isso.

**Settings é PUT que substitui tudo.** O PUT da página troca o corpo inteiro. O que não estiver no Markdown desaparece da página.

## O que a validação verifica

Roda antes de qualquer escrita; qualquer problema aborta com exit 1:

- **Tabelas com número de colunas inconsistente** entre linhas — sintoma de pipe mal escapado.
- **`PLACEHOLDER` sobrando** no texto — link ou valor que ficou pendente.
- **Code blocks desbalanceados** (`<ac:plain-text-body>` abre e fecha em contagens diferentes).
- **Referências internas quebradas**: `seção X.Y` sem título correspondente, `seção 8, item N` ou `limitação #N` sem a linha na tabela, `Apêndice X` inexistente.

Após publicar, confere que todos os títulos do Markdown aparecem na página.

## Manutenção

`md_to_confluence.py` cobre o subconjunto de Markdown usado nestes relatórios: títulos, tabelas com header, code fences, blockquotes, listas, negrito, strikethrough, inline code, links e regra horizontal. Markdown fora disso (listas aninhadas, imagens, HTML embutido) não é convertido — se precisar, estenda `convert()` e adicione a checagem correspondente em `validar_render()`.
