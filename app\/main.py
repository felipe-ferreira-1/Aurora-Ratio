# main.py
import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client
import importlib
from planos import mostrar_planos
from checkout_intervalos import checkout
from aurora_connect import show_connect_page
from utils.logger import registrar_acao
from utils.fluxo_caixa import mostrar_fluxo

# Configuração visual e Supabase
st.set_page_config(page_title="Aurora Ratio", layout="wide")
load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Banner visual da muralha
st.image("assets/banner-aurora.png", use_column_width=True)
st.markdown("<h1 style='text-align: center;'>Aurora Ratio</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; font-style: italic;'>Ex tenebris statisticis ad lucem consilii</h4>", unsafe_allow_html=True)

# Login via token
token = st.sidebar.text_input("🔑 Token de acesso", type="password")
if not token:
    st.stop()

usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data
if not usuario:
    st.error("Token inválido.")
    st.stop()
usuario_nome = usuario["email"]
cargo = usuario["cargo"]

st.success(f"👤 Acesso concedido: {usuario_nome}")
st.session_state["usuario_nome"] = usuario_nome
st.session_state["user_data"] = usuario
# Menu lateral de navegação
pagina = st.sidebar.selectbox("📂 Menu", [
    "🏠 Muralha Principal",
    "📊 Planos e Checkout",
    "🕹️ Painel do Game Master",
    "🌐 Comunidade Aurora"
])

# Página principal
if pagina == "🏠 Muralha Principal":
    st.subheader("⚔️ Bem-vindo ao Aurora Ratio")
    st.write("Acompanhe seus planos, métricas e evolução intergaláctica.")

# Página de planos + pagamento
elif pagina == "📊 Planos e Checkout":
    mostrar_planos()
    checkout(supabase, usuario)

# Painel restrito do Game Master
elif pagina == "🕹️ Painel do Game Master":
    game_master = importlib.import_module("4_Game_Master")
    game_master.painel_master()

# Rede social colaborativa
elif pagina == "🌐 Comunidade Aurora":
    show_connect_page(usuario)
    # Dados adicionais para cargos especiais
    if cargo in ["gamemaster", "ceo"]:
        st.divider()
        st.subheader("📊 Fluxo Imperial")
        mostrar_fluxo(supabase, usuario_nome)

        st.subheader("📋 Auditoria")
        logs = supabase.table("auditoria").select("*").execute().data
        st.dataframe(logs)
        
        