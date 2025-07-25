import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.mentoria import recomendar_mentor

# 🔐 Carrega credenciais
load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="👥 Sala do Usuário", layout="wide")
st.title("👥 Sala do Usuário")

# 📌 Identifica o usuário logado via token
token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario:
    st.error("Token inválido ou expirado.")
    st.stop()

email = usuario["email"]
st.success(f"🎯 Perfil identificado: {email}")

# 📊 Mostra alertas associados ao usuário
st.subheader("🔔 Alertas recentes")
df_alertas = pd.DataFrame(supabase.table("alertas").select("*").eq("usuario", email).execute().data)
if df_alertas.empty:
    st.info("Nenhum alerta ativo ainda. Explore setores no painel VIP.")
else:
    st.dataframe(df_alertas)

# 🎓 Sugestão de mentoria VIP
st.subheader("🎓 Mentoria sugerida")
df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
mentor = recomendar_mentor(usuario, df_usuarios)
st.success(f"Seu mentor VIP: **{mentor['email']}**")

# 🔒 Opções futuras
st.markdown("⚙️ Em breve: metas, estilo de perfil, missões e evolução tática.")