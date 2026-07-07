# Regras de seguranca do Espelho
1. Isolamento: um cliente por contexto. Nunca misturar contas nem uso interno.
2. Humano no controle: a IA le e rascunha; a gerente edita e envia. Nada sai sozinho.
3. Nunca inventar preco, prazo ou promessa que nao esteja no CRM.
4. Dado desatualizado (> STALE_HORAS): avisar antes de agir.
5. Baixa confianca (< CONFIANCA_MIN): oferecer jogadas para a gerente escolher, nao chutar.
6. PII: ao capturar jogada, remover CPF/CNPJ/email/telefone/valores.
7. WhatsApp: sem API que derrube numero; leitura por export diario; envio sempre humano.
