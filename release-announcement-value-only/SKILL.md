---
name: release-announcement-value-only
description: Gera e publica (como RASCUNHO) no canal do Slack do time um anúncio de release focado em VALOR DE PRODUTO, a partir de uma release tag ou de uma PR. Pede o link do canal e a referência (tag/PR), filtra refatorações/detalhes técnicos e escreve em linguagem de produto. Use quando o usuário pedir para anunciar/comunicar uma release ou entrega no Slack.
---

# Anúncio de Release — só valor de produto

Transforma uma entrega (release tag **ou** PR) num anúncio curto e visual no canal do
time, **focado no que muda para o usuário final** (síndico / atendente / morador) —
sem jargão técnico, sem refator/chore/melhoria interna.

Scripts ficam em `~/.claude/skills/release-announcement-value-only/scripts/` — execute
via ferramenta Bash. Prefixe comandos de shell com `rtk`.

## Entradas (peça ao usuário se não vierem)

1. **Canal do Slack** — link ou ID. Do link `https://<org>.slack.com/archives/C09DS8C3ZFA`,
   o `channel_id` é o `C...` depois de `/archives/`.
2. **Referência da entrega** — uma **release tag** (ex.: `v1.12.0`) **ou** o número de uma **PR** (ex.: `276`).
3. _(Opcional)_ print/screenshot de demonstração.

Faltando alguma, **pergunte** antes de seguir (use `AskUserQuestion` ou pergunta direta).

## Passo a passo

1. **Verifique o Slack** (rápido):
   `bash ~/.claude/skills/release-announcement-value-only/scripts/check-slack-mcp.sh`
   Se não houver Slack disponível, oriente a conectar antes de prosseguir.

2. **Pegue o conteúdo bruto da entrega**:
   `bash ~/.claude/skills/release-announcement-value-only/scripts/fetch-source.sh tag <vX.Y.Z>`
   ou `bash ~/.claude/skills/release-announcement-value-only/scripts/fetch-source.sh pr <numero>`

3. **Filtre só o que tem valor para o usuário final.** **NÃO reportar:**
   - `refactor`, `chore`, `style`, `test`, `ci`, `build`, `docs` internos;
   - resiliência / observabilidade / performance interna (ex.: "tolerante a falhas",
     "conditional edge", "retry", "checkpoint", "índice no banco");
   - qualquer coisa que não mude o que o usuário percebe.
   Mantenha `feat`/`fix` com impacto visível e **traduza para linguagem de produto**
   (o benefício, não a implementação). Ver memória [[feedback_release_announcement_value_only]].
   > Se a entrega só tiver refator/chore, **avise o usuário** que não há valor de
   > usuário a anunciar — não invente impacto.

4. **Monte a mensagem no template** abaixo: 3–5 bullets no máximo, **negrito** no
   benefício, 1 emoji por bullet, sem blocos de código.

5. **Publique como RASCUNHO** com `slack_send_message_draft` (use o `channel_id`).
   Motivo: as ferramentas do Slack **não fazem upload de imagem** — o usuário anexa o
   print e revisa antes de enviar. Só use `slack_send_message` (envio direto) se não
   houver print **e** o usuário pedir para enviar na hora.

6. **Devolva** ao usuário: link do canal + próximos passos (anexar print → revisar → enviar).

## Template

```
:rocket: :rocket: :rocket:   **Nova versão do <Produto> em produção — <vX.Y.Z>**   :rocket: :rocket: :rocket:

Acabamos de subir uma atualização do <Produto> com melhorias importantes <no atendimento ao ...>:

**:sparkles: O que está melhor**
- :emoji: **<benefício curto>** — <o que o usuário ganha, sem termo técnico>.
- :emoji: **<benefício curto>** — <...>.

**:link: Detalhes técnicos completos**
- <link da release/compare/PR>

**:camera_with_flash: Demonstração abaixo (Opcinal)**
- _(print em anexo)_ :point_down:
```

O link de **detalhes técnicos** no fim é o único "técnico" permitido — serve para quem
quiser se aprofundar, sem poluir o corpo do anúncio.

## Regras de ouro

- **Produto, não engenharia.** Se um bullet só faz sentido para devs, corte.
- Máx. ~5 bullets; cada um = 1 benefício tangível.
- Negrito no benefício, emoji por bullet, recursos visuais do Slack para leitura rápida.
- Nunca invente impacto.

## Skills relacionadas

- `pull-request` — abrir/editar PR (cria via `gh`, edita via `gh api`).
