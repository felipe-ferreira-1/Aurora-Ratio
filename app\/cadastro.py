import streamlit as st # pyright: ignore[reportMissingImports]
from supabase import create_client # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
import os
from uuid import uuid4

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("Cadastro no Império Aurora Ratio 👑")

nome = st.text_input("Nome")
email = st.text_input("E-mail")
plano = st.selectbox("Plano", ["mensal", "anual"])
pais = st.text_input("País")
moeda = st.text_input("Moeda preferida")
lang = st.selectbox("Idioma", ["pt", "en", "es"])

if st.button("Cadastrar"):
    token = str(uuid4())

    resposta = supabase.table("usuarios").insert({
        "nome": nome,
        "email": email,
        "plano": plano,
        "pais": pais,
        "moeda_preferida": moeda,
        "lang": lang,
        "token": token,
        "cargo": "usuario"
    }).execute()

    if resposta.get("status_code") == 201:
        st.success(f"""
🧠 Bem-vindo ao Aurora Ratio, {nome}!

🔐 Token: {token}  
🌐 Idioma: {lang}  
🪙 Moeda: {moeda}
        """)
    else:
        st.error("Não foi possível cadastrar o usuário.")