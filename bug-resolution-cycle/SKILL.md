---
name: bug-resolution-cycle
description: 'Ciclo estruturado para investigar e resolver bugs do começo ao fim — da causa raiz ao Pull Request. Use SEMPRE que o usuário relatar um bug, erro, comportamento inesperado, exceção, stack trace, crash, falha, ou pedir para "corrigir", "consertar", "debugar", "investigar" ou "resolver" algo que não está funcionando. Vale tanto para pedidos explícitos ("tem um bug em X") quanto implícitos ("isso aqui tá retornando errado", "por que isso quebra?"). Termos de disparo — bug, erro, falha, exceção, crash, debug, corrigir, consertar, não funciona, comportamento estranho, error, exception, fix, broken, not working.'
---

# Ciclo de Resolução de Bugs

Um processo disciplinado para resolver bugs sem pular etapas. A ideia central é **não saltar direto para a solução**: a maioria das correções ruins vem de tratar o sintoma antes de entender a causa. Este ciclo força investigação antes de ação, e usa o usuário como ponto de controle em dois momentos críticos (escolha da solução e validação).

## Princípios que valem o ciclo inteiro

- **Causa raiz antes de qualquer correção.** Se você ainda não sabe *por que* o bug acontece, você não está pronto para consertar. Resista à pressa.
- **O usuário decide nos gates.** Não aplique uma correção sem o usuário escolher a abordagem (Fase 4→5), e não faça commit antes de o usuário validar (Fase 7). Esses dois portões existem pra evitar retrabalho e mudanças não autorizadas.
- **Correção mínima e direcionada.** Resolva o bug em questão. Não aproveite para refatorar coisas não relacionadas — isso obscurece o que de fato corrigiu o problema e dificulta o review.
- **Uma volta no loop é normal.** Se o teste falhar (Fase 7), voltar para a Fase 1 com a nova informação não é fracasso — é o ciclo funcionando.

---

## Fase 1 — Investigar a causa raiz

Entenda o problema antes de propor qualquer coisa. Peça os artefatos necessários ao invés de adivinhar:

- **Logs e stack traces** completos (não só a última linha).
- **Prints / vídeos** do comportamento, quando for visual.
- **Passos para reproduzir** e o resultado esperado vs. o obtido.
- **Ambiente**: versões (linguagem, framework, libs), SO, navegador, dados de entrada.
- **Código relevante** ao redor do ponto de falha.

Depois, vá fundo:
- Tente **reproduzir** o bug. Um bug que você não consegue reproduzir você não tem como confirmar que corrigiu.
- **Separe sintoma de causa.** O erro que aparece na tela raramente é a origem. Pergunte "por que?" sucessivamente até chegar no mecanismo real.
- Se faltar informação para localizar a causa, **pare e peça** — não prossiga com hipóteses frágeis.

**Só avance quando a causa raiz estiver clara.**

## Fase 2 — Explicar em detalhe

Explique para o usuário, em linguagem clara, **o que** está acontecendo, **por que** acontece e **qual o mecanismo**. Conecte a explicação às evidências concretas (a linha do log, o trecho de código, a condição que dispara o erro). O usuário deve terminar essa fase entendendo o bug, não só aceitando que você o entendeu.

## Fase 3 — Propor 2-3 soluções

Apresente de 2 a 3 abordagens distintas. Para cada uma:
- **Descrição** breve do que muda.
- **Vantagens.**
- **Trade-offs / desvantagens** (risco, esforço, impacto em outras partes, dívida técnica).

Soluções genuinamente diferentes — não a mesma ideia em três roupagens.

## Fase 4 — Recomendar a melhor

Indique qual das opções você recomenda e **por quê** (qual trade-off pesou). Então **espere o usuário escolher ou aprovar** antes de mexer no código. Este é um gate: não aplique nada ainda.

## Fase 5 — Aplicar a correção

Com a abordagem escolhida, aplique a correção:
- Mantenha-a **mínima e focada** na causa raiz identificada.
- Considere adicionar um **teste de regressão** que falharia com o bug e passa com a correção — é a melhor garantia de que o problema não volta.
- Aponte claramente o que mudou e onde.

## Fase 6 — Propor testes manuais

Proponha **passos de teste concretos** para o usuário validar (não "teste aí"). Liste o que verificar, incluindo o caso que originou o bug e casos de borda relacionados. Então **espere o usuário testar e dar o retorno.**

## Fase 7 — Gate de validação

> O usuário confirmou que a correção funcionou?
> - **Sim** → siga para a Fase 8.
> - **Não** → volte para a **Fase 1**, agora incorporando o que o novo teste revelou. Não tente um remendo por cima sem reinvestigar.

## Fase 8 — Branch, commit e push

Proponha (sem executar sem confirmação, salvo se o usuário já tiver dado sinal verde):
- **Branch**, se necessário, com nome descritivo (ex.: `fix/login-timeout`, `bugfix/null-pointer-checkout`).
- **Commit** em formato convencional: `fix(escopo): descrição curta no imperativo`. Ex.: `fix(auth): corrige expiração prematura de sessão`.
- **Push** para o remoto.

## Fase 9 — Propor Pull Request

Proponha um PR com:
- **Título** claro.
- **Descrição** cobrindo: o problema/sintoma, a causa raiz, a solução adotada, e **como testar**.
- Referência à issue, se houver.

---

## Resumo do fluxo

```
1. Investigar causa raiz (pedir logs/prints/artefatos)
2. Explicar em detalhe
3. Propor 2-3 soluções (vantagens + trade-offs)
4. Recomendar a melhor  ──► [GATE: usuário escolhe]
5. Aplicar correção (mínima + teste de regressão)
6. Propor testes manuais ──► [espera o usuário testar]
7. Validou? ── Não ──► volta ao passo 1
            └─ Sim ─┐
8. Branch + commit + push
9. Propor Pull Request
```
