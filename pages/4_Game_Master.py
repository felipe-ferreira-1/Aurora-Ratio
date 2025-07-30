# 4_Game_Master.py

import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import pycountry # pyright: ignore[reportMissingImports]
import plotly.express as px # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]

# Conexão com Supabase
SUPABASE_URL = "https://wegwcsfapippzwiltmtg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def painel_master():
    if st.session_state.get("usuario_nome") != "GameMaster":
        st.warning("🔐 Acesso restrito ao Game Máster.")
        return

    st.title("🧙‍♂️ Painel do Game Máster")

    # 🧮 Edição de valores dos planos
    preco_atual_pro = st.session_state.get("preco_pro", 19.0)
    preco_atual_enterprise = st.session_state.get("preco_enterprise", 49.0)

    novo_pro = st.number_input("💳 Valor Aurora Pro", value=preco_atual_pro)
    novo_enterprise = st.number_input("💳 Valor Aurora Enterprise", value=preco_atual_enterprise)

    if st.button("💾 Atualizar Preços"):
        st.session_state["preco_pro"] = novo_pro
        st.session_state["preco_enterprise"] = novo_enterprise
        st.success("✅ Preços atualizados.")

        historico = st.session_state.setdefault("historico_precos", [])
        historico.append({
            "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
            "Plano": "Pro e Enterprise",
            "Valor Pro": novo_pro,
            "Valor Enterprise": novo_enterprise
        })

    st.metric("💰 Receita Total", "$7,412")

    # 📜 Histórico de alterações
    st.subheader("📜 Histórico de Preços")
    historico_df = pd.DataFrame(st.session_state.get("historico_precos", []))
    if not historico_df.empty:
        st.dataframe(historico_df)
    else:
        st.info("Nenhuma alteração registrada ainda.")

    # 🚷 Banimento e Desbanimento
    st.subheader("🚷 Moderação de Usuários")
    usuario_banido = st.text_input("👤 Usuário a ser banido ou desbanido")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Banir usuário"):
            banidos = st.session_state.setdefault("usuarios_banidos", [])
            if usuario_banido not in banidos:
                banidos.append(usuario_banido)
                st.success(f"Usuário {usuario_banido} banido com sucesso!")

    with col2:
        if st.button("✅ Desbanir usuário"):
            banidos = st.session_state.get("usuarios_banidos", [])
            if usuario_banido in banidos:
                banidos.remove(usuario_banido)
                st.success(f"Usuário {usuario_banido} foi desbanido.")
            else:
                st.info(f"O usuário {usuario_banido} não está na lista de banidos.")

    st.metric("🔒 Usuários Banidos", len(st.session_state.get("usuarios_banidos", [])))
    # 🌐 Mural colaborativo
    st.subheader("🌐 Mural de Experiências dos Usuários")
    novo_post = st.text_area("📬 Compartilhe uma dica, experiência ou insight:")

    if st.button("📝 Publicar no Mural"):
        feed = st.session_state.setdefault("feed_comunidade", [])
        if novo_post.strip():
            autor = st.session_state.get("usuario_nome", "Anônimo")
            feed.append({"autor": autor, "mensagem": novo_post.strip()})
            st.success("🚀 Mensagem publicada com sucesso!")

    for post in reversed(st.session_state.get("feed_comunidade", [])):
        st.markdown(f"**{post['autor']}** disse:")
        st.info(post['mensagem'])

    # 🌍 Painel geográfico secreto
    st.subheader("🌍 Inteligência Geográfica Imperial")

    df = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)

    def get_country_emoji(pais):
        try:
            country = pycountry.countries.lookup(pais)
            offset = 127397
            return ''.join([chr(ord(char) + offset) for char in country.alpha_2.upper()])
        except:
            return "🏳️"

    df["bandeira"] = df["pais"].apply(get_country_emoji)

    agrupado = df.groupby("pais").agg({
        "id": "count",
        "receita": "sum"
    }).reset_index()
    agrupado["bandeira"] = agrupado["pais"].apply(get_country_emoji)
    agrupado.columns = ["País", "Usuários", "Receita", "Bandeira"]

    continentes = {
        "América": ["Brasil", "Argentina", "USA", "México", "Colômbia"],
        "Europa": ["Portugal", "França", "Alemanha", "Itália", "Espanha"],
        "Ásia": ["Japão", "China", "Índia", "Coreia do Sul"],
        "África": ["Nigéria", "África do Sul", "Egito"],
    }
    continente_selecionado = st.selectbox("🧭 Filtrar por continente", options=["Todos"] + list(continentes.keys()))
    if continente_selecionado != "Todos":
        paises_disponiveis = [p for p in agrupado["País"].tolist() if p in continentes[continente_selecionado]]
    else:
        paises_disponiveis = agrupado["País"].tolist()
    paises_selecionados = st.multiselect("🌍 Filtrar por país", options=paises_disponiveis)

    # Exemplo de exibição dos dados filtrados
    if paises_selecionados:
        st.dataframe(agrupado[agrupado["País"].isin(paises_selecionados)])
    else:
        st.dataframe(agrupado)