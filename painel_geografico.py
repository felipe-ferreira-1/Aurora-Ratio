# painel_geografico.py

import pandas as pd
import pycountry
import plotly.express as px
import streamlit as st

def get_country_emoji(pais):
    try:
        country = pycountry.countries.lookup(pais)
        offset = 127397
        return ''.join([chr(ord(char) + offset) for char in country.alpha_2.upper()])
    except:
        return "🏳️"

def painel_geografico(supabase):
    df = pd.DataFrame(supabase.table("usuarios").select("*").execute().data)
    df["bandeira"] = df["pais"].apply(get_country_emoji)

    agrupado = df.groupby("pais").agg({
        "id": "count",
        "receita": "sum"
    }).reset_index()
    agrupado["bandeira"] = agrupado["pais"].apply(get_country_emoji)
    agrupado.columns = ["País", "Usuários", "Receita", "Bandeira"]

    # 🔍 Filtros dinâmicos
    paises_selecionados = st.multiselect("🌍 Filtrar por país", options=agrupado["País"].tolist())
    continentes = {
        "América": ["Brasil", "Argentina", "USA", "México", "Colômbia"],
        "Europa": ["Portugal", "França", "Alemanha", "Itália", "Espanha"],
        "Ásia": ["Japão", "China", "Índia", "Coreia do Sul"],
        "África": ["Nigéria", "África do Sul", "Egito"],
    }
    continente_selecionado = st.selectbox("🧭 Filtrar por continente", options=["Todos"] + list(continentes.keys()))
    if continente_selecionado != "Todos":
        paises_selecionados += continentes[continente_selecionado]

    if paises_selecionados:
        agrupado = agrupado[agrupado["País"].isin(paises_selecionados)]

    # 🏆 Top 5 países mais lucrativos
    st.subheader("🏆 Top 5 países mais lucrativos")
    top5 = agrupado.sort_values(by="Receita", ascending=False).head(5)
    top5["Troféu"] = ["🥇", "🥈", "🥉", "🏅", "🎖️"]
    st.dataframe(top5[["Troféu", "Bandeira", "País", "Receita"]])

    # 🌐 Tabela geral
    st.subheader("📊 Usuários por país")
    st.dataframe(agrupado[["Bandeira", "País", "Usuários", "Receita"]])

    # 📈 Gráfico
    fig = px.bar(agrupado, x="País", y="Receita", text="Receita", color="Receita")
    st.plotly_chart(fig)

    # 🗺️ Mapa
    st.subheader("🗺️ Mapa geográfico")
    mapa = px.choropleth(
        agrupado,
        locations="País",
        locationmode="country names",
        color="Usuários",
        hover_name="País",
        color_continuous_scale="Turbo"
    )
    st.plotly_chart(mapa)
    from painel_geografico import painel_geografico

    # Dentro da verificação secreta
    if session_state.usuario == "game_master":
        st.subheader("🧙 Página secreta do Mestre do Jogo")
        painel_geografico(supabase)