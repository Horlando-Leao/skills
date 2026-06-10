---
name: semantic-commits
description: "Analyzes staged files, groups them semantically by logical relationship, and creates separate conventional commits for each group. Ideal when you have many staged files that should be split into multiple meaningful commits."
---

### Workflow

#### Step 1 - Gather context

Run in parallel:
- `git log --oneline -5` — recent commit style.
- `git diff --cached --stat` — staged files overview.

If no staged files, inform the user and stop.

Only read `git diff --cached -- <file>` for specific files when grouping is ambiguous from the stat alone. Do NOT read the full `git diff --cached` upfront.

#### Step 2 - Analyze and group

Group files by:
- **Logical relationship**: same feature/bug/purpose (e.g., controller + service + test).
- **Module proximity**: same module/directory changed for the same reason.
- **Type of change**: separate functional (feat, fix, refactor) from support (docs, chore, style, test, ci, build).

Rules:
- Each file belongs to exactly one group.
- Prefer fewer cohesive groups over granular ones.
- If all files belong together, propose a single group.
- Each group must have a single purpose expressible in one commit message.

#### Step 3 - Present groups for confirmation

Format:

```
## Proposed Commit Groups

### Group 1: <short description>
Type: <feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert>
Scope: <optional>
Files:
  - path/to/file1
  - path/to/file2
```

Ask: "Approve these groups? You can request changes (merge, split, move files, rename) or confirm to proceed."

**Do NOT proceed until explicit confirmation.**

#### Step 4 - Execute commits

1. Unstage everything once: `git reset HEAD -- .`
2. For each group, in order:
   - `git add <files>`
   - `git commit -m "type(scope): description" -m "- Change one\n- Change two"`
3. After all commits, run `git log --oneline -<n>` to show the result.

### Commit Message Format

**Header (required):** `type(scope): description`
- `type`: `feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert`
- `scope`: optional, module/area affected
- `description`: imperative mood ("add", not "added")
- **Max 69 characters** (GitHub truncation limit). If exceeded: shorten the description first, then drop the scope if still too long.

**Body (required):** bullet list starting with `- `, at least one bullet.

**Footer (optional):** `BREAKING CHANGE: ...` or issue refs.

Never include AI attribution or co-authorship metadata.

For examples, read `references/examples.md` only if needed.
