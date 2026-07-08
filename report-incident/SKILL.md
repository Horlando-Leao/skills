---
name: report-incident
description: Monta e publica (como RASCUNHO) no Slack um reporte de incidente técnico com estrutura padronizada — causa, diagnóstico com dados reais, correção aplicada, risco estrutural. Use quando o usuário pedir para reportar/comunicar um incidente no Slack. Exige que o usuário informe o canal (link ou ID) e quem reportou o incidente.
---

# Reporte de Incidente no Slack

Gera um rascunho de reporte de incidente **sempre como draft** (nunca envia direto) no canal do Slack informado, seguindo uma estrutura fixa e ancorando o diagnóstico em **dados reais coletados na sessão** — nunca placeholders.

## 🔴 Entradas OBRIGATÓRIAS

Antes de montar qualquer coisa, o usuário **precisa** ter informado os dois itens abaixo. Se faltar algum, siga a regra de fallback correspondente — não invente nem assuma silenciosamente.

1. **Canal do Slack** — aceite qualquer uma das formas:
   - Link: `https://<workspace>.slack.com/archives/<CHANNEL_ID>` → o `channel_id` é o trecho após `/archives/` (um código como `Cxxxxxxxxxx`).
   - ID direto: `Cxxxxxxxxxx`.
   - Link/menção de usuário para DM: resolva o `user_id` via `slack_search_users` e use como `channel_id`.
   - **Se o usuário NÃO passar o canal:** ver "Fallback de canal via memória" abaixo antes de perguntar do zero.
2. **Quem reportou** o incidente (nome da pessoa / cliente que abriu o chamado). Se faltar, **pare e pergunte**.

### 🧠 Fallback de canal via memória

Se o usuário não informar o canal, **antes de pedir**:

1. Procure uma referência de canal já registrada na memória:
   - Memória automática do Claude: o arquivo `MEMORY.md` (e os arquivos de memória `reference`/`feedback` que ele indexa).
   - Memória do projeto: `MEMORY.md`, `CLAUDE.md` ou similar na raiz do repositório.
   - Busque por termos como *canal*, *slack*, *incidente*, *alertas*, `channel_id`, ou um ID no formato `Cxxxxxxxxxx`.
2. **Se encontrar uma referência**, NÃO use direto — **pergunte ao usuário**: *"Não recebi o canal. Encontrei `<canal/descrição>` na memória — posso usar esse?"* e só prossiga com o "ok".
3. **Se não encontrar nada**, peça explicitamente: *"Me passe o canal (link ou ID) do Slack para eu criar o rascunho."*

## 🧩 Regra de dados (inegociável)

- Todo número, ID, `external_id`, tenant, valor de antes/depois **deve vir de dados reais** já levantados na sessão (query no banco, resposta de API, log). **Nunca placeholders.**
- Se um dado citado no incidente ainda não foi verificado, colete antes (ex.: rode a query, bata na API) ou marque claramente como *"a confirmar"*.

## 🏗️ Estrutura FIXA da mensagem (Slack markdown)

Reproduza exatamente esta ordem e formatação. Omita uma seção apenas se não se aplicar (ex.: "Correção aplicada" quando ainda não houve correção → troque por "Ação em andamento").

```
:rotating_light: *Incidente — <título curto do problema> (<cliente/escopo>)*

*Reportado por:* <usuário informado>
*Cliente:* <cliente afetado> — <escopo: condomínio/tenant/módulo>
*<Identificador técnico>:* `<id real>` (<referência ex.: external_id_value>)

*O que aconteceu*
<2-4 linhas: o gatilho, por que quebrou, e o efeito observado. Use _itálico_ para o termo-chave (ex.: _fora de sincronia_).>

*Diagnóstico (<X de Y itens OK, Z divergentes>)*
<Uma frase do método de investigação.>

​```
<tabela/bloco com os dados reais: item -> valor errado -> valor esperado>
​```

<1-2 linhas interpretando os dados: o que os IDs/timestamps revelam sobre a causa.>

*Correção aplicada (<ambiente>, verificada)*
<O que foi feito, o que foi preservado, e a confirmação (ex.: "conferido: status = OK, N/N consistentes").>

*Risco estrutural (pra discutir)*
<O que ainda deixa o sistema vulnerável + 1-2 sugestões objetivas numeradas.>

_Observação à parte:_ <itens secundários que não afetam o incidente principal, se houver.>
```

### Diretrizes de tom
- Direto, escaneável, sem enrolação — quem lê entende o incidente em < 1 min.
- Foque no **porquê** e no **impacto**, não em detalhe de implementação irrelevante.
- Negrito nos rótulos de seção; bloco de código para dados tabulares (IDs, antes/depois).
- Português. Código/identificadores em inglês quando for o caso.

## 🔄 Fluxo (obrigatório nesta ordem)

1. **Cheque as entradas obrigatórias.** Faltou quem reportou → pergunte e pare. Faltou o canal → aplique o "Fallback de canal via memória".
2. **Resolva o `channel_id`** a partir do link/ID/usuário/memória (com confirmação).
3. **Reúna os dados reais** do incidente já disponíveis na sessão. Se algo essencial faltar, colete antes.
4. **Monte a mensagem** na estrutura fixa acima.
5. **VALIDE COM O USUÁRIO ANTES DE CRIAR O DRAFT.** Apresente a mensagem completa no chat e pergunte se está boa / se quer ajustes (tom, marcar alguém, encurtar, remover seção). **Não crie o draft sem o "ok".**
6. **Só após aprovação, crie o rascunho** com `slack_send_message_draft` (channel_id + message). **Sempre draft — nunca `slack_send_message`**, a menos que o usuário peça explicitamente para enviar.
7. **Retorne o link do canal/rascunho** e ofereça ajustes (marcar pessoa, encurtar, versão executiva).

## ⚠️ Observações
- Só existe **um draft anexado por canal**. Se retornar `draft_already_exists`, avise o usuário para editar/apagar o rascunho existente antes de recriar.
- `channel_not_found` → o `channel_id` está errado ou o usuário não tem acesso ao canal.
- Não salve a mensagem no repositório; ela vive apenas no rascunho do Slack.
