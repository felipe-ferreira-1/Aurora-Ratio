# login.py

import streamlit as st # pyright: ignore[reportMissingImports]

def autenticar_usuario():
    st.sidebar.title("🔐 Login Aurora Ratio")

    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar"):
        if usuario == "GameMaster" and senha == "aurora@2025":
            st.session_state["usuario_logado"] = True
            st.session_state["usuario_nome"] = "GameMaster"
            st.success("🧙‍♂️ Bem-vindo ao painel imperial!")
        elif usuario == "Comandante" and senha == "comando@123":
            st.session_state["usuario_logado"] = True
            st.session_state["usuario_nome"] = "Comandante"
            st.success("🚀 Acesso liberado ao painel tático!")
        else:
            st.error("❌ Credenciais inválidas.")