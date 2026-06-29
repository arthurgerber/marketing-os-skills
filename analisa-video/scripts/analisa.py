#!/usr/bin/env python3
"""analisa-video/audio v3 — 2-em-1, 100% local, zero custo.

Adições v3:
  - Diarização de speakers (pyannote.audio) — quem fala quando
  - Saída JSON estruturada — pronto para agente e base de dados
  - Suporte a múltiplos closers e múltiplos leads na mesma call
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".opus", ".m4a", ".aac", ".flac", ".weba", ".wma"}


def _e_audio(source: str) -> bool:
    return Path(source).suffix.lower() in AUDIO_EXTS


def _e_url(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")


def _extrair_audio(video_path: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-i", str(Path(video_path).resolve()),
           "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
           str(out_path.resolve())]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg falhou: {r.stderr.strip()}")
    return out_path


def _converter_audio(source: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-i", str(Path(source).resolve()),
           "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
           str(out_path.resolve())]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg falhou ao converter áudio: {r.stderr.strip()}")
    return out_path


def _format_transcript_simples(segments: list[dict]) -> str:
    lines = []
    for seg in segments:
        s = int(seg["start"])
        lines.append(f"[{s//60:02d}:{s%60:02d}] {seg['text']}")
    return "\n".join(lines)


def _format_transcript_com_speakers(segmentos: list[dict]) -> str:
    lines = []
    ultimo_speaker = None
    for seg in segmentos:
        s = int(seg["start"])
        stamp = f"[{s//60:02d}:{s%60:02d}]"
        speaker = seg.get("speaker", "??")
        if speaker != ultimo_speaker:
            lines.append(f"\n**{speaker}**")
            ultimo_speaker = speaker
        lines.append(f"{stamp} {seg['texto']}")
    return "\n".join(lines)


def _salvar_json(data: dict, titulo: str) -> Path:
    safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in (titulo or "arquivo"))[:60].strip()
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    save_dir = Path.home() / "Downloads" / "Analises"
    save_dir.mkdir(parents=True, exist_ok=True)
    path = save_dir / f"analise_{safe}_{ts}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _salvar_txt(transcript: str, titulo: str, voz: dict | None,
                speakers: dict | None, tipo: str) -> Path:
    safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in (titulo or "arquivo"))[:60].strip()
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    save_dir = Path.home() / "Downloads" / "Transcricoes"
    save_dir.mkdir(parents=True, exist_ok=True)
    path = save_dir / f"transcricao_{safe}_{ts}.txt"

    linhas = [f"# Transcrição — {titulo}", f"# Tipo: {tipo}",
              f"# Gerado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ""]

    if speakers:
        linhas += ["## SPEAKERS IDENTIFICADOS", ""]
        for nome, m in speakers.items():
            linhas.append(f"**{nome}:** {m['wpm']} wpm | {m['tempo_fala_s']}s de fala | {m['total_palavras']} palavras")
        linhas += ["", "---", ""]

    if voz and not voz.get("erro"):
        linhas += ["## VOZ GERAL", f"Ritmo: {voz.get('wpm')} wpm | Pitch: {voz.get('pitch_medio_hz')} Hz ({voz.get('pitch_caracter')})",
                   f"Expressividade: {voz.get('expressividade')} | Silêncio: {voz.get('pct_silencio')}%",
                   "", "---", ""]

    linhas += ["## TRANSCRIÇÃO", "", transcript]
    path.write_text("\n".join(linhas), encoding="utf-8")
    return path



# ── CACHE DE TRANSCRIÇÃO ──────────────────────────────────────────────────────
import hashlib as _hashlib

def _cache_path(audio_source: str) -> Path:
    """Retorna caminho do cache para este arquivo de áudio."""
    h = _hashlib.md5(str(Path(audio_source).resolve()).encode()).hexdigest()[:12]
    cache_dir = Path.home() / "Downloads" / "Analises" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"transcricao_{h}.json"

def _salvar_cache(audio_source: str, segments: list, modelo: str) -> None:
    import json as _json
    p = _cache_path(audio_source)
    _json.dump({"modelo": modelo, "segments": segments}, p.open("w", encoding="utf-8"),
               ensure_ascii=False, indent=2)
    print(f"[analisa] cache de transcrição salvo: {p.name}", file=sys.stderr)

def _carregar_cache(audio_source: str) -> list | None:
    import json as _json
    p = _cache_path(audio_source)
    if p.exists():
        data = _json.loads(p.read_text(encoding="utf-8"))
        segs = data.get("segments", [])
        if segs:
            print(f"[analisa] cache encontrado ({len(segs)} segmentos) — pulando Whisper", file=sys.stderr)
            return segs
    return None
# ── FIM CACHE ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="analisa-video/audio v3")
    parser.add_argument("source")
    parser.add_argument("--max-frames", type=int, default=400, help="Frames totais a extrair. Default 400 = ~1 frame/10s para call de 63min. Use --fast para reduzir.")
    parser.add_argument("--resolution", type=int, default=512)
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--so-audio", action="store_true")
    parser.add_argument("--no-voz", action="store_true")
    parser.add_argument("--no-diarizacao", action="store_true", help="Pula identificação de speakers")
    parser.add_argument("--speakers", type=int, default=None, help="Número exato de speakers (ex: 2)")
    parser.add_argument("--roles", default=None,
                        help='Mapa speaker→nome: "Speaker_00=Closer,Speaker_01=Lead"')
    parser.add_argument("--cookies", default=None)
    parser.add_argument("--modelo", default="small")
    parser.add_argument("--no-save", action="store_true")
    parser.add_argument("--so-diarizacao", action="store_true", help="Pula transcrição, usa cache ou último JSON salvo, roda só diarização")
    parser.add_argument("--force-retranscribe", action="store_true", help="Ignora cache e refaz transcrição do zero")
    args = parser.parse_args()

    modo_so_audio = args.so_audio or (not _e_url(args.source) and _e_audio(args.source))
    tipo_label = "AUDIO" if modo_so_audio else "VIDEO"

    titulo = Path(args.source).stem if not args.source.startswith("http") else (args.source.split("/")[-1].split("?")[0] or "analise")
    if args.out_dir:
        out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True); cleanup = False
    else:
        # Salva frames permanentemente em ~/Downloads/Analises/frames_[titulo]/
        # Nunca usa /tmp — frames devem persistir para análise visual por Claude
        _safe_titulo = "".join(c if c.isalnum() or c in " _-" else "_" for c in titulo)[:40].strip()
        _frames_base = Path.home() / "Downloads" / "Analises" / f"frames_{_safe_titulo}"
        _frames_base.mkdir(parents=True, exist_ok=True)
        out_dir = _frames_base
        cleanup = False  # NUNCA deletar frames

    frames_dir = out_dir / "frames"
    audio_out = out_dir / "audio.wav"

    try:
        import download as dl_mod
        import frames as fr_mod
        import local_whisper as lw_mod
        import transcribe as tr_mod
        import voice_features as vf_mod
        import diarize as dz_mod

        # ── DOWNLOAD / RESOLVE ────────────────────────────────────────────────
        video_path = None
        titulo = ""
        info = {}

        if modo_so_audio and not _e_url(args.source):
            audio_path_converted = _converter_audio(args.source, audio_out)
            titulo = Path(args.source).stem
            info = {"title": titulo, "url": args.source}
            print(f"[analisa] AUDIO: {titulo}", file=sys.stderr)
        else:
            dl_result = dl_mod.download(args.source, out_dir, cookies_file=args.cookies)
            video_path = dl_result["video_path"]
            info = dl_result.get("info", {})
            titulo = info.get("title") or Path(video_path).stem
            print(f"[analisa] VIDEO: {titulo}", file=sys.stderr)

        # ── FRAMES (só vídeo) ─────────────────────────────────────────────────
        frames = []
        meta = {}
        duracao_s = None

        if video_path and not modo_so_audio:
            meta = fr_mod.get_metadata(video_path)
            duracao_s = meta["duration_seconds"]
            start_sec = fr_mod.parse_time(args.start)
            end_sec = fr_mod.parse_time(args.end)
            max_frames = min(args.max_frames, 50 if args.fast else args.max_frames)
            if args.fast:
                fps, target = fr_mod.auto_fps_fast(duracao_s, max_frames=max_frames)
            else:
                fps, target = fr_mod.auto_fps(duracao_s, max_frames=max_frames)
            modo = "RAPIDO" if args.fast else "COMPLETO"
            print(f"[analisa] {modo}: {target} frames | {fr_mod.format_time(duracao_s)}", file=sys.stderr)
            frames = fr_mod.extract(video_path, frames_dir, fps=fps, resolution=args.resolution,
                                    max_frames=max_frames, start_seconds=start_sec, end_seconds=end_sec)

        # ── TRANSCRIÇÃO LOCAL (faster-whisper) ────────────────────────────────
        segments = []
        transcript_source = "none"

        # Tenta legendas primeiro (mais rápido)
        if video_path and not modo_so_audio:
            for vtt in out_dir.glob("*.vtt"):
                try:
                    start_sec = fr_mod.parse_time(args.start)
                    end_sec = fr_mod.parse_time(args.end)
                    segs = tr_mod.parse_vtt(str(vtt))
                    segments = tr_mod.filter_range(segs, start_sec, end_sec)
                    transcript_source = "legendas"
                    break
                except Exception:
                    pass

        # Fonte de áudio para cache
        _audio_source_for_cache = args.source

        if not segments:
            # 1. Tenta carregar do cache (a menos que --force-retranscribe)
            if not getattr(args, "force_retranscribe", False) and not getattr(args, "so_diarizacao", False):
                cached = _carregar_cache(_audio_source_for_cache)
                if cached:
                    segments = cached
                    transcript_source = "cache"

        if not segments:
            src = str(audio_out) if (modo_so_audio and audio_out.exists()) else (video_path or str(audio_out))
            try:
                if not getattr(args, "so_diarizacao", False):
                    segments, ts_info = lw_mod.transcrever(src, audio_out, modelo=args.modelo)
                    transcript_source = ts_info
                    # Salva no cache após transcrição bem-sucedida
                    if segments:
                        _salvar_cache(_audio_source_for_cache, segments, args.modelo)
                else:
                    print("[analisa] --so-diarizacao: transcrição pulada", file=sys.stderr)
            except SystemExit as exc:
                print(f"[analisa] transcrição falhou: {exc}", file=sys.stderr)

        # ── EXTRAÇÃO DE ÁUDIO (para análise, se ainda não feita) ──────────────
        if not audio_out.exists() and video_path:
            try:
                _extrair_audio(video_path, audio_out)
            except Exception as exc:
                print(f"[analisa] extração de áudio falhou: {exc}", file=sys.stderr)

        # ── ANÁLISE ACÚSTICA GLOBAL (librosa) ─────────────────────────────────
        voz_data = None
        if not args.no_voz and audio_out.exists():
            voz_data = vf_mod.analisar(audio_out, segmentos_whisper=segments)

        # ── DIARIZAÇÃO DE SPEAKERS ────────────────────────────────────────────
        diar_result = None
        speakers_metricas = None
        transcript_com_speakers = None
        roles_map = {}

        if not args.no_diarizacao and audio_out.exists() and segments:
            diar_result = dz_mod.diarizar(
                audio_out, segments,
                num_speakers=args.speakers,
                min_speakers=2,
                max_speakers=8,
            )

            if not diar_result.get("erro"):
                # Aplicar roles se fornecidos
                if args.roles:
                    for pair in args.roles.split(","):
                        if "=" in pair:
                            sp_id, nome = pair.split("=", 1)
                            roles_map[sp_id.strip()] = nome.strip()
                    diar_result = dz_mod.aplicar_roles(diar_result, roles_map)

                speakers_metricas = diar_result.get("metricas_por_speaker", {})
                transcript_com_speakers = _format_transcript_com_speakers(
                    diar_result.get("segmentos", [])
                )
            else:
                print(f"[analisa] diarização: {diar_result['erro']}", file=sys.stderr)

        # ── MONTAR JSON ESTRUTURADO ───────────────────────────────────────────
        transcript_text = (transcript_com_speakers or
                           _format_transcript_simples(segments))

        json_data = {
            "titulo": titulo,
            "tipo": tipo_label,
            "fonte": info.get("url") or args.source,
            "canal": info.get("uploader"),
            "data_analise": datetime.now().isoformat(),
            "duracao_s": duracao_s,
            "transcricao_via": transcript_source,
            "modelo_whisper": args.modelo,
            "voz_global": voz_data,
            "speakers": speakers_metricas,
            "num_speakers": diar_result.get("num_speakers") if diar_result and not diar_result.get("erro") else None,
            "speakers_detectados": diar_result.get("speakers_detectados") if diar_result and not diar_result.get("erro") else None,
            "segmentos_transcritos": len(segments),
            "frames_extraidos": len(frames),
            "transcricao_segmentos": diar_result.get("segmentos") if (diar_result and not diar_result.get("erro")) else [
                {"start": s["start"], "end": s["end"], "texto": s["text"]} for s in segments
            ],
        }

        # ── SALVAR ARQUIVOS ───────────────────────────────────────────────────
        saved_json = None
        saved_txt = None
        if not args.no_save:
            try:
                saved_json = _salvar_json(json_data, titulo)
                print(f"[analisa] JSON salvo: {saved_json}", file=sys.stderr)
            except Exception as exc:
                print(f"[analisa] erro ao salvar JSON: {exc}", file=sys.stderr)
            try:
                saved_txt = _salvar_txt(transcript_text, titulo, voz_data, speakers_metricas, tipo_label)
                print(f"[analisa] TXT salvo: {saved_txt}", file=sys.stderr)
            except Exception as exc:
                print(f"[analisa] erro ao salvar TXT: {exc}", file=sys.stderr)

        # ── RELATÓRIO PARA CLAUDE ─────────────────────────────────────────────
        linhas = [
            f"# analisa-video v3 — {titulo}",
            f"**Tipo:** {tipo_label} | **Fonte:** {info.get('url') or args.source}",
        ]
        if info.get("uploader"):
            linhas.append(f"**Canal:** {info['uploader']}")
        if duracao_s:
            linhas.append(f"**Duração:** {fr_mod.format_time(duracao_s) if video_path else f'{duracao_s:.0f}s'}")
        linhas.append(f"**Transcrição via:** {transcript_source} | **Modelo:** {args.modelo}")
        if saved_json:
            linhas.append(f"**JSON salvo:** `{saved_json}`")
        if saved_txt:
            linhas.append(f"**TXT salvo:** `{saved_txt}`")
        linhas += ["", "---", ""]

        # Speakers
        if speakers_metricas and not diar_result.get("erro"):
            linhas += ["## SPEAKERS IDENTIFICADOS", ""]
            linhas.append("| Speaker | WPM | Tempo de fala | Palavras |")
            linhas.append("|---------|-----|---------------|----------|")
            for nome, m in speakers_metricas.items():
                linhas.append(f"| **{nome}** | {m['wpm']} | {m['tempo_fala_s']}s | {m['total_palavras']} |")
            linhas.append("")
            for nome, m in speakers_metricas.items():
                linhas.append(f"**{nome} — amostra de fala:** \"{m.get('amostra', '')}\"")
            linhas += ["", "---", ""]
        elif diar_result and diar_result.get("erro"):
            linhas += [f"## DIARIZAÇÃO — {diar_result['erro']}", "", "---", ""]

        # Voz global
        if voz_data and not voz_data.get("erro"):
            v = voz_data
            linhas += [
                "## ANÁLISE ACÚSTICA DE VOZ (global)",
                f"| Métrica | Valor |",
                f"|---------|-------|",
                f"| Ritmo | {v['wpm']} wpm ({v['ritmo']}) |",
                f"| Pitch médio | {v['pitch_medio_hz']} Hz ({v['pitch_caracter']}) |",
                f"| Expressividade | {v['expressividade']} (±{v['pitch_variacao_hz']} Hz) |",
                f"| Silêncio | {v['pct_silencio']}% | {v['num_pausas']} pausas |",
                "", "---", "",
            ]

        # Frames
        if frames:
            modo_label = "Rápido" if args.fast else "Completo"
            linhas += [
                f"## FRAMES — {len(frames)} extraídos ({modo_label})",
                "",
                "⛔ CLAUDE — REGRA ABSOLUTA:",
                "   1. Leia TODOS os frames abaixo com Read. Sem exceção. Sem amostragem.",
                "   2. Para CADA frame: descreva olhar, mãos, expressão facial, postura, micro-expressões.",
                "   3. NÃO produza análise antes de ler o último frame da lista.",
                "   4. Relate micro-expressões: lábios comprimidos, sobrancelha franzida, olho estreitado,",
                "      tensão no maxilar, desvio de olhar, piscar excessivo, sorriso falso vs genuíno.",
                "",
            ]
            for frame in frames:
                t = int(frame["timestamp_seconds"])
                linhas.append(f"[{t//60:02d}:{t%60:02d}] {frame['path']}")
            linhas += ["", "⛔ FIM DOS FRAMES — AGORA leia cada um com Read antes de continuar.", "", "---", ""]

        # Transcrição
        if transcript_text:
            linhas += ["## TRANSCRIÇÃO", "", transcript_text]
        else:
            linhas += ["## TRANSCRIÇÃO", "", "*(sem transcrição disponível)*"]

        print("\n".join(linhas))

    finally:
        # cleanup desabilitado permanentemente — frames são ativos de análise
        # Frames ficam em ~/Downloads/Analises/frames_[titulo]/ para leitura por Claude
        pass


if __name__ == "__main__":
    main()
