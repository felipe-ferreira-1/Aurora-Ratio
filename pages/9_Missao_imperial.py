import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.missoes import listar_missoes, progresso_do_usuario, registrar_progresso

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🎯 Missão Imperial", layout="wide")
st.title("🎯 Missão Imperial")

token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario:
    st.error("Token inválido ou expirado.")
    st.stop()

email = usuario["email"]
cargo = usuario["cargo"]
st.success(f"Bem-vindo à jornada imperial, {email} ({cargo.upper()})")

st.subheader("📜 Missões disponíveis")
missoes = listar_missoes(supabase)
progresso = progresso_do_usuario(email, supabase)

for m in missoes:
    st.markdown(f"### 🧩 {m['titulo']}")
    st.write(m["descricao"])
    if m["id"] in progresso:
        st.success("Missão já concluída 🎉")
    else:
        if st.button(f"Concluir missão: {m['titulo']}"):
            registrar_progresso(email, m["id"], supabase)
            st.success("Missão registrada com sucesso!")