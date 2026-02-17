# Rotina VOTOS (n8n)

Este diretório contém uma rotina para n8n que:
- monitora a caixa de e-mail `john.sh.watson@outlook.com` via IMAP;
- filtra mensagens cujo assunto contenha `VOTOS`;
- converte anexos `.docx` em `.pdf` via script Python;
- encaminha os PDFs para `charles.santos.lima@gmail.com`.

## Arquivos
- `workflow_n8n_votos.json`: workflow para importar no n8n.
- `docx_to_pdf.py`: script Python chamado pelo nó `Execute Command`.

## Pré-requisitos (Linux, n8n self-hosted)
- `python3` instalado.
- LibreOffice instalado (`libreoffice` ou `soffice` no PATH).
- Acesso de escrita em `/tmp`.
- Credenciais configuradas no n8n:
  - IMAP da conta Outlook de origem.
  - SMTP da conta Outlook de envio.
- Nó `Execute Command` habilitado no n8n (`N8N_ENABLE_EXECUTE_COMMAND=true`).

## Instalação no Linux (Ubuntu/Debian)
1. Instale dependências:
   - `sudo apt-get update`
   - `sudo apt-get install -y python3 libreoffice nodejs npm`
2. Valide comandos:
   - `python3 --version`
   - `node --version`
   - `npm --version`
   - `libreoffice --version` (ou `soffice --version`)
3. Instale o n8n via npm:
   - `sudo npm install -g n8n`
4. Suba o n8n com `Execute Command` habilitado:
   - `export N8N_ENABLE_EXECUTE_COMMAND=true`
   - `n8n`

## Passo a passo
1. Copie `docx_to_pdf.py` para o servidor n8n em `/opt/n8n/scripts/docx_to_pdf.py`.
2. Dê permissão de execução:
   - `chmod +x /opt/n8n/scripts/docx_to_pdf.py`
3. No n8n, importe `workflow_n8n_votos.json`.
4. No workflow, substitua os placeholders de credenciais:
   - `SEU_ID_CREDENCIAL_IMAP`
   - `SEU_ID_CREDENCIAL_SMTP`
5. Verifique se o nó `Execute Command` aponta para:
   - `python3 /opt/n8n/scripts/docx_to_pdf.py "{{$json.docxPath}}" "{{$json.pdfPath}}"`
6. Execute um teste com e-mail contendo `VOTOS` no assunto e anexo `.docx`.
7. Ative o workflow.

## n8n via npm como serviço Linux (systemd)
- Garanta que o usuário do serviço n8n tenha permissão de leitura/execução em:
  - `/opt/n8n/scripts/docx_to_pdf.py`
- Exemplo de instalação para o usuário `n8n`:
  - `sudo npm install -g n8n`
- No arquivo do serviço, confirme a variável:
  - `Environment=\"N8N_ENABLE_EXECUTE_COMMAND=true\"`
- Após alterações no serviço:
  - `sudo systemctl daemon-reload`
  - `sudo systemctl restart n8n`

## Observações
- O filtro do assunto usa `contains` e é sensível ao texto; ajuste se quiser aceitar variações.
- Apenas anexos `.docx` são processados; outros anexos são ignorados.
- Para limpeza de arquivos temporários em `/tmp`, pode-se adicionar um nó extra após o envio.
- O script detecta automaticamente `libreoffice` ou `soffice`.
