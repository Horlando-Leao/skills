#!/usr/bin/env python3
"""
Converte o relatorio Markdown para o formato storage (XHTML) do Confluence Cloud.

Cobre o subconjunto usado no relatorio: headings, tabelas com header, code fences,
blockquotes, listas, negrito, strikethrough, inline code e links.

Fences ```mermaid nao viram code block nem a macro `mermaid` do app instalado no site:
essa macro so renderiza quando alguem abre o editor pelo navegador (o app tem seu
proprio pipeline de render que a escrita via API nao aciona), entao ficaria em branco
na pagina. Em vez disso, cada bloco vira uma referencia <ac:image> para um anexo SVG
com nome estavel (ver mermaid_blocks) — o publicador renderiza esse SVG de verdade
com mermaid-cli (mesmo parser do navegador) e faz o upload antes do PUT da pagina.

Links http(s) viram <a>. Caminhos relativos de arquivo local viram <code> em vez de
<a>, porque em uma pagina do Confluence um href relativo resolve contra a URL da
pagina e sempre quebra — o texto do caminho e preservado integralmente.

Uso: python3 md_to_confluence.py ../relatorio.md > /tmp/body.xhtml
"""
import html
import re
import sys
from pathlib import Path

CODE_PLACEHOLDER = "\x00CODE{}\x00"

# Tipos de diagrama aceitos na primeira linha util de um bloco mermaid. Um bloco que
# nao comeca com um deles renderiza como erro na pagina, entao e melhor barrar antes.
MERMAID_TIPOS = (
    "architecture-beta", "block-beta", "C4Context", "classDiagram", "erDiagram",
    "flowchart", "gantt", "gitGraph", "graph", "journey", "kanban", "mindmap",
    "packet-beta", "pie", "quadrantChart", "requirementDiagram", "sankey-beta",
    "sequenceDiagram", "stateDiagram-v2", "stateDiagram", "timeline",
    "xychart-beta", "zenuml",
)


def render_inline(text: str) -> str:
    """Converte formatacao inline de uma linha de Markdown para XHTML."""
    code_spans: list[str] = []

    def stash_code(match: re.Match) -> str:
        code_spans.append(match.group(1))
        return CODE_PLACEHOLDER.format(len(code_spans) - 1)

    text = re.sub(r"`([^`]+)`", stash_code, text)
    text = html.escape(text, quote=False)

    def render_link(match: re.Match) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "mailto:")):
            return f'<a href="{html.escape(target, quote=True)}">{label}</a>'
        # caminho local: preserva o texto, sem href quebrado
        return f"<code>{label}</code>"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", render_link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"~~([^~]+)~~", r"<s>\1</s>", text)

    for index, span in enumerate(code_spans):
        text = text.replace(
            CODE_PLACEHOLDER.format(index),
            f"<code>{html.escape(span, quote=False)}</code>",
        )
    return text


def split_row(line: str) -> list[str]:
    """Divide uma linha de tabela em celulas, respeitando pipes escapados (\\|).

    Sem isso, um `\\|` dentro de uma celula (comum em comandos shell com pipe)
    e tratado como separador e a linha ganha colunas fantasmas.
    """
    inner = line.strip().removeprefix("|").removesuffix("|")
    cells = re.split(r"(?<!\\)\|", inner)
    return [cell.strip().replace("\\|", "|") for cell in cells]


def is_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:|-]+\|", line.strip()))


def render_table(lines: list[str]) -> str:
    header = split_row(lines[0])
    body_rows = [split_row(line) for line in lines[2:]]

    out = ["<table><tbody>", "<tr>"]
    out += [f"<th>{render_inline(cell)}</th>" for cell in header]
    out.append("</tr>")
    for row in body_rows:
        out.append("<tr>")
        out += [f"<td>{render_inline(cell)}</td>" for cell in row]
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def linha_util_mermaid(code: str) -> str:
    """Primeira linha que declara o tipo do diagrama, pulando frontmatter e comentarios."""
    linhas = [l.strip() for l in code.strip().splitlines()]
    if linhas and linhas[0] == "---":
        fim = next((i for i, l in enumerate(linhas[1:], 1) if l == "---"), None)
        linhas = linhas[fim + 1:] if fim is not None else []
    for linha in linhas:
        if linha and not linha.startswith("%%"):
            return linha
    return ""


def tipo_mermaid(code: str) -> str | None:
    """Tipo declarado no bloco, ou None se o bloco nao declara um tipo conhecido."""
    primeira = linha_util_mermaid(code)
    return next((t for t in MERMAID_TIPOS if primeira.startswith(t)), None)


def mermaid_filename(n: int) -> str:
    """Nome estavel do anexo SVG do n-esimo diagrama (1-based, ordem de aparicao)."""
    return f"diagrama-mermaid-{n}.svg"


def mermaid_blocks(markdown: str) -> list[tuple[str, str]]:
    """[(nome_do_anexo, codigo_mermaid), ...] na ordem em que os fences aparecem."""
    codigos = re.findall(r"^```mermaid[ \t]*\n(.*?)^```", markdown, re.S | re.M)
    return [(mermaid_filename(i), codigo.strip()) for i, codigo in enumerate(codigos, 1)]


def render_mermaid_image(n: int) -> str:
    """Referencia a um anexo SVG ja enviado para a pagina (ver mermaid_blocks)."""
    return f'<ac:image ac:align="center"><ri:attachment ri:filename="{mermaid_filename(n)}" /></ac:image>'


def render_code_block(lines: list[str], language: str) -> str:
    body = "\n".join(lines)
    macro = ['<ac:structured-macro ac:name="code" ac:schema-version="1">']
    if language:
        macro.append(f'<ac:parameter ac:name="language">{language}</ac:parameter>')
    macro.append(f"<ac:plain-text-body><![CDATA[{body}]]></ac:plain-text-body>")
    macro.append("</ac:structured-macro>")
    return "".join(macro)


def convert(markdown: str) -> str:
    lines = markdown.split("\n")
    out: list[str] = []
    index = 0
    mermaid_count = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        # regra horizontal
        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            out.append("<hr/>")
            index += 1
            continue

        # heading
        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            index += 1
            continue

        # code fence
        fence = re.match(r"```(\w*)", stripped)
        if fence:
            language = fence.group(1)
            index += 1
            block: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.append(lines[index])
                index += 1
            index += 1  # consome o fence de fechamento
            if language == "mermaid":
                mermaid_count += 1
                out.append(render_mermaid_image(mermaid_count))
            else:
                out.append(render_code_block(block, language))
            continue

        # tabela
        if stripped.startswith("|") and index + 1 < len(lines) and is_separator(lines[index + 1]):
            table: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table.append(lines[index])
                index += 1
            out.append(render_table(table))
            continue

        # blockquote (agrupa linhas consecutivas)
        if stripped.startswith("> "):
            quote: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("> "):
                quote.append(render_inline(lines[index].strip()[2:]))
                index += 1
            out.append("<blockquote><p>" + "<br/>".join(quote) + "</p></blockquote>")
            continue

        # lista ordenada
        if re.match(r"\d+\.\s+", stripped):
            items: list[str] = []
            while index < len(lines) and re.match(r"\d+\.\s+", lines[index].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[index].strip()))
                index += 1
            out.append("<ol>" + "".join(f"<li>{render_inline(i)}</li>" for i in items) + "</ol>")
            continue

        # lista nao ordenada
        if stripped.startswith("- "):
            items = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip()[2:])
                index += 1
            out.append("<ul>" + "".join(f"<li>{render_inline(i)}</li>" for i in items) + "</ul>")
            continue

        # paragrafo: junta linhas consecutivas de texto
        paragraph: list[str] = []
        while index < len(lines):
            current = lines[index].strip()
            if not current or re.match(r"(#{1,6})\s|```|\||>\s|-\s|\d+\.\s", current):
                break
            if re.fullmatch(r"-{3,}|\*{3,}", current):
                break
            paragraph.append(render_inline(current))
            index += 1
        out.append("<p>" + "<br/>".join(paragraph) + "</p>")

    return "\n".join(out)


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / ".." / "relatorio.md"
    sys.stdout.write(convert(source.read_text()))


if __name__ == "__main__":
    main()
