#!/usr/bin/env python3
"""
gera_composites.py — Agrupa frames em grades compostas para análise rápida
Transforma 400 imagens individuais → 20 composites (grade 4×5 = 20 frames por imagem)
Reduz leituras de 400 → 20, de ~50min → ~3min de análise

USO:
  python3 gera_composites.py <pasta_de_frames>
  
SAÍDA:
  <pasta_de_frames>/../composites/composite_001.jpg ... composite_020.jpg
"""

import sys
import os
import glob
from pathlib import Path

def criar_composites(pasta_frames, frames_por_grade=20, colunas=4):
    """Agrupa frames em imagens compostas para análise eficiente."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import math
    except ImportError:
        print("Instalando Pillow...")
        os.system("pip install Pillow --break-system-packages -q")
        from PIL import Image, ImageDraw, ImageFont
        import math

    pasta_frames = Path(pasta_frames)
    frames = sorted(glob.glob(str(pasta_frames / "frame_*.jpg")))
    
    if not frames:
        print(f"ERRO: Nenhum frame encontrado em {pasta_frames}")
        sys.exit(1)
    
    total = len(frames)
    print(f"Encontrados {total} frames. Gerando composites...")
    
    # Pasta de saída
    pasta_out = pasta_frames.parent / "composites"
    pasta_out.mkdir(exist_ok=True)
    
    # Dimensões do frame original (assume todos iguais)
    with Image.open(frames[0]) as img:
        fw, fh = img.size
    
    # Escalar frame para caber na grade
    escala = 0.4  # 40% do tamanho original
    fw_s = int(fw * escala)
    fh_s = int(fh * escala)
    linhas = math.ceil(frames_por_grade / colunas)
    
    # Calcular duração total aproximada
    # Cada frame = (num_total_frames / 400) * 9.5s se total ~= 400
    fps_aprox = 9.5  # segundos por frame
    
    composites_criados = 0
    for i in range(0, total, frames_por_grade):
        lote = frames[i:i + frames_por_grade]
        n_lote = len(lote)
        
        # Grade composta
        grade_w = colunas * fw_s
        grade_h = linhas * fh_s + 30  # +30px para header
        composite = Image.new("RGB", (grade_w, grade_h), (20, 20, 20))
        draw = ImageDraw.Draw(composite)
        
        # Header com range de tempo
        frame_inicio = i + 1
        frame_fim = i + n_lote
        t_inicio_s = i * fps_aprox
        t_fim_s = (i + n_lote) * fps_aprox
        t_inicio = f"{int(t_inicio_s//60):02d}:{int(t_inicio_s%60):02d}"
        t_fim = f"{int(t_fim_s//60):02d}:{int(t_fim_s%60):02d}"
        draw.text((5, 5), f"Frames {frame_inicio:04d}-{frame_fim:04d} | {t_inicio}–{t_fim}", fill=(255, 255, 0))
        
        for j, frame_path in enumerate(lote):
            col = j % colunas
            row = j // colunas
            x = col * fw_s
            y = row * fh_s + 30
            
            with Image.open(frame_path) as fr:
                fr_s = fr.resize((fw_s, fh_s), Image.LANCZOS)
                composite.paste(fr_s, (x, y))
            
            # Timestamp no canto do frame
            frame_num = i + j + 1
            t_s = (i + j) * fps_aprox
            t_label = f"{int(t_s//60):02d}:{int(t_s%60):02d}"
            draw.text((x + 2, y + 2), t_label, fill=(255, 255, 255))
        
        # Salvar composite
        n_composite = composites_criados + 1
        out_path = pasta_out / f"composite_{n_composite:03d}.jpg"
        composite.save(out_path, "JPEG", quality=85)
        composites_criados += 1
        print(f"  composite_{n_composite:03d}.jpg — frames {frame_inicio:04d}-{frame_fim:04d} ({t_inicio}–{t_fim})")
    
    print(f"\n✅ {composites_criados} composites gerados em: {pasta_out}")
    print(f"   Leituras necessárias: {composites_criados} (em vez de {total})")
    print(f"   Tempo de análise estimado: ~{composites_criados * 10}s (em vez de ~50min)")
    return str(pasta_out)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USO: python3 gera_composites.py <pasta_de_frames>")
        print("EX:  python3 gera_composites.py ~/Downloads/Analises/frames_MinhaCall/frames/")
        sys.exit(1)
    
    criar_composites(sys.argv[1])
