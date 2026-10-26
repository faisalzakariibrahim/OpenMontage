"""Validate a weekly creator script batch and send it to the owner on Telegram (no LLM).

  python scripts/creator_send_scripts.py projects/creator-batch/scripts.json \
      --out projects/creator-batch/telegram.json [--dry-run]

Needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID. Writes {script_id: message_id} so a clip sent as a
reply to a script message can be matched to that script later.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

MAX_MSG = 4000  # Telegram limit is 4096
SHOW_ICONS = {"face": "🎥 You", "screen_recording": "🖥 Screen", "synthetic_screen": "🧪 Mock-up",
              "stock_broll": "🎞 B-roll"}
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ID_RE = re.compile(r"^W\d{2}-\d{1,2}$")


def clean(text, limit: int = 2000) -> str:
    return _CONTROL.sub("", str(text or "")).strip()[:limit]


def https_url(url) -> bool:
    p = urlparse(str(url or ""))
    return p.scheme == "https" and bool(p.hostname)


def validate(batch: dict) -> list[str]:
    errors = []
    scripts = batch.get("scripts")
    if not isinstance(scripts, list) or not scripts:
        return ["no scripts"]
    if len(scripts) > 10:
        errors.append("more than 10 scripts")
    ids = set()
    for i, s in enumerate(scripts):
        sid = s.get("id", "")
        if not ID_RE.match(str(sid)):
            errors.append(f"script {i}: bad id {sid!r} (expected like W44-1)")
        if sid in ids:
            errors.append(f"duplicate id {sid}")
        ids.add(sid)
        for key in ("title", "hook", "script"):
            if not clean(s.get(key)):
                errors.append(f"{sid}: missing {key}")
        for b in s.get("beats") or []:
            if b.get("show") == "screen_recording" and not https_url(b.get("url")):
                errors.append(f"{sid}: screen_recording beat without https url")
    return errors


def render(s: dict, week: str) -> str:
    e = html.escape
    kind = "AI tool" if s.get("category") == "ai_tool" else "Cyber tip"
    lines = [f"<b>#{e(clean(s['id'], 20))} · {kind}</b>", f"<b>{e(clean(s['title'], 120))}</b>", ""]
    if s.get("hook_text"):
        lines.append(f"🪝 On screen: <i>{e(clean(s['hook_text'], 80))}</i>")
    lines += ["", "<b>Say this:</b>", e(clean(s["script"], 2200)), ""]
    shots = []
    for b in s.get("beats") or []:
        show = b.get("show", "face")
        label = SHOW_ICONS.get(show, show)
        detail = ""
        if show == "screen_recording":
            detail = f" {clean(b.get('url'), 200)} ({clean(b.get('action'), 120)})"
        elif show == "synthetic_screen":
            detail = f" {clean(b.get('mock'), 160)}"
        elif show == "stock_broll":
            detail = f" {clean(b.get('broll_query'), 60)}"
        shots.append(f"• {label}{e(detail)}")
    if shots:
        lines += ["<b>Shots (auto-added in edit):</b>", *shots, ""]
    if s.get("filming_notes"):
        lines += [f"🎬 {e(clean(s['filming_notes'], 400))}", ""]
    if s.get("topic_reason"):
        lines.append(f"📈 Why now: {e(clean(s['topic_reason'], 200))}")
    lines.append(f"↩️ Reply to this message with your clip, or caption it <code>#{e(clean(s['id'], 20))}</code>.")
    text = "\n".join(lines)
    return text if len(text) <= MAX_MSG else text[: MAX_MSG - 20] + "\n…(trimmed)"


def send(token: str, chat_id: str, text: str) -> int:
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", timeout=30, json={
        "chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True})
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram sendMessage failed: {data.get('description', r.status_code)}")
    return data["result"]["message_id"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    batch = json.loads(Path(args.batch).read_text())
    errors = validate(batch)
    if errors:
        print("Batch invalid:\n- " + "\n- ".join(errors))
        return 2

    week = clean(batch.get("week"), 10)
    intro = (f"🎬 <b>CyberBrief week {html.escape(week)}</b>: {len(batch['scripts'])} scripts.\n"
             "Film them in one session. Then <b>reply to each script</b> with its clip (under 20 MB), "
             "or send clips from your Mac or the Drive inbox.")
    messages = {"intro": intro, **{s["id"]: render(s, week) for s in batch["scripts"]}}

    if args.dry_run:
        for key, text in messages.items():
            print(f"----- {key} ({len(text)} chars)\n{text}\n")
        return 0

    token, chat_id = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set. Run scripts/setup_telegram.sh")
        return 2

    ids = {}
    for key, text in messages.items():
        ids[key] = send(token, chat_id, text)
    Path(args.out).write_text(json.dumps({"week": week, "message_ids": ids}, indent=2))
    print(f"Sent {len(ids)} messages to Telegram")
    return 0


if __name__ == "__main__":
    sys.exit(main())
