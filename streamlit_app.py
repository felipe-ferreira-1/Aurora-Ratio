import .streamlit as st
from aurora_ratio import analisar_texto

st.set_page_config(page_title="Aurora Ratio", page_icon="🌌", layout="centered")

# ---- Estilo ----
st.markdown("""
    <style>
    .big-font { font-size:30px !important; }
    .result-box {
        background-color: #1f1f2e;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Cabeçalho ----
st.markdown('<p class="big-font">🌌 Aurora Ratio</p>', unsafe_allow_html=True)
st.write("Análise de polaridade emocional e intensidade com toque expressivo.")

# ---- Entrada de texto ----
texto = st.text_area("Digite o texto para análise", height=150)

# ---- Botão de análise ----
if st.button("Analisar"):
    if texto.strip():
        with st.spinner("✨ Aurora está pensando..."):
            resultado = analisar_texto(texto)

        polaridade = resultado['polaridade']
        intensidade = resultado['intensidade']

        # ---- Reação expressiva da IA ----
        reacao = "😡" if polaridade < -0.5 else "😐" if polaridade < 0.5 else "😊"
        intensidade_desc = "intensa" if abs(intensidade) > 0.7 else "moderada" if abs(intensidade) > 0.3 else "suave"

        st.markdown(f"## Resultado {reacao}")
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write(f"- **Polaridade**: `{polaridade:.2f}` → {'Negativa' if polaridade < 0 else 'Positiva'}")
        st.write(f"- **Intensidade**: `{intensidade:.2f}` → {intensidade_desc.capitalize()}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Por favor, insira algum texto para análise.")

# ---- Rodapé ----
st.markdown("---")
st.caption("Desenvolvido por Felipe Ferreira • Powered by Aurora 🪐")