# painel_noticias.py

import streamlit as st
import pandas as pd
from monitoramento_aurora import monitorar_noticias, carregar_empresas_monitoradas
from supabase import create_client
import os
from dotenv import load_dotenv

# Configuração
st.set_page_config(page_title="📡 Aurora Ratio — Central de Notícias", layout="wide")
load_dotenv()

SUPABASE_URL = os.getenv("https://wegwcsfapippzwiltmtg.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
st.title("🧠 Painel Global de Alertas — Aurora Ratio")

# Filtros dinâmicos
empresas_disponíveis = carregar_empresas_monitoradas()
empresa_filtrada = st.selectbox("🏢 Filtrar por empresa", options=["Todas"] + empresas_disponíveis)
risco_filtrado = st.multiselect("⚠️ Nível de risco", options=["ALTO", "MODERADO", "BAIXO"], default=["ALTO", "MODERADO", "BAIXO"])
sentimento_filtrado = st.multiselect("💬 Sentimento detectado", options=["positivo", "neutro", "negativo"], default=["positivo", "neutro", "negativo"])

# 🔄 Carrega dados do Supabase
dados = supabase.table("alertas").select("*").execute().data
df_alertas = pd.DataFrame(dados)

# Aplica filtros
if empresa_filtrada != "Todas":
    df_alertas = df_alertas[df_alertas["empresa"] == empresa_filtrada]
df_alertas = df_alertas[df_alertas["risco"].isin(risco_filtrado)]
df_alertas = df_alertas[df_alertas["sentimento"].isin(sentimento_filtrado)]

# Conversão de timestamp
df_alertas["timestamp"] = pd.to_datetime(df_alertas["timestamp"])
df_alertas = df_alertas.sort_values(by="timestamp", ascending=False)
# 🔎 Detalhes por alerta
st.subheader("🗂️ Últimos alertas detectados")
if not df_alertas.empty:
    st.dataframe(df_alertas[["timestamp", "empresa", "noticia", "sentimento", "risco", "frase_ia"]])
else:
    st.info("Nenhum alerta corresponde aos filtros selecionados.")

# 📈 Gráfico de risco
st.subheader("📊 Distribuição de risco")
st.bar_chart(df_alertas["risco"].value_counts())

# 📈 Gráfico de sentimento
st.subheader("📊 Distribuição de sentimento")
st.bar_chart(df_alertas["sentimento"].value_counts())

# 📅 Evolução temporal
st.subheader("📆 Tendência de alertas ao longo do tempo")
linha_tempo = df_alertas.groupby(df_alertas["timestamp"].dt.date).size()
st.line_chart(linha_tempo)
st.subheader("🗂️ Últimos alertas detectados")

if not df_alertas.empty:
    for i, alerta in df_alertas.iterrows():
        st.markdown(f"### 📰 {alerta['noticia']}")
        st.caption(f"📆 {alerta['timestamp'].strftime('%d/%m/%Y %H:%M')} — 🏢 {alerta['empresa']}")
        st.write(f"💬 **Sentimento:** {alerta['sentimento'].capitalize()} | ⚠️ **Risco:** {alerta['risco']}")

        st.markdown(f"🧙‍♀️ Aurora Ratio diz: *{alerta['frase_ia']}*")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚨 Marcar como URGENTE", key=f"urgente_{i}"):
                alerta["risco"] = "URGENTE"
                supabase.table("alertas").update({"risco": "URGENTE"}).eq("noticia", alerta["noticia"]).execute()
                st.success("🚨 Alerta elevado para URGENTE!")

        with col2:
            comentario = st.text_input("📝 Comentário estratégico", key=f"coment_{i}")
            if comentario:
                supabase.table("alertas").update({"comentario_analista": comentario}).eq("noticia", alerta["noticia"]).execute()
                st.info("💾 Comentário registrado.")

        with col3:
            if st.button("📣 Reagir como Aurora", key=f"aurora_reage_{i}"):
                reacao = f"Aurora Ratio responde: *'Este alerta exige vigilância. Risco: {alerta['risco']} — A muralha está de olhos abertos.'*"
                st.warning(reacao)
else:
    st.info("Nenhum alerta corresponde aos filtros selecionados.")