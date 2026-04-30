import streamlit as st
import pandas as pd
from groq import Groq
from supabase import create_client
from datetime import datetime

# ─── RITUAL DE ABERTURA ──────────────────────────────────────────
st.set_page_config(page_title="ODA ENGINE · A Arte da Reconstrução", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #0d0d0d 100%);
        color: #f0e6d3;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 107, 0, 0.25);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        backdrop-filter: blur(4px);
        transition: 0.3s ease;
    }
    .metric-card:hover {
        border-color: #ff6b00;
        background: rgba(255, 107, 0, 0.05);
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #ff6b00 !important;
    }
    .stButton>button {
        background: #ff6b00;
        color: #0a0a0a;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        border: none;
        letter-spacing: 0.5px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: #ff8533;
        box-shadow: 0 0 12px #ff6b0040;
    }
    .whisper {
        color: #b0a090;
        font-style: italic;
    }
    .quote {
        font-family: 'Georgia', serif;
        color: #e0c090;
        text-align: center;
        margin-top: 24px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── EVOCAÇÃO DAS SECRETS ────────────────────────────────────────
try:
    client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception:
    st.warning("A chama ainda não encontrou as suas chaves. Guarde as secrets no painel do Streamlit e regresse.")
    st.stop()

# ─── O CORAÇÃO LÓGICO DO PROTOCOLO ──────────────────────────────
def definir_modo(mental, cigs, sinais):
    """
    Devolve o modo do dia, a mensagem do instrutor interior e a cor da chama.
    """
    if any(s in ["Tontura", "Dor Torácica"] for s in sinais):
        return (
            "ABORTAR",
            "O corpo pede silêncio. Suspensão imediata do movimento, apenas respiração.",
            "#FF3B30"
        )
    if mental == "Apatia" or cigs >= 16:
        return (
            "RECUPERAÇÃO",
            "Hoje és terra a repousar. Cultiva o hábito mínimo, que até a semente no escuro trabalha.",
            "#007AFF"
        )
    if mental == "Hipomania" or cigs >= 10:
        return (
            "ESTRATÉGICO",
            "A chama arde alta, mas o sábio sopra devagar. Bloqueia cargas, reduz Aeróbico 15%.",
            "#FF9F0A"
        )
    return (
        "LIMITE",
        "O altar está firme. Executa as 4 Âncoras como quem reza.",
        "#FF6B00"
    )

# ─── ESTADO INICIAL (antes do check-in) ──────────────────────────
if "modo" not in st.session_state:
    st.session_state.modo = "LIMITE"
    st.session_state.instr = "O altar está firme. Executa as 4 Âncoras como quem reza."
    st.session_state.cor = "#FF6B00"

# ─── INTERFACE: TÍTULO E CITAÇÃO ─────────────────────────────────
st.title("ODA PROTOCOL · A Arte da Reconstrução")
st.markdown("<p class='whisper'>“Somos o que repetidamente fazemos. A excelência, então, não é um ato — é um hábito.” — Aristóteles</p>", unsafe_allow_html=True)

# ─── SIDEBAR: O CONFESSIONÁRIO ──────────────────────────────────
with st.sidebar:
    st.header("Confissão do Dia")
    st.markdown("Cada resposta é um espelho. Não há juízo, apenas escuta.")

    mental = st.selectbox(
        "Como está a tua paisagem interior?",
        ["Estável", "Hipomania", "Apatia"],
        index=0,
        help="Estável: o lago sem ondas. Hipomania: vento nas velas. Apatia: neblina densa."
    )
    cigs = st.number_input(
        "Quantas testemunhas de fumo te acompanharam hoje?",
        min_value=0, max_value=40, value=0,
        help="Cada cigarro é uma pequena renúncia ao oxigénio que os teus músculos amam."
    )
    sinais = st.multiselect(
        "Há sinais no corpo que pedem atenção?",
        ["Normal", "Tontura", "Dor Torácica"],
        default=["Normal"],
        help="Tontura ou dor torácica são cartas vermelhas do teu corpo."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🜂 SINCRONIZAR"):
            modo, instr, cor = definir_modo(mental, cigs, sinais)
            st.session_state.modo = modo
            st.session_state.instr = instr
            st.session_state.cor = cor

            # Registo no livro sagrado (Supabase)
            try:
                supabase.table("oda_logs").insert({
                    "peso": 113.0,
                    "cigarros": cigs,
                    "estado_mental": mental,
                    "modo_calculado": modo,
                    "timestamp": datetime.utcnow().isoformat()
                }).execute()
                st.success("A tua confissão foi guardada no livro invisível.")
            except Exception as e:
                st.error("Houve um sopro contrário ao registar. Tenta de novo.")
    with col2:
        st.markdown("")  # respiro visual

# ─── DASHBOARD: O TRÍPTICO ───────────────────────────────────────
st.markdown("---")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class='metric-card'>
        <p style='font-size:0.9rem; letter-spacing:1px;'>MODO DE HOJE</p>
        <h1 style='color:{st.session_state.cor} !important; margin:0;'>{st.session_state.modo}</h1>
        <p class='whisper'>A chama que guia a sessão</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='metric-card'>
        <p style='font-size:0.9rem; letter-spacing:1px;'>PROTEÍNA SAGRADA</p>
        <h1 style='color:#ff6b00 !important; margin:0;'>270g</h1>
        <p class='whisper'>Pilar do templo muscular</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='metric-card'>
        <p style='font-size:0.9rem; letter-spacing:1px;'>A TERRA PROMETIDA</p>
        <h1 style='color:#ff6b00 !important; margin:0;'>-20 kg</h1>
        <p class='whisper'>Em seis luas, o homem novo</p>
    </div>
    """, unsafe_allow_html=True)

# ─── MENSAGEM DO INSTRUTOR INTERIOR ──────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='padding:16px; border-left:4px solid {st.session_state.cor}; background: rgba(255,255,255,0.02); border-radius:8px;'>
    <p style='font-size:1.1rem; margin:0;'><strong>🜁 Sussurro do Instrutor:</strong> {st.session_state.instr}</p>
</div>
""", unsafe_allow_html=True)

# ─── O ORÁCULO (GROQ) ────────────────────────────────────────────
st.markdown("---")
st.subheader("A Voz do Ferro")

if st.button("🜃 FORJAR TREINO DE HOJE"):
    with st.spinner("O fogo está a moldar a tua sessão... Aguarda um instante."):
        try:
            prompt = (
                f"João está em modo {st.session_state.modo}. "
                "Cria um treino ODA para hoje, coerente com o protocolo: "
                "Âncoras (agachamento, supino, stiff, remada curvada) sempre primeiro, "
                "descanso 120s para compostos pesados, 60–90s para moderados, 60s para isolados. "
                "Se for Lower A, inclui agachamento livre, leg press, cadeira extensora, e panturrilhas. "
                "Se for Upper A, inclui supino, remada curvada, desenvolvimento, e rosca direta. "
                "O tom deve ser poético, como um ritual de autossuperação."
            )
            resp = client_groq.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",  # Modelo válido atualizado
                temperature=0.7,
                max_tokens=800
            )
            treino = resp.choices[0].message.content
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding:20px; border-radius:12px; border:1px dashed #ff6b00;'>
                {treino}
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"O oráculo encontrou uma névoa: {e}")

# ─── RODAPÉ COM A FILOSOFIA ──────────────────────────────────────
st.markdown("---")
st.markdown("<p class='quote'>“O alarme das 04:30 e a confissão anti‑cigarro são as decisões que importam. O protocolo não exige perfeição — exige presença diária.”</p>", unsafe_allow_html=True)
st.markdown("<p class='whisper' style='text-align:center;'>ODA Protocol · Edição Anotada · Decisões validadas pelo teu psiquiatra</p>", unsafe_allow_html=True)
