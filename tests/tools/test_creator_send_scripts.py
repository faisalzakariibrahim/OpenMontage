"""Tests for scripts/creator_send_scripts.py (validation + rendering; no network)."""

import importlib.util
import json
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("creator_send_scripts", ROOT / "scripts" / "creator_send_scripts.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def good_script(i=1, **extra):
    s = {
        "id": f"W44-{i}", "category": "ai_tool", "title": "Summarize any PDF free",
        "hook": "Stop reading 40-page PDFs.", "hook_text": "Stop reading long PDFs",
        "script": "Here's the free tool <b>I</b> use & why.",
        "beats": [{"say": "x", "show": "screen_recording", "url": "https://example.com", "action": "upload a PDF"},
                  {"say": "y", "show": "face"}],
        "filming_notes": "Smile", "topic_reason": "Trending on r/productivity", "cta": "Follow", "sources": [],
    }
    s.update(extra)
    return s


def test_validate_ok():
    assert mod.validate({"week": "2026-W44", "scripts": [good_script(1), good_script(2)]}) == []


def test_validate_catches_problems():
    bad = good_script(1, beats=[{"show": "screen_recording", "url": "http://insecure"}])
    errors = mod.validate({"scripts": [bad, good_script(1), {"id": "nope"}]})
    joined = " ".join(errors)
    assert "without https url" in joined
    assert "duplicate id W44-1" in joined
    assert "bad id" in joined and "missing title" in joined


def test_render_escapes_html_and_strips_controls():
    text = mod.render(good_script(1, title="Tool \x07<script>"), "2026-W44")
    assert "&lt;b&gt;I&lt;/b&gt; use &amp; why" in text
    assert "<script>" not in text and "\x07" not in text
    assert "#W44-1" in text and "🖥 Screen" in text
    assert len(text) <= mod.MAX_MSG


def test_main_sends_and_records_message_ids(tmp_path, monkeypatch):
    batch = tmp_path / "scripts.json"
    batch.write_text(json.dumps({"week": "2026-W44", "scripts": [good_script(1), good_script(2)]}))
    out = tmp_path / "telegram.json"
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "1")
    counter = iter(range(100, 200))

    class R:
        def json(self):
            return {"ok": True, "result": {"message_id": next(counter)}}

    monkeypatch.setattr(sys, "argv", ["x", str(batch), "--out", str(out)])
    with mock.patch.object(mod.requests, "post", return_value=R()) as post:
        assert mod.main() == 0
    assert post.call_count == 3  # intro + 2 scripts
    ids = json.loads(out.read_text())["message_ids"]
    assert set(ids) == {"intro", "W44-1", "W44-2"}
