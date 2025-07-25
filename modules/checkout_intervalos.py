# checkout_intervalos.py

import stripe
import requests
import streamlit as st

stripe.api_key = "pk_test_51RBI8PQDyOQGLKdNMimL6Y6GMMOTPN08b9wySobJTlJtP4LJqXKS9DSViBuoIaSF2iBTxDD7NPbzMEroEySh5Q7A00qjjZchsO"  # Substitua pela sua chave real

# Detecta moeda local pelo IP (usando API externa)
def detectar_moeda_local():
    try:
        ip_data = requests.get("https://ipapi.co/json/").json()
        moeda = ip_data.get("currency", "USD")
        return moeda.upper()
    except:
        return "USD"

# Busca taxa de câmbio (dólar → moeda local)
def buscar_taxa_dolar_para(moeda_local):
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        taxa = response.json()["rates"].get(moeda_local, 1)
        return taxa
    except:
        return 1

# Cria link de checkout
def gerar_sessao_checkout(intervalo, moeda_local, preco_usd):
    taxa = buscar_taxa_dolar_para(moeda_local)
    preco_convertido = round(preco_usd * taxa, 2)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": moeda_local.lower(),
                "product_data": {"name": f"Aurora Ratio - Plano {intervalo.title()}"},
                "unit_amount": int(preco_convertido * 100),
            },
            "quantity": 1,
        }],
        mode="subscription",
        success_url="https://auroraratio.com/sucesso",
        cancel_url="https://auroraratio.com/cancelado",
    )
    return session.url, preco_convertido