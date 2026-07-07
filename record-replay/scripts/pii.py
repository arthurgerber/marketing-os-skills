#!/usr/bin/env python3
"""Remocao de PII antes de guardar jogadas na biblioteca (guarda o padrao, nao o dado)."""
import re

_SUBS = [
    (r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "[CPF]"),
    (r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b", "[CNPJ]"),
    (r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL]"),
    (r"\+?\d{2}\s?\(?\d{2}\)?\s?9?\d{4}-?\d{4}", "[TELEFONE]"),
    (r"R\$\s?\d[\d.,]*", "[VALOR]"),
]

def scrub(texto: str) -> str:
    texto = texto or ""
    for pad, rep in _SUBS:
        texto = re.sub(pad, rep, texto)
    return texto
