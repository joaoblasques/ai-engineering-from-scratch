# Two-Claude Review Protocol

**Purpose:** Structured cross-check between Claude Code (Builder) and Claude.ai (Reviewer) for the *AI Engineering from Scratch* course.

## Roles

| Role | Tool | Responsibility |
|------|------|----------------|
| **Builder** | Claude Code (CLI, in repo) | Implement lesson, run tests, write `handoff.md` |
| **Reviewer** | Claude.ai (this chat project) | Audit handoff, run checklist, return verdict |
| **Curator** | Reviewer (post-approval) | Generate `kb-entry.md` content for user to dump into local llm-wiki-system raw/_inbox/ |

## Per-Lesson Flow

1. **Start lesson** — Builder reads `phases/XX/NN-lesson/docs/en.md`, implements code in the lesson's recommended language.
2. **Validate** — Builder runs the lesson's verification script (or writes one).
3. **Handoff** — Builder writes `.two-claude-review/handoffs/PHASE-LESSON-handoff.md` using `templates/handoff-template.md`.
4. **Paste to Reviewer** — User copies handoff content into Claude.ai chat. Reviewer may request specific code excerpts.
5. **Review** — Reviewer runs checklist, writes `.two-claude-review/reviews/PHASE-LESSON-review.md` using `templates/review-template.md`.
6. **Verdict:**
   - `APPROVED` → go to step 7
   - `NEEDS-REVISION` → Builder addresses action items, returns to step 3
   - `NEEDS-DISCUSSION` → user mediates between the two
7. **KB export** — Reviewer generates `kb-entry.md` content using `templates/kb-export-template.md` and returns it in chat. User dumps it into ~/Dev/second-brain/03_Resources/llm-wiki-system/raw/_inbox/ as `NN-MM-<topic>-kb.md` (where NN-MM is phase-lesson). User files/processes it into corpus/ later via the llm-wiki-system itself. KB entries are NOT uploaded to any Claude project.
8. **Next lesson.**

## Review checklist (Reviewer applies this)

1. **Correctness** — Does the code actually do what the handoff claims?
2. **Conceptual integrity** — Is the explanation accurate? Any misconceptions?
3. **First-principles depth** — Built from scratch as the course mandates, or framework shortcuts?
4. **Cross-lesson links** — Connections to prior lessons identified? Foreshadowing later ones?
5. **Test rigor** — Validation sufficient? Edge cases considered?
6. **Open question quality** — Are the unknowns the *right* unknowns?
7. **Artifact reusability** — Produced prompts/skills/agents portable and well-formed?

## Directory layout (in repo, gitignored)

```
.two-claude-review/
├── REVIEW_PROTOCOL.md              # this file
├── templates/
│   ├── handoff-template.md
│   ├── review-template.md
│   └── kb-export-template.md
├── handoffs/
│   └── 00-01-handoff.md           # Phase 00, Lesson 01
└── reviews/
    └── 00-01-review.md
```

## Why this works

- **Builder is biased toward "it runs."** Reviewer catches conceptual sloppiness Builder rationalized away.
- **Reviewer has no execution context.** Forces Builder to write clear handoffs — a learning artifact in itself.
- **KB export is post-approval only.** Nothing half-baked enters the Corpus KB.
