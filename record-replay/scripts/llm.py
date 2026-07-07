#!/usr/bin/env python3
"""Ponto unico de integracao com o modelo. Troque `_provedor` pela chamada real (Claude).
Mantido como stub deterministico para o smoke test rodar sem credencial."""
import os

def _provedor(prompt: str) -> str:
    # INTEGRACAO: substituir por chamada ao Claude (Agent SDK / API).
    # Stub deterministico: nunca inventa numeros; sinaliza que precisa de humano.
    return "[RASCUNHO ESPELHO] " + prompt.strip().splitlines()[0][:180]

def gerar(prompt: str) -> str:
    if os.environ.get("ESPELHO_LLM") == "off":
        return _provedor(prompt)
    return _provedor(prompt)
