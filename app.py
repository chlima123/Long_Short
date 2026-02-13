import re
import unicodedata
from typing import Iterable, Optional

import pandas as pd
import streamlit as st

SPREADSHEET_ID = "1o215MO_glpQDpRevyCL9lBUKGinqmuc8qPLTXX5sRUk"
DEFAULT_GID = "0"


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", text.lower()).strip()


def column_letter_to_index(letter: str) -> int:
    letter = letter.strip().upper()
    idx = 0
    for ch in letter:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def resolve_column(
    df: pd.DataFrame,
    aliases: Iterable[str],
    fallback_letter: Optional[str] = None,
) -> str:
    normalized_map = {normalize_text(col): col for col in df.columns}

    for alias in aliases:
        key = normalize_text(alias)
        if key in normalized_map:
            return normalized_map[key]

    if fallback_letter:
        idx = column_letter_to_index(fallback_letter)
        if 0 <= idx < len(df.columns):
            return df.columns[idx]

    raise KeyError(f"Coluna nao encontrada. Aliases: {list(aliases)}")


@st.cache_data(ttl=300)
def load_sheet(spreadsheet_id: str, gid: str) -> pd.DataFrame:
    csv_url = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
    )
    return pd.read_csv(csv_url)


def main() -> None:
    st.set_page_config(page_title="Long & Short - Consulta", layout="wide")
    st.title("Consulta Long & Short")

    with st.sidebar:
        st.subheader("Fonte")
        gid = st.text_input("GID da aba", value=DEFAULT_GID, help="Normalmente 0")
        st.caption(f"Planilha: `{SPREADSHEET_ID}`")

    try:
        df = load_sheet(SPREADSHEET_ID, gid)
    except Exception as exc:
        st.error(f"Nao foi possivel carregar a planilha. Detalhe: {exc}")
        st.stop()

    try:
        col_corretora = resolve_column(df, ["Corretora"])
        col_cliente = resolve_column(df, ["Cliente"])
        col_data_fecho = resolve_column(df, ["Data Fecho", "DataFecho"], "N")
        col_data_montagem = resolve_column(df, ["Data Montagem", "DataMontagem"])
        col_compra = resolve_column(df, ["Compra"])
        col_financeiro_h = resolve_column(df, ["Financeiro Compra", "Financeiro"], "H")
        col_venda = resolve_column(df, ["Venda"])
        col_financeiro_l = resolve_column(df, ["Financeiro Venda"], "L")
        col_abertura = resolve_column(df, ["Abertura"])
        col_evolucao = resolve_column(df, ["Evolucao", "Evolução"])
        col_evol_pct = resolve_column(df, ["Evol %", "Evol%", "Evolucao %", "Evolução %"])
        col_atual_ag = resolve_column(df, ["Atual"], "AG")
    except KeyError as exc:
        st.error(str(exc))
        st.info("Revise os nomes das colunas na planilha para alinhar o app.")
        st.stop()

    # Operacao em aberto: coluna N/Data Fecho igual a 0.
    data_fecho_num = pd.to_numeric(df[col_data_fecho], errors="coerce")
    mask_abertas = (data_fecho_num == 0) | (df[col_data_fecho].astype(str).str.strip() == "0")
    abertas = df.loc[mask_abertas].copy()

    corretoras = sorted(
        value for value in abertas[col_corretora].dropna().astype(str).str.strip().unique() if value
    )
    if not corretoras:
        st.warning("Nenhuma operacao em aberto encontrada para os filtros atuais.")
        st.stop()

    corretora_sel = st.selectbox("Corretora", corretoras)
    base_cliente = abertas[abertas[col_corretora].astype(str).str.strip() == corretora_sel]

    clientes = sorted(
        value for value in base_cliente[col_cliente].dropna().astype(str).str.strip().unique() if value
    )
    if not clientes:
        st.warning("Nenhum cliente encontrado para a corretora selecionada.")
        st.stop()

    cliente_sel = st.selectbox("Cliente", clientes)
    consulta = base_cliente[base_cliente[col_cliente].astype(str).str.strip() == cliente_sel].copy()

    output_columns = [
        col_data_montagem,
        col_compra,
        col_financeiro_h,
        col_venda,
        col_financeiro_l,
        col_abertura,
        col_evolucao,
        col_evol_pct,
        col_atual_ag,
    ]
    output = consulta[output_columns].rename(
        columns={
            col_data_montagem: "Data Montagem",
            col_compra: "Compra",
            col_financeiro_h: "Financeiro H",
            col_venda: "Venda",
            col_financeiro_l: "Financeiro L",
            col_abertura: "Abertura",
            col_evolucao: "Evolucao",
            col_evol_pct: "Evol %",
            col_atual_ag: "Atual (AG)",
        }
    )

    st.subheader("Operacoes em aberto")
    st.caption(f"Corretora: {corretora_sel} | Cliente: {cliente_sel} | Registros: {len(output)}")
    st.dataframe(output, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
