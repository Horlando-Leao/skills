#!/usr/bin/env python3
"""
Publica um relatorio Markdown em uma pagina do Confluence Cloud, via REST API v2.

Converte o Markdown para o formato storage (via md_to_confluence.py), valida a
renderizacao e as referencias internas, le a versao atual da pagina e publica a
proxima. Dry-run por padrao: sem --apply, nada e escrito.

Uso:
    python3 publicar_confluence.py                       # dry-run
    python3 publicar_confluence.py --apply -m "mensagem" --expect-version N
    python3 publicar_confluence.py --page <id-ou-URL> --file caminho/doc.md --apply -m "..."

Defaults (projeto OP-631): pagina 4256497705 em superlogica.atlassian.net, e o
Markdown procurado em analise/relatorio.md, relatorio.md ou ../relatorio.md a
partir do diretorio atual. Sobrescreva com --page, --site e --file.

Credencial:
    Token lido de ~/token_confluence_jira_atlassian.txt (ou --token-file / a var de
    ambiente CONFLUENCE_TOKEN_FILE). O arquivo pode conter so o token, ou
    "email:token" em uma linha. O token nunca e impresso nem passado em argv.

Protecao contra sobrescrever edicao manual:
    O dry-run mostra a versao atual e a mensagem da ultima versao. Use
    --expect-version N para abortar caso a pagina nao esteja exatamente na versao
    que voce espera (sinal de que alguem editou pelo navegador).

Diagramas mermaid:
    Cada bloco ```mermaid do Markdown e renderizado para SVG de verdade com
    mermaid-cli (via npx — mesmo parser que roda no navegador), enviado como anexo
    da pagina e referenciado no corpo via <ac:image>. A macro nativa `mermaid` do
    Confluence nao serve para isso: ela so renderiza quando alguem abre o editor
    pelo navegador, entao escrita via API fica em branco.

Codigos de saida: 0 = ok, 1 = qualquer falha (validacao, versao inesperada,
credencial, rede, HTTP, render de diagrama).
"""
import argparse
import base64
import html
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_to_confluence import convert, mermaid_blocks, tipo_mermaid  # noqa: E402

DEFAULT_SITE = "https://superlogica.atlassian.net"
DEFAULT_PAGE_ID = "4256497705"  # OP-631 — Análise financeira
PAGE_TITLE_FALLBACK = "Análise financeira"
DEFAULT_EMAIL = "horlando.leao@superlogica.com"
DEFAULT_TOKEN_FILE = Path.home() / "token_confluence_jira_atlassian.txt"

# Candidatos para --file quando ele nao e passado, relativos ao diretorio atual.
CANDIDATOS_MD = ["analise/relatorio.md", "relatorio.md", "../relatorio.md"]


def localizar_markdown() -> Path | None:
    for candidato in CANDIDATOS_MD:
        p = Path(candidato)
        if p.is_file():
            return p.resolve()
    return None


def extrair_page_id(valor: str) -> str:
    """Aceita um id puro ou uma URL de pagina do Confluence."""
    if valor.isdigit():
        return valor
    achado = re.search(r"/pages/(\d+)", valor)
    if not achado:
        sys.exit(f"ERRO: nao consegui extrair o id da pagina de: {valor}")
    return achado.group(1)


# ---------------------------------------------------------------- credencial


def ler_credencial(token_file: Path, email: str) -> tuple[str, str]:
    """Devolve (email, token). Nunca imprime o token."""
    if not token_file.is_file():
        sys.exit(f"ERRO: arquivo de token nao encontrado: {token_file}")

    modo = token_file.stat().st_mode
    if modo & (stat.S_IRGRP | stat.S_IROTH):
        print(
            f"AVISO: {token_file} e legivel por grupo/outros "
            f"({stat.filemode(modo)}). Considere: chmod 600 {token_file}",
            file=sys.stderr,
        )

    linhas = [l.strip() for l in token_file.read_text().splitlines() if l.strip()]
    if not linhas:
        sys.exit(f"ERRO: arquivo de token vazio: {token_file}")

    primeira = linhas[0]
    # aceita "email:token" ou so o token
    if "@" in primeira and ":" in primeira:
        email_arq, _, token = primeira.partition(":")
        return email_arq.strip(), token.strip()
    return email, primeira


def cabecalhos(email: str, token: str) -> dict:
    basic = base64.b64encode(f"{email}:{token}".encode()).decode()
    return {
        "Authorization": f"Basic {basic}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def chamar(url: str, headers: dict, metodo: str = "GET", corpo: bytes | None = None) -> dict:
    req = urllib.request.Request(url, data=corpo, headers=headers, method=metodo)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode(errors="replace")[:600]
        sys.exit(f"ERRO HTTP {e.code} em {metodo} {url}\n{detalhe}")
    except urllib.error.URLError as e:
        sys.exit(f"ERRO de rede em {metodo} {url}: {e.reason}")


# ---------------------------------------------------------------- validacao


def validar_mermaid_sintaxe(md: str) -> list[str]:
    """Checagem rapida (sem subprocesso): cada bloco declara um tipo de diagrama valido."""
    problemas = []
    for filename, codigo in mermaid_blocks(md):
        if not codigo:
            problemas.append(f"diagrama mermaid ({filename}): bloco vazio")
        elif tipo_mermaid(codigo) is None:
            primeira = next((l.strip() for l in codigo.splitlines() if l.strip()), "")
            problemas.append(f"diagrama mermaid ({filename}): tipo nao reconhecido em {primeira!r}")
    return problemas


def renderizar_mermaid(md: str, workdir: Path) -> tuple[list[Path], list[str]]:
    """Renderiza cada bloco mermaid para SVG com o mermaid-cli real (via npx).

    E a autoridade final sobre sintaxe valida: o mesmo parser que roda no navegador.
    Retorna (arquivos_svg_na_ordem, problemas) — lista de problemas vazia = tudo ok.
    """
    blocks = mermaid_blocks(md)
    if not blocks:
        return [], []

    puppeteer_cfg = workdir / "puppeteer-config.json"
    puppeteer_cfg.write_text(json.dumps({"args": ["--no-sandbox", "--disable-dev-shm-usage"]}))

    env = os.environ.copy()
    env.setdefault("PUPPETEER_EXECUTABLE_PATH", "/usr/bin/google-chrome")

    arquivos: list[Path] = []
    problemas: list[str] = []
    for filename, codigo in blocks:
        entrada = workdir / filename.replace(".svg", ".mmd")
        entrada.write_text(codigo)
        saida = workdir / filename

        resultado = subprocess.run(
            [
                "npx", "-y", "-p", "@mermaid-js/mermaid-cli", "mmdc",
                "-p", str(puppeteer_cfg),
                "-i", str(entrada), "-o", str(saida),
                "--backgroundColor", "transparent",
            ],
            capture_output=True, text=True, env=env,
        )

        if resultado.returncode != 0 or not saida.is_file():
            linhas_erro = [l for l in resultado.stderr.splitlines() if l.strip()]
            resumo = next(
                (l for l in linhas_erro if "Error" in l or "error" in l),
                linhas_erro[-1] if linhas_erro else "erro desconhecido (sem stderr)",
            )
            problemas.append(f"diagrama mermaid ({filename}): falha ao renderizar — {resumo}")
        else:
            arquivos.append(saida)

    return arquivos, problemas


def montar_multipart(caminho: Path) -> tuple[bytes, str]:
    boundary = "confluence-mermaid-upload-boundary"
    corpo = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{caminho.name}"\r\n'
        "Content-Type: image/svg+xml\r\n\r\n"
    ).encode() + caminho.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return corpo, boundary


def enviar_anexo(site: str, page_id: str, caminho: Path, auth_header: str) -> None:
    """Envia (ou versiona, se ja existir) um anexo na pagina via REST API v1.

    A v2 nao tem endpoint de upload multipart; a v1 aceita reenviar o mesmo
    filename e cria uma nova versao do anexo automaticamente.
    """
    corpo, boundary = montar_multipart(caminho)
    url = f"{site.rstrip('/')}/wiki/rest/api/content/{page_id}/child/attachment"
    req = urllib.request.Request(
        url,
        data=corpo,
        method="POST",
        headers={
            "Authorization": auth_header,
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode(errors="replace")[:600]
        sys.exit(f"ERRO HTTP {e.code} ao enviar anexo {caminho.name}\n{detalhe}")
    except urllib.error.URLError as e:
        sys.exit(f"ERRO de rede ao enviar anexo {caminho.name}: {e.reason}")


def validar_render(xhtml: str) -> list[str]:
    """Problemas que nao devem ir para a pagina. Lista vazia = ok."""
    problemas = []

    for i, tabela in enumerate(re.findall(r"<table>.*?</table>", xhtml, re.S), 1):
        linhas = re.findall(r"<tr>(.*?)</tr>", tabela, re.S)
        colunas = [len(re.findall(r"<t[hd]>", l)) for l in linhas]
        if len(set(colunas)) > 1:
            problemas.append(f"tabela {i}: numero de colunas inconsistente {colunas}")

    if "PLACEHOLDER" in xhtml:
        problemas.append("sobrou um PLACEHOLDER no texto")

    abertas = xhtml.count("<ac:plain-text-body>")
    fechadas = xhtml.count("</ac:plain-text-body>")
    if abertas != fechadas:
        problemas.append(f"code blocks desbalanceados: {abertas} abrem, {fechadas} fecham")

    return problemas


def resumir(xhtml: str) -> str:
    marcador_code = 'ac:name="code"'
    marcador_mermaid = "diagrama-mermaid-"
    return (
        f"{len(xhtml)} chars · "
        f"{xhtml.count('<table>')} tabelas · "
        f"{len(re.findall(r'<h[1-6]>', xhtml))} titulos · "
        f"{xhtml.count(marcador_code)} code blocks · "
        f"{xhtml.count(marcador_mermaid)} diagramas mermaid · "
        f"{xhtml.count('<blockquote>')} blockquotes"
    )


def validar_referencias(md: str) -> list[str]:
    """Referencias internas ('secao 5.2', 'secao 8, item 3', 'Apendice B') que nao existem."""
    problemas = []

    secoes = {m.group(1) for m in re.finditer(r"^#{2,4}\s+((?:\d+\.)?\d+(?:\.\d+)?)\.", md, re.M)}
    for ref in sorted(set(re.findall(r"se[çc][ãa]o\s+\*{0,2}(\d+(?:\.\d+)?)", md, re.I))):
        if ref not in secoes:
            problemas.append(f"referencia a secao inexistente: {ref}")

    if "## 8. Limita" in md:
        tabela8 = md.split("## 8. Limita")[1]
        itens = {
            l.split("|")[1].strip()
            for l in tabela8.splitlines()
            if l.startswith("|") and l.split("|")[1].strip().isdigit()
        }
        citados = set(re.findall(r"se[çc][ãa]o\s+\*{0,2}8\*{0,2},\s*item\s+(\d+)", md, re.I))
        citados |= set(re.findall(r"limita[çc][ãa]o\s+#(\d+)", md, re.I))
        for item in sorted(citados, key=int):
            if item not in itens:
                problemas.append(f"referencia a item inexistente da secao 8: {item}")

    apendices = set(re.findall(r"^##\s+Ap[êe]ndice\s+([A-Z])", md, re.M))
    for citado in sorted(set(re.findall(r"Ap[êe]ndice\s+([A-Z])\b", md))):
        if citado not in apendices:
            problemas.append(f"referencia a apendice inexistente: {citado}")

    return problemas


# ---------------------------------------------------------------- publicacao


def main() -> None:
    ap = argparse.ArgumentParser(description="Publica o relatorio no Confluence (dry-run por padrao).")
    ap.add_argument("--apply", action="store_true", help="publica de verdade; sem isso, so mostra o que faria")
    ap.add_argument("-m", "--message", default="", help="mensagem de versao (aparece no historico da pagina)")
    ap.add_argument("--expect-version", type=int, help="aborta se a pagina nao estiver nesta versao")
    ap.add_argument("--file", type=Path, help=f"Markdown a publicar (default: {' ou '.join(CANDIDATOS_MD)})")
    ap.add_argument("--token-file", type=Path,
                    default=Path(os.environ.get("CONFLUENCE_TOKEN_FILE", DEFAULT_TOKEN_FILE)))
    ap.add_argument("--email", default=os.environ.get("CONFLUENCE_EMAIL", DEFAULT_EMAIL))
    ap.add_argument("--page", default=DEFAULT_PAGE_ID, help="id da pagina ou a URL dela")
    ap.add_argument("--site", default=os.environ.get("CONFLUENCE_SITE", DEFAULT_SITE))
    args = ap.parse_args()

    arquivo = args.file or localizar_markdown()
    if arquivo is None:
        sys.exit(
            "ERRO: nenhum Markdown encontrado. Rode a partir da raiz do projeto ou passe --file.\n"
            f"Procurei por: {', '.join(CANDIDATOS_MD)}"
        )
    if not arquivo.is_file():
        sys.exit(f"ERRO: markdown nao encontrado: {arquivo}")
    args.file = arquivo
    page_id = extrair_page_id(args.page)

    md = args.file.read_text()
    xhtml = convert(md)

    print(f"Origem:  {args.file.resolve()}")
    print(f"Render:  {resumir(xhtml)}")

    problemas = validar_render(xhtml) + validar_referencias(md) + validar_mermaid_sintaxe(md)
    if problemas:
        print("\nPROBLEMAS ENCONTRADOS — nada foi publicado:")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)

    with tempfile.TemporaryDirectory(prefix="publicar-confluence-mermaid-") as tmp:
        workdir = Path(tmp)
        svgs = mermaid_blocks(md)
        if svgs:
            print(f"Renderizando {len(svgs)} diagrama(s) mermaid com mermaid-cli...")
        arquivos_svg, problemas_render = renderizar_mermaid(md, workdir)
        if problemas_render:
            print("\nPROBLEMAS ENCONTRADOS — nada foi publicado:")
            for p in problemas_render:
                print(f"  - {p}")
            sys.exit(1)
        print("Validacao: ok (tabelas consistentes, referencias internas resolvem, mermaid renderiza)")

        email, token = ler_credencial(args.token_file, args.email)
        headers = cabecalhos(email, token)

        url_base = f"{args.site.rstrip('/')}/wiki/api/v2/pages/{page_id}"
        atual = chamar(f"{url_base}?body-format=storage", headers)
        versao_atual = atual["version"]["number"]
        proxima = versao_atual + 1

        print(f"\nPagina:  {atual['title']} ({page_id})")
        print(f"URL:     {args.site.rstrip('/')}/wiki/spaces/OP/pages/{page_id}")
        print(f"Versao:  {versao_atual} -> {proxima}")
        print(f"Ultima mensagem: {atual['version'].get('message') or '(sem mensagem)'}")
        corpo_atual = atual["body"]["storage"]["value"]
        print(f"No ar:   {len(corpo_atual)} chars")

        if args.expect_version is not None and versao_atual != args.expect_version:
            sys.exit(
                f"\nABORTADO: esperava a versao {args.expect_version}, encontrei {versao_atual}.\n"
                "Alguem pode ter editado a pagina pelo navegador. Confira o historico antes de sobrescrever."
            )

        if not args.apply:
            print("\nDRY-RUN — nada foi publicado. Para publicar:")
            invocado = sys.argv[0]
            print(f'  python3 {invocado} --apply -m "descreva a mudanca" --expect-version {versao_atual}')
            return

        if not args.message.strip():
            sys.exit("ERRO: --apply exige -m/--message (a mensagem vai para o historico da pagina)")

        if arquivos_svg:
            for arquivo in arquivos_svg:
                enviar_anexo(args.site, page_id, arquivo, headers["Authorization"])
            print(f"\n{len(arquivos_svg)} diagrama(s) mermaid enviados como anexo SVG")

        payload = json.dumps(
            {
                "id": page_id,
                "status": "current",
                "title": atual["title"] or PAGE_TITLE_FALLBACK,
                "body": {"representation": "storage", "value": xhtml},
                "version": {"number": proxima, "message": args.message.strip()},
            },
            ensure_ascii=False,
        ).encode()

        resposta = chamar(url_base, headers, metodo="PUT", corpo=payload)
        print(f"\nPublicado — versao {resposta['version']['number']}")

        # Verificacao: o Confluence devolve acentos como entidades HTML nomeadas
        # (&aacute;), entao comparar texto acentuado cru da falso negativo.
        confirmacao = chamar(f"{url_base}?body-format=storage", headers)
        corpo = html.unescape(confirmacao["body"]["storage"]["value"])
        print(f"Confirmado: versao {confirmacao['version']['number']} no ar")

        titulos_md = re.findall(r"^#{2,4}\s+(.*)", md, re.M)
        faltando = [t for t in titulos_md if html.unescape(t.replace("**", "")) not in corpo]
        if faltando:
            print(f"AVISO: {len(faltando)} titulo(s) do Markdown nao encontrados na pagina:")
            for t in faltando[:5]:
                print(f"  - {t}")
        else:
            print(f"Todos os {len(titulos_md)} titulos do Markdown estao na pagina")


if __name__ == "__main__":
    main()
