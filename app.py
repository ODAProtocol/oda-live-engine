import streamlit as st
import pandas as pd
from groq import Groq
from supabase import create_client

# --- ESTÉTICA TÁTICA ODA ---
st.set_page_config(page_title="ODA ENGINE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 107, 0, 0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    h1, h2 { color: #ff6b00 !important; }
    .stButton>button { background: #ff6b00; color: black; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO SEGURA (SECRETS) ---
# O erro de ModuleNotFoundError deve sumir após o reboot com o requirements.txt
try:
    client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("Aguardando configuração das Secrets no painel do Streamlit...")
    st.stop()

# --- MOTOR DE LÓGICA ODA ---
def definir_modo(mental, cigs, sinais):
    if any(s in ["Tontura", "Dor Torácica"] for s in sinais):
        return "ABORTAR", "⚠️ SUSPENSÃO IMEDIATA", "#FF3B30"
    if mental == "Apatia" or cigs >= 16:
        return "RECUPERAÇÃO", "Foco no hábito mínimo.", "#007AFF"
    if mental == "Hipomania" or cigs >= 10:
        return "ESTRATÉGICO", "Bloquear cargas. -15% Aeróbico.", "#FF9F0A"
    return "LIMITE", "Padrão: Executar 4 Âncoras.", "#FF6B00"

# --- INTERFACE ---
st.title("ODA PROTOCOL // LIVE")

with st.sidebar:
    st.header("Check-in")
    mental = st.selectbox("Mental", ["Estável", "Hipomania", "Apatia"])
    cigs = st.number_input("Cigarros", 0, 40, 0)
    sinais = st.multiselect("Alertas", ["Normal", "Tontura", "Dor Torácica"])
    
    if st.button("SINCRONIZAR"):
        modo, instr, cor = definir_modo(mental, cigs, sinais)
        supabase.table("oda_logs").insert({
            "peso": 113.0, "cigarros": cigs, "estado_mental": mental, 
            "modo_calculado": modo
        }).execute()
        st.success("Dados na Supabase!")

# DASHBOARD
modo, instr, cor = definir_modo(mental, cigs, sinais)
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='metric-card'><p>MODO</p><h1 style='color:{cor} !important;'>{modo}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><p>PROTEÍNA</p><h1>270g</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><p>META</p><h1>-20kg</h1></div>", unsafe_allow_html=True)

st.warning(f"**INSTRUTOR:** {instr}")

if st.button("GERAR TREINO (GROQ)"):
    resp = client_groq.chat.completions.create(
        messages=[{"role": "user", "content": f"João em modo {modo}. Gere treino ODA."}],
        model="llama3-70b-8192"
    )
    st.write(resp.choices[0].message.content)