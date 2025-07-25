# planos.py

import streamlit as st
from streamlit_card import card  # Instale via `pip install streamlit-card`

def mostrar_planos():
    st.subheader("🛡️ Escolha seu Plano Imperial")

    col1, col2 = st.columns(2)

    with col1:
        card(
            title="Aurora Pro",
            text="Plano completo com IA e relatórios estratégicos",
            image="assets/pro_card.png",
            url="https://auroraratio.com/pro",
            styles={"card": {"background-color": "#eeeeff"}}
        )

    with col2:
        card(
            title="Aurora Enterprise",
            text="Painel avançado, API e suporte galáctico",
            image="assets/enterprise_card.png",
            url="https://auroraratio.com/enterprise",
            styles={"card": {"background-color": "#ffeeee"}}
        )