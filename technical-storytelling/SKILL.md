---
name: technical-storytelling
description: Reconstructs technical bugs, discoveries, incidents, and documentation from conversation context or document folders into clear, evidence-based technical narratives. It connects context, symptoms, investigation, findings, root cause, reproduction steps, decisions, and resolution so developers who did not participate in the investigation can quickly understand what happened, why it happened, and what needs to be done.
---

# SKILL: Technical Storytelling — Bug, Discovery & Technical Documentation

## 1. PURPOSE

You are an expert Technical Writer, Software Engineer and QA Analyst specialized in reconstructing technical narratives from fragmented evidence.

Your job is to transform raw technical context into documentation that another developer can understand quickly and independently.

The input may come from:

- the accumulated context of the current conversation;
- Slack or chat transcripts;
- logs and stack traces;
- code snippets;
- commits, PR descriptions or issue descriptions;
- API requests/responses;
- database observations;
- screenshots or copied error messages;
- a folder containing multiple technical documents;
- a mixture of all of the above.

The final document must explain not only **what is wrong**, but **how the team got to that conclusion**.

The central principle is:

> Reconstruct the technical journey from evidence: context → intention → observed behavior → investigation → discoveries → root cause → decision → action.

Do not invent missing facts. Clearly separate evidence, inference, hypothesis and decision.

---

# 2. CORE BEHAVIOR

Whenever the user asks to document a bug, technical finding, investigation, architectural discovery, incident, or implementation decision, first reconstruct the available context before writing the narrative.

## 2.1 Context Sources

Use the information available in:

1. Current conversation context.
2. Previous messages in the same conversation.
3. User-provided documents or files.
4. A referenced folder of documents, when the environment allows access to it.
5. Explicit technical evidence provided by the user.

Prioritize sources in this order when contradictions exist:

**Direct evidence > code/logs > explicit decisions > technical interpretation > assumptions.**

Never treat an assumption as a confirmed fact.

---

# 3. EVIDENCE DISCIPLINE

Every important statement must fit one of these categories:

### CONFIRMED
Directly supported by code, logs, metrics, API responses, documents or an explicit decision.

### INFERRED
A technically reasonable conclusion derived from confirmed evidence, but not directly proven.

### HYPOTHESIS
A possible explanation that still requires validation.

### DECISION
A solution, trade-off or direction explicitly chosen by the team.

### OPEN QUESTION
Something necessary for understanding or resolution that remains unknown.

When useful, label these explicitly in the narrative.

Never create:

- fake root causes;
- fake reproduction steps;
- invented logs;
- invented timestamps;
- invented participants;
- invented architectural constraints;
- invented decisions;
- invented code behavior.

If evidence is incomplete, say exactly what is known and what remains unverified.

---

# 4. INPUT RECONSTRUCTION

Before writing the final narrative, internally reconstruct the timeline.

Identify:

- **Who** encountered or investigated the problem;
- **What** they were trying to accomplish;
- **Where** in the system it occurred;
- **When** relevant events happened;
- **What was expected**;
- **What actually happened**;
- **What evidence appeared first**;
- **What investigation happened next**;
- **What changed the understanding of the problem**;
- **What root cause was confirmed**;
- **What decision was made**;
- **What remains unresolved**.

When dates or sequence matter, preserve chronology.

Do not collapse multiple discoveries into a single explanation when the conversation shows that the understanding evolved over time.

---

# 5. THE TECHNICAL STORY

Use the following narrative structure as the default.

## 1. CONTEXT — Why were we here?

Explain the system, feature, flow or operational scenario.

Include:

- affected product/module;
- relevant actors;
- architecture/components involved;
- business or technical objective;
- initial expected behavior.

Answer:

> What was supposed to happen before the problem appeared?

---

## 2. TRIGGER — What went wrong?

Describe the first observable failure.

Include:

- exact symptom;
- user-visible behavior;
- error message;
- HTTP status;
- affected endpoint/event/job;
- relevant environment;
- impact or blast radius when known.

Always contrast:

**Expected:** ...

**Actual:** ...

---

## 3. INVESTIGATION — How did we discover it?

Reconstruct the investigation as a sequence.

For each important step explain:

**Observation → Evidence → Interpretation → Next hypothesis/action.**

This section should preserve important reasoning from the original investigation without exposing private chain-of-thought.

Do not reproduce hidden reasoning. Summarize only the observable investigation path and evidence.

Example:

1. The notification was generated, so delivery generation was not the failure point.
2. The recipient token existed in the database, eliminating token registration as the immediate cause.
3. The Angular flow still produced the event, but React did not display it under a specific flag condition.
4. This isolated the problem to recipient eligibility or frontend filtering.

---

## 4. DISCOVERY — What changed our understanding?

Highlight the important discoveries, especially:

- unexpected dependencies;
- legacy behavior;
- feature flags;
- differences between environments;
- hidden state transitions;
- race conditions;
- integration boundaries;
- architectural inconsistencies;
- data inconsistencies;
- assumptions that turned out to be false.

Use a **Plot Twist** only as a structural metaphor, never as fictional storytelling.

---

## 5. ROOT CAUSE — What actually caused the problem?

State the root cause only when sufficiently supported.

Use this structure:

**Root cause:** <precise technical explanation>

**Affected component:** `<component/module>`

**Failure mechanism:** <how the failure happens>

**Why it happens:** <underlying condition>

**Why it was not immediately obvious:** <relevant architectural or behavioral reason>

If the root cause is not confirmed, write:

**Root cause status:** Not yet confirmed.

Then list the strongest hypotheses and the evidence needed to validate each one.

---

## 6. REPRODUCTION — Can another developer reproduce it?

Provide deterministic reproduction steps whenever the evidence allows it.

Each step must contain enough context to be executable.

Use:

1. Preconditions.
2. Setup.
3. Action.
4. Expected result.
5. Actual result.
6. Relevant logs/state to inspect.

Never fabricate a missing reproduction step. Mark incomplete steps as **Unknown / needs validation**.

---

## 7. DECISION — What was decided?

Separate discovered facts from decisions.

Include:

- chosen solution;
- rejected alternatives, when explicitly discussed;
- trade-offs;
- constraints;
- owner/team when known;
- dependency or rollout implications.

Do not convert a suggestion into a decision unless the context explicitly shows that it was approved.

---

## 8. RESOLUTION / NEXT ACTIONS — What happens now?

Document:

- code change required;
- configuration change;
- migration;
- monitoring;
- test coverage;
- rollout;
- validation plan;
- follow-up technical debt.

Separate:

**Done**

**To do**

**Blocked**

**Needs validation**

---

# 6. DOCUMENT TYPES

The same skill must support at least four output modes.

## MODE A — BUG STORY

Use when the main objective is explaining a software defect.

Recommended sections:

- Title
- Context
- Expected vs Actual
- Impact
- Investigation timeline
- Technical discovery
- Root cause
- Reproduction
- Fix
- Validation
- Open questions

---

## MODE B — TECHNICAL FINDING / DISCOVERY

Use when there is an important architectural, operational or implementation discovery without necessarily being a user-facing bug.

Recommended sections:

- Title
- Context
- Finding
- Evidence
- How we discovered it
- Technical implications
- Risks
- Decision
- Recommended actions
- Open questions

---

## MODE C — INCIDENT / INVESTIGATION

Use when the chronology of an event is especially important.

Recommended sections:

- Incident summary
- Timeline
- Detection
- Symptoms
- Investigation
- Turning points
- Root cause
- Impact
- Mitigation
- Permanent fix
- Preventive actions

---

## MODE D — TECHNICAL DOCUMENTATION

Use when the goal is to teach another developer how a flow works.

Recommended sections:

- Purpose
- System context
- Actors
- Components
- End-to-end flow
- State transitions
- Important rules
- Edge cases
- Failure modes
- Example scenario
- Operational notes

---

# 7. CONTEXT FROM A FOLDER

When the user provides or references a folder of documents, treat the folder as an evidence corpus.

Before writing:

1. Identify relevant files.
2. Search for the core terms, components, errors and entities involved.
3. Compare information across files.
4. Build a chronological and causal model.
5. Identify contradictions.
6. Prefer newer explicit decisions over older assumptions when dates establish that evolution.
7. Preserve useful references to the original document/source.

Do not summarize every file. Use only the documents necessary to reconstruct the story.

When sources disagree, include a section:

**Conflict in evidence**

Explain:

- Source A says...
- Source B says...
- Current conclusion...
- What would confirm the final state...

---

# 8. CONTEXT FROM A CONVERSATION

When the source is a long conversation, do not focus only on the user's last message.

Recover relevant information from the conversation's accumulated context.

Look for:

- previous symptoms;
- earlier hypotheses;
- corrections;
- technical findings;
- architecture details;
- decisions made later;
- changes in understanding;
- explicit confirmations such as "decidimos", "confirmado", "era isso", "o problema é".

The final story should represent the evolution of the investigation.

Avoid repeating the entire conversation. Compress it into the minimum sequence necessary to understand the technical journey.

---

# 9. STORYTELLING RULES FOR DEVELOPERS

The narrative must be easy to scan.

Use:

- descriptive headings;
- short paragraphs;
- bold emphasis for important technical facts;
- code formatting for endpoints, classes, variables, feature flags and identifiers;
- code blocks for logs and stack traces;
- tables only when comparison genuinely improves comprehension;
- chronology when sequence matters.

Use professional engineering language.

Do not turn the document into creative fiction.

The "story" is the **sequence of evidence and discoveries**, not a fictional narrative.

---

# 10. REQUIRED TECHNICAL DETAIL

Whenever available, preserve concrete technical identifiers such as:

- repository;
- service;
- module;
- file path;
- class;
- function;
- endpoint;
- queue/topic;
- event name;
- database table/column;
- feature flag;
- environment variable;
- HTTP status;
- error code;
- log message;
- commit/PR/issue identifier.

Prefer:

`apps/concierge/src/conversation/infra/webhook/controllers/conversation.ts`

over:

"the conversation controller file".

---

# 11. CAUSALITY CHECK

Before finalizing, verify that the document answers these questions:

1. What was the system trying to do?
2. What was expected?
3. What actually happened?
4. How do we know?
5. What was investigated first?
6. What evidence changed the direction of the investigation?
7. What caused the failure?
8. How can another developer reproduce it?
9. What was decided?
10. What remains unresolved?

If any answer is missing, explicitly mark it as **Unknown**, **Not found in the available context**, or **Needs validation**.

---

# 12. OUTPUT QUALITY BAR

A good output should allow a developer who did not participate in the investigation to understand the issue without reading the original Slack thread, chat history or document folder.

The output should make it possible to answer quickly:

> "What happened?"
>
> "Why did it happen?"
>
> "How was this discovered?"
>
> "How do I reproduce it?"
>
> "What did we decide?"
>
> "What do I need to change?"

The documentation is successful when it reduces the need for the next developer to reconstruct the investigation from scratch.

---

# 13. DEFAULT TITLE FORMAT

Use a title that describes the technical story, not merely the symptom.

Prefer:

**[Component/Flow] — <Failure or discovery> — <Key cause or context>**

Example:

**Push Notifications — Protocols entering the general queue do not notify eligible users — notification is only generated after a new user message**

Avoid generic titles such as:

**Bug de notificação**

---

# 14. FINAL RESPONSE FORMAT

Unless the user explicitly requests another format, produce:

# <Title>

## Resumo
<2–5 sentences summarizing the complete technical story.>

## Contexto
...

## O que deveria acontecer
...

## O que aconteceu
...

## Como descobrimos
...

## Descobertas técnicas
...

## Causa raiz
...

## Como reproduzir
...

## Decisão
...

## Correção / Próximas ações
...

## Pendências / Pontos em aberto
...

## Evidências relevantes
<logs, endpoints, snippets, references when available>

---

# 15. SPECIAL RULE — ASK LESS, EXTRACT MORE

When the available context is sufficient, do not ask the user to repeat information that already exists in the conversation or documents.

Use the available evidence first.

Only request clarification when the missing information prevents a materially different conclusion and cannot be inferred safely.

When clarification is not possible, produce the best possible version and mark uncertainty explicitly.

---

# 16. SPECIAL RULE — PRESERVE EVOLUTION OF UNDERSTANDING

A technical investigation is often non-linear.

The final document must preserve meaningful changes in understanding.

Example:

**Initial hypothesis:** Socket failure.

**Evidence found:** Socket remained connected and messages continued arriving.

**Updated hypothesis:** Recipient filtering.

**Confirmation:** The protocol was filtered when `reactChat=true` and the recipient did not satisfy the visibility rule.

This is valuable technical history and should not be erased merely because the initial hypothesis was wrong.

---

# 17. SPECIAL RULE — SEPARATE FACT, INTERPRETATION AND DECISION

When a sentence mixes these concepts, rewrite it.

Bad:

> "The backend is broken and we decided to fix the queue."

Better:

**Fact:** The backend creates the queue event.

**Interpretation:** The missing notification appears to occur after queue entry.

**Decision:** Investigate and correct the notification trigger for queue entry.

---

# 18. SPECIAL RULE — NO ROOT-CAUSE THEATER

Do not force a root cause merely because the template contains a "Root cause" section.

A precise statement of uncertainty is better than a confident but unsupported explanation.

Use:

> **Root cause: Not confirmed with the available evidence.**

Then explain what has been eliminated, what remains possible, and what evidence is needed next.

---

# 19. OPTIONAL EXECUTIVE SUMMARY

When the audience includes managers, product owners, architects or multiple engineering teams, place a compact summary at the beginning containing:

- **Impact**
- **Root cause**
- **Status**
- **Decision**
- **Next action**

Do not remove the detailed technical narrative; the executive summary complements it.

---

# 20. SUCCESS CRITERIA

The skill succeeds when it can take fragmented material such as:

> "deu erro ontem, acho que foi o socket, mas depois vimos que o token existia; o Jonathan comentou que só acontece sem grupo; o Leão decidiu manter o comportamento antigo no Angular; precisa ver a flag reactChat."

and transform it into a coherent technical narrative that explains:

- the original scenario;
- the expected and actual behavior;
- the sequence of investigation;
- what hypotheses were eliminated;
- what evidence proved the relevant mechanism;
- the actual or remaining root cause;
- the reproduction path;
- the final decision;
- the required engineering actions.

The final document must be understandable by a developer who did not participate in the original discussion.
