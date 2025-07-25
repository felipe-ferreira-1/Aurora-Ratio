# missao_imperial.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from utils.missoes import listar_missoes, progresso_do_usuario, registrar_progresso

load_dotenv()
SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🎯 Missão Imperial", layout="wide")
st.title("🎯 Missão Imperial")

# 🔐 Autenticação
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
# 📜 Missões disponíveis
st.subheader("📜 Missões disponíveis")
missoes = listar_missoes(supabase)
progresso = progresso_do_usuario(email, supabase)

# 🧠 Mini tutoriais da Aurora Ratio
def aurora_diz(titulo):
    frases = {
        "Fundamentos da Muralha": "🧙 Aurora Ratio diz: 'Toda muralha começa com uma pedra. Aprenda a base antes de buscar o topo.'",
        "Leitura de Métricas": "🧙 Aurora Ratio diz: 'Cada número é um eco do passado. Leia com olhos atentos e verá o futuro.'",
        "Escolha de Plano Estratégico": "🧙 Aurora Ratio diz: 'Não é o plano que define o sucesso, é o estrategista que o executa.'",
        "Psicologia do Investidor": "🧙 Aurora Ratio diz: 'Medo e ganância são os ventos. Você é o leme.'"
    }
    return frases.get(titulo, "🧙 Aurora Ratio observa em silêncio...")

# 🏅 Registro visual da jornada
st.subheader("🏅 Sua evolução na muralha")
concluidas = [m["titulo"] for m in missoes if m["id"] in progresso]
medalhas = {
    1: "🥉 Explorador",
    3: "🥈 Estrategista",
    5: "🥇 Guardião da Aurora"
}
nivel = medalhas.get(len(concluidas), "🔰 Iniciante")
st.markdown(f"**Nível atual:** {nivel} — {len(concluidas)} missão(ões) concluída(s)")

# 📂 Exibição das missões
for m in missoes:
    st.markdown(f"### 🧩 {m['titulo']}")
    st.write(m["descricao"])
    st.info(aurora_diz(m["titulo"]))

    if m["id"] in progresso:
        st.success("✅ Missão já concluída")
    else:
        if st.button(f"Concluir missão: {m['titulo']}"):
            registrar_progresso(email, m["id"], supabase)
            st.success("🎉 Missão registrada com sucesso!")
            # 🔮 Invocação da IA Aurora Ratio
            st.subheader("🔮 Invocar Aurora Ratio")

            if st.button("🧙‍♀️ Chamar Aurora Ratio"):
                st.markdown("🧙‍♀️ *Aurora Ratio materializa-se em luz e sabedoria...*")
                st.markdown("💬 *“A muralha responde ao estrategista, não ao aventureiro.”*")
                st.markdown("💬 *“Você dominou o ciclo de fluxo. Agora verá que o tempo é o ativo invisível.”*")
                st.markdown("💬 *“Continue. A muralha observa e recompensa os que persistem.”*")