---
name: review-board
description: >
  Implementation review orchestrator for iterative project development. Use when
  you have a Spec document with partially completed objectives and need to review
  the implementation details of the next objective. The review reads the Spec,
  existing code, and current progress, then considers deviations in completed work,
  remaining resources, and potential impacts on future objectives. Multiple roles
  collaboratively review how the objective should be concretely implemented, or
  propose alternative/compensating approaches.
  Use when: (1) reviewing implementation details before starting the next Spec objective,
  (2) existing implementation deviates from the original Spec and impact assessment is needed,
  (3) resource or technical constraints have changed and an objective's implementation
  approach needs re-evaluation, (4) user mentions "review", "review board", or
  "implementation review", (5) user invokes /review-board.
---

# Review Board — Iterative Implementation Review

For the next objective in a project Spec, collaboratively review the concrete implementation
plan considering existing code and current progress.

## Input Requirements

At review start, clarify:
1. **Spec document** location (or user provides content directly)
2. **Current progress**: which objectives are done, which is under review
3. **Project codebase**: existing implementation (auto-read from working directory)

## Execution Flow

### Phase 1: Context Building

1. Read the Spec document; understand overall goals and phase planning
2. Read existing code; understand how completed objectives were actually implemented
3. Identify deviations: differences between existing implementation and original Spec design
4. Focus on target: extract the Spec description of the objective under review
5. Forward scan: which future objectives might be affected by this implementation

Output a context summary (concise, for subsequent roles to reference):

```
## Context Summary
- Spec overview: N total objectives, X completed
- Current objective: #Y - [Objective Name]
- Deviation log: [Key differences between implementation and Spec]
- Forward impact: [Points where future objective #Z may be affected]
- Tech stack/constraints: [Current tech stack and known constraints]
```

### Phase 2: Multi-Role Implementation Review

6 roles in three groups, all focused on "how exactly to implement this objective."

**Output constraint:** Each role's output must stay under 300 words — conclusions and key points only, no expanded details. Specific test cases, detailed code design, etc. are left for the implementation phase. Groups B/C external agents must strictly follow this word limit.

#### Group A: Main Model Direct Review

**🏗️ Architect** — Evaluate from an architecture perspective:
- Can the current architecture directly support the target functionality? What structural changes are needed?
- Compatibility with existing implementation (interfaces, data models, dependencies)
- Architectural impact on future objectives (will this block future paths?)
- If the original Spec approach conflicts with current architecture, suggest adjustments

**📋 Project Manager** — Evaluate from a resource and schedule perspective:
- Are remaining time/resources sufficient to fully implement this objective per Spec?
- Is scope trimming needed (which sub-items can be deferred)?
- Dependency relationships and priority conflicts with other objectives
- If resources are insufficient, suggest phased delivery

**😈 Devil's Advocate** — Deliberately challenge assumptions in the plan:
- Are deviations in existing implementation being underestimated? Could they explode in this objective?
- Is there a simpler implementation path being overlooked?
- What happens in the worst case? What's the fallback plan?
- Could future objective requirement changes render this implementation wasted?

#### Group B: Codex Agent Review (dispatched in parallel)

Read [references/codex-prompts.md](references/codex-prompts.md) for prompt templates; dispatch via `dispatch.py`.

**💻 Development Engineer** — Concrete implementation plan: which files to change, interface design, data flow, key code logic, estimated effort.

**🧪 QA Engineer** — Test strategy: how to verify, regression risks, boundary conditions, impact on existing functionality.

#### Group C: Gemini Agent Review (dispatched on demand)

Read [references/gemini-prompts.md](references/gemini-prompts.md) for prompt templates.

**🎨 UX/Product Review** — Triggered only when the objective involves user interface or interaction flows. Evaluate UX impact, interaction consistency, integration with existing UI.

**Parallel strategy:** Groups B and C can be dispatched simultaneously. Each role uses an independent handover JSON (`.review-board-<role>.json`).

Each role output format:

```
【Role Name】
- Conclusion: Feasible / Needs Adjustment / Infeasible
- Implementation Suggestions: [concrete approach]
- Risks: [what could go wrong]
- Alternatives: [fallback if original approach is infeasible]
```

### Dispatch Method

Generate handover JSON for Group B/C roles and dispatch via `dispatch.py`:

```json
{
  "target_agent": "Codex",
  "task_id": "review-dev-engineer-01",
  "project_context": "Context summary from Phase 1",
  "primary_objective": "Role prompt + target Spec content + existing implementation key info",
  "read_files": ["spec file", "relevant code files"],
  "strict_boundaries": ["Output review opinions only — do not modify any files", "Strictly follow the review output format"]
}
```

```bash
python "<skill_dir>/scripts/dispatch.py" .review-board-<role>.json \
  --working-dir "<project_dir>" --timeout 300
```

Never call `gemini` or `codex` CLI directly. If dispatch fails, complete that role's review yourself.

### Phase 3: Implementation Decision

Consolidate all role review results into a final implementation decision.

**Consolidation principle:** Deduplicate and merge overlapping opinions across roles. If multiple roles raise the same point (e.g., "notifications need async decoupling"), it appears only once in the final plan with source roles noted — no repetition.

#### 1. Deviation Impact Analysis

How deviations between existing implementation and Spec concretely affect this objective, and what adaptation measures are needed.

#### 2. Implementation Plan

Provide a clear implementation path:
- List of files to modify/create
- Key interface and data flow design
- Implementation steps (in order)
- Estimated effort

If the original Spec approach is infeasible, provide:
- Reason (technical limitation / insufficient resources / conflicts with existing implementation)
- Alternative approach and its trade-offs
- Impact assessment on future objectives
- Compensating measures (how to make up for it in later iterations)

#### 3. Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| ... | High/Medium/Low | ... |

#### 4. Disputed Decision Points

Areas where roles disagree, requiring team confirmation before proceeding. For each disputed point, list:
- What the disagreement is about
- Each side's position (with source role noted)
- Recommended option and rationale

#### 5. Impact on Future Objectives

How this implementation choice affects subsequent objectives in the Spec, and whether future objective designs need preemptive adjustment.

#### 6. Action Items

- [ ] Concrete next steps (directly executable)
- [ ] ...

## Cleanup

After review is complete, delete all `.review-board-*.json` temporary files.
