---
name: slack-meeting-scheduler
description: A partir de um link de mensagem ou thread do Slack, identifica as pessoas @mencionadas, busca os e-mails delas, encontra um horário livre em comum e cria um evento no Google Calendar com Google Meet, título e tema da reunião. Em seguida envia de volta, no mesmo lugar de origem (canal, thread ou DM), uma mensagem agendada para ~2 minutos avisando sobre a reunião marcada. Use quando o usuário pedir para "marcar uma agenda/reunião com os marcados/mencionados" a partir de um link do Slack, ou pedir para agendar uma call com quem está numa thread/mensagem específica.
metadata:
  author: horlando.leao
  version: "1.0"
---

# Slack Meeting Scheduler

Automatiza o fluxo: link do Slack → identificar envolvidos → achar e-mails → achar horário livre → criar evento no Google Calendar com Meet → avisar no Slack (mensagem agendada).

## Ferramentas usadas

- `mcp__claude_ai_Slack__slack_read_thread` — ler a mensagem/thread apontada pelo link
- `mcp__claude_ai_Slack__slack_read_user_profile` — resolver `user_id` → e-mail
- `mcp__claude_ai_Google_Calendar__suggest_time` — achar horário livre comum
- `mcp__claude_ai_Google_Calendar__create_event` — criar o evento com Meet
- `mcp__claude_ai_Slack__slack_schedule_message` — avisar no Slack, agendado
- `Bash` (`date +%s`) — calcular o `post_at` da mensagem agendada

Essas ferramentas são deferidas (MCP). Se não aparecerem já carregadas no contexto, use `ToolSearch` com `select:<nome1>,<nome2>,...` antes de chamá-las.

## Passo 1 — Parsear o link do Slack

Formato típico:

```
https://<workspace>.slack.com/archives/<channel_id>/p<timestamp17digits>?thread_ts=<thread_ts>&cid=<channel_id>
```

- `channel_id`: segmento após `/archives/` (ex: `C0BHK13LWPJ`)
- Timestamp da mensagem apontada: o `p<17 dígitos>` do path — insira um ponto decimal antes dos últimos 6 dígitos para virar o `message_ts` do Slack (ex: `p1788281214920759` → `1788281214.920759`)
- Se a query string tiver `thread_ts=`, a mensagem faz parte de uma thread cujo pai é `thread_ts` — use esse valor como `message_ts` ao chamar `slack_read_thread` (é o parâmetro que a ferramenta espera: timestamp da mensagem *raiz*)
- Se não houver `thread_ts` na URL, a própria mensagem é a raiz — use o timestamp derivado do `p...` como `message_ts`

Sem link — se o usuário descrever o pedido sem colar um link, peça o link antes de prosseguir (não dá para localizar os envolvidos sem ele).

## Passo 2 — Ler a thread e identificar os envolvidos

Chame `slack_read_thread` com `channel_id` e `message_ts` (a raiz, conforme passo 1).

Os **envolvidos** são as pessoas `@mencionadas` (`<@U...|Nome>`) na mensagem específica apontada pelo link (a última reply do thread, se o link apontar para uma reply específica — não todo mundo que já falou na thread). Use o restante da thread apenas como **contexto** para entender do que se trata a reunião, não para definir a lista de convidados.

Extraia os `user_id` (formato `U0XXXXXXX`) das menções dessa mensagem.

## Passo 3 — Buscar e-mail de cada envolvido

Para cada `user_id`, chame `slack_read_user_profile(user_id)` e extraia o campo `Email`. Chame em paralelo quando houver mais de um envolvido — essas chamadas são independentes.

Se algum perfil não tiver e-mail visível, avise o usuário e pergunte como prosseguir (não invente e-mail).

## Passo 4 — Definir título e tema

Resuma o assunto da reunião a partir do contexto lido na thread (não apenas da última mensagem — normalmente o "gancho" da reunião está nas mensagens anteriores que motivaram o pedido). Escreva:

- **Título curto** (para o `summary` do evento)
- **Tema/descrição** (2-4 linhas de contexto, para a `description` do evento)

Se o assunto da thread for genuinamente ambíguo (múltiplos tópicos sem um fio condutor claro), pare e pergunte ao usuário qual é o tema antes de criar o evento. Não é necessário confirmar quando o tema está razoavelmente claro pelo contexto.

## Passo 5 — Buscar horário disponível

Chame `suggest_time` com:
- `attendeeEmails`: e-mails do passo 3
- `startTime` / `endTime`: janela de busca — por padrão, do próximo horário útil até +3 dias úteis
- `timeZone`: `America/Sao_Paulo` (a menos que o contexto indique outro)
- `durationMinutes`: 30 por padrão (ajuste se o usuário pedir duração diferente)
- `preferences`: `startHour: "09:00"`, `endHour: "18:00"`, `excludeWeekends: true`

Escolha o **primeiro slot livre** retornado que comporte a duração desejada. Se nenhum slot for retornado, informe o usuário que não há horário comum livre na janela buscada e pergunte se quer ampliar a janela — não force um horário com conflito.

## Passo 6 — Criar o evento

Chame `create_event` com:
- `summary`: título do passo 4
- `description`: tema do passo 4 + link da thread/mensagem original do Slack (para rastreabilidade)
- `startTime` / `endTime`: slot escolhido no passo 5, com o mesmo `timeZone`
- `attendees`: lista de `{email}` do passo 3
- `addGoogleMeetUrl: true`

Guarde da resposta: `conferenceUrl` (link do Meet), `start.dateTime`, `htmlLink` (link do evento no Google Calendar).

## Passo 7 — Avisar no Slack (mensagem agendada)

O aviso volta para o **mesmo lugar de origem do link**:
- Se o link apontava para uma **thread** (havia `thread_ts` na URL, ou a mensagem raiz tem replies): responda na mesma thread, passando `thread_ts` igual ao `message_ts` usado no passo 2.
- Se o link apontava para uma **mensagem solta em canal** (sem thread): envie no canal, sem `thread_ts`.
- Se `channel_id` resolver para uma **DM** (canal começando com `D`) ou o pedido for para uma pessoa específica: use esse `channel_id` normalmente — `slack_schedule_message` funciona igual para canal, thread ou DM.

Calcule `post_at`:
```bash
date +%s
```
Some **120** (2 minutos) ao valor retornado — é o mínimo aceito pela API do Slack (`post_at` precisa ser >= 2 min no futuro). Se o usuário pedir um valor diferente de "2 minutos", respeite o pedido dele, mas nunca menos que 120s de folga.

Monte a mensagem mencionando cada envolvido com `<@USER_ID>`, informando data/hora da reunião, o link do Meet **e** o link do evento no Google Calendar (`htmlLink`), por exemplo:

```
Lembrete: marquei a reunião "<título>" para <dia> às <hora>. Convite enviado a <@U...> <@U...> ... — link do Meet: <conferenceUrl> — agenda: <htmlLink>
```

Chame `slack_schedule_message(channel_id, message, post_at, thread_ts?)`.

## Passo 8 — Reportar ao usuário

Resuma em poucas linhas: título, data/hora, link do Meet, quem foi convidado, e que o lembrete foi agendado (com o horário exato, já que raramente cai em exatamente "2 minutos" por causa do arredondamento da API).

## Erros comuns a evitar

- Não confundir `message_ts` da URL com `thread_ts` — quando a URL já tem `thread_ts=`, é esse valor que vai no parâmetro `message_ts` de `slack_read_thread` (a ferramenta quer a raiz da thread, não a reply específica).
- Não convidar todo mundo que participou da thread — só quem foi `@mencionado` na mensagem apontada pelo link.
- Não usar `slack_send_message` para o aviso — o pedido é sempre para mensagem **agendada** (`slack_schedule_message`), mesmo que o destino seja uma DM.
- Não esquecer `addGoogleMeetUrl: true` — sem isso o evento não tem link de reunião.
- A mensagem agendada precisa trazer **os dois links**: o do Meet (`conferenceUrl`) e o do evento na agenda (`htmlLink`) — não só um deles.
