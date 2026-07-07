#!/usr/bin/env python3
"""Registro dinamico de subagentes. Adicionar um novo = registrar, sem reescrever o orquestrador.
Isso destrava a organizacao: nao ha limite de 5 subagentes."""
_AGENTES = {}

def registrar(nome: str, fn, descricao: str = ""):
    _AGENTES[nome] = {"fn": fn, "descricao": descricao}

def obter(nome: str):
    a = _AGENTES.get(nome)
    return a["fn"] if a else None

def listar() -> dict:
    return {k: v["descricao"] for k, v in _AGENTES.items()}
