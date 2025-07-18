import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, timedelta

# 🔐 Conectar Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🎨 Streamlit
st.set_page_config(page_title="Aurora Ratio", layout="wide")
st.title("Aurora Ratio 🔮")

# 🔑 Login por token
token = st.text_input("Token de acesso", type="password")
if not token:
    st.stop()

if token.startswith("TEMP:"):
    import json, base64
    dados = json.loads(base64.urlsafe_b64decode(token[5:].encode()).decode())
    usuario = {"email": dados["email"], "cargo": dados["cargo"]}
else:
    usuario = supabase.table("usuarios").select("*").eq("token", token).single().execute().data

if not usuario:
    st.error("Token inválido")
    st.stop()

# ✅ Info do usuário
email = usuario["email"]
cargo = usuario["cargo"]
st.success(f"Bem-vindo {email} ({cargo.upper()})")
from utils.mentoria import recomendar_mentor
from utils.ia_predictor import sugestao_com_dados
from utils.metas_ai import metas_para_usuario
from utils.fiscal import gerar_nota_fiscal, exportar_para_contador, calcular_imposto
from utils.temporal_gate import gerar_portao_temporal
from utils.logger import registrar_acao

df_usuarios = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
moeda = "R$"

# 👥 Usuário
if cargo == "usuario":
    st.subheader("👥 Painel do Usuário")
    mentor = recomendar_mentor(usuario, df_usuarios)
    st.success(f"🎓 Mentor sugerido: {mentor['email']}")

# 💎 VIP
elif cargo == "vip":
    st.subheader("💎 Painel VIP Estratégico")
    sugestao = sugestao_com_dados("perfil estratégico, setor energia", "BRL")
    st.write(f"🔮 Sugestão da IA: **{sugestao.upper()}**")
    metas = metas_para_usuario(usuario["email"], df_usuarios)
    st.json(metas)

# 👑 CEO
elif cargo == "ceo":
    st.subheader("👑 Painel do CEO")
    st.metric("Usuários ativos", len(df_usuarios))
    df_usuarios["valor_pago"] = df_usuarios["plano"].map({"mensal": 50, "anual": 500})
    total = df_usuarios["valor_pago"].sum()
    st.metric("Valor arrecadado", f"{moeda} {total:.2f}".replace(",", "."))

    st.subheader("📄 Emitir Nota Fiscal")
    alvo = st.selectbox("Email do cliente", df_usuarios["email"])
    plano_nf = st.selectbox("Plano", ["mensal", "anual"])
    valor_nf = {"mensal": 50, "anual": 500}[plano_nf]
    if st.button("Gerar NFE"):
        nota = gerar_nota_fiscal({"email": alvo, "id": 123}, plano_nf, valor_nf)
        st.json(nota)

    st.subheader("🧾 Exportação contábil")
    st.dataframe(exportar_para_contador(df_usuarios))

    st.subheader("🛡️ Cálculo de impostos")
    pais = st.selectbox("País", ["br", "us", "eu"])
    plano = st.selectbox("Plano", ["mensal", "anual"])
    imposto = calcular_imposto(pais, plano)
    st.metric("Imposto estimado", f"{moeda} {imposto:.2f}")

    st.subheader("🕰️ Portão Temporal")
    email_sim = st.text_input("Email destino")
    cargo_sim = st.selectbox("Cargo simulado", ["usuario", "vip", "ceo", "gamemaster"])
    if st.button("Criar acesso temporário"):
        token_temp = gerar_portao_temporal(email_sim, cargo_sim)
        st.code(token_temp)

# 🧙‍♂️ Game Master
elif cargo == "gamemaster":
    st.subheader("🕹️ Painel do Game Master")

    # 🔍 Logs
    logs_raw = supabase.table("auditoria").select("*").execute().data
    st.dataframe(pd.DataFrame(logs_raw))

    # 📊 Fluxo financeiro
    df_fin = pd.DataFrame(supabase.table("transacoes").select("*").execute().data)
    if not df_fin.empty:
        df_fin["data"] = pd.to_datetime(df_fin["data"])
        st.line_chart(df_fin.set_index("data")["valor"])
        st.dataframe(df_fin)

    # 💸 Retirada
    valor_retirada = st.number_input("Valor da retirada", 0.0, float(total))
    destino = st.text_input("Destino bancário/carteira")
    if st.button("Executar retirada"):
        registrar_acao(email, f"Retirada de {valor_retirada} → {destino}", "localhost", cargo)
        st.success(f"{moeda} {valor_retirada:.2f} enviado para {destino}")

    # 🏰 Conselho Imperial
    membros = df_usuarios[df_usuarios["cargo"].isin(["ceo", "gamemaster"])]
    st.subheader("🏰 Conselho Imperial")
    for _, m in membros.iterrows():
        st.markdown(f"👤 {m['email']} — {m['cargo'].upper()}")
    st.text_area("📜 Discussão interna dos conselheiros")
  st.subheader("🔎 Relatório de uso (últimos 7 dias)")
  df_log = pd.DataFrame(supabase.table("auditoria").select("*").execute().data)
  df_log["timestamp"] = pd.to_datetime(df_log["timestamp"])
  df_7d = df_log[df_log["timestamp"] >= (datetime.now() - timedelta(days=7))]
  st.bar_chart(df_7d["acao"].value_counts())

  st.write("🎯 Sistema Imperial Aurora Ratio concluído.")