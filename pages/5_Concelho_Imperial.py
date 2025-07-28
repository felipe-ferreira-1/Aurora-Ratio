import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]

load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🏰 Conselho Imperial", layout="wide")
st.title("🏰 Sala do Conselho Imperial")

token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario or usuario["cargo"] not in ["ceo", "gamemaster"]:
    st.error("Acesso restrito ao Conselho Imperial.")
    st.stop()

email = usuario["email"]
st.success(f"Acesso autorizado: {email}")

st.subheader("📜 Discussões estratégicas")
topico = st.text_input("Assunto atual do império")
resposta = st.text_area("Proposta ou análise")

if st.button("Enviar para registro"):
    supabase.table("conselho").insert({
        "autor": email,
        "topico": topico,
        "resposta": resposta
    }).execute()
    st.success("Proposta registrada com sucesso.")

st.subheader("📂 Histórico de pautas")
registros = supabase.table("conselho").select("*").order("id", desc=True).limit(15).execute().data
st.dataframe(pd.DataFrame(registros))