# PROJETO CS — Customer Success
**Status:** Iniciando | **Data:** 2026-06-30  
**Problema:** CS com problemas na empresa — solução via agentes + plataforma  
**Owner:** Arthur Gerber

---

## PROBLEMA A RESOLVER

> *[Arthur preenche aqui: quais são as dores específicas do CS?]*  
> Exemplos: tempo de resposta alto, clientes churning sem aviso, processo de onboarding falho, falta de visibilidade de métricas, atendimento manual sobrecarregado...

---

## SETORES DO CS (cada um vira um módulo da plataforma)

```
CS — Customer Success
│
├── 📥 ATENDIMENTO
│   ├── Agente WhatsApp (responde, triagem, encaminha)
│   ├── Agente Email (responde dúvidas padrão)
│   └── Agente Urgência (detecta problemas críticos e escala)
│
├── 🚀 ONBOARDING
│   ├── Agente Boas-Vindas (ativa novo cliente, envia materiais)
│   ├── Agente Acompanhamento (verifica se está usando o produto)
│   └── Agente Check-in (contato nos dias 7, 14, 30)
│
├── 🔴 RETENÇÃO / ANTI-CHURN
│   ├── Agente Monitor (detecta sinais de risco: sumiu, sem resposta, reclama)
│   ├── Agente Reativação (aborda clientes em risco antes do churn)
│   └── Agente Diagnóstico (identifica por que está pensando em sair)
│
├── 📊 MÉTRICAS CS
│   ├── Agente NPS (coleta e analisa net promoter score)
│   ├── Agente Relatório (gera relatório semanal de saúde da base)
│   └── Dashboard CS (visão geral — quantos ativos, em risco, churned)
│
└── 🔗 INTEGRAÇÃO COM OUTRAS PLATAFORMAS
    ├── Recebe dados da Plataforma Comercial (quem fechou → entra no CS)
    ├── Alimenta Empresa Hub (métricas de retenção, NPS)
    └── Alerta closers quando cliente volta com objeção
```

---

## COMO OS SETORES SE COMUNICAM

```
[Plataforma Comercial]
  → novo cliente fechou → aciona Agente Boas-Vindas do CS
  
[Agente Monitor do CS]
  → detecta cliente em risco → avisa líder + agente de Retenção
  
[Agente Retenção]
  → aborda cliente → registra resposta no banco
  → se precisa de closer → avisa Plataforma Comercial
  
[Dashboard CS]
  ← lê tudo do banco (Supabase) ← exibe saúde da base em tempo real
```

---

## STACK TÉCNICA (mesma das outras plataformas)

- **Banco:** Supabase (tabelas: clientes, interações, status, nps)
- **Backend:** Python / N8N para automações
- **Frontend:** Next.js + shadcn/ui (mesma base da Plataforma Comercial)
- **WhatsApp:** WhatsApp Business API (via N8N ou Make)
- **Skills ativas:** analisa-video, devstack, auto-qa, watchdog, debugger

---

## PRÓXIMOS PASSOS

1. ⏳ Arthur define: qual o problema principal do CS agora?
2. ⏳ Mapear: quais clientes, qual volume, qual canal de atendimento
3. ⏳ Montar MVP: começar pelo módulo mais urgente
4. ⏳ Testar em 1 grupo antes de expandir para todos os sócios

---

## ENFORCEMENT (padrão Marketing OS)

```
ANTES de executar:
  □ Entendeu o problema real do cliente (não só o ticket)?
  □ Tem acesso ao histórico desse cliente?
  □ Verificou se outro agente já está tratando isso?

DURANTE:
  □ Seguindo processo sem atalhos?
  □ Registrando tudo no banco (rastreabilidade)?

ANTES de entregar:
  □ Cliente foi realmente resolvido (não só respondido)?
  □ Próximo follow-up agendado?
```

---

*Projeto CS — Marketing OS / Grupos VR, Silva, Lazari*
