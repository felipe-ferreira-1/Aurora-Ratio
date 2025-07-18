import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.logger import registrar_acao

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🕹️ Painel do Game Master", layout="wide")
st.title("🧙‍♂️ Painel do Game Master")

token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario or usuario["cargo"] != "gamemaster":
    st.error("Acesso restrito ao perfil Game Master.")
    st.stop()

email = usuario["email"]
st.success(f"Acesso concedido: {email}")

st.subheader("📋 Auditoria Imperial")
logs_raw = supabase.table("auditoria").select("*").execute().data
st.dataframe(pd.DataFrame(logs_raw))

st.subheader("📊 Fluxo financeiro imperial")
df_fin = pd.DataFrame(supabase.table("transacoes").select("*").execute().data)
if not df_fin.empty:
    df_fin["data"] = pd.to_datetime(df_fin["data"])
    st.line_chart(df_fin.set_index("data")["valor"])
    st.dataframe(df_fin)

st.subheader("💸 Retirada imperial")
df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
df_usuarios["valor_pago"] = df_usuarios["plano"].map({"mensal": 50, "anual": 500})
total = df_usuarios["valor_pago"].sum()
moeda = "R$"

valor_retirada = st.number_input("Valor da retirada", min_value=0.0, max_value=float(total))
destino = st.text_input("Destino bancário")
if st.button("Executar retirada"):
    registrar_acao(email, f"Retirada de {valor_retirada} → {destino}", "localhost", "gamemaster")
    st.success(f"{moeda} {valor_retirada:.2f} enviado para {destino}")

st.subheader("🏰 Conselho Imperial")
membros = df_usuarios[df_usuarios["cargo"].isin(["ceo", "gamemaster"])]
for _, m in membros.iterrows():
    st.markdown(f"👤 {m['email']} — {m['cargo'].upper()}")
st.text_area("📜 Discussão interna dos conselheiros")
from utils.fluxo_caixa import mostrar_fluxo

mostrar_fluxo(supabase, email)