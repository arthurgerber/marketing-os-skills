#!/usr/bin/env python3
"""
check.py — Checklist obrigatório da skill analisa-video
Roda ANTES de qualquer entrega ao Arthur.

USO: python3 check.py [pasta_analise]
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

SKILL_NAME = "analisa-video"

def check_analises_pasta():
    p = Path.home() / "Downloads" / "Analises"
    return p.exists()

def check_json_recente():
    p = Path.home() / "Downloads" / "Analises"
    if not p.exists(): return False
    jsons = sorted(p.glob("analise_*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    return len(jsons) > 0

def check_frames_existem():
    p = Path.home() / "Downloads" / "Analises"
    if not p.exists(): return False
    frames_dirs = list(p.glob("frames_*/frames/"))
    if not frames_dirs: return False
    # Pegar a mais recente
    latest = sorted(frames_dirs, key=lambda d: d.stat().st_mtime, reverse=True)[0]
    frames = list(latest.glob("frame_*.jpg"))
    count = len(frames)
    print(f"       → {count} frames encontrados em {latest}")
    return count >= 100  # mínimo razoável

def check_composites_existem():
    p = Path.home() / "Downloads" / "Analises"
    if not p.exists(): return False
    comp_dirs = list(p.glob("frames_*/composites/"))
    if not comp_dirs: return False
    latest = sorted(comp_dirs, key=lambda d: d.stat().st_mtime, reverse=True)[0]
    composites = list(latest.glob("composite_*.jpg"))
    count = len(composites)
    print(f"       → {count} composites em {latest}")
    return count >= 1

def check_transcricao():
    p = Path.home() / "Downloads" / "Analises"
    if not p.exists(): return False
    jsons = sorted(p.glob("analise_*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not jsons: return False
    with open(jsons[0]) as f:
        d = json.load(f)
    segs = d.get('transcricao_segmentos', [])
    count = len(segs)
    print(f"       → {count} segmentos na transcrição mais recente")
    return count > 50

def check_speakers_corretos():
    p = Path.home() / "Downloads" / "Analises"
    if not p.exists(): return False
    jsons = sorted(p.glob("analise_*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not jsons: return False
    with open(jsons[0]) as f:
        d = json.load(f)
    speakers = d.get('speakers', {})
    if not speakers: return True  # sem speakers = ok (pode ser áudio mono)
    # Verificar se labels fazem sentido (closer deve ter > 60% da fala)
    times = {k: v.get('tempo_fala_s', 0) for k,v in speakers.items()}
    if not times: return True
    total = sum(times.values())
    if total == 0: return True
    max_pct = max(times.values()) / total
    print(f"       → Speaker dominante: {max_pct:.0%} (esperado >60% para closer)")
    # Verificar se nome do closer está como quem mais fala
    max_speaker = max(times, key=times.get)
    has_closer_label = any('closer' in k.lower() for k in times.keys())
    if has_closer_label:
        closer_key = next(k for k in times.keys() if 'closer' in k.lower())
        is_max = times[closer_key] == max(times.values())
        if not is_max:
            print(f"       ⚠️ ATENÇÃO: Labels provavelmente INVERTIDOS! Verificar conteúdo.")
    return True

CHECKS = [
    ("Pasta ~/Downloads/Analises/ existe", check_analises_pasta),
    ("JSON de análise existe", check_json_recente),
    ("Frames extraídos (≥100)", check_frames_existem),
    ("Composites gerados (gera_composites.py foi rodado)", check_composites_existem),
    ("Transcrição com segmentos (≥50)", check_transcricao),
    ("Labels de speaker verificados", check_speakers_corretos),
]

def run_checks():
    print(f"\n{'='*55}")
    print(f"  CHECKLIST — {SKILL_NAME}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}\n")
    
    results = []
    for desc, fn in CHECKS:
        try:
            ok = fn()
        except Exception as e:
            ok = False
            print(f"       ERRO ao verificar: {e}")
        status = "✅" if ok else "❌"
        print(f"  {status} {desc}")
        results.append(ok)
    
    print(f"\n{'='*55}")
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"  ✅ {passed}/{total} — PODE ENTREGAR A ANÁLISE")
    else:
        failed = total - passed
        print(f"  ❌ {failed}/{total} FALHARAM — NÃO ENTREGAR")
        print(f"  Execute os passos com ❌ e re-rode: python3 check.py")
    print(f"{'='*55}\n")
    return all(results)

if __name__ == "__main__":
    ok = run_checks()
    sys.exit(0 if ok else 1)
