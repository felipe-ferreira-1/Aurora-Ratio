import streamlit as st
import pandas as pd
from datetime import date

def mostrar_fluxo(supabase, email):
    st.subheader("📊 Transações do Império")

    # 🔄 Consulta da tabela
    dados = supabase.table("transacoes").select("*").execute().data
    df_fin = pd.DataFrame(dados)

    if df_fin.empty:
        st.info("Nenhuma transação registrada ainda.")
        return

    # 📈 Gráfico e tabela
    df_fin["data"] = pd.to_datetime(df_fin["data"])
    df_fin["valor"] = df_fin["valor"].astype(float)
    st.line_chart(df_fin.set_index("data")["valor"])
    st.dataframe(df_fin)

def registrar_transacao(supabase, email):
    st.subheader("🧾 Nova entrada ou saída")

    tipo = st.selectbox("Tipo de operação", ["entrada", "saída"])
    valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0)
    descricao = st.text_input("Descrição da transação")
    data = st.date_input("Data da operação", value=date.today())

    if st.button("Salvar transação"):
        supabase.table("transacoes").insert({
            "tipo": tipo,
            "valor": valor,
            "descricao": descricao,
            "data": str(data),
            "autor": email
        }).execute()
        st.success("Transação registrada com sucesso!")