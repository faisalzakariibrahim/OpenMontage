"""Summarize a headless Claude Code run (stream-json) as Markdown for $GITHUB_STEP_SUMMARY.

  python scripts/agent_run_summary.py <run.jsonl> [stderr.log] [--title "Agent result"]

Shows the outcome, turns, cost, duration, final message, the last few things the agent said,
permission denials, and the stderr tail, so a failed run explains itself on the Summary page.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_events(path: Path) -> list[dict]:
    events = []
    if not path.exists():
        return events
    for line in path.read_text(errors="ignore").splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return events


def assistant_texts(events: list[dict]) -> list[str]:
    texts = []
    for e in events:
        if e.get("type") != "assistant":
            continue
        for block in (e.get("message") or {}).get("content") or []:
            if block.get("type") == "text" and block.get("text", "").strip():
                texts.append(block["text"].strip())
    return texts


def tool_errors(events: list[dict]) -> list[str]:
    errors = []
    for e in events:
        if e.get("type") != "user":
            continue
        for block in (e.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_result" and block.get("is_error"):
                content = block.get("content")
                if isinstance(content, list):
                    content = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
                errors.append(str(content)[:300])
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("stderr", nargs="?")
    ap.add_argument("--title", default="Agent result")
    args = ap.parse_args()

    events = load_events(Path(args.jsonl))
    result = next((e for e in reversed(events) if e.get("type") == "result"), None)
    print(f"## {args.title}\n")
    if result:
        print(f"- **Outcome:** {result.get('subtype')} (error: {result.get('is_error')})")
        print(f"- **Turns:** {result.get('num_turns')}  ·  **Claude cost:** ${result.get('total_cost_usd') or 0:.2f}")
        print(f"- **Duration:** {round((result.get('duration_ms') or 0) / 60000, 1)} min\n")
        print("**Final message:**\n\n```\n" + str(result.get("result", ""))[:3000] + "\n```")
        denials = result.get("permission_denials") or []
        if denials:
            print("\n**Permission denials:**")
            for d in denials[:10]:
                print(f"- `{d.get('tool_name')}`: `{json.dumps(d.get('tool_input'))[:200]}`")
    else:
        print(f"No result event: the agent did not finish ({len(events)} events logged).")

    texts = assistant_texts(events)
    if texts:
        print("\n**Last things the agent said:**\n")
        for t in texts[-3:]:
            print("> " + t[:600].replace("\n", "\n> ") + "\n")

    errors = tool_errors(events)
    if errors:
        print("\n**Tool errors (last 5):**\n")
        for err in errors[-5:]:
            print(f"- `{err}`")

    if args.stderr and Path(args.stderr).exists():
        tail = Path(args.stderr).read_text(errors="ignore").splitlines()[-30:]
        if any(line.strip() for line in tail):
            print("\n**stderr (last 30 lines):**\n\n```\n" + "\n".join(tail) + "\n```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
