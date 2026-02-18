# Agent Skills

A collection of custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), extending its capabilities through specialized agent workflows.

## What Are Skills?

Skills are reusable prompt-based extensions that give Claude Code domain-specific knowledge, workflows, and tool integrations. They live in your `~/.claude/skills/` directory and are automatically available in all Claude Code sessions.

## Available Skills

| Skill | Description |
|-------|-------------|
| [cli-crew](./cli-crew/) | Multi-agent orchestrator that delegates tasks to Gemini-CLI and Codex-CLI via a structured JSON handover protocol |
| [ios-style-designer](./ios-style-designer/) | Architects web interfaces following Apple's Human Interface Guidelines — glassmorphism, SF Pro typography, 8pt grid, adaptive Light/Dark mode |
| [review-board](./review-board/) | Implementation review orchestrator for iterative project development — multi-role review of Spec objectives considering existing code and progress |

## Installation

Copy the desired skill folder into your Claude Code skills directory:

```bash
# Linux / macOS
cp -r cli-crew ~/.claude/skills/cli-crew

# Windows
xcopy /E /I cli-crew %USERPROFILE%\.claude\skills\cli-crew
```

Once installed, the skill is automatically loaded by Claude Code. You can invoke it by name (e.g., `/cli-crew`) or let Claude route to it based on your request.

## Project Structure

```
agent-skills/
├── README.md
├── cli-crew/              # Multi-agent orchestrator skill
│   ├── SKILL.md
│   ├── README.md
│   ├── references/        # Routing rules & JSON schema
│   └── scripts/           # Dispatcher + CLI wrappers
├── ios-style-designer/    # Apple HIG web design skill
│   ├── SKILL.md
│   └── README.md
└── review-board/          # Iterative implementation review skill
    ├── SKILL.md
    ├── references/        # Role-specific prompts (Codex, Gemini)
    └── scripts/           # Dispatcher + CLI wrappers
```

## Contributing

Feel free to open issues or submit PRs to improve existing skills or add new ones.

## License

MIT
