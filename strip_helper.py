import stripe
import os
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET")

def criar_sessao_pagamento(email, plano):
    preco = "price_mensal_id" if plano == "mensal" else "price_anual_id"
    sessao = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": preco, "quantity": 1}],
        customer_email=email,
        success_url="https://aurora.com/sucesso",
        cancel_url="https://aurora.com/cancelado"
    )
    return sessao.url
    import mercadopago
    sdk = mercadopago.SDK("ACCESS_TOKEN")

    def gerar_pagamento(email, valor):
        pagamento = sdk.preference().create({
            "items": [{
                "title": "Aurora Plano VIP",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor
            }],
            "payer": {"email": email},
            "back_urls": {
                "success": "https://aurora.com/sucesso",
                "failure": "https://aurora.com/erro",
            },
            "auto_return": "approved"
        })
        return pagamento["response"]["init_point"]