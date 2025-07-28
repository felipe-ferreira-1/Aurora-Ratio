import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]
from utils.fiscal import gerar_nota_fiscal, exportar_para_contador, calcular_imposto # pyright: ignore[reportMissingImports]
from utils.temporal_gate import gerar_portao_temporal # pyright: ignore[reportMissingImports]

load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="👑 Sala do CEO", layout="wide")
st.title("👑 Sala do CEO")

token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario or usuario["cargo"] != "ceo":
    st.error("Acesso restrito ao perfil CEO.")
    st.stop()

email = usuario["email"]
st.success(f"Acesso CEO: {email}")

df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
df_usuarios["valor_pago"] = df_usuarios["plano"].map({"mensal": 50, "anual": 500})
arrecadado = df_usuarios["valor_pago"].sum()
moeda = "R$"

st.metric("💰 Total arrecadado", f"{moeda} {arrecadado:.2f}")
st.metric("📊 Usuários ativos", len(df_usuarios))

st.subheader("📄 Emitir nota fiscal")
alvo = st.selectbox("Destinatário", df_usuarios["email"])
plano_nf = st.selectbox("Plano", ["mensal", "anual"])
valor_nf = {"mensal": 50, "anual": 500}[plano_nf]
if st.button("Gerar NFE"):
    nota = gerar_nota_fiscal({"email": alvo, "id": 123}, plano_nf, valor_nf)
    st.json(nota)

st.subheader("🧾 Exportação contábil")
st.dataframe(exportar_para_contador(df_usuarios))

st.subheader("🛡️ Cálculo de impostos")
pais = st.selectbox("País", ["br", "us", "eu"])
plano = st.selectbox("Plano fiscal", ["mensal", "anual"])
imposto = calcular_imposto(pais, plano)
st.metric("Imposto estimado", f"{moeda} {imposto:.2f}")

st.subheader("🕰️ Criar acesso temporário")
email_sim = st.text_input("Email para simular acesso")
cargo_sim = st.selectbox("Cargo temporário", ["usuario", "vip", "ceo", "gamemaster"])
if st.button("Gerar token temporal"):
    token_temp = gerar_portao_temporal(email_sim, cargo_sim)
    st.code(token_temp)