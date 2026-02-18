# review-board

Implementation review orchestrator for iterative project development. When you have a Spec document with partially completed objectives, this skill runs a multi-role collaborative review to determine how the next objective should be concretely implemented — considering existing code, deviations, and future impact.

## How It Works

Claude acts as **Review Facilitator**, coordinating 6 specialized roles across three groups:

1. **Phase 1 — Context Building**: Reads the Spec, existing code, and progress; identifies deviations and forward impacts
2. **Phase 2 — Multi-Role Review**: 6 roles evaluate the objective from different angles (architecture, PM, devil's advocate, dev engineer, QA, UX)
3. **Phase 3 — Implementation Decision**: Consolidates all opinions into a final implementation plan with risks, alternatives, and action items

## Review Roles

| Group | Role | Focus |
|-------|------|-------|
| A (Claude) | Architect | Architecture fit, structural changes, future-path impact |
| A (Claude) | Project Manager | Resource/schedule feasibility, scope trimming, phased delivery |
| A (Claude) | Devil's Advocate | Challenge assumptions, find simpler paths, worst-case fallbacks |
| B (Codex) | Dev Engineer | Concrete file changes, interface design, data flow, effort estimate |
| B (Codex) | QA Engineer | Test strategy, regression risks, boundary conditions |
| C (Gemini) | UX/Product | UI/interaction impact (triggered only when objective involves UI) |

## When It Triggers

- Reviewing implementation details before starting the next Spec objective
- Existing implementation deviates from the original Spec
- Resource or technical constraints have changed
- User mentions "review", "review board", or "implementation review"
- User invokes `/review-board`

## Prerequisites

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed and configured
- [Codex CLI](https://github.com/openai/codex) installed and configured
- Python 3.10+

## File Structure

```
review-board/
├── SKILL.md                       # Skill definition (loaded by Claude Code)
├── README.md                      # This file
├── references/
│   ├── codex-prompts.md           # Prompt templates for Dev Engineer & QA roles
│   └── gemini-prompts.md          # Prompt templates for UX/Product role
└── scripts/
    ├── dispatch.py                # Python dispatcher
    ├── gemini-run.cmd             # Gemini CLI wrapper (Windows)
    └── codex-run.cmd              # Codex CLI wrapper (Windows)
```
