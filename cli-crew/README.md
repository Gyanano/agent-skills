# cli-crew

Multi-agent orchestrator skill for Claude Code. Delegates tasks to specialized external CLI agents — **Gemini-CLI** for UI/UX work and **Codex-CLI** for logic/debugging — using a structured JSON handover protocol.

## How It Works

Claude acts as **Project Manager & Architect**:

1. Analyzes the user's request and breaks it into sub-tasks
2. Routes each sub-task to the best-fit agent
3. Generates a JSON handover payload and dispatches via CLI wrappers
4. Reviews output, enforces constraints, and integrates results

## Agent Routing

| Agent | Domain | Trigger Examples |
|-------|--------|-----------------|
| @Gemini | UI/UX, styling, visual design, multimodal | "make it look good", component design, layout |
| @Codex | Logic, bugs, algorithms, strict refactoring | "fix this bug", algorithm work, precise edits |
| @Claude | Architecture, planning, integration | Task breakdown, system design, assembly |

## Prerequisites

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed and configured
- [Codex CLI](https://github.com/openai/codex) installed and configured
- Python 3.10+

## File Structure

```
cli-crew/
├── SKILL.md                    # Skill definition (loaded by Claude Code)
├── README.md                   # This file
├── references/
│   └── routing-protocol.md     # Detailed routing rules & JSON schema
└── scripts/
    ├── dispatch.py             # Python dispatcher
    ├── gemini-run.cmd          # Gemini CLI wrapper (Windows)
    └── codex-run.cmd           # Codex CLI wrapper (Windows)
```
