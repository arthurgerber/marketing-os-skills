#!/usr/bin/env python3
"""Record & Replay: rascunha resposta a partir das jogadas humanas. Humano valida antes de enviar."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.llm import gerar

def _carregar_jogadas(jogadas_dir: Path, tipo: str) -> str:
    f = Path(jogadas_dir) / f"{tipo}.md"
    if f.exists():
        return f.read_text(encoding="utf-8", errors="ignore")
    return ""

def rascunhar(tipo: str, confianca: float, contexto: dict, jogadas_dir: Path, cfg) -> dict:
    jogadas = _carregar_jogadas(jogadas_dir, tipo)
    if confianca < cfg.CONFIANCA_MIN or not jogadas:
        # baixa confianca: nao chuta, devolve as jogadas para a gerente escolher
        return {"tipo": tipo, "confianca": confianca, "precisa_escolha_humana": True,
                "jogadas_sugeridas": jogadas[:1500], "rascunho": None, "validado": False}
    prompt = (f"Situacao: {tipo}. Use SOMENTE o tom e os padroes das jogadas abaixo e os fatos do CRM. "
              f"NUNCA invente preco ou prazo que nao esteja no contexto.\n\nJOGADAS:\n{jogadas[:2000]}")
    rascunho = gerar(prompt)
    return {"tipo": tipo, "confianca": confianca, "precisa_escolha_humana": False,
            "rascunho": rascunho, "validado": False}  # validado=False: humano aperta enviar
