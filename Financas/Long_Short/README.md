# Consulta Long & Short (Streamlit)

App Streamlit para consultar operacoes em aberto da planilha Google Sheets:
`1o215MO_glpQDpRevyCL9lBUKGinqmuc8qPLTXX5sRUk`

## Regras da consulta
- Filtro 1: `Corretora`
- Filtro 2: `Cliente` (dependente da corretora)
- Apenas operacoes em aberto: `Data Fecho` (coluna `N`) igual a `0`
- Colunas exibidas:
  - `Data Montagem`
  - `Compra`
  - `Financeiro H` (coluna H)
  - `Venda`
  - `Financeiro L` (coluna L)
  - `Abertura`
  - `Evolucao`
  - `Evol %`
  - `Atual (AG)` (coluna AG)

## Executar localmente
```bash
cd Financas/Long_Short
pip install -r requirements.txt
streamlit run app.py
```

## Publicar no Streamlit Cloud
1. Suba a pasta `Financas/Long_Short` no GitHub.
2. No Streamlit Cloud (`streamlit.app`), clique em **New app**.
3. Selecione repositório/branch.
4. Em **Main file path**, informe: `Financas/Long_Short/app.py`
5. Deploy.

## Observacao
Se a aba da planilha nao for a primeira, ajuste o `GID` no menu lateral do app.
Se aparecer erro de coluna (`Corretora`/`Cliente`), ajuste:
- `Linha do cabecalho` (quando os titulos nao estao na primeira linha)
- `Fallback por letra` para `Corretora` e `Cliente` (ex.: `B`, `C`)
