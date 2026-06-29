#!/usr/bin/env python3
"""Transcribe a video via Groq or OpenAI Whisper API. Pure stdlib."""
from __future__ import annotations
import io, json, mimetypes, os, shutil, ssl, subprocess, sys, time, urllib.error, uuid
from pathlib import Path
from urllib.request import Request, urlopen

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_MODEL = "whisper-large-v3"
OPENAI_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_MODEL = "whisper-1"

def load_api_key(preferred=None):
    def _from_env(name): v = os.environ.get(name); return v.strip() if v else None
    def _from_dotenv(path, name):
        if not path.exists(): return None
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line: continue
                key, _, value = line.partition("=")
                if key.strip() != name: continue
                value = value.strip()
                if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]: value = value[1:-1]
                return value or None
        except OSError: return None
    dotenv_paths = [Path.home() / ".config" / "watch" / ".env", Path.cwd() / ".env"]
    candidates = (("GROQ_API_KEY", "groq"), ("OPENAI_API_KEY", "openai"))
    if preferred is not None: candidates = tuple(c for c in candidates if c[1] == preferred)
    for key_name, backend in candidates:
        value = _from_env(key_name)
        if not value:
            for candidate in dotenv_paths:
                value = _from_dotenv(candidate, key_name)
                if value: break
        if value: return backend, value
    return None, None

def extract_audio(video_path, out_path):
    if shutil.which("ffmpeg") is None: raise SystemExit("ffmpeg is not installed. Install with: brew install ffmpeg")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(Path(video_path).resolve()),"-vn","-acodec","libmp3lame","-ar","16000","-ac","1","-b:a","64k",str(out_path.resolve())]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0: raise SystemExit(f"ffmpeg audio extraction failed: {result.stderr.strip()}")
    if not out_path.exists() or out_path.stat().st_size == 0: raise SystemExit("ffmpeg produced no audio")
    return out_path

def _build_multipart(fields, file_path):
    boundary = f"----WatchBoundary{uuid.uuid4().hex}"; eol = b"\r\n"; buf = io.BytesIO()
    for name, value in fields.items():
        buf.write(f"--{boundary}".encode()); buf.write(eol)
        buf.write(f'Content-Disposition: form-data; name="{name}"'.encode()); buf.write(eol); buf.write(eol)
        buf.write(str(value).encode()); buf.write(eol)
    mimetype = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    buf.write(f"--{boundary}".encode()); buf.write(eol)
    buf.write(f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"'.encode()); buf.write(eol)
    buf.write(f"Content-Type: {mimetype}".encode()); buf.write(eol); buf.write(eol)
    buf.write(file_path.read_bytes()); buf.write(eol)
    buf.write(f"--{boundary}--".encode()); buf.write(eol)
    return buf.getvalue(), boundary

def _post_whisper(endpoint, api_key, model, audio_path):
    fields = {"model": model, "response_format": "verbose_json", "temperature": "0"}
    body, boundary = _build_multipart(fields, audio_path)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "analisa-video/1.0"}
    context = ssl.create_default_context()
    for attempt in range(4):
        req = Request(endpoint, data=body, headers=headers, method="POST")
        try:
            with urlopen(req, timeout=300, context=context) as response:
                return json.loads(response.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as exc:
            if 400 <= exc.code < 500 and exc.code != 429: raise SystemExit(f"Whisper request failed: {exc}")
            if attempt < 3: time.sleep(2 * (attempt + 1)); continue
            raise SystemExit(f"Whisper request failed: {exc}")
        except Exception as exc:
            if attempt < 3: time.sleep(2 * (attempt + 1)); continue
            raise SystemExit(f"Whisper network error: {exc}")
    raise SystemExit("Whisper request failed after 4 attempts")

def _segments_from_response(data):
    out = []
    for seg in data.get("segments") or []:
        text = (seg.get("text") or "").strip()
        if not text: continue
        out.append({"start": round(float(seg.get("start") or 0.0), 2), "end": round(float(seg.get("end") or 0.0), 2), "text": text})
    if not out:
        full = (data.get("text") or "").strip()
        if full: out.append({"start": 0.0, "end": 0.0, "text": full})
    return out

def transcribe_video(video_path, audio_out, backend=None, api_key=None):
    if backend is None or api_key is None:
        detected_backend, detected_key = load_api_key()
        backend = backend or detected_backend; api_key = api_key or detected_key
    if not backend or not api_key:
        raise SystemExit("No Whisper API key available. Set GROQ_API_KEY or OPENAI_API_KEY in ~/.config/watch/.env")
    print(f"[analisa-video] extracting audio for Whisper ({backend})…", file=sys.stderr)
    audio_path = extract_audio(video_path, audio_out)
    if backend == "groq": response = _post_whisper(GROQ_ENDPOINT, api_key, GROQ_MODEL, audio_path)
    elif backend == "openai": response = _post_whisper(OPENAI_ENDPOINT, api_key, OPENAI_MODEL, audio_path)
    else: raise SystemExit(f"Unknown whisper backend: {backend}")
    segments = _segments_from_response(response)
    if not segments: raise SystemExit("Whisper returned no transcript segments")
    print(f"[analisa-video] transcribed {len(segments)} segments via {backend}", file=sys.stderr)
    return segments, backend

if __name__ == "__main__":
    if len(sys.argv) < 2: print("usage: whisper.py <video-path> [<audio-out.mp3>]", file=sys.stderr); raise SystemExit(2)
    video = sys.argv[1]; audio_out = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else Path("audio.mp3")
    segments, backend = transcribe_video(video, audio_out)
    print(json.dumps({"backend": backend, "segments": segments}, indent=2))
