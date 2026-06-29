#!/usr/bin/env python3
"""Instala todas as dependências da skill analisa-video v3.
Execute uma vez: python3 setup.py
Tudo roda 100% local, sem API, sem custo por uso.
"""
import shutil, subprocess, sys, os
from pathlib import Path

def cmd(args, desc):
    print(f"\n→ {desc}…")
    r = subprocess.run(args)
    ok = r.returncode == 0
    print("  ✅ ok" if ok else f"  ⚠️  falhou (código {r.returncode})")
    return ok

def check(bin_name, hint):
    if shutil.which(bin_name):
        print(f"  ✅ {bin_name}")
        return True
    print(f"  ⚠️  {bin_name} não encontrado — instale: {hint}")
    return False

print("=" * 55)
print("  analisa-video v3 — setup")
print("  Zero APIs. Zero custo. Tudo local.")
print("=" * 55)

print("\n[1/5] Ferramentas de sistema…")
check("ffmpeg", "brew install ffmpeg")
check("yt-dlp", "brew install yt-dlp")

print("\n[2/5] faster-whisper (transcrição local)…")
cmd([sys.executable, "-m", "pip", "install", "faster-whisper", "-q", "--break-system-packages"],
    "pip install faster-whisper")

print("\n[3/5] librosa (análise acústica)…")
cmd([sys.executable, "-m", "pip", "install", "librosa", "numpy", "scipy", "-q", "--break-system-packages"],
    "pip install librosa numpy scipy")

print("\n[4/5] pyannote.audio (diarização de speakers)…")
cmd([sys.executable, "-m", "pip", "install", "pyannote.audio", "torch", "-q", "--break-system-packages"],
    "pip install pyannote.audio torch")

print("\n[5/5] Modelo Whisper 'small' (download único ~240MB)…")
try:
    from faster_whisper import WhisperModel
    WhisperModel("small", device="cpu", compute_type="int8")
    print("  ✅ modelo small pronto")
except Exception as e:
    print(f"  ⚠️  {e}")

# Verificar HuggingFace token
dotenv = Path.home() / ".config" / "watch" / ".env"
hf_token = os.environ.get("HUGGINGFACE_TOKEN", "")
if not hf_token and dotenv.exists():
    for line in dotenv.read_text().splitlines():
        if "HUGGINGFACE_TOKEN=" in line:
            hf_token = line.split("=",1)[1].strip().strip('"').strip("'")

print("\n" + "=" * 55)
print("  ✅ Setup concluído!")
if not hf_token:
    print("""
  ⚠️  PRÓXIMO PASSO — Diarização de speakers:
  Para identificar quem fala (closer, lead, etc.):

  1. Crie conta GRATUITA em: huggingface.co
  2. Aceite os termos em:
     huggingface.co/pyannote/speaker-diarization-3.1
  3. Gere token em: huggingface.co/settings/tokens
  4. Adicione ao arquivo ~/.config/watch/.env:
     HUGGINGFACE_TOKEN=hf_seutoken

  Sem isso, tudo funciona EXCETO a separação de speakers.
""")
else:
    print("  ✅ HUGGINGFACE_TOKEN configurado — diarização ativa!")
print("""
  Modelos Whisper disponíveis:
    --modelo tiny    ultra-rápido (~75MB)
    --modelo small   padrão, bom balanço (~240MB)
    --modelo medium  mais preciso (~770MB)
    --modelo large-v3  máxima precisão (~1.5GB)
""")
print("=" * 55)
