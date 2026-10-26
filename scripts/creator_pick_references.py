"""Pick reference videos for the creator style study (no LLM involved).

For each profile URL, list its recent posts with yt-dlp (metadata only, no download) and keep the
most-viewed N. Explicit video URLs are added as-is. Only TikTok, YouTube and Instagram https URLs
are accepted. Writes a JSON list the analysis agent works through.

  python scripts/creator_pick_references.py --profiles "<url> <url>" --urls "<url> ..." \
      --per-profile 3 --out projects/style-study/references.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOSTS = ("tiktok.com", "youtube.com", "youtu.be", "instagram.com")
RECENT_POSTS = 30


def allowed(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "https" and any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS)


def split_urls(raw: str) -> list[str]:
    return [u for u in re.split(r"[\s,]+", raw or "") if u]


def top_videos(profile: str, per_profile: int) -> list[dict]:
    import yt_dlp

    opts = {"quiet": True, "skip_download": True, "extract_flat": "in_playlist",
            "playlistend": RECENT_POSTS, "ignoreerrors": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(profile, download=False) or {}
    entries = [e for e in (info.get("entries") or []) if e]
    entries.sort(key=lambda e: e.get("view_count") or 0, reverse=True)
    picked = []
    for e in entries[:per_profile]:
        url = e.get("url") or e.get("webpage_url")
        if url and not url.startswith("http") and "tiktok" in profile:
            url = f"{profile.rstrip('/')}/video/{e.get('id')}"
        if url and allowed(url):
            picked.append({"url": url, "title": (e.get("title") or "")[:200],
                           "views": e.get("view_count"), "source": profile})
    return picked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", default="")
    ap.add_argument("--urls", default="")
    ap.add_argument("--per-profile", type=int, default=3)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    refs: list[dict] = []
    for url in split_urls(args.urls):
        if allowed(url):
            refs.append({"url": url, "title": "", "views": None, "source": "pasted"})
        else:
            print(f"skipping non-allowed URL: {url}", file=sys.stderr)

    for profile in split_urls(args.profiles):
        if not allowed(profile):
            print(f"skipping non-allowed profile: {profile}", file=sys.stderr)
            continue
        try:
            found = top_videos(profile, max(1, min(args.per_profile, 10)))
            print(f"{profile}: picked {len(found)}", file=sys.stderr)
            refs.extend(found)
        except Exception as exc:  # TikTok often blocks listing from datacenter IPs
            print(f"{profile}: listing failed ({exc}); paste video links instead", file=sys.stderr)

    seen, unique = set(), []
    for r in refs:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(unique, indent=2))
    print(f"{len(unique)} reference videos -> {out}", file=sys.stderr)
    return 0 if unique else 1


if __name__ == "__main__":
    sys.exit(main())
