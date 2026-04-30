import streamlit as st
import pandas as pd
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone


# ────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ────────────────────────────────────────────
st.set_page_config(page_title="ODA · Protocolo de Reconstituição", layout="wide")


# ────────────────────────────────────────────
# ESTILO VISUAL — CSS construído sem triple quotes
# ────────────────────────────────────────────
css = (
    "<style>"
    ".stApp { background: #030303; color: #ebe5d5; font-family: 'Georgia', serif; }"
    "h1, h2, h3, h4 { color: #ff6b00 !important; font-weight: normal; letter-spacing: 0.5px; }"
    ".metric-card {"
    "background: rgba(20, 20, 20, 0.8);"
    "border: 1px solid rgba(255, 107, 0, 0.2);"
    "border-radius: 10px;"
    "padding: 24px 16px;"
    "text-align: center;"
    "backdrop-filter: blur(8px);"
    "box-shadow: 0 0 10px rgba(0,0,0,0.5);"
    "}"
    ".metric-card:hover { border-color: #ff6b00; background: rgba(255, 107, 0, 0.05); }"
    ".stButton > button {"
    "background: #ff6b00;"
    "color: #0a0a0a;"
    "font-weight: bold;"
    "border: none;"
    "border-radius: 6px;"
    "width: 100%;"
    "letter-spacing: 0.8px;"
    "font-family: 'Georgia', serif;"
    "transition: 0.2s;"
    "}"
    ".stButton > button:hover { background: #ff8533; box-shadow: 0 0 14px rgba(255, 107, 0, 0.4); }"
    ".whisper-box {"
    "border-left: 4px solid #ff6b00;"
    "background: rgba(255, 107, 0, 0.04);"
    "padding: 16px 20px;"
    "border-radius: 0 8px 8px 0;"
    "margin: 16px 0;"
    "}"
    ".footer-quote {"
    "text-align: center;"
    "color: #b0a080;"
    "font-style: italic;"
    "margin-top: 32px;"
    "font-size: 0.9rem;"
    "}"
    "[data-testid='stSidebar'] { background: #0a0a0a; }"
    "</style>"
)
st.markdown(css, unsafe_allow_html=True)


# ────────────────────────────────────────────
# CONEXÃO COM AS SECRETS
# ────────────────────────────────────────────
try:
    client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception:
    st.warning("A chama ainda não encontrou as suas chaves. Guarde as secrets no painel do Streamlit e regresse.")
    st.stop()


# ────────────────────────────────────────────
# MOTOR DE MODOS (extraído do PDF)
# ────────────────────────────────────────────
def definir_modo(mental, cigs, sinais):
    if any(s in ["Tontura", "Dor Torácica"] for s in sinais):
        return ("ABORTAR", "Suspensão imediata. O corpo falou — escuta-o como se fosse uma prece.", "#FF3B30")
    if mental == "Apatia" or cigs >= 16:
        return ("RECUPERAÇÃO", "Hábito mínimo hoje. A semente no escuro também trabalha. Ceia sagrada, respiração.", "#007AFF")
    if mental == "Hipomania" or cigs >= 10:
        return ("ESTRATÉGICO", "Domar o fogo sem apagá-lo. Bloqueia cargas, reduz aeróbico 15%.", "#FF9F0A")
    return ("LIMITE", "Altar firme. As quatro âncoras chamam por ti.", "#FF6B00")


# ────────────────────────────────────────────
# ESTADO INICIAL
# ────────────────────────────────────────────
if "modo" not in st.session_state:
    st.session_state.modo = "LIMITE"
    st.session_state.instr = "Altar firme. As quatro âncoras chamam por ti."
    st.session_state.cor = "#FF6B00"
    st.session_state.ultima_sincro = False


# ────────────────────────────────────────────
# CABEÇALHO
# ────────────────────────────────────────────
st.title("ODA · Protocolo de Reconstituição")
st.markdown(
    "<p style='color:#b0a080; font-style:italic;'>João, 38 anos · 113 kg · 1,78 m · Seis meses para –20 kg</p>",
    unsafe_allow_html=True
)
st.markdown("---")


# ────────────────────────────────────────────
# DASHBOARD — três colunas
# ────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    html_modo = (
        "<div class='metric-card'>"
        "<p style='color:#a09080; margin:0; letter-spacing:1px;'>MODO ATUAL</p>"
        "<h1 style='color:" + st.session_state.cor + " !important; margin:0; font-size:2.5rem;'>"
        + st.session_state.modo +
        "</h1>"
        "<p style='color:#b0a080;'>A rota decidida pelo corpo</p>"
        "</div>"
    )
    st.markdown(html_modo, unsafe_allow_html=True)

with col2:
    st.markdown(
        "<div class='metric-card'>"
        "<p style='color:#a09080; margin:0; letter-spacing:1px;'>PROTEÍNA DIÁRIA</p>"
        "<h1 style='color:#ff6b00 !important; margin:0; font-size:2.5rem;'>270g</h1>"
        "<p style='color:#b0a080;'>Pilar inegociável da massa magra</p>"
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div class='metric-card'>"
        "<p style='color:#a09080; margin:0; letter-spacing:1px;'>META FINAL</p>"
        "<h1 style='color:#ff6b00 !important; margin:0; font-size:2.5rem;'>-20 kg</h1>"
        "<p style='color:#b0a080;'>Homem novo em seis luas</p>"
        "</div>",
        unsafe_allow_html=True
    )

st.markdown("---")


# ────────────────────────────────────────────
# MENSAGEM DO INSTRUTOR INTERIOR
# ────────────────────────────────────────────
html_sussurro = (
    "<div class='whisper-box'>"
    "<p style='margin:0; font-size:1.2rem;'><strong>🜁 Instrutor Interior:</strong> "
    + st.session_state.instr +
    "</p></div>"
)
st.markdown(html_sussurro, unsafe_allow_html=True)
st.markdown("---")


# ────────────────────────────────────────────
# SIDEBAR — Confissão diária
# ────────────────────────────────────────────
with st.sidebar:
    st.header("Confissão do Dia")
    st.markdown("A verdade do corpo, sem filtro.")

    mental = st.selectbox(
        "Paisagem interior",
        ["Estável", "Hipomania", "Apatia"],
        index=0,
        help="Estável: águas calmas. Hipomania: vento veloz. Apatia: nevoeiro cerrado."
    )

    cigs = st.number_input(
        "Cigarros que te acompanharam",
        min_value=0,
        max_value=40,
        value=0,
        help="Cada um é um sopro a menos de oxigénio para os músculos."
    )

    sinais = st.multiselect(
        "Sinais do corpo",
        ["Normal", "Tontura", "Dor Torácica"],
        default=["Normal"],
        help="Tontura ou dor torácica acionam ABORTAR imediatamente."
    )

    if st.button("🜂 SINCRONIZAR"):
        modo, instr, cor = definir_modo(mental, cigs, sinais)
        st.session_state.modo = modo
        st.session_state.instr = instr
        st.session_state.cor = cor

        try:
            data = {
                "peso": 113.0,
                "cigarros": int(cigs),
                "estado_mental": mental,
                "modo_calculado": modo,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            result = supabase.table("oda_logs").insert(data).execute()
            if result.data:
                st.success("A tua confissão foi guardada no livro invisível.")
                st.session_state.ultima_sincro = True
            else:
                st.warning("O registo foi aceite, mas o livro silenciou. Verifica a tabela.")
        except Exception as e:
            st.error("Sopro contrário ao registar. Detalhe: " + str(e))
            st.info(
                "Provável causa: a tabela `oda_logs` ainda não foi criada no Supabase. "
                "Cria-a com as colunas: peso (float8), cigarros (int2), estado_mental (text), "
                "modo_calculado (text), timestamp (timestamptz). "
                "E certifica-te de que a chave usada (`SUPABASE_KEY`) é a service_role."
            )


# ────────────────────────────────────────────
# FORJA DO TREINO — Oráculo com IA
# ────────────────────────────────────────────
st.markdown("---")
st.subheader("Forja do Treino · Llama 3.3")

if st.button("🜃 FORJAR TREINO DE HOJE"):
    with st.spinner("O fogo está a moldar a tua sessão... respira fundo."):
        try:
            prompt = (
                "João está em modo " + st.session_state.modo + ". "
                "Gera um treino ODA completo para hoje, seguindo o protocolo de Reconstituição. "
                "Hoje é Segunda-feira (Lower A). Inclui: aquecimento específico nas âncoras (1x15 com 40% da carga de trabalho), "
                "Agachamento Livre (barra no trapézio, coxas paralelas, 4x8-10, 120s descanso), Leg Press 45° (4x10, 90s), "
                "Cadeira Extensora (4x10, 60s), Panturrilhas em pé (3x15, 60s). "
                "No final, uma nota poética para motivar, coerente com a filosofia ODA: "
                "'Somos o que repetidamente fazemos. A excelência é um hábito.'"
            )
            resp = client_groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.85,
                max_tokens=900
            )
            treino = resp.choices[0].message.content
            # Renderiza o texto do treino de forma segura
            html_treino = (
                "<div style='background: rgba(20,20,20,0.9); padding:24px; border-radius:12px; border:1px dashed #ff6b00;'>"
                + treino.replace("\n", "<br>") +
                "</div>"
            )
            st.markdown(html_treino, unsafe_allow_html=True)
        except Exception as e:
            st.error("O oráculo encontrou uma névoa: " + str(e))


# ────────────────────────────────────────────
# RODAPÉ
# ────────────────────────────────────────────
st.markdown(
    "<div class='footer-quote'>“O alarme das 04:30 e a confissão anti‑cigarro são as decisões que importam. "
    "O protocolo não exige perfeição — exige presença diária.”</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#a09080; font-size:0.8rem;'>ODA Protocol · Reconstituição · Decisões clínicas validadas pelo psiquiatra</p>",
    unsafe_allow_html=True
)
