import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]
from utils.mentoria import recomendar_mentor # pyright: ignore[reportMissingImports]

load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🎓 Mentoria Imperial", layout="wide")
st.title("🎓 Mentoria Imperial")

token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario:
    st.error("Token inválido ou usuário não encontrado.")
    st.stop()

email = usuario["email"]
cargo = usuario["cargo"]
st.success(f"Acesso confirmado: {email} ({cargo.upper()})")

st.subheader("🔍 Análise de estilo de perfil")
estilo = st.selectbox("Selecione seu estilo:", ["estratégico", "intuitivo", "analítico", "executivo"])
st.write(f"Seu estilo é: **{estilo.upper()}** — orientado para ações táticas no império.")

st.subheader("👥 Sugestão de mentor")
df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
mentor = recomendar_mentor(usuario, df_usuarios)
st.success(f"Mentor sugerido: **{mentor['email']}**")

st.markdown("📌 Em breve: perfil psicológico imperial, desenvolvimento de habilidades e trilhas evolutivas.")