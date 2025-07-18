import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.mentoria import recomendar_mentor

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
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