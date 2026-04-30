E certifica-te de que a chave usada (`SUPABASE_KEY`) é a **service_role** (tem permissão de inserção).
""")

# ══════════════════════════════════════════════════════════════════
# FORJAR TREINO — O Oráculo com IA
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.subheader("Forja do Treino · Llama 3.3")

if st.button("🜃 FORJAR TREINO DE HOJE"):
with st.spinner("O fogo está a moldar a tua sessão... respira fundo."):
try:
# Prompt contextual com base no PDF
prompt = (
    f"João está em modo {st.session_state.modo}. "
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
st.markdown(f"""
<div style='background: rgba(20,20,20,0.9); padding:24px; border-radius:12px; border:1px dashed #ff6b00;'>
    {treino}
</div>
""", unsafe_allow_html=True)
except Exception as e:
st.error(f"O oráculo encontrou uma névoa: {e}")

# ══════════════════════════════════════════════════════════════════
# RODAPÉ — Como a última página do PDF
# ══════════════════════════════════════════════════════════════════
st.markdown("<div class='footer-quote'>“O alarme das 04:30 e a confissão anti‑cigarro são as decisões que importam. O protocolo não exige perfeição — exige presença diária.”</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#a09080; font-size:0.8rem;'>ODA Protocol · Reconstituição · Decisões clínicas validadas pelo psiquiatra</p>", unsafe_allow_html=True)
