---
name: pr-flow-watch
description: Acompanha o ciclo de vida de uma PR do início ao fim — checks de CI no envio, aviso no Slack pedindo aprovação, aprovação da PR e build/deploy pós-merge — usando comandos bloqueantes únicos em vez de polling manual turno-a-turno. Funciona para qualquer fluxo de PR (não é específico de release). Use quando o usuário pedir para "monitorar/acompanhar uma PR", "avisar quando a PR for aprovada", "esperar o CI/build/deploy" ou pedir esse acompanhamento de ponta a ponta.
---

# PR Flow Watch

Acompanha uma PR em 4 etapas, sempre com **uma única chamada de ferramenta bloqueante por
etapa** — nunca um loop de "checar, esperar, checar de novo" feito pelo próprio agente.

## Princípio de eficiência (leia antes de executar)

Monitorar algo que demora minutos ou horas tem duas formas de implementação, com custo muito
diferente:

- ❌ **Polling manual repetido**: o agente chama uma ferramenta para checar status, vê que
  ainda está rodando, e precisa de uma *nova rodada de raciocínio* para checar de novo depois.
  Cada checagem reprocessa o histórico da conversa (que só cresce) e gasta tokens de output só
  para "pensar" de novo. Isso também vale para a ferramenta `Monitor`: ela gera **uma
  notificação por linha de stdout**, então um loop que imprime a cada iteração (`echo` dentro
  de um `while`) gera uma notificação — e um novo turno do agente — por iteração.
- ✅ **Comando bloqueante único**: um único comando de shell que já sabe esperar por conta
  própria e só retorna (ou só imprime) quando termina. O shell fica bloqueado esperando — sem
  custo de LLM enquanto espera — e o agente só "pensa" de novo quando o processo termina.

**Regras práticas para esta skill:**

1. Sempre invoque os scripts abaixo com a ferramenta `Bash` e `run_in_background: true`. O
   `Bash` em background notifica **uma vez**, quando o comando termina — diferente do
   `Monitor`, que notifica a cada linha de stdout. **Não use `Monitor` nesta skill.**
2. Os scripts em `scripts/` não imprimem nada durante o polling interno — só imprimem a
   linha final de resultado. Isso é intencional: eles fazem o `sleep` em loop dentro do
   *shell*, não em turnos do agente.
3. Quando o `gh` CLI tiver um comando bloqueante nativo (ex.: `gh run watch <id>
   --exit-status`), use-o em vez de reimplementar polling. `watch-build.sh` já faz isso.
   `gh pr checks --watch` **não está disponível** na versão do `gh` deste ambiente (testado:
   `unknown flag: --watch`) — por isso `wait-checks.sh` implementa o próprio loop silencioso.
4. Nunca faça `sleep` dentro de um turno do agente (isso bloqueia a conversa e ainda conta
   como raciocínio). O `sleep` sempre vive dentro do script bash, não entre chamadas de
   ferramenta.

## Pré-requisitos / inputs

Antes de começar, obtenha (pergunte ao usuário se não estiver claro):

- **PR**: número ou URL. Se omitido, descubra a PR da branch atual:
  `gh pr view --json number --jq .number`.
- **Destino do aviso no Slack**: canal ou usuário (ID ou link) para pedir aprovação na
  Etapa 1.1. Não invente um destinatário — se o usuário não informou, pergunte.
- **(Opcional) branch base**: para a Etapa 3, o padrão é a `baseRefName` da própria PR
  (normalmente `main`).

## Etapa 1 — Esperar os checks de CI da PR

```bash
bash .agents/skills/pr-flow-watch/scripts/wait-checks.sh <PR_NUMBER>
```

Rode via `Bash` com `run_in_background: true`. Ao terminar, o output final será
`CI_RESULT=success` ou `CI_RESULT=failure` (com a lista de checks que falharam).

- Se `failure`: avise o usuário no chat com os checks que falharam e **pare aqui** — não
  peça aprovação de uma PR com CI quebrado.
- Se `success`: siga para a Etapa 1.1.

## Etapa 1.1 — Pedir aprovação no Slack

Envie uma mensagem (ferramenta MCP do Slack, ex. `slack_send_message`) para o destino
combinado nos pré-requisitos, com:

- Link da PR (`gh pr view <PR_NUMBER> --json url --jq .url`)
- Título da PR
- Resumo de 1 linha do que mudou (não invente — leia o título/corpo real da PR)
- Pedido claro de aprovação

Isso é uma única chamada de ferramenta — não precisa de polling.

## Etapa 2 — Esperar a aprovação

```bash
bash .agents/skills/pr-flow-watch/scripts/wait-approval.sh <PR_NUMBER>
```

Rode via `Bash` com `run_in_background: true`. Output final:
`APPROVAL_RESULT=approved` ou `APPROVAL_RESULT=closed_without_approval`.

- Se `closed_without_approval`: avise o usuário e pare.
- Se `approved`: avise o usuário que a PR foi aprovada e siga para a Etapa 3.

## Etapa 3 — Esperar o merge e assistir o build/deploy

Primeiro espera o merge (a aprovação por si só não dispara build/deploy — precisa do merge):

```bash
bash .agents/skills/pr-flow-watch/scripts/wait-merge.sh <PR_NUMBER>
```

Rode via `Bash` com `run_in_background: true`. Output final:
`MERGE_RESULT=merged` + `MERGE_SHA=<sha>` + `MERGE_BRANCH=<branch>`, ou
`MERGE_RESULT=closed_unmerged`.

Depois, com o SHA do merge, assista o workflow disparado por ele:

```bash
bash .agents/skills/pr-flow-watch/scripts/watch-build.sh <MERGE_SHA> <MERGE_BRANCH>
```

Também via `Bash` com `run_in_background: true`. Output final: `BUILD_RESULT=success` ou
`BUILD_RESULT=failure` (ou `not_found`, se nenhum run apareceu em ~5 minutos), seguido da
URL do run.

> Se o pipeline do repositório não dispara build/deploy no merge em si, e sim na criação de
> uma tag/Release (como no fluxo de `release-flow`), passe para `watch-build.sh` o SHA da tag
> em vez do `MERGE_SHA` — o script funciona igual, só precisa do commit certo.

## Etapa final — Resumo

Ao final (sucesso ou falha em qualquer etapa), resuma para o usuário no chat o que aconteceu
em cada etapa. Só envie mensagem adicional no Slack se o usuário tiver pedido explicitamente
um aviso de conclusão — não assuma.
