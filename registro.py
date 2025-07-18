import streamlit as st
import requests

st.set_page_config(page_title="Registro Aurora")
st.title("🛂 Registro no Império Aurora Ratio")

email = st.text_input("Email")
plano = st.selectbox("Plano", ["mensal", "anual"])
pais = st.text_input("País")
moeda = st.selectbox("Moeda", ["BRL", "USD", "EUR"])
lang = st.selectbox("Idioma", ["pt", "en", "es"])

if st.button("Cadastrar"):
    res = requests.post("http://localhost:8000/cadastro", json={
        "email": email, "plano": plano, "pais": pais,
        "moeda_preferida": moeda, "lang": lang
    }).json()
    st.success("Registrado com sucesso!")
    st.code(f"Token de acesso: {res['token']}")