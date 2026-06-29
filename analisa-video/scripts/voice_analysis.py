#!/usr/bin/env python3
"""Analyze voice tone and sentiment via AssemblyAI API.

Pure stdlib — no pip install needed.
Returns: pace (wpm), dominant sentiment, energy curve, sentiment per segment.
"""
from __future__ import annotations

import io
import json
import os
import ssl
import sys
import time
import uuid
import mimetypes
from pathlib import Path
from urllib.request import Request, urlopen
import urllib.error

ASSEMBLYAI_UPLOAD = "https://api.assemblyai.com/v2/upload"
ASSEMBLYAI_TRANSCRIPT = "https://api.assemblyai.com/v2/transcript"


def load_api_key() -> str | None:
    key = os.environ.get("ASSEMBLYAI_API_KEY", "").strip()
    if key:
        return key
    for dotenv in [Path.home() / ".config" / "watch" / ".env", Path.cwd() / ".env"]:
        if dotenv.exists():
            for line in dotenv.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("ASSEMBLYAI_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return None


def _upload_audio(audio_path: Path, api_key: str) -> str:
    ctx = ssl.create_default_context()
    data = audio_path.read_bytes()
    req = Request(
        ASSEMBLYAI_UPLOAD,
        data=data,
        headers={
            "authorization": api_key,
            "content-type": "application/octet-stream",
            "User-Agent": "analisa-video/1.0",
        },
        method="POST",
    )
    with urlopen(req, timeout=120, context=ctx) as resp:
        return json.loads(resp.read())["upload_url"]


def _request_transcript(audio_url: str, api_key: str) -> str:
    ctx = ssl.create_default_context()
    body = json.dumps({
        "audio_url": audio_url,
        "sentiment_analysis": True,
        "auto_highlights": True,
        "language_detection": True,
    }).encode()
    req = Request(
        ASSEMBLYAI_TRANSCRIPT,
        data=body,
        headers={
            "authorization": api_key,
            "content-type": "application/json",
            "User-Agent": "analisa-video/1.0",
        },
        method="POST",
    )
    with urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read())["id"]


def _poll_transcript(transcript_id: str, api_key: str, timeout: int = 300) -> dict:
    ctx = ssl.create_default_context()
    url = f"{ASSEMBLYAI_TRANSCRIPT}/{transcript_id}"
    headers = {"authorization": api_key, "User-Agent": "analisa-video/1.0"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30, context=ctx) as resp:
            data = json.loads(resp.read())
        status = data.get("status")
        if status == "completed":
            return data
        if status == "error":
            raise SystemExit(f"AssemblyAI error: {data.get('error')}")
        time.sleep(3)
    raise SystemExit("AssemblyAI timed out waiting for transcript")


def _calc_wpm(words: list[dict], duration_ms: float) -> float:
    if not words or duration_ms <= 0:
        return 0.0
    return round(len(words) / (duration_ms / 60000), 1)


def _dominant_sentiment(results: list[dict]) -> str:
    counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for r in results:
        counts[r.get("sentiment", "NEUTRAL")] += 1
    return max(counts, key=counts.get)  # type: ignore


def _energy_curve(results: list[dict]) -> list[dict]:
    """Simplified energy curve: sentiment confidence over time."""
    curve = []
    for r in results:
        start_s = round((r.get("start") or 0) / 1000, 1)
        sentiment = r.get("sentiment", "NEUTRAL")
        confidence = round(r.get("confidence", 0.5), 2)
        energy = confidence if sentiment == "POSITIVE" else (1 - confidence if sentiment == "NEGATIVE" else 0.5)
        curve.append({"t": start_s, "sentiment": sentiment, "energy": round(energy, 2), "text": r.get("text", "")[:60]})
    return curve


def analyze(audio_path: str | Path) -> dict:
    api_key = load_api_key()
    if not api_key:
        return {"error": "ASSEMBLYAI_API_KEY not set. Add it to ~/.config/watch/.env"}

    audio_path = Path(audio_path)
    if not audio_path.exists():
        return {"error": f"Audio file not found: {audio_path}"}

    print("[analisa-video] uploading audio to AssemblyAI…", file=sys.stderr)
    audio_url = _upload_audio(audio_path, api_key)

    print("[analisa-video] requesting sentiment analysis…", file=sys.stderr)
    transcript_id = _request_transcript(audio_url, api_key)

    print("[analisa-video] processing… (may take 30-90s)", file=sys.stderr)
    data = _poll_transcript(transcript_id, api_key)

    words = data.get("words") or []
    duration_ms = words[-1]["end"] if words else 0
    sentiment_results = data.get("sentiment_analysis_results") or []
    highlights = data.get("auto_highlights_result", {}).get("results") or []

    # Top highlights = key phrases by importance
    top_highlights = sorted(highlights, key=lambda x: x.get("rank", 0), reverse=True)[:5]

    result = {
        "pace_wpm": _calc_wpm(words, duration_ms),
        "dominant_sentiment": _dominant_sentiment(sentiment_results) if sentiment_results else "N/A",
        "language_detected": data.get("language_code", "unknown"),
        "duration_s": round(duration_ms / 1000, 1),
        "total_words": len(words),
        "sentiment_breakdown": {
            "POSITIVE": sum(1 for r in sentiment_results if r.get("sentiment") == "POSITIVE"),
            "NEGATIVE": sum(1 for r in sentiment_results if r.get("sentiment") == "NEGATIVE"),
            "NEUTRAL": sum(1 for r in sentiment_results if r.get("sentiment") == "NEUTRAL"),
        },
        "energy_curve": _energy_curve(sentiment_results),
        "key_phrases": [h.get("text", "") for h in top_highlights],
        "full_transcript": data.get("text", ""),
    }

    print(f"[analisa-video] voice analysis complete. Pace: {result['pace_wpm']} wpm, "
          f"Sentiment: {result['dominant_sentiment']}", file=sys.stderr)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: voice_analysis.py <audio-path>", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(analyze(sys.argv[1]), indent=2))
