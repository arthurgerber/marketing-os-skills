# Scores de Probabilidade por Motivo

> Escala 0–100. Usado para ordenar e colorir os leads nas planilhas.
> Verde ≥70 | Amarelo 55–69 | Laranja 40–54 | Vermelho <40

---

## Grupo VR

```javascript
const MOTIVO_SCORE = {
  'Fechamento na Segunda Call':              80,
  'Analise de Contrato':                    75,
  'Sem sócio presente na call':             70,
  'Quer falar com Sócio':                   65,
  'Quer conhecer alguma loja':              60,
  'Erro de Sistema (impossível fazer a call)': 55,
  'Erro Closer (cite qual erro)':           45,
  'Lead com interesse, mas não é o momento': 40,
  'Não é o momento':                        35,
  'Modelo de negócio não fez sentido':      35,
  'Objeção Forte (diga qual)':              35,
  'Expectativas desalinhadas':              25,
  'Sem capacidade financeira':              25,
};
```

---

## Grupo Lazari

```javascript
const MOTIVO_SCORE = {
  'Não é o momento':                        65,
  'Precisar esperar o cartão virar':        60,
  'Reunião interrompida':                   55,
  'Não toma decisão na hora (analítica)':   50,
  'Não toma decisão sem o marido/esposa':   50,
  'Não tem urgência':                       40,
  'Expectativas desalinhadas':              30,
  'Sem capacidade financeira':              20,
};
```

---

## Grupo Silva

```javascript
const MOTIVO_SCORE = {
  'Aguardando o pagamento':                 80,
  'Analisando o contrato':                  75,
  'Analisando Proposta':                    70,
  'Decisor não entrou / Esposa / Sócio':    65,
  'Decisor não entrou':                     65,
  'Precisa falar com esposa/sócio':         60,
  'Call Interompida':                       55,
  'Cliente precisou sair':                  55,
  'Internet deu problema':                  55,
  'Não é o momento':                        40,
  'Expectativas desalinhadas':              30,
  'Sem capacidade financeira':              20,
  'Não responde mais':                      15,
  'Fechou com outra empresa':               10,
  'Erro de qualificação':                   10,
  'Não usar mais':                           5,
};
```

---

## Como ajustar scores

Se um motivo novo aparecer no dashboard que não está na lista:
- Avaliar a probabilidade relativa de fechamento
- Adicionar ao dicionário da empresa e atualizar este arquivo
- Sugestão: motivos de "espera ativa" (contrato, pagamento) ficam ≥70;
  motivos de "objeção" ficam 30–55; motivos de "desqualificação" ficam <30
