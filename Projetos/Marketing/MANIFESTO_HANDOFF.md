# MANIFESTO DE HANDOFF — Marketing OS

> **ATUALIZAÇÃO 2026-07-10:** O Drive foi **descontinuado como alvo de sync de docs**. A redundância agora é **Local + GitHub + GitLab** (2 remotes versionados). O Drive permanece só para **arquivos** (vídeos, gravações, planilhas, materiais a compartilhar). As seções abaixo sobre estado/stubs do Drive ficam como **registro histórico**.
**Gerado:** 2026-07-08 · **Origem:** sessão de auditoria (chat web)
**Para:** a próxima conversa (Cowork / Claude Code) que vai auditar + sincronizar.

> Este arquivo é a "foto" do que foi descoberto. As URLs do Drive são reais (verificadas nesta sessão).
> O estado em Local/GitHub está marcado como "a confirmar" — o `deploy_marketing_os.sh audit` confirma.

---

## 1. GITHUB
- Org/usuário: **`github.com/arthurgerber`**
- Repo de skills (existe): **`github.com/arthurgerber/marketing-os-skills`**
- Repos planejados (criar ao entrar em código): `plataforma-marketing`, `plataforma-comercial`, `empresa-hub`, `plataforma-cs`

## 2. ESTRUTURA NO DRIVE (URLs reais — 08/jul)
Guarda-chuva: **Marketing OS › Projetos**

| Item | Tipo | ID | URL |
|---|---|---|---|
| Marketing OS (pasta raiz) | folder | `131DWxPAXhT6LIGBZpy5ojeop8Zynzmvx` | https://drive.google.com/drive/folders/131DWxPAXhT6LIGBZpy5ojeop8Zynzmvx |
| Projetos | folder | `1qnfnrZRrMPUbTVsV6zI0zdzyoYCLxGpd` | https://drive.google.com/drive/folders/1qnfnrZRrMPUbTVsV6zI0zdzyoYCLxGpd |
| Projetos/CS | folder | `112aOIrCPM6WzcTRDYx2avaux_2YEA2QN` | https://drive.google.com/drive/folders/112aOIrCPM6WzcTRDYx2avaux_2YEA2QN |
| Projetos/Comercial | folder | `1FPh4tv8yVgUjUpPVr2D_PbRdM4zRIoBr` | https://drive.google.com/drive/folders/1FPh4tv8yVgUjUpPVr2D_PbRdM4zRIoBr |
| Projetos/Empresa | folder | `1idWNJLnXy4PczO29Y3UwiwLZoVUzoirj` | https://drive.google.com/drive/folders/1idWNJLnXy4PczO29Y3UwiwLZoVUzoirj |
| **Projetos/Marketing** | folder | *(NÃO EXISTE — criar)* | — |
| INDICE_PROJETOS | doc (3009 b) | `1A1rohv-UBF4V_mbqi0hVbNQeZVvVqpLN` | https://drive.google.com/file/d/1A1rohv-UBF4V_mbqi0hVbNQeZVvVqpLN/view |
| GUIA_ORGANIZACAO_PROJETOS | doc (946 b) | `1VkC78f0FdcFJb1DHOayS9kdchMoCOs1i` | https://drive.google.com/file/d/1VkC78f0FdcFJb1DHOayS9kdchMoCOs1i/view |
| PROJETO_CS_ARQUITETURA | doc (3446 b) | `1Bq5zpDBUot1YOD2IjwTeRnKndrCBP9sq` | https://drive.google.com/file/d/1Bq5zpDBUot1YOD2IjwTeRnKndrCBP9sq/view |
| PLATAFORMA_COMERCIAL_ARQUITETURA | doc (269 b · STUB) | `1NSMuZOHj5SNBoedS522FSFwRqGdipjee` | https://drive.google.com/file/d/1NSMuZOHj5SNBoedS522FSFwRqGdipjee/view |
| MARKETING_OS_EMPRESA_AUTOMATIZADA | doc (330 b · STUB) | `1HzGa2SyN42JEjhD2IyTzFnE4TOFZfX66` | https://drive.google.com/file/d/1HzGa2SyN42JEjhD2IyTzFnE4TOFZfX66/view |
| Blueprint_Projetos_Claude.pdf | pdf (445 b) | `1RBU28a2zMe_HL-gxvP5UgvMVKbke2wrm` | https://drive.google.com/file/d/1RBU28a2zMe_HL-gxvP5UgvMVKbke2wrm/view |

Docs de planejamento (contexto, não canônicos):
| Doc | ID | URL |
|---|---|---|
| Planejamento de projetos (síntese de ~9 respostas) | `1rZrT53425Eyyeg69yCpvx1gMN8a4Bt5HGqXLSp5Ag0U` | https://docs.google.com/document/d/1rZrT53425Eyyeg69yCpvx1gMN8a4Bt5HGqXLSp5Ag0U/edit |
| Situação CS (cargos/RH) | `1vk4YCmFNIbnGiRQYnKQ3tP_7bB9lVD2TgnO2vtABvJQ` | https://docs.google.com/document/d/1vk4YCmFNIbnGiRQYnKQ3tP_7bB9lVD2TgnO2vtABvJQ/edit |
| CS_Arquitetura_Record_Replay | `13PQIRa6wxEWZnWK79yWRWiEIIUWsH7BOCfNEQTUJKF0` | https://docs.google.com/document/d/13PQIRa6wxEWZnWK79yWRWiEIIUWsH7BOCfNEQTUJKF0/edit |
| INVENTARIO COMPLETO - Analise de Conteudo | `17UfGnQv9GOQXNor8SCPGDnEAIjIp4Om-MoVRc93n6F8` | https://docs.google.com/document/d/17UfGnQv9GOQXNor8SCPGDnEAIjIp4Om-MoVRc93n6F8/edit |

## 3. FUROS CONFIRMADOS (Drive NÃO é espelho completo)
- **AUSENTE no Drive:** `MARKETING_OS_ARQUITETURA.md` (ground truth global) — busca por título retornou vazio.
- **AUSENTE no Drive:** `PROCESSO_BASE_CLOSER.md`.
- **STUB (270–330 b):** `PLATAFORMA_COMERCIAL_ARQUITETURA`, `MARKETING_OS_EMPRESA_AUTOMATIZADA` (este diz "arquivo completo — ver Mac").
- **Conclusão:** o corpo completo dos docs mora no **Mac** (`~/Downloads/...`) e/ou **GitHub**; o Drive tem só índice + guia + 1 CS + stubs. Enforcement de sync NÃO está segurando.

## 4. CAUSA PROVÁVEL (a confirmar)
A skill de enforcement/sync provavelmente só dispara em ambiente Cowork/terminal; sessões de **chat web** gravam por fora dela → stubs e ausências. Nenhum arquivo de watchdog/auto-sync foi achado no Drive.

## 5. PENDÊNCIAS ABERTAS
1. **Recuperar fluxo de agentes/sub-agentes** (mkt, tráfego, copy, webinário, produto, funil) — provável em `MARKETING_OS_ARQUITETURA.md` / `Empresa/MARKETING_OS_EMPRESA_AUTOMATIZADA.md` (Mac/GitHub). Consolidar em `Marketing/PLATAFORMA_MARKETING_ARQUITETURA.md`.
2. **Auditar e corrigir a skill de enforcement** para gravar nos 3 lugares sempre.
3. **Tornar o Drive espelho real** (subir os ausentes, engordar os stubs) — via rclone ou conector do Drive.

## 6. LIMITE DA ORIGEM
Esta sessão foi **chat web**: sem acesso ao Mac, sem git autenticado, e o conector do Drive travou na escrita ("aprovação não recebida"). Por isso o deploy foi empacotado em script para rodar na sua máquina/Cowork.
