#!/usr/bin/env python3
"""Download a video via yt-dlp, or resolve a local file path.

Also fetches subtitles (manual first, then auto-generated) in VTT format so
transcribe.py can parse them without needing Whisper.

Extended: supports --cookies flag for authenticated platforms (Hotmart, Kiwify, etc.)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov", ".m4v", ".avi", ".flv", ".wmv"}


def is_url(source: str) -> bool:
    if source.startswith("-"):
        return False
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def resolve_local(path: str) -> dict:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise SystemExit(f"File not found: {p}")
    if p.suffix.lower() not in VIDEO_EXTS:
        print(f"[analisa-video] warning: {p.suffix} is not a known video extension", file=sys.stderr)
    return {"video_path": str(p), "subtitle_path": None, "info": {"title": p.name, "url": str(p)}, "downloaded": False}


def _pick_subtitle(out_dir: Path) -> Path | None:
    candidates = sorted(out_dir.glob("video*.vtt"))
    if not candidates:
        return None
    preferred = [c for c in candidates if ".en" in c.name]
    return preferred[0] if preferred else candidates[0]


def _pick_video(out_dir: Path) -> Path | None:
    for ext in (".mp4", ".mkv", ".webm", ".mov"):
        for candidate in out_dir.glob(f"video*{ext}"):
            return candidate
    for candidate in out_dir.glob("video.*"):
        if candidate.suffix.lower() in VIDEO_EXTS:
            return candidate
    return None


def download_url(url: str, out_dir: Path, cookies_file: str | None = None) -> dict:
    if shutil.which("yt-dlp") is None:
        raise SystemExit("yt-dlp is not installed. Install with: brew install yt-dlp")

    out_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(out_dir / "video.%(ext)s")

    cmd = [
        "yt-dlp", "-N", "8",
        "-f", "bv*[height<=720]+ba/b[height<=720]/bv+ba/b",
        "--merge-output-format", "mp4",
        "--write-info-json",
        "--write-subs", "--write-auto-subs",
        "--sub-langs", "en,en-US,en-GB,pt,pt-BR",
        "--sub-format", "vtt", "--convert-subs", "vtt",
        "--no-playlist", "--ignore-errors",
        "-o", output_template,
    ]

    # Cookie support for authenticated platforms (Hotmart, Kiwify, etc.)
    if cookies_file:
        cookies_path = Path(cookies_file).expanduser()
        if cookies_path.exists():
            cmd += ["--cookies", str(cookies_path)]
            print(f"[analisa-video] using cookies from {cookies_path}", file=sys.stderr)
        else:
            print(f"[analisa-video] warning: cookies file not found: {cookies_path}", file=sys.stderr)

    cmd += ["--", url]

    result = subprocess.run(cmd, stdout=sys.stderr, stderr=sys.stderr)
    video = _pick_video(out_dir)
    if video is None:
        raise SystemExit(f"yt-dlp did not produce a video file in {out_dir} (exit {result.returncode})")

    subtitle = _pick_subtitle(out_dir)
    info_path = out_dir / "video.info.json"
    info: dict = {}
    if info_path.exists():
        try:
            raw = json.loads(info_path.read_text(encoding="utf-8"))
            info = {"title": raw.get("title"), "uploader": raw.get("uploader") or raw.get("channel"), "duration": raw.get("duration"), "url": raw.get("webpage_url") or url}
        except Exception:
            info = {"url": url}

    return {"video_path": str(video), "subtitle_path": str(subtitle) if subtitle else None, "info": info or {"url": url}, "downloaded": True}


def download(source: str, out_dir: Path, cookies_file: str | None = None) -> dict:
    if is_url(source):
        return download_url(source, out_dir, cookies_file)
    return resolve_local(source)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: download.py <url-or-path> <out-dir> [--cookies <path>]", file=sys.stderr)
        raise SystemExit(2)
    cookies = None
    if "--cookies" in sys.argv:
        cookies = sys.argv[sys.argv.index("--cookies") + 1]
    result = download(sys.argv[1], Path(sys.argv[2]), cookies)
    print(json.dumps(result, indent=2))
