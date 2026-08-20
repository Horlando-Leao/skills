---
name: language-agnostic-pythonic
description: Aplica princípios de engenharia de software inspirados no Zen of Python e no PEP 8 de forma independente da linguagem, preservando as convenções idiomáticas de cada ecossistema. Use ao escrever, revisar, refatorar ou projetar código em Python, Java, TypeScript, JavaScript, Go, C#, Kotlin, Rust ou outras linguagens, especialmente quando houver dúvidas sobre legibilidade, simplicidade, explicitude, consistência, complexidade, abstração ou tratamento de erros.
---

# Language-Agnostic Pythonic Principles

## Objetivo

Aplicar princípios tradicionalmente associados ao estilo "Pythonic" como princípios gerais de engenharia de software, sem transformar outras linguagens em Python.

A regra central é:

> Preserve a filosofia; preserve a sintaxe idiomática da linguagem.

Os princípios desta skill devem melhorar a clareza, previsibilidade, simplicidade e manutenção do código independentemente da linguagem utilizada.

---

## Princípio fundamental

Distinguir sempre entre:

1. **Princípio de engenharia**
2. **Convenção da linguagem**
3. **Preferência pessoal**

Princípios de engenharia podem ser generalizados.

Convenções devem seguir a linguagem, framework e ecossistema utilizados.

Preferências pessoais nunca devem substituir convenções consolidadas sem uma razão concreta.

### Exemplo

Não transformar Java em Python:

```java
calculate_user_balance()
````

quando a convenção idiomática do projeto é:

```java
calculateUserBalance()
```

O princípio aplicável não é `snake_case`.

O princípio aplicável é:

> Use uma convenção de nomenclatura consistente e idiomática para a linguagem.

---

# Princípios

## 1. Explícito é melhor que implícito

Evite comportamento que exija conhecimento oculto para ser compreendido.

Prefira código em que seja possível identificar:

* entrada;
* transformação;
* saída;
* efeitos colaterais;
* dependências;
* tratamento de erros.

Evite abstrações que escondam comportamento relevante.

### Evitar

```text
process(data)
```

quando `process()` realiza:

```text
validar
salvar
publicar evento
enviar notificação
```

### Preferir

Tornar as responsabilidades e efeitos relevantes identificáveis pelo código e pela arquitetura.

---

## 2. Simples é melhor que complexo

Quando duas soluções resolvem corretamente o mesmo problema, prefira a solução com menor complexidade acidental.

Não adicionar:

* abstrações desnecessárias;
* camadas sem responsabilidade real;
* padrões apenas porque são conhecidos;
* configurações sem necessidade;
* generalizações prematuras.

Perguntar:

> Essa complexidade é necessária pelo domínio ou foi criada pela implementação?

---

## 3. Complexidade necessária deve continuar compreensível

Nem todo problema pode ser simples.

Sistemas distribuídos, autenticação, concorrência, filas, transações e regras de negócio podem naturalmente possuir complexidade.

Quando a complexidade é necessária:

* divida o problema;
* dê nomes precisos;
* reduza dependências;
* isole decisões;
* mantenha cada componente compreensível.

O objetivo não é eliminar toda complexidade.

O objetivo é evitar **complexidade acidental**.

---

## 4. Legibilidade conta

Código é lido muito mais vezes do que é escrito.

Priorizar:

* nomes significativos;
* fluxo evidente;
* pequenas unidades de responsabilidade;
* estrutura previsível;
* baixo nível de aninhamento;
* ausência de "truques";
* convenções consistentes.

Não otimizar código apenas para:

* reduzir quantidade de linhas;
* utilizar menos caracteres;
* parecer mais sofisticado;
* demonstrar domínio avançado da linguagem.

Código curto não é necessariamente código simples.

---

## 5. Prefira uma forma óbvia e consistente de fazer cada coisa

Dentro de um mesmo projeto, problemas semelhantes devem possuir soluções semelhantes.

Evite situações como:

```text
Feature A → Service
Feature B → UseCase
Feature C → Manager
Feature D → Handler
Feature E → Orchestrator
```

quando todas representam essencialmente o mesmo conceito.

Consistência reduz custo cognitivo.

Quando uma convenção arquitetural foi estabelecida e funciona, reutilize-a.

---

## 6. Flat é melhor que profundamente aninhado

Evite estruturas com muitos níveis de:

* `if`;
* `else`;
* loops;
* callbacks;
* promises;
* funções aninhadas;
* classes dentro de classes;
* abstrações encadeadas.

Prefira reduzir o nível de aninhamento utilizando, quando adequado:

* guard clauses;
* funções menores;
* composição;
* early return;
* extração de responsabilidades.

### Exemplo conceitual

Evitar:

```text
if user:
    if account:
        if active:
            if authorized:
                execute()
```

Preferir:

```text
if user is invalid:
    return

if account is invalid:
    return

if user is inactive:
    return

if user is unauthorized:
    return

execute()
```

A implementação concreta deve seguir a sintaxe idiomática da linguagem.

---

## 7. Erros não devem desaparecer silenciosamente

Nunca ocultar uma falha sem uma razão explícita.

Evitar:

```text
catch error:
    do nothing
```

quando o erro possui relevância operacional.

Erros devem ser:

* propagados;
* tratados;
* transformados;
* registrados;

de acordo com o contexto.

Ignorar deliberadamente um erro pode ser válido, mas deve ser uma decisão explícita.

---

## 8. Falhe de maneira previsível

Estados inválidos devem possuir comportamento definido.

Evite funções que:

* retornam valores inconsistentes;
* modificam estado parcialmente;
* escondem erros;
* produzem efeitos colaterais inesperados.

Quando uma operação não pode ser concluída corretamente, o contrato deve deixar isso claro.

---

## 9. Evite abstração prematura

Não crie uma abstração apenas porque existe a possibilidade de reutilização futura.

Evitar criar prematuramente:

* interfaces;
* factories;
* wrappers;
* repositories;
* managers;
* frameworks internos;
* configurações genéricas;
* hierarquias de classes.

Perguntar:

> Existe uma necessidade concreta de abstração agora?

Uma abstração deve reduzir complexidade, não apenas movê-la para outro arquivo.

---

## 10. Prefira composição quando ela reduzir complexidade

Quando comportamentos independentes podem ser combinados de maneira simples, prefira composição a estruturas hierárquicas excessivamente profundas.

Não aplicar composição como dogma.

A escolha deve considerar as capacidades e convenções da linguagem.

O princípio é:

> Escolha a estrutura que torne o comportamento mais fácil de compreender e modificar.

---

## 11. Responsabilidade deve ser clara

Cada componente deve possuir uma responsabilidade identificável.

Isso não significa exigir classes minúsculas ou funções de uma única linha.

Significa evitar componentes que acumulam responsabilidades não relacionadas.

Exemplo conceitual de responsabilidade excessiva:

```text
UserService
 ├─ autenticação
 ├─ persistência
 ├─ envio de e-mail
 ├─ publicação de eventos
 ├─ geração de relatório
 └─ integração com pagamento
```

Separar responsabilidades quando isso reduzir acoplamento e complexidade.

---

## 12. Evite comportamento surpreendente

O nome, contrato e comportamento de uma unidade devem ser coerentes.

Uma função chamada:

```text
calculateTotal()
```

não deveria inesperadamente:

```text
UPDATE database
sendNotification()
publishEvent()
```

Efeitos colaterais importantes devem ser evidentes pela arquitetura ou pelo contrato.

---

## 13. Consistência é mais importante que preferência pessoal

Quando o projeto já possui uma convenção funcional:

> siga a convenção existente.

Não introduzir um estilo diferente apenas porque outra abordagem é pessoalmente preferida.

A consistência do sistema é mais importante do que a preferência individual.

---

## 14. Não confundir "Pythonic" com "Python"

Os seguintes elementos são específicos de Python e não devem ser impostos a outras linguagens:

* `snake_case`;
* indentação de 4 espaços;
* list comprehensions;
* decorators;
* duck typing;
* EAFP;
* type hints no formato Python;
* convenções específicas do PEP 8;
* idioms exclusivos da linguagem.

Ao trabalhar em outra linguagem, utilizar sua própria convenção.

### Exemplo

Java:

```java
calculateUserBalance()
```

TypeScript:

```typescript
calculateUserBalance()
```

Python:

```python
calculate_user_balance()
```

O princípio comum entre os três é:

> O nome deve ser claro, consistente e idiomático para a linguagem.

---

# Processo de aplicação

Ao escrever ou revisar código, seguir esta ordem.

## 1. Identificar o idioma e o ecossistema

Determinar:

* linguagem;
* framework;
* versão relevante;
* convenções existentes no projeto;
* formatter;
* linter;
* padrões arquiteturais já adotados.

---

## 2. Preservar o estilo nativo

Nunca aplicar automaticamente convenções sintáticas de outra linguagem.

Exemplo:

```text
Python → seguir PEP 8 e convenções Python
Java → seguir convenções Java
TypeScript → seguir convenções TypeScript
Go → seguir convenções Go
C# → seguir convenções C#
Rust → seguir convenções Rust
```

---

## 3. Aplicar os princípios universais

Avaliar:

```text
É explícito?
É simples?
É legível?
É previsível?
Existe complexidade desnecessária?
Existe abstração prematura?
Existem efeitos colaterais ocultos?
Os erros são tratados explicitamente?
Existe aninhamento excessivo?
Existe duplicação conceitual?
A responsabilidade está clara?
O código segue a convenção existente?
```

---

## 4. Preferir mudanças pequenas e justificáveis

Não refatorar apenas para "deixar mais Pythonic".

Toda alteração deve possuir uma justificativa relacionada a:

* clareza;
* manutenção;
* redução de complexidade;
* consistência;
* segurança;
* testabilidade;
* previsibilidade.

---

# Regra de decisão

Quando houver conflito entre um princípio geral e a convenção idiomática da linguagem:

> **A convenção idiomática da linguagem vence, desde que preserve legibilidade, simplicidade e consistência.**

Quando houver conflito entre uma preferência pessoal e a convenção consolidada do projeto:

> **A convenção do projeto vence.**

Quando houver conflito entre uma convenção e uma necessidade concreta de engenharia:

> **A necessidade deve vencer, desde que a decisão seja explícita e justificável.**

---

# Checklist de revisão

Antes de considerar o código concluído, verificar:

```text
[ ] O código é explícito?
[ ] O fluxo principal é fácil de identificar?
[ ] A solução é tão simples quanto pode ser?
[ ] A complexidade existente é necessária?
[ ] Existem abstrações prematuras?
[ ] Existem efeitos colaterais ocultos?
[ ] Erros relevantes são tratados explicitamente?
[ ] Existe aninhamento desnecessário?
[ ] Cada componente possui responsabilidade clara?
[ ] O comportamento é previsível?
[ ] A solução segue a convenção do projeto?
[ ] A solução segue a linguagem, sem importar estilos de outra linguagem?
```

# Princípio final

Não escreva Java como Python.

Não escreva TypeScript como Python.

Não escreva Go como Python.

Não escreva Python como Java.

Em vez disso:

> **Escreva cada linguagem de forma idiomática, utilizando princípios de engenharia que transcendem a linguagem.**

A filosofia deve ser transportável.

A sintaxe não.
