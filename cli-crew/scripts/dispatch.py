#!/usr/bin/env python3
"""
dispatch.py - CLI Teams Handover Dispatcher

Reads a JSON handover payload, constructs a structured prompt,
and dispatches it to the appropriate CLI agent (Gemini or Codex).

Usage:
    python dispatch.py <handover.json> [--scripts-dir <path>] [--working-dir <path>]

The handover JSON schema:
{
    "target_agent": "Gemini" | "Codex",
    "task_id": "unique_id",
    "project_context": "Brief project state summary",
    "primary_objective": "What needs to be achieved",
    "read_files": ["file1.tsx", "file2.css"],
    "write_target": "output_file.tsx",
    "strict_boundaries": ["constraint 1", "constraint 2"]
}
"""

import json
import os
import sys
import subprocess
import tempfile
import argparse
from pathlib import Path


def load_handover(json_path: str) -> dict:
    """Load and validate the handover JSON payload."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required = ["target_agent", "task_id", "primary_objective"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"Error: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    if data["target_agent"] not in ("Gemini", "Codex"):
        print(f"Error: target_agent must be 'Gemini' or 'Codex', got '{data['target_agent']}'", file=sys.stderr)
        sys.exit(1)

    return data


def build_prompt(data: dict) -> str:
    """Convert handover JSON into a structured text prompt for the target agent."""
    lines = []

    lines.append(f"## Task: {data['task_id']}")
    lines.append("")

    if data.get("project_context"):
        lines.append(f"### Context")
        lines.append(data["project_context"])
        lines.append("")

    lines.append("### Objective")
    lines.append(data["primary_objective"])
    lines.append("")

    if data.get("read_files"):
        lines.append("### Files to Read")
        for f in data["read_files"]:
            lines.append(f"- {f}")
        lines.append("")

    if data.get("write_target"):
        lines.append(f"### Write Output To")
        lines.append(data["write_target"])
        lines.append("")

    if data.get("strict_boundaries"):
        lines.append("### Constraints (MUST follow)")
        for b in data["strict_boundaries"]:
            lines.append(f"- {b}")
        lines.append("")

    return "\n".join(lines)


def resolve_script(agent: str, scripts_dir: str) -> str:
    """Resolve the path to the agent's cmd script."""
    name_map = {"Gemini": "gemini-run.cmd", "Codex": "codex-run.cmd"}
    script = os.path.join(scripts_dir, name_map[agent])
    if not os.path.isfile(script):
        print(f"Error: Script not found: {script}", file=sys.stderr)
        sys.exit(1)
    return script


def main():
    parser = argparse.ArgumentParser(description="CLI Teams Handover Dispatcher")
    parser.add_argument("handover_json", help="Path to the handover JSON file")
    parser.add_argument("--scripts-dir", default=None,
                        help="Directory containing gemini-run.cmd and codex-run.cmd")
    parser.add_argument("--working-dir", default=".",
                        help="Working directory for the agent")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Timeout in seconds (default: 600)")
    args = parser.parse_args()

    data = load_handover(args.handover_json)
    prompt_text = build_prompt(data)

    # Default scripts dir: same directory as this script (cmd files are bundled here)
    scripts_dir = args.scripts_dir or os.path.dirname(os.path.abspath(__file__))

    script_path = resolve_script(data["target_agent"], scripts_dir)

    # Write prompt to temp file (avoids CMD 8191-char limit)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", prefix=f"cli-crew-{data['task_id']}-",
        delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(prompt_text)
        prompt_file = tmp.name

    try:
        cmd = [script_path, "-f", prompt_file, "-d", args.working_dir,
               "-t", str(args.timeout)]

        print(f"=== Dispatching to {data['target_agent']} ===", file=sys.stderr)
        print(f"Task: {data['task_id']}", file=sys.stderr)
        print(f"Script: {script_path}", file=sys.stderr)
        print(f"Working dir: {args.working_dir}", file=sys.stderr)
        print("---", file=sys.stderr)

        result = subprocess.run(cmd, shell=True)
        sys.exit(result.returncode)
    finally:
        if os.path.exists(prompt_file):
            os.remove(prompt_file)


if __name__ == "__main__":
    main()
