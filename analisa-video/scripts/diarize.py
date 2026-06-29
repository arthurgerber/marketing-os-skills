#!/usr/bin/env python3
"""Diarização de speakers — identifica QUEM fala em cada momento.

Usa pyannote.audio localmente. Suporta N speakers (múltiplos closers + leads).
Requer token gratuito do HuggingFace (configurar uma vez em ~/.config/watch/.env).

Saída: segmentos com speaker_id, timestamps e texto da transcrição alinhado.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _load_hf_token() -> str | None:
    token = os.environ.get("HUGGINGFACE_TOKEN", "").strip()
    if token:
        return token
    for dotenv in [Path.home() / ".config" / "watch" / ".env", Path.cwd() / ".env"]:
        if dotenv.exists():
            for line in dotenv.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("HUGGINGFACE_TOKEN="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return None


def _alinhar_com_transcricao(
    diar_segments: list[dict],
    whisper_segments: list[dict],
) -> list[dict]:
    """
    Alinha segmentos de diarização (quem fala) com segmentos do Whisper (o que fala).
    Para cada segmento Whisper, encontra o speaker com maior sobreposição de tempo.
    """
    resultado = []
    for w in whisper_segments:
        w_start, w_end = w["start"], w["end"]
        melhor_speaker = "Speaker_??"
        melhor_overlap = 0.0

        for d in diar_segments:
            d_start, d_end, speaker = d["start"], d["end"], d["speaker"]
            overlap = max(0.0, min(w_end, d_end) - max(w_start, d_start))
            if overlap > melhor_overlap:
                melhor_overlap = overlap
                melhor_speaker = speaker

        resultado.append({
            "start": w_start,
            "end": w_end,
            "speaker": melhor_speaker,
            "texto": w["text"],
        })
    return resultado


def _metricas_por_speaker(
    segmentos_alinhados: list[dict],
    voice_data: dict | None = None,
) -> dict:
    """Agrega métricas de fala por speaker."""
    speakers: dict[str, dict] = {}

    for seg in segmentos_alinhados:
        sp = seg["speaker"]
        if sp not in speakers:
            speakers[sp] = {
                "total_palavras": 0,
                "tempo_fala_s": 0.0,
                "segmentos": 0,
                "textos": [],
            }
        palavras = len(seg["texto"].split())
        duracao = seg["end"] - seg["start"]
        speakers[sp]["total_palavras"] += palavras
        speakers[sp]["tempo_fala_s"] = round(speakers[sp]["tempo_fala_s"] + duracao, 2)
        speakers[sp]["segmentos"] += 1
        speakers[sp]["textos"].append(seg["texto"])

    # Calcula WPM por speaker
    for sp, data in speakers.items():
        wpm = 0.0
        if data["tempo_fala_s"] > 0:
            wpm = round(data["total_palavras"] / (data["tempo_fala_s"] / 60), 1)
        data["wpm"] = wpm
        data["tempo_fala_s"] = round(data["tempo_fala_s"], 1)
        # Amostra de fala para contexto
        data["amostra"] = " ".join(data["textos"][:3])[:200]
        del data["textos"]

    return speakers



def _patch_all_version_conflicts():
    """
    Corrige todos os conflitos de versão conhecidos antes de carregar pyannote:
      1. huggingface_hub >= 0.23 removeu use_auth_token= de hf_hub_download
      2. torch >= 2.6 mudou weights_only default para True (quebra modelos antigos)
    Chamado automaticamente antes de qualquer uso do Pipeline.
    """
    import importlib
    import re

    # Patch 1: huggingface_hub use_auth_token → token
    try:
        import huggingface_hub as _hf
        _orig = _hf.hf_hub_download
        def _patched(*a, **kw):
            if "use_auth_token" in kw:
                v = kw.pop("use_auth_token")
                if v and "token" not in kw:
                    kw["token"] = v
            return _orig(*a, **kw)
        _hf.hf_hub_download = _patched
        try:
            _hf.file_download.hf_hub_download = _patched
        except Exception:
            pass
    except Exception:
        pass

    # Patch 2: torch.load — weights_only=False por padrão
    try:
        import torch
        import torch.serialization
        # Adiciona globals seguros conhecidos do pyannote
        try:
            torch.serialization.add_safe_globals([torch.torch_version.TorchVersion])
        except Exception:
            pass
        _orig_load = torch.serialization.load
        def _permissive_load(f, map_location=None, pickle_module=None, *, weights_only=False, mmap=None, **kw):
            return _orig_load(f, map_location=map_location, pickle_module=pickle_module,
                              weights_only=weights_only, mmap=mmap, **kw)
        torch.serialization.load = _permissive_load
        torch.load = _permissive_load
    except Exception:
        pass


# ── APLICAR PATCHES NO NÍVEL DO MÓDULO ───────────────────────────────────────
# Crítico: deve rodar ANTES de qualquer `from pyannote.audio import Pipeline`
# para que pyannote já capture as versões patcheadas do hf_hub_download.
# Quando analisa.py faz `import diarize`, estes patches são aplicados imediatamente.
_patch_all_version_conflicts()


def diarizar(
    audio_path: str | Path,
    whisper_segments: list[dict],
    num_speakers: int | None = None,
    min_speakers: int = 2,
    max_speakers: int = 6,
) -> dict:
    """
    Executa diarização e retorna segmentos alinhados + métricas por speaker.

    audio_path: WAV 16kHz mono (gerado pelo analisa.py)
    whisper_segments: segmentos do Whisper (start, end, text)
    num_speakers: se souber exatamente quantos speakers (opcional)
    """
    hf_token = _load_hf_token()
    if not hf_token:
        return {
            "erro": (
                "HUGGINGFACE_TOKEN não configurado.\n"
                "1. Crie conta gratuita em huggingface.co\n"
                "2. Acesse: huggingface.co/pyannote/speaker-diarization-3.1 e aceite os termos\n"
                "3. Gere um token em huggingface.co/settings/tokens\n"
                "4. Adicione ao ~/.config/watch/.env:\n"
                "   HUGGINGFACE_TOKEN=seu_token_aqui"
            )
        }

    try:
        from pyannote.audio import Pipeline
        import torch
    except ImportError:
        return {
            "erro": (
                "pyannote.audio não instalado.\n"
                "Execute: python3 ${CLAUDE_SKILL_DIR}/scripts/setup.py"
            )
        }

    audio_path = Path(audio_path)
    if not audio_path.exists():
        return {"erro": f"Arquivo de áudio não encontrado: {audio_path}"}

    print("[analisa] carregando pipeline de diarização (pyannote)…", file=sys.stderr)
    try:
        import importlib
        import re as _re
        import torch

        device = "cpu"
        try:
            if torch.backends.mps.is_available():
                device = "mps"
            elif torch.cuda.is_available():
                device = "cuda"
        except Exception:
            pass

        # Aplica todos os patches de compatibilidade de versão
        _patch_all_version_conflicts()

        # Carrega pipeline com auto-descoberta de safe globals (pyannote 3.1 usa use_auth_token=)
        pipeline = None
        _safe_extra = []
        for _attempt in range(20):
            try:
                if _safe_extra:
                    torch.serialization.add_safe_globals(_safe_extra)
                pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=hf_token,
                )
                break
            except Exception as _e:
                _m = _re.search(r"GLOBAL\s+(\S+)\s+was not an allowed global", str(_e))
                if _m:
                    _cp = _m.group(1)
                    _mp, _cn = _cp.rsplit(".", 1)
                    try:
                        _mod = importlib.import_module(_mp)
                        _cls = getattr(_mod, _cn)
                        _safe_extra.append(_cls)
                        print(f"[analisa] safe global adicionado: {_cp}", file=sys.stderr)
                        continue
                    except Exception:
                        pass
                raise

        if pipeline is None:
            return {"erro": "Falha ao carregar pipeline após múltiplas tentativas"}

        pipeline.to(torch.device(device))
    except Exception as exc:
        return {"erro": f"Erro ao carregar pipeline: {exc}"}

    print(f"[analisa] diarizando speakers (device: {device})…", file=sys.stderr)
    try:
        kwargs = {}
        if num_speakers:
            kwargs["num_speakers"] = num_speakers
        else:
            kwargs["min_speakers"] = min_speakers
            kwargs["max_speakers"] = max_speakers

        diarization = pipeline(str(audio_path), **kwargs)
    except Exception as exc:
        return {"erro": f"Erro na diarização: {exc}"}

    # Converter resultado pyannote para lista de dicts
    diar_segments = []
    speakers_detectados = set()
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diar_segments.append({
            "start": round(turn.start, 2),
            "end": round(turn.end, 2),
            "speaker": speaker,
        })
        speakers_detectados.add(speaker)

    print(f"[analisa] {len(speakers_detectados)} speaker(s) detectado(s): {sorted(speakers_detectados)}", file=sys.stderr)

    # Alinhar com transcrição Whisper
    segmentos_alinhados = _alinhar_com_transcricao(diar_segments, whisper_segments)

    # Métricas por speaker
    metricas = _metricas_por_speaker(segmentos_alinhados)

    return {
        "speakers_detectados": sorted(speakers_detectados),
        "num_speakers": len(speakers_detectados),
        "segmentos": segmentos_alinhados,
        "metricas_por_speaker": metricas,
        "diar_raw": diar_segments,
    }


def aplicar_roles(diar_result: dict, roles: dict[str, str]) -> dict:
    """
    Aplica nomes reais aos speakers detectados.
    roles: {"SPEAKER_00": "Closer", "SPEAKER_01": "Lead"}
    """
    if not roles or diar_result.get("erro"):
        return diar_result

    # Renomear nos segmentos
    for seg in diar_result.get("segmentos", []):
        seg["speaker_id"] = seg["speaker"]
        seg["speaker"] = roles.get(seg["speaker"], seg["speaker"])

    # Renomear nas métricas
    novas_metricas = {}
    for sp_id, data in diar_result.get("metricas_por_speaker", {}).items():
        nome = roles.get(sp_id, sp_id)
        data["speaker_id"] = sp_id
        novas_metricas[nome] = data
    diar_result["metricas_por_speaker"] = novas_metricas

    # Renomear na lista de speakers detectados
    diar_result["speakers"] = [roles.get(sp, sp) for sp in diar_result.get("speakers_detectados", [])]

    return diar_result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: diarize.py <audio_path> [--speakers N]", file=sys.stderr)
        raise SystemExit(2)
    audio = sys.argv[1]
    n = None
    if "--speakers" in sys.argv:
        n = int(sys.argv[sys.argv.index("--speakers") + 1])
    result = diarizar(audio, [], num_speakers=n)
    print(json.dumps(result, indent=2, ensure_ascii=False))
