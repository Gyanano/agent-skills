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

Windows compatibility note:
    Claude Code always executes commands in a Bash shell (Git Bash on Windows),
    even when launched from CMD. This dispatcher explicitly uses cmd.exe /c to
    run .cmd scripts, bypassing the Bash shell entirely.
"""

import json
import os
import sys
import subprocess
import tempfile
import argparse
import shutil
import platform
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"


def load_handover(json_path: str) -> dict:
    """Load and validate the handover JSON payload."""
    path = Path(json_path)
    if not path.is_file():
        print(f"[DISPATCH_ERROR] Handover file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[DISPATCH_ERROR] Invalid JSON in {json_path}: {e}", file=sys.stderr)
        sys.exit(1)

    required = ["target_agent", "task_id", "primary_objective"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"[DISPATCH_ERROR] Missing required fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    if data["target_agent"] not in ("Gemini", "Codex"):
        print(f"[DISPATCH_ERROR] target_agent must be 'Gemini' or 'Codex', got '{data['target_agent']}'", file=sys.stderr)
        sys.exit(1)

    return data


def build_prompt(data: dict) -> str:
    """Convert handover JSON into a structured text prompt for the target agent."""
    lines = []

    lines.append(f"## Task: {data['task_id']}")
    lines.append("")

    if data.get("project_context"):
        lines.append("### Context")
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
        lines.append("### Write Output To")
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
        print(f"[DISPATCH_ERROR] Script not found: {script}", file=sys.stderr)
        sys.exit(1)
    return script


def check_cli_available(agent: str) -> bool:
    """Pre-flight check: is the target CLI tool installed and on PATH?"""
    cli_name = "gemini" if agent == "Gemini" else "codex"
    # On Windows, also check for .cmd variant
    names_to_check = [cli_name]
    if IS_WINDOWS:
        names_to_check.append(f"{cli_name}.cmd")

    for name in names_to_check:
        if shutil.which(name):
            return True
    return False


def to_windows_path(p: str) -> str:
    """Convert a potentially mixed/POSIX path to a Windows-native path.

    Git Bash may pass paths like /c/Users/... or C:/Users/... — both need
    to become C:\\Users\\... for cmd.exe to handle them correctly.
    """
    if not IS_WINDOWS:
        return p
    # Handle MSYS/Git Bash /c/... style paths
    if len(p) >= 3 and p[0] == "/" and p[1].isalpha() and p[2] == "/":
        p = f"{p[1].upper()}:{p[2:]}"
    return p.replace("/", "\\")


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

    # Normalize paths for Windows (Git Bash may pass POSIX-style paths)
    handover_path = to_windows_path(args.handover_json)
    working_dir = to_windows_path(args.working_dir)

    data = load_handover(handover_path)

    # Pre-flight: check if the target CLI is installed
    if not check_cli_available(data["target_agent"]):
        cli_name = "gemini" if data["target_agent"] == "Gemini" else "codex"
        print(f"[DISPATCH_ERROR] {data['target_agent']} CLI ('{cli_name}') is not installed or not on PATH.", file=sys.stderr)
        print(f"[DISPATCH_ERROR] Install it first, then retry.", file=sys.stderr)
        sys.exit(1)

    prompt_text = build_prompt(data)

    # Default scripts dir: same directory as this script (cmd files are bundled here)
    scripts_dir = args.scripts_dir or os.path.dirname(os.path.abspath(__file__))
    scripts_dir = to_windows_path(scripts_dir)

    script_path = resolve_script(data["target_agent"], scripts_dir)

    # Write prompt to temp file (avoids CMD 8191-char limit)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", prefix=f"cli-crew-{data['task_id']}-",
        delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(prompt_text)
        prompt_file = tmp.name

    try:
        print(f"=== Dispatching to {data['target_agent']} ===", file=sys.stderr)
        print(f"Task: {data['task_id']}", file=sys.stderr)
        print(f"Script: {script_path}", file=sys.stderr)
        print(f"Working dir: {working_dir}", file=sys.stderr)
        print(f"Platform: {platform.system()} | Shell override: {'cmd.exe' if IS_WINDOWS else 'native'}", file=sys.stderr)
        print("---", file=sys.stderr)

        if IS_WINDOWS:
            # CRITICAL: Claude Code runs in Bash (Git Bash) on Windows.
            # .cmd files MUST be executed via cmd.exe, not Bash.
            # We explicitly invoke cmd.exe /c to bypass the Bash shell.
            cmd = [
                "cmd.exe", "/c",
                script_path,
                "-f", prompt_file,
                "-d", working_dir,
                "-t", str(args.timeout),
            ]
            # shell=False so subprocess does NOT route through Bash
            result = subprocess.run(cmd, shell=False)
        else:
            # On Linux/macOS, run the script directly
            cmd = [script_path, "-f", prompt_file, "-d", working_dir,
                   "-t", str(args.timeout)]
            result = subprocess.run(cmd, shell=False)

        if result.returncode != 0:
            print(f"[DISPATCH_ERROR] {data['target_agent']} exited with code {result.returncode}", file=sys.stderr)

        sys.exit(result.returncode)

    except FileNotFoundError as e:
        print(f"[DISPATCH_ERROR] Could not execute script: {e}", file=sys.stderr)
        print(f"[DISPATCH_ERROR] This usually means cmd.exe or the script was not found.", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"[DISPATCH_ERROR] OS error during dispatch: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            if os.path.exists(prompt_file):
                os.remove(prompt_file)
        except OSError:
            pass


if __name__ == "__main__":
    main()
