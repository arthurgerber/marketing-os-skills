#!/usr/bin/env python3
"""Análise acústica de voz com librosa — 100% local, zero custo, escalável.

Extrai: pitch, energia, ritmo, brilho espectral, pausas, curva emocional.
Funciona com vídeo ou áudio puro (WhatsApp, ligação, MP3, etc.)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def _classificar_pitch(hz: float) -> str:
    if hz <= 0: return "não detectado"
    if hz < 100: return "muito grave"
    if hz < 150: return "grave"
    if hz < 200: return "médio-grave"
    if hz < 250: return "médio"
    if hz < 300: return "médio-agudo"
    return "agudo"


def _classificar_ritmo(wpm: float) -> str:
    if wpm <= 0: return "não calculado"
    if wpm < 100: return "muito lento"
    if wpm < 130: return "lento"
    if wpm < 160: return "normal"
    if wpm < 190: return "rápido"
    return "muito rápido"


def _calcular_wpm(segmentos: list[dict]) -> float:
    """Calcula palavras por minuto a partir dos segmentos do Whisper."""
    if not segmentos:
        return 0.0
    total_palavras = sum(len(seg["text"].split()) for seg in segmentos)
    duracao_total = segmentos[-1]["end"] - segmentos[0]["start"]
    if duracao_total <= 0:
        return 0.0
    return round(total_palavras / (duracao_total / 60), 1)


def analisar(audio_path: str | Path, segmentos_whisper: list[dict] | None = None) -> dict:
    """
    Analisa features acústicas de um arquivo de áudio.
    segmentos_whisper: segmentos do Whisper para calcular WPM e sincronizar com energia.
    """
    try:
        import librosa
        import numpy as np
    except ImportError:
        return {
            "erro": "librosa não instalado. Execute: pip install librosa --break-system-packages",
            "wpm": _calcular_wpm(segmentos_whisper or []),
        }

    audio_path = Path(audio_path)
    if not audio_path.exists():
        return {"erro": f"Arquivo não encontrado: {audio_path}"}

    print(f"[analisa-video] analisando features de voz (librosa)…", file=sys.stderr)

    try:
        # Carrega áudio — mono 16kHz (mesmo padrão do Whisper)
        y, sr = librosa.load(str(audio_path), sr=16000, mono=True)
        duracao = librosa.get_duration(y=y, sr=sr)

        hop_length = 512
        frame_length = 2048

        # ── 1. ENERGIA/VOLUME ao longo do tempo ──────────────────────────────
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
        rms_max = rms.max() + 1e-8
        rms_norm = rms / rms_max

        # ── 2. PITCH (frequência fundamental) ────────────────────────────────
        try:
            f0, voiced_flag, _ = librosa.pyin(
                y,
                fmin=librosa.note_to_hz("C2"),  # ~65 Hz
                fmax=librosa.note_to_hz("C6"),  # ~1047 Hz
                sr=sr, hop_length=hop_length
            )
            voiced_f0 = f0[voiced_flag & ~np.isnan(f0)]
            pitch_medio = float(np.mean(voiced_f0)) if len(voiced_f0) > 0 else 0.0
            pitch_variacao = float(np.std(voiced_f0)) if len(voiced_f0) > 0 else 0.0
            # Variação alta = voz expressiva, baixa = monotônica
            expressividade = "expressiva" if pitch_variacao > 30 else ("moderada" if pitch_variacao > 15 else "monotônica")
        except Exception:
            pitch_medio = 0.0
            pitch_variacao = 0.0
            expressividade = "não calculado"

        # ── 3. BRILHO ESPECTRAL (qualidade/cor da voz) ───────────────────────
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
        brilho_medio = float(np.mean(centroid))

        # ── 4. TEMPO / RITMO DE FALA ─────────────────────────────────────────
        try:
            tempo_estimado, _ = librosa.beat.beat_track(y=y, sr=sr)
            tempo_estimado = float(tempo_estimado)
        except Exception:
            tempo_estimado = 0.0

        # ── 5. PAUSAS (silêncio < 10% da energia máxima) ─────────────────────
        limiar_silencio = 0.10
        em_silencio = rms_norm < limiar_silencio
        # Transições silencio→fala = número de pausas
        transicoes = np.diff(em_silencio.astype(int))
        num_pausas = int(np.sum(transicoes == -1))  # fim de pausa

        # Duração total em silêncio
        pct_silencio = round(float(np.mean(em_silencio)) * 100, 1)

        # ── 6. WPM (a partir do Whisper) ─────────────────────────────────────
        wpm = _calcular_wpm(segmentos_whisper or [])

        # ── 7. CURVA DE ENERGIA (downsample para ~80 pontos) ─────────────────
        n_pontos = min(80, len(rms))
        idx = np.linspace(0, len(rms) - 1, n_pontos, dtype=int)
        curva_energia = [
            {"t": round(float(times[i]), 1), "energia": round(float(rms_norm[i]), 2)}
            for i in idx
        ]

        # ── 8. PICOS DE ENERGIA (momentos de maior intensidade) ──────────────
        top_idx = np.argsort(rms)[-8:][::-1]
        picos = sorted(
            [{"t": round(float(times[i]), 1), "energia": round(float(rms_norm[i]), 2)} for i in top_idx],
            key=lambda x: x["t"]
        )

        # ── 9. PERFIL VOCAL (para replicação) ────────────────────────────────
        perfil_vocal = {
            "pitch_hz": round(pitch_medio, 1),
            "pitch_caracter": _classificar_pitch(pitch_medio),
            "expressividade": expressividade,
            "ritmo_wpm": wpm,
            "ritmo_caracter": _classificar_ritmo(wpm),
            "brilho_espectral_hz": round(brilho_medio, 1),
            "pausas": num_pausas,
            "pct_silencio": pct_silencio,
        }

        return {
            "duracao_s": round(duracao, 1),
            "wpm": wpm,
            "ritmo": _classificar_ritmo(wpm),
            "pitch_medio_hz": round(pitch_medio, 1),
            "pitch_caracter": _classificar_pitch(pitch_medio),
            "pitch_variacao_hz": round(pitch_variacao, 1),
            "expressividade": expressividade,
            "brilho_espectral": round(brilho_medio, 1),
            "num_pausas": num_pausas,
            "pct_silencio": pct_silencio,
            "curva_energia": curva_energia,
            "picos_energia": picos,
            "perfil_vocal": perfil_vocal,
        }

    except Exception as exc:
        return {"erro": f"Erro na análise acústica: {exc}", "wpm": _calcular_wpm(segmentos_whisper or [])}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: voice_features.py <audio_path>", file=sys.stderr)
        raise SystemExit(2)
    result = analisar(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
