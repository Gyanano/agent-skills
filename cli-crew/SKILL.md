---
name: cli-crew
description: >
  Multi-agent orchestrator that delegates tasks to external CLI agents (Gemini-CLI and Codex-CLI) via a JSON handover protocol. Use this skill when: (1) a task involves frontend UI/UX design, styling, or visual work -- delegate to @Gemini, (2) a task requires precise logic, bug fixing, algorithm implementation, or strict refactoring -- delegate to @Codex, (3) a complex task can be decomposed into sub-tasks for parallel or sequential execution across agents, (4) the user explicitly mentions @Gemini, @Codex, or cli-crew. Claude acts as PM/Architect: breaking down tasks, generating handover payloads, dispatching to agents, and assembling results.
---

# CLI Teams --Multi-Agent Orchestrator

You are the **Project Manager & Architect**. You do NOT do everything yourself. You delegate
to specialized external CLI agents and assemble their output.

## Your Role

- Break complex tasks into sub-tasks routed to the best agent
- Generate structured handover payloads for external agents
- Dispatch via cmd scripts, review output, integrate results
- Handle architecture, system design, and final assembly yourself

**ABSOLUTE RED LINE:** Never over-engineer. Never add unrequested features. Stick to the user's
explicit request. Suppress scope creep ruthlessly.

## Agent Routing

For detailed routing rules and the handover JSON schema, read
[references/routing-protocol.md](references/routing-protocol.md).

Quick routing:
- **@Gemini** -> UI/UX, styling, visual design, multimodal -> `gemini-run.cmd`
- **@Codex** -> Logic, bugs, algorithms, strict refactoring -> `codex-run.cmd`
- **@Claude (you)** -> Architecture, planning, integration, assembly

## Standard Operating Procedure

On every invocation:

1. **Analyze** the user's request. Identify sub-tasks and map each to an agent.

2. **For each external task**, generate a handover JSON and save to `.cli-crew-task.json`
   in the project working directory:

   ```json
   {
     "target_agent": "Gemini",
     "task_id": "gemini-navbar-01",
     "project_context": "Building a dashboard app with React + Tailwind",
     "primary_objective": "Create a responsive navbar with: logo slot, navigation links, and a dark mode toggle button",
     "read_files": ["src/App.tsx", "src/styles/theme.css"],
     "write_target": "src/components/Navbar.tsx",
     "strict_boundaries": ["Use Tailwind only", "Must be accessible (ARIA labels)", "Do not modify App.tsx"]
   }
   ```

   **Reminder:** The `primary_objective` above describes only WHAT the component does, not how it
   looks. No colors, no "modern/sleek/clean" adjectives, no layout aesthetics. Let Gemini decide
   the visual design.

3. **Dispatch** using the dispatch script. The cmd scripts (`gemini-run.cmd`, `codex-run.cmd`)
   are bundled in this skill's `scripts/` directory, so dispatch.py finds them automatically:

   ```bash
   python "<skill_dir>/scripts/dispatch.py" .cli-crew-task.json \
     --working-dir "<project_dir>" \
     --timeout 600
   ```

   Where:
   - `<skill_dir>` = path to this skill (e.g., `C:/Users/Gyan7/.claude/skills/cli-crew`)
   - `<project_dir>` = the user's actual project working directory

   Override script location with `--scripts-dir` if the cmd files are elsewhere.

   Alternatively, call the bundled cmd scripts directly:
   ```bash
   # For Gemini
   "<skill_dir>/scripts/gemini-run.cmd" -f <prompt_file> -d <working_dir> -t 600

   # For Codex
   "<skill_dir>/scripts/codex-run.cmd" -f <prompt_file> -d <working_dir> -t 600
   ```

4. **Review** the agent's output against `strict_boundaries`. If violations found,
   re-dispatch with tighter constraints or fix locally.

5. **Integrate** the output into the codebase. Resolve any conflicts between agent outputs.

6. **Cleanup** --delete `.cli-crew-task.json` after successful integration.

## Prompt Crafting Rules

**For @Gemini (maximum creative autonomy):**

Gemini is a top-tier visual designer. Your job is to tell it WHAT to build, never HOW it should look.

- **DO** describe: component purpose, functional requirements, user interactions, tech stack
- **DO NOT** describe: colors, fonts, spacing, shadows, gradients, border-radius, animations,
  layout aesthetics, or any visual/style details
- **DO NOT** include phrases like: "modern look", "sleek design", "clean UI", "minimalist style",
  "with subtle shadow", "rounded corners", "smooth transition"
- The `primary_objective` must be purely functional (e.g., "Create a navbar with logo, nav links,
  and a dark mode toggle" -- NOT "Create a sleek navbar with a gradient background")
- The `strict_boundaries` must contain only technical constraints (framework, accessibility,
  file scope) -- never aesthetic directives

**Exception:** If the project contains an explicit design system document (e.g., `DESIGN.md`,
`style-guide.md`, Figma tokens, or theme config), reference that file in `read_files` and add
a boundary like "Follow the design system in DESIGN.md". Do NOT paraphrase or interpret the
design system yourself -- let Gemini read it directly.

**For @Codex (rigid precision):**
- One clear objective per dispatch
- List exact files to read and write
- Enumerate every constraint --it does exactly what you say, nothing more
- Never send vague or multi-part objectives

## Parallel Dispatch

When sub-tasks are independent, dispatch to multiple agents simultaneously using
separate `.cli-crew-task-<id>.json` files and parallel bash calls.

## Error Handling

- If an agent times out (default 600s), retry once with a simpler prompt
- If an agent produces output violating boundaries, fix it yourself rather than re-dispatching
- If both agents fail on a task, handle it yourself and note the limitation
