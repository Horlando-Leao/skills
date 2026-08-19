# Agent Skills Repository

Coleção de skills especializadas para agentes de IA, seguindo a especificação oficial do [agentskills.io](https://agentskills.io).

![GitHub](https://img.shields.io/badge/GitHub-Horlando--Leao/skills-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Skills](https://img.shields.io/badge/Skills-22-brightgreen)

## 📌 Categorias

- [🔀 Pull Requests & Code Review](#-pull-requests--code-review)
- [🐛 Investigação & Incidentes](#-investigação--incidentes)
- [🧪 Testes & Execução Local](#-testes--execução-local)
- [🛠️ Desenvolvimento & Refatoração](#%EF%B8%8F-desenvolvimento--refatoração)
- [🛡️ Segurança](#%EF%B8%8F-segurança)
- [📢 Comunicação & Documentação](#-comunicação--documentação)
- [⚙️ Meta-Skills & Gerenciamento](#%EF%B8%8F-meta-skills--gerenciamento)

---

## 🚀 Skills Disponíveis

### 🔀 Pull Requests & Code Review

#### **code-comment-review** 💬
Varre um escopo de código (diff, path ou repo) em busca de comentários grandes, com racional/histórico ou referências a card/ticket, e os enxuga para uma única linha funcional ("recebe X, faz Y, devolve Z"). Use quando o usuário pedir para revisar, limpar, enxugar ou "arrumar" comentários de código, ou remover referências a card/issue de comentários.

- **Diretório:** [code-comment-review/](code-comment-review/)

---

#### **pr-flow-watch** 👁️
Acompanha o ciclo de vida de uma PR do início ao fim — checks de CI no envio, aviso no Slack pedindo aprovação, aprovação da PR e build/deploy pós-merge — usando comandos bloqueantes únicos em vez de polling manual turno-a-turno. Funciona para qualquer fluxo de PR (não é específico de release). Use quando o usuário pedir para "monitorar/acompanhar uma PR", "avisar quando a PR for aprovada", "esperar o CI/build/deploy" ou pedir esse acompanhamento de ponta a ponta.

- **Diretório:** [pr-flow-watch/](pr-flow-watch/)

---

#### **pr-with-diagrams** 📈
Gera uma descrição de PR completa com diagrama Mermaid baseado em dados reais do banco — nunca usa placeholders. Orquestra query-local para buscar IDs e external_ids antes de gerar qualquer artefato.

- **Diretório:** [pr-with-diagrams/](pr-with-diagrams/)

---

#### **pull-request** 🔀
Instructions for writing a good PR description

- **Diretório:** [pull-request/](pull-request/)

---

#### **review-pr** ✅
Code review assistant with architecture and database validation criteria

- **Diretório:** [review-pr/](review-pr/)

---

#### **task-criteria-review** 📋
Revisa se os critérios e requisitos de uma tarefa (Jira etc.) foram implementados no diff da branch atual vs main. Use quando o usuário fornecer ID ou conteúdo de um ticket e quiser validar se as mudanças de código atendem aos requisitos, critérios de aceite ou subtarefas.

- **Diretório:** [task-criteria-review/](task-criteria-review/)

---

### 🐛 Investigação & Incidentes

#### **bug-resolution-cycle** 🐛
Ciclo estruturado para investigar e resolver bugs do começo ao fim — da causa raiz ao Pull Request. Use SEMPRE que o usuário relatar um bug, erro, comportamento inesperado, exceção, stack trace, crash, falha, ou pedir para "corrigir", "consertar", "debugar", "investigar" ou "resolver" algo que não está funcionando. Vale tanto para pedidos explícitos ("tem um bug em X") quanto implícitos ("isso aqui tá retornando errado", "por que isso quebra?"). Termos de disparo — bug, erro, falha, exceção, crash, debug, corrigir, consertar, não funciona, comportamento estranho, error, exception, fix, broken, not working.

- **Diretório:** [bug-resolution-cycle/](bug-resolution-cycle/)

---

#### **report-incident** 🚨
Monta e publica (como RASCUNHO) no Slack um reporte de incidente técnico com estrutura padronizada — causa, diagnóstico com dados reais, correção applied, risco estrutural. Use quando o usuário pedir para reportar/comunicar um incidente no Slack. Exige que o usuário informe o canal (link ou ID) e quem reportou o incidente.

- **Diretório:** [report-incident/](report-incident/)

---

#### **technical-storytelling** 📖
Reconstructs technical bugs, discoveries, incidents, and documentation from conversation context or document folders into clear, evidence-based technical narratives. It connects context, symptoms, investigation, findings, root cause, reproduction steps, decisions, and resolution so developers who did not participate in the investigation can quickly understand what happened, why it happened, and what needs to be done.

- **Diretório:** [technical-storytelling/](technical-storytelling/)

---

### 🧪 Testes & Execução Local

#### **query-local** 🔍
Executa queries SQL diretamente no banco Postgres local (gruvi-concierge-orquestrador) para validar/verificar dados ou tabelas

- **Diretório:** [query-local/](query-local/)

---

#### **test-api** 🧪
Busca a documentação da API local (http://localhost:3001/api/docs.json), localiza o endpoint que o usuário quer testar e gera um curl completo e pronto para executar

- **Diretório:** [test-api/](test-api/)

---

#### **teste-local** 🔧
Guia completo para testar uma feature localmente: orienta quando usar as skills arquitetura, query-local e test-api durante o ciclo de desenvolvimento e validação local.

- **Diretório:** [teste-local/](teste-local/)

---

### 🛠️ Desenvolvimento & Refatoração

#### **nestjs-di-patterns** 🏗️
Guia para uso de interfaces vs classes abstratas no NestJS DI. Use quando criar repositórios, services ou qualquer abstração que será injetada via DI.

- **Diretório:** [nestjs-di-patterns/](nestjs-di-patterns/)

---

#### **new-migration-typeorm** 📦
Create TypeORM migrations using native CLI commands. Use when creating database migrations, schema changes, adding/removing columns, or modifying table structure.

- **Diretório:** [new-migration-typeorm/](new-migration-typeorm/)

---

#### **safe-rename** ♻️
Renomeia com segurança um campo de DTO, entidade ou propriedade em todo o repositório, garantindo que nenhum arquivo dependente fique quebrado antes de declarar a tarefa concluída

- **Diretório:** [safe-rename/](safe-rename/)

---

#### **semantic-commits** 💾
Analyzes staged files, groups them semantically by logical relationship, and creates separate conventional commits for each group. Ideal when you have many staged files that should be split into multiple meaningful commits.

- **Diretório:** [semantic-commits/](semantic-commits/)

---

### 🛡️ Segurança

#### **secret-detector** 🔐
Analisa diretórios inteiros procurando por segredos, tokens, chaves privadas e credenciais expostas usando padrões regex avançados. Identifica exposições de segurança como API keys, senhas, tokens de GitHub, AWS credentials e chaves SSH antes de fazer commit ou deploy.

- **Diretório:** [secret-detector/](secret-detector/)

---

### 📢 Comunicação & Documentação

#### **mermaid-to-svg** 📊
Use esta skill quando o usuário pedir para converter, renderizar ou transformar um diagrama Mermaid (texto ou arquivo .mmd) em um arquivo de imagem SVG.

- **Diretório:** [mermaid-to-svg/](mermaid-to-svg/)

---

#### **publicar-confluence** 📘
Publica um relatório Markdown em uma página do Confluence Cloud via REST API, convertendo para o formato storage e validando antes de escrever. Use quando o usuário pedir para publicar, republicar ou atualizar um documento no Confluence.

- **Diretório:** [publicar-confluence/](publicar-confluence/)

---

#### **release-announcement-value-only** 📢
Gera e publica (como RASCUNHO) no canal do Slack do time um anúncio de release focado em VALOR DE PRODUTO, a partir de uma release tag ou de uma PR. Pede o link do canal e a referência (tag/PR), filtra refatorações/detalhes técnicos e escreve em linguagem de produto. Use quando o usuário pedir para anunciar/comunicar uma release ou entrega no Slack.

- **Diretório:** [release-announcement-value-only/](release-announcement-value-only/)

---

### ⚙️ Meta-Skills & Gerenciamento

#### **github-skill-manager** 🐙
Gerencia o ciclo de vida de Agent Skills usando os comandos oficiais 'gh skill' da GitHub CLI. Valida, inspeciona e publica pacotes de habilidades diretamente em repositórios do GitHub.

- **Diretório:** [github-skill-manager/](github-skill-manager/)

---

#### **skill-generator** 🛠️
Meta-skill especializada na criação e arquitetura de novas habilidades para agentes de IA. Guia o usuário na estruturação modular (scripts, references, assets) e validação técnica seguindo os padrões oficiais do agentskills.io.

- **Diretório:** [skill-generator/](skill-generator/)

---

## 🔧 Instalação e Uso

Você pode instalar qualquer uma das skills deste repositório utilizando a ferramenta `npx` ou a CLI oficial do GitHub:

### Usando npx
```bash
npx skills add Horlando-Leao/skills <nome-da-skill>
```

### Usando GitHub CLI
```bash
gh skill install Horlando-Leao/skills <nome-da-skill>
```

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Skills Totais** | 22 |
| **Padrões de Detecção** | 20+ (secret-detector) |
| **Licença** | MIT |

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes

---

## 👤 Autor

**Horlando Leão**

- GitHub: [@Horlando-Leao](https://github.com/Horlando-Leao)
- Email: horlandoleao8@gmail.com

---

**Última atualização:** 19 de agosto de 2026
