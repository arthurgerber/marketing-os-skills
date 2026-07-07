---
name: fup-mensal
description: >
  Gera planilhas de Follow-Up (FUP) por closer para os Grupos VR, Silva e Lazari.
  Use SEMPRE que o usuário mencionar FUP, follow-up, planilha de leads, relatório de
  não fechamentos, leads do mês, closers, ou pedir qualquer extração do dashboard
  comercial. Exemplos: "gera o FUP do VR", "faz o follow-up do Silva de junho",
  "quero os leads do Lazari", "atualiza as planilhas dos closers", "quais leads têm
  follow marcado", "faz o FUP do período X ao Y". Aciona mesmo que o usuário não use
  a palavra exata "FUP".
---

# FUP Mensal — Grupos VR, Silva e Lazari

## PRIMEIRO: perguntar as 2 variáveis obrigatórias

Antes de qualquer ação, fazer estas duas perguntas em uma única mensagem:

> **Para gerar o FUP, preciso de duas informações:**
> 1. **Qual empresa?** VR / Silva / Lazari / Todas
> 2. **Qual período?** (ex: 01/06 a 27/06)

Não prosseguir sem as respostas. Se o usuário já informou empresa ou período na
mensagem original, considerar como respondido — não perguntar de novo.

Filtro de follow **não perguntar** — padrão é sempre "todos". Só aplicar filtro
se o usuário mencionar explicitamente ("só os com follow ativo", "só sem follow").

Com as respostas em mãos, definir internamente:
```
EMPRESA  = "VR" | "Silva" | "Lazari" | "Todas"
PERIODO  = "01/06 a 27/06"  // exatamente como o usuário informou
NOME_MES = "Jun/2026"        // derivado do período, para nomear pasta e arquivo
```

## Configuração das empresas

Leia o arquivo de referência completo antes de começar:
→ `references/empresas.md` — URLs, IDs de pastas no Drive, lista de closers por empresa

Convenção de nome para pasta mensal no Drive: `FUP Grupo [EMPRESA] — [NOME_MES]`
Exemplos: `FUP Grupo VR — Jul/2026`, `FUP Grupo Lazari — Ago/2026`

## Processo passo a passo

### 1. Acessar o dashboard

Navegar para a URL da empresa (ver `references/empresas.md`). Se redirecionar ou der erro:
- Informar ao usuário que a URL pode ter mudado
- Pedir a URL atual
- Atualizar `references/empresas.md` com a nova URL para uso futuro

Após carregar, clicar no link "Dashboard" do menu se necessário.

### 2. Configurar o período

Na aba **Vendas** (não usar /follow-ups — essa página mostra apenas leads com follow
ativo e perde os demais):
- Selecionar o intervalo de datas conforme PERIODO
- Confirmar que o heading mostra "Vendas — DD/MM – DD/MM"

### 3. Extrair os leads

Com "Todos os closers" selecionado e período correto:

**Instalar o parser no browser (executar uma vez):**
```javascript
function parseLeads(text, motivo) {
  const leads = [];
  const lines = text.split('\n').map(l=>l.trim()).filter(l=>l);
  const FOLLOW = new Set(['Sem follow','Follow ativo','Em acompanhamento','Sem Follow']);
  const isPhone = l => /^(?:\+?55[\s()\-\d]{8,}|\+[1-9][\d\s()\-]{8,})$/.test(l.replace(/\s/g,'').replace(/[()]/g,''));

  let i = 0;
  if(lines[0]?.startsWith('Motivo:')) i = 1;

  while(i < lines.length - 1) {
    if(FOLLOW.has(lines[i+1])) {
      const lead = { motivo, nome: lines[i], followStatus: lines[i+1],
        status:'', data:'', telefone:'', closer:'', sdr:'', canal:'', explicacao:'', observacoes:'' };
      i += 2;

      if(i < lines.length && /Realizada/i.test(lines[i])) { lead.status = lines[i]; i++; }
      if(i < lines.length && /\d{2}\/\d{2} às/.test(lines[i])) { lead.data = lines[i]; i++; }
      if(i < lines.length && isPhone(lines[i])) { lead.telefone = lines[i]; i++; }
      if(i < lines.length && lines[i] === 'Closer:') { i++; if(i<lines.length){lead.closer=lines[i];i++;} }
      if(i < lines.length && lines[i] === 'SDR:') { i++; if(i<lines.length){lead.sdr=lines[i];i++;} }
      if(i < lines.length && /^Criado em/.test(lines[i])) i++;
      while(i < lines.length && /^(Agendado|Reagendado|Canal:)/.test(lines[i])) {
        if(lines[i].startsWith('Canal:')) { lead.canal=lines[i].replace('Canal:','').trim(); }
        i++;
      }
      while(i < lines.length && lines[i] !== 'EXPLICAÇÃO DO PORQUÊ NÃO FECHOU') {
        if(i+1 < lines.length && FOLLOW.has(lines[i+1])) { i = lines.length; break; }
        i++;
      }
      if(i >= lines.length) { leads.push(lead); continue; }
      if(lines[i] === 'EXPLICAÇÃO DO PORQUÊ NÃO FECHOU') i++;
      const explLines = [];
      while(i < lines.length && lines[i] !== 'OBSERVAÇÕES') {
        if(i+1 < lines.length && FOLLOW.has(lines[i+1])) break;
        if(FOLLOW.has(lines[i])) break;
        explLines.push(lines[i]); i++;
      }
      lead.explicacao = explLines.join(' ').trim();
      if(i < lines.length && lines[i] === 'OBSERVAÇÕES') {
        i++;
        const obsLines = [];
        while(i < lines.length) {
          if(i+1 < lines.length && FOLLOW.has(lines[i+1])) break;
          if(FOLLOW.has(lines[i])) break;
          obsLines.push(lines[i]); i++;
        }
        lead.observacoes = obsLines.join(' ').trim();
      }
      leads.push(lead);
    } else { i++; }
  }
  return leads;
}
window.__parseLeads = parseLeads;
window.__all_leads = [];
```

**Para cada botão de motivo:**
```javascript
// Clicar no botão de motivo (index i)
const btns = Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.match(/\d+\s*\(\d+%\)/));
['pointerover','pointerenter','pointerdown','mousedown','pointerup','mouseup','click']
  .forEach(evt=>btns[i].dispatchEvent(new PointerEvent(evt,{bubbles:true,cancelable:true,pointerId:1})));
await new Promise(r=>setTimeout(r,1200));

const dialog = document.querySelector('[role="dialog"]');
window.__dialogText = dialog?.innerText || '';
const motivoName = window.__dialogText.split('\n')[0].replace('Motivo:','').split('—')[0].trim();
const leads = window.__parseLeads(window.__dialogText, motivoName);
window.__all_leads = window.__all_leads.concat(leads);

// Fechar dialog
const cb = Array.from(document.querySelectorAll('button')).find(b=>b.textContent.trim()==='Close');
if(cb) cb.click();
await new Promise(r=>setTimeout(r,400));
```

Repetir para todos os botões de motivo. Ao final **validar obrigatoriamente**:
```javascript
// 1. Total deve bater com "X não fechou" na página
console.log('Total leads:', window.__all_leads.length);

// 2. Nenhum closer deve estar vazio — se houver, parar e depurar o parser
const semCloser = window.__all_leads.filter(l => !l.closer);
console.log('Leads sem closer:', semCloser.length);
if(semCloser.length > 0) console.table(semCloser.slice(0,5));
```

Se `semCloser.length > 0`, **não gerar xlsx**. Verificar o parser antes de continuar.

**Filtro de follow (só aplicar se o usuário solicitou):**
```javascript
// Apenas Follow ativo:
window.__all_leads = window.__all_leads.filter(l => l.followStatus === 'Follow ativo');
// Apenas Sem follow:
window.__all_leads = window.__all_leads.filter(l => l.followStatus === 'Sem follow');
```

### 4. Gerar os xlsx (coloridos, via SheetJS no browser)

Carregar SheetJS:
```javascript
const s1 = document.createElement('script');
s1.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
document.head.appendChild(s1);
await new Promise((res,rej)=>{s1.onload=res;s1.onerror=rej;});
```

Consultar os scores de motivo em `references/scores.md` para a empresa correta.

Gerar e baixar um xlsx por closer:
```javascript
// PERIODO e NOME_MES definidos no início da skill
const PERIODO_LABEL = 'PERIODO';  // substituir pelo valor real: ex "01/06 a 27/06"

const MOTIVO_SCORE = { /* scores da empresa — ver references/scores.md */ };

function getNota(motivo) { return MOTIVO_SCORE[motivo] || 30; }
function getLabel(n) {
  if(n>=70) return '🟢 Alta';
  if(n>=55) return '🟡 Média-Alta';
  if(n>=40) return '🟠 Média';
  return '🔴 Baixa';
}

const byCloser = {};
window.__all_leads.forEach(l => {
  if(!byCloser[l.closer]) byCloser[l.closer] = new Map();
  const key = (l.nome||'').toLowerCase()+'|'+(l.telefone||'')+'|'+(l.motivo||'');
  if(!byCloser[l.closer].has(key)) byCloser[l.closer].set(key, l);
});

for(const [closer, leadsMap] of Object.entries(byCloser)) {
  let leads = [...leadsMap.values()].sort((a,b) => getNota(b.motivo) - getNota(a.motivo));
  const wb = XLSX.utils.book_new();

  // === SHEET 1: Leads FUP ===
  const headers = ['Nota','Probabilidade','Motivo de Não Fechamento','Nome','Telefone',
    'Data Reunião','Follow Status','Canal','SDR','Explicação','Observações',
    'Status FUP','Data Contato','Resultado'];
  const rows = [headers];
  leads.forEach(l => {
    const nota = getNota(l.motivo);
    rows.push([nota, getLabel(nota), l.motivo, l.nome, l.telefone, l.data,
      l.followStatus, l.canal, l.sdr, l.explicacao, l.observacoes, '', '', '']);
  });
  const ws1 = XLSX.utils.aoa_to_sheet(rows);
  ws1['!cols'] = [8,16,32,24,18,16,14,18,18,45,45,15,14,20].map(w=>({wch:w}));
  ws1['!freeze'] = {xSplit:0, ySplit:1};
  XLSX.utils.book_append_sheet(wb, ws1, 'Leads FUP');

  // === SHEET 2: Resumo ===
  const alta = leads.filter(l=>getNota(l.motivo)>=70).length;
  const mediaAlta = leads.filter(l=>getNota(l.motivo)>=55&&getNota(l.motivo)<70).length;
  const media = leads.filter(l=>getNota(l.motivo)>=40&&getNota(l.motivo)<55).length;
  const baixa = leads.filter(l=>getNota(l.motivo)<40).length;
  const motivoCounts = {};
  leads.forEach(l=>{ motivoCounts[l.motivo]=(motivoCounts[l.motivo]||0)+1; });

  const resumoRows = [
    [`FUP — ${closer} | ${PERIODO_LABEL}`], [],
    ['Indicador','Qtd','Prioridade'],
    ['Total de leads',leads.length,''],
    ['🟢 Alta probabilidade (≥70)',alta,'Ligar hoje'],
    ['🟡 Média-Alta (55–69)',mediaAlta,'Ligar esta semana'],
    ['🟠 Média (40–54)',media,'Vale tentar'],
    ['🔴 Baixa (<40)',baixa,'Último recurso'],
    [], ['Motivo','Qtd',''],
    ...Object.entries(motivoCounts).sort((a,b)=>b[1]-a[1]).map(([m,c])=>[m,c,''])
  ];
  const ws2 = XLSX.utils.aoa_to_sheet(resumoRows);
  ws2['!cols'] = [{wch:35},{wch:12},{wch:20}];
  XLSX.utils.book_append_sheet(wb, ws2, 'Resumo');

  // Download
  const safeName = closer.normalize('NFD').replace(/[̀-ͯ]/g,'')
    .replace(/[^\w\s-]/g,'').trim().replace(/\s+/g,'_');
  XLSX.writeFile(wb, `FUP_[EMPRESA]_${safeName}.xlsx`);
  await new Promise(r=>setTimeout(r,500));
}
```

### 5. Criar pasta mensal e fazer upload para o Google Drive

**Se for um período novo** (pasta mensal ainda não existe):
```
mcp__33817896-01eb-4fed-9962-1bbf34c33fea__create_file
  title: "FUP Grupo [EMPRESA] — [NOME_MES]"
  contentMimeType: application/vnd.google-apps.folder
  parentId: [ID pasta-raiz do grupo — ver references/empresas.md]
```

Para cada closer, navegar à pasta do closer no Drive e fazer upload:

```javascript
// Abrir pasta do closer no Drive
// URL: https://drive.google.com/drive/folders/[FOLDER_ID]

const btn = Array.from(document.querySelectorAll('button,div[role="button"]'))
  .find(b=>b.textContent.trim()==='Novo');
['pointerover','pointerenter','pointerdown','mousedown','pointerup','mouseup','click']
  .forEach(evt=>btn.dispatchEvent(new PointerEvent(evt,{bubbles:true,cancelable:true,pointerId:1})));
await new Promise(r=>setTimeout(r,700));
const items = Array.from(document.querySelectorAll('[role="menuitem"]'))
  .filter(el=>el.textContent.includes('Upload de arquivo'));
if(items[0]) items[0].click();
```

Usar `mcp__Claude_in_Chrome__find` para localizar o `input[type="file"]` e depois
`mcp__Claude_in_Chrome__file_upload` com o caminho do arquivo em Downloads.

## Tratamento de novos closers

Se aparecer um closer no dashboard que não está em `references/empresas.md`:
1. Criar pasta no Drive dentro da pasta mensal da empresa
2. Registrar o novo ID em `references/empresas.md`
3. Fazer upload normalmente

## Ao finalizar

Reportar ao usuário:
- Lista de closers com quantidade de leads cada
- Links para as pastas no Drive (pasta mensal da empresa)
- Qualquer closer com 0 leads (não gerou arquivo)
