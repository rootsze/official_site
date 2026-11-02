#!/usr/bin/env python3
"""
GitHub Agent Helper CLI
Coordinates state machine transitions, issue ranking, and configuration for the ATB GitHub automation series.
"""

import argparse
import datetime
import json
import os
import re
import sys
import tempfile
from pathlib import Path

STATE_FILE = Path(".github-agent-state.yml")
CONFIG_FILE = Path(".github-agent.yml")

def load_yaml(path: Path):
    if not path.exists():
        return {}
    try:
        import yaml
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"Warning: Failed to load {path}: {e}", file=sys.stderr)
        return {}

def save_yaml(path: Path, data: dict):
    try:
        import yaml
        tmp_fd, tmp_path = tempfile.mkstemp(dir=path.parent or ".", suffix=".tmp")
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        os.replace(tmp_path, path)
    except Exception as e:
        print(f"Error saving {path}: {e}", file=sys.stderr)
        sys.exit(1)

def get_state():
    data = load_yaml(STATE_FILE)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def set_state(state: str, key: str = None, value: str = None, json_data: str = None):
    data = load_yaml(STATE_FILE)
    data["state"] = state
    data["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if key and value is not None:
        data[key] = value
    if json_data:
        try:
            extra = json.loads(json_data)
            data.update(extra)
        except Exception as e:
            print(f"Error parsing json_data: {e}", file=sys.stderr)
            sys.exit(1)
    save_yaml(STATE_FILE, data)
    print(f"State updated to: {state}")

def check_config():
    if not CONFIG_FILE.exists():
        print("missing")
        sys.exit(1)
    cfg = load_yaml(CONFIG_FILE)
    gh = cfg.get("github", {})
    if not gh.get("owner") or not gh.get("repo"):
        print("incomplete")
        sys.exit(1)
    print("exists")

def status_table(input_stream):
    raw = input_stream.read()
    if not raw.strip():
        print("No open issues.")
        return
    try:
        issues = json.loads(raw)
    except Exception as e:
        print(f"Error parsing issues JSON: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"{'#':<6} | {'Title':<50} | {'Labels':<35} | {'Status'}")
    print("-" * 110)
    for issue in issues:
        num = f"#{issue.get('number')}"
        title = (issue.get('title') or '')[:48]
        labels = [l.get("name", "") if isinstance(l, dict) else str(l) for l in (issue.get("labels") or [])]
        label_str = ", ".join(labels)[:33]
        status = "in-progress" if "in-progress" in labels else ("in-pr" if "in-pr" in labels else "open")
        print(f"{num:<6} | {title:<50} | {label_str:<35} | {status}")

def rank_issues(input_stream, concurrency_mode="serial"):
    raw = input_stream.read()
    if not raw.strip():
        print("[]")
        return

    try:
        issues = json.loads(raw)
    except Exception as e:
        print(f"Error parsing issues JSON: {e}", file=sys.stderr)
        sys.exit(1)

    cfg = load_yaml(CONFIG_FILE)
    state = load_yaml(STATE_FILE)
    labels_cfg = cfg.get("labels", {})
    p_high = labels_cfg.get("priority_high", "priority: high").lower()
    bug_label = labels_cfg.get("bug", "bug").lower()

    open_numbers = {i.get("number") for i in issues if i.get("number") is not None}
    active_epic = state.get("active_epic") or {}
    active_epic_num = active_epic.get("number")

    # 1. Serial Gate
    if concurrency_mode == "serial":
        in_progress = []
        for issue in issues:
            labels = [
                l.get("name", "").lower() if isinstance(l, dict) else str(l).lower()
                for l in (issue.get("labels") or [])
            ]
            if "in-progress" in labels:
                in_progress.append(issue)

        if in_progress:
            active = in_progress[0]
            print(
                f"SERIAL_GUARD_BLOCKED: Issue #{active.get('number')} (\"{active.get('title')}\") is already in-progress.",
                file=sys.stderr,
            )
            print("[]")
            sys.exit(0)

    # 2. Filter backlog
    candidates = []
    for issue in issues:
        labels = [
            l.get("name", "").lower() if isinstance(l, dict) else str(l).lower()
            for l in (issue.get("labels") or [])
        ]
        # Skip Epics
        if "epic" in labels:
            continue
        # Skip already in-pr
        if "in-pr" in labels:
            continue
        # In parallel mode, also skip existing in-progress
        if concurrency_mode == "parallel" and "in-progress" in labels:
            continue

        body = issue.get("body") or ""
        # Check DAG dependencies
        deps_match = re.search(r"\*\*Depends On\*\*:\s*([^\n\r]+)", body)
        is_blocked = False
        if deps_match:
            dep_text = deps_match.group(1).strip()
            if dep_text and dep_text.lower() != "none":
                # Find all #X references
                dep_ids = [int(m) for m in re.findall(r"#(\d+)", dep_text)]
                for dep_id in dep_ids:
                    if dep_id in open_numbers:
                        is_blocked = True
                        break
        if is_blocked:
            continue

        candidates.append(issue)

    def sort_key(issue):
        labels = [
            l.get("name", "").lower() if isinstance(l, dict) else str(l).lower()
            for l in (issue.get("labels") or [])
        ]
        body = issue.get("body") or ""
        # Is part of active epic
        is_active_epic = 0
        if active_epic_num:
            epic_match = re.search(r"Parent Epic[\*\s:]*#(\d+)", body)
            if epic_match and int(epic_match.group(1)) == active_epic_num:
                is_active_epic = -1

        is_high = 0 if any("high" in l for l in labels) else 1
        is_bug = 0 if bug_label in labels else 1

        # Check sequence step
        step_match = re.search(r"Step\s+(\d+)\s+of", body)
        step_num = int(step_match.group(1)) if step_match else 999
        num = issue.get("number") if issue.get("number") is not None else sys.maxsize

        return (is_active_epic, is_high, is_bug, step_num, num)

    ranked = sorted(candidates, key=sort_key)
    print(json.dumps(ranked, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="GitHub Agent Helper")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("check-config")
    subparsers.add_parser("get-state")
    subparsers.add_parser("status-table")

    set_state_p = subparsers.add_parser("set-state")
    set_state_p.add_argument("--state", required=True, help="State name")
    set_state_p.add_argument("--key", help="State key to update")
    set_state_p.add_argument("--value", help="State value to update")
    set_state_p.add_argument("--json-data", help="JSON string of additional state keys")

    rank_p = subparsers.add_parser("rank-issues")
    rank_p.add_argument("--concurrency-mode", default="serial", choices=["serial", "parallel"])

    args = parser.parse_args()
    if args.command == "check-config":
        check_config()
    elif args.command == "get-state":
        get_state()
    elif args.command == "status-table":
        status_table(sys.stdin)
    elif args.command == "set-state":
        set_state(args.state, args.key, args.value, args.json_data)
    elif args.command == "rank-issues":
        rank_issues(sys.stdin, args.concurrency_mode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
