#!/usr/bin/env python3
"""Transcrição local com faster-whisper — zero API, zero custo, escalável.

faster-whisper roda na CPU ou MPS (Apple Silicon). Primeira execução faz download
do modelo (~500MB para 'medium'). Depois: 100% offline.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


MODELO_PADRAO = "medium"
DEVICE_PADRAO = "auto"   # faster-whisper detecta CUDA/CPU automaticamente


def _extrair_audio(video_path: str, out_path: Path) -> Path:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg não instalado. Instale com: brew install ffmpeg")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(Path(video_path).resolve()),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(out_path.resolve()),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg falhou na extração de áudio: {result.stderr.strip()}")
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise SystemExit("ffmpeg não produziu áudio — vídeo pode não ter trilha de áudio")
    return out_path


def transcrever(video_path: str, audio_out: Path, modelo: str = MODELO_PADRAO) -> tuple[list[dict], str]:
    """Transcreve localmente. Retorna (segmentos, info_modelo)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit(
            "faster-whisper não instalado.\n"
            "Execute: pip install faster-whisper --break-system-packages\n"
            "Ou rode: python3 ${CLAUDE_SKILL_DIR}/scripts/setup.py"
        )

    print(f"[analisa-video] extraindo áudio para transcrição local…", file=sys.stderr)
    audio_path = _extrair_audio(video_path, audio_out)

    print(f"[analisa-video] carregando modelo Whisper '{modelo}'…", file=sys.stderr)
    # compute_type="auto" usa int8 na CPU (rápido), float16 em GPU se disponível
    model = WhisperModel(modelo, device="cpu", compute_type="int8")

    print(f"[analisa-video] transcrevendo (100% local, sem API)…", file=sys.stderr)
    segments_gen, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        language=None,   # detecção automática de idioma
        vad_filter=True, # remove silêncio — mais preciso
    )

    segments = []
    for seg in segments_gen:
        text = seg.text.strip()
        if text:
            segments.append({
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": text,
            })

    idioma = info.language if hasattr(info, "language") else "?"
    info_str = f"faster-whisper/{modelo} (idioma: {idioma})"
    print(f"[analisa-video] {len(segments)} segmentos transcritos via {info_str}", file=sys.stderr)
    return segments, info_str


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: local_whisper.py <video_path> [modelo]", file=sys.stderr)
        raise SystemExit(2)
    segs, info = transcrever(sys.argv[1], Path("/tmp/audio_whisper.wav"),
                              modelo=sys.argv[2] if len(sys.argv) > 2 else MODELO_PADRAO)
    print(json.dumps({"modelo": info, "segmentos": segs}, indent=2, ensure_ascii=False))
