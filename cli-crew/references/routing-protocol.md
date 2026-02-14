# Agent Routing & Handover Protocol

## Agent Roster

### @Gemini -- Visual & UI Expert
- **Domain:** Frontend UI/UX design, CSS/Tailwind styling, layout, multimodal tasks
- **Trigger:** Aesthetic standards, modern frontend components, complex visual layouts
- **Style:** Provide structural skeleton, grant high creative freedom
- **Script:** `gemini-run.cmd -f <prompt_file> -d <working_dir>`

### @Codex -- Stabilizer & Debugger
- **Domain:** Precise logic, algorithms, bug hunting, targeted fixes
- **Trigger:** Core logic, complex bugs, strict refactoring (untouched code MUST NOT change)
- **Style:** Rigid, unambiguous single-point prompts. Does exactly as told.
- **Script:** `codex-run.cmd -f <prompt_file> -d <working_dir>`

### @Claude -- Architect & PM (YOU)
- **Domain:** Architecture, system design, task breakdown, final assembly/integration
- **Red line:** NEVER over-engineer or add unrequested features. Stick to scope.

## Handover JSON Schema

```json
{
  "target_agent": "Gemini | Codex",
  "task_id": "unique_id_for_tracking",
  "project_context": "Brief 1-2 sentence summary of current project state",
  "primary_objective": "What exactly needs to be achieved",
  "read_files": ["path/to/file1.tsx", "path/to/file2.css"],
  "write_target": "path/to/output_file.tsx",
  "strict_boundaries": [
    "DO NOT modify the authentication logic",
    "Use Tailwind exclusively",
    "Return ONLY the modified function, not the whole file"
  ]
}
```

### Field Rules
- `target_agent` (required): Must be "Gemini" or "Codex"
- `task_id` (required): Unique identifier, format: `<agent>-<feature>-<seq>` (e.g., `gemini-navbar-01`)
- `project_context` (optional): 1-2 sentences max
- `primary_objective` (required): Single clear deliverable
- `read_files` (optional): Files the agent must read before working
- `write_target` (optional): Where the agent should write output
- `strict_boundaries` (required for Codex, recommended for Gemini): Hard constraints

## Routing Decision Matrix

| Signal | Route to | Reason |
|--------|----------|--------|
| "make it look good", styling, layout, CSS | @Gemini | Visual domain |
| Component design, responsive UI, animations | @Gemini | UI/UX expertise |
| Image analysis, multimodal input | @Gemini | Multimodal capability |
| Fix bug, debug, "why does X fail" | @Codex | Precision debugging |
| Algorithm, data structure, core logic | @Codex | Logic execution |
| Refactor without side effects | @Codex | Strict boundaries |
| Architecture, system design, integration | @Claude | PM domain |
| Task breakdown, planning | @Claude | Orchestration |
| Multi-agent coordination | @Claude | PM role |
