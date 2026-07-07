#!/usr/bin/env python3
"""Classifica a situacao da conversa. Sempre regex com re.IGNORECASE (padrao universal)."""
import re

PADROES = {
    "reembolso":  r"REEMBOLS|CANCELA|ESTORN|N.O QUERO MAIS|QUERO SAIR|DEVOLU",
    "objecao":    r"CARO|N.O TENHO TEMPO|N.O FUNCIONA|N.O VI RESULTAD|T. DIF.CIL|D.VIDA",
    "onboarding": r"COME.AR|PRIMEIRO PASSO|COMO FUN|ONBOARD|IN.CIO",
    "elogio":     r"OBRIGAD|AMEI|EXCELENTE|MUITO BOM|PERFEITO|ajudou",
    "check_in":   r"OI|OL.|BOM DIA|BOA TARDE|TUDO BEM|ACOMPANH",
}

def classificar(texto: str):
    """Retorna (tipo, confianca 0..1). Conta ocorrencias por padrao."""
    texto = texto or ""
    escores = {}
    for tipo, pad in PADROES.items():
        n = len(re.findall(pad, texto, re.IGNORECASE))
        if n:
            escores[tipo] = n
    if not escores:
        return ("check_in", 0.3)
    tipo = max(escores, key=escores.get)
    total = sum(escores.values())
    confianca = min(1.0, 0.4 + 0.2 * escores[tipo]) if total else 0.3
    # reembolso e objecao sao criticos: nunca deixar passar como check_in
    if "reembolso" in escores:
        return ("reembolso", max(confianca, 0.7))
    return (tipo, round(confianca, 2))
