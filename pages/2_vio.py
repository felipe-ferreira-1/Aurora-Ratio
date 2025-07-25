import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.ia_predictor import sugestao_com_dados
from utils.metas_ai import metas_para_usuario

# 🔐 Conecta Supabase
load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="💎 Painel VIP Estratégico", layout="wide")
st.title("💎 Painel VIP Estratégico")

# 📌 Token do usuário VIP
token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario or usuario["cargo"] != "vip":
    st.error("Acesso restrito ao perfil VIP.")
    st.stop()

email = usuario["email"]
st.success(f"Acesso VIP confirmado: {email}")

# 🔮 Sugestão IA com base no estilo de perfil
st.subheader("🔮 Sugestão estratégica da IA")
estilo = st.selectbox("Estilo de perfil", ["tático", "observador", "agressivo"])
setor = st.selectbox("Setor de interesse", ["infraestrutura", "tecnologia", "energia", "varejo"])
sugestao = sugestao_com_dados(f"{estilo}, setor {setor}", "BRL")
st.code(f"Sugestão preditiva: {sugestao.upper()}")

# 🎯 Metas mensais
st.subheader("🎯 Metas táticas do mês")
df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
metas = metas_para_usuario(email, df_usuarios)
if metas:
    st.write("Plano estratégico gerado pela muralha:")
    st.json(metas)
else:
    st.info("Nenhuma meta atribuída ainda. Explore atividades no painel CEO.")

# 📌 Missões VIP (expansível)
st.markdown("⚔️ Em breve: missões personalizadas, recompensas e desbloqueio de painéis ocultos.")