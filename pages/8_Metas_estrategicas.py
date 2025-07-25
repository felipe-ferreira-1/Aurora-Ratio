import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.metas_ai import metas_para_usuario

load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🎯 Metas Estratégicas", layout="wide")
st.title("🎯 Painel de Metas Estratégicas")

token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario:
    st.error("Token inválido ou usuário não encontrado.")
    st.stop()

email = usuario["email"]
cargo = usuario["cargo"]
st.success(f"Perfil: {email} ({cargo.upper()})")

st.subheader("🧠 Metas mensais sugeridas pela IA")
df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
metas = metas_para_usuario(email, df_usuarios)
if metas:
    st.write("Plano estratégico gerado automaticamente:")
    st.json(metas)
else:
    st.info("Nenhuma meta atribuída no momento.")

st.subheader("📌 Nova meta manual")
objetivo = st.text_input("Meta")
prazo = st.date_input("Prazo final")
if st.button("Salvar meta"):
    supabase.table("metas").insert({
        "email": email,
        "objetivo": objetivo,
        "prazo": str(prazo)
    }).execute()
    st.success("Meta registrada com sucesso.")

st.subheader("🧾 Histórico de metas")
historico = supabase.table("metas").select("*").eq("email", email).execute().data
st.dataframe(pd.DataFrame(historico))