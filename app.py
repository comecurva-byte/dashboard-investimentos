import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# ==========================================
# CONFIGURAÇÃO INICIAL DA PÁGINA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Painel de Investimentos",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INICIALIZAÇÃO DO ESTADO DA SESSÃO (DADOS)
# ==========================================
if "carteira" not in st.session_state:
    st.session_state.carteira = [
        # Ações Brasil (Meta: 40%)
        {"Ativo": "ALUP11", "Categoria": "Ações Brasil", "Qtd": 27, "PM": 34.82, "Preco": 39.31},
        {"Ativo": "B3SA3", "Categoria": "Ações Brasil", "Qtd": 65, "PM": 12.28, "Preco": 23.49},
        {"Ativo": "BBAS3", "Categoria": "Ações Brasil", "Qtd": 109, "PM": 21.50, "Preco": 24.28},
        {"Ativo": "BBDC3", "Categoria": "Ações Brasil", "Qtd": 85, "PM": 11.90, "Preco": 18.27},
        {"Ativo": "BBSE3", "Categoria": "Ações Brasil", "Qtd": 26, "PM": 34.39, "Preco": 42.25},
        {"Ativo": "BPAC3", "Categoria": "Ações Brasil", "Qtd": 28, "PM": 18.39, "Preco": 28.89},
        {"Ativo": "CMIG4", "Categoria": "Ações Brasil", "Qtd": 88, "PM": 9.61, "Preco": 11.86},
        {"Ativo": "CSMG3", "Categoria": "Ações Brasil", "Qtd": 35, "PM": 19.46, "Preco": 63.87},
        {"Ativo": "CXSE3", "Categoria": "Ações Brasil", "Qtd": 29, "PM": 19.31, "Preco": 21.31},
        {"Ativo": "EQTL3", "Categoria": "Ações Brasil", "Qtd": 25, "PM": 40.19, "Preco": 50.09},
        {"Ativo": "ITUB4", "Categoria": "Ações Brasil", "Qtd": 14, "PM": 27.19, "Preco": 49.18},
        {"Ativo": "KLBN4", "Categoria": "Ações Brasil", "Qtd": 241, "PM": 4.22, "Preco": 3.66},
        {"Ativo": "PSSA3", "Categoria": "Ações Brasil", "Qtd": 27, "PM": 28.61, "Preco": 52.49},
        {"Ativo": "RAIZ4", "Categoria": "Ações Brasil", "Qtd": 4, "PM": 3.79, "Preco": 0.43},
        {"Ativo": "SAPR11", "Categoria": "Ações Brasil", "Qtd": 18, "PM": 23.80, "Preco": 41.02},
        {"Ativo": "SAPR3", "Categoria": "Ações Brasil", "Qtd": 27, "PM": 3.67, "Preco": 9.12},
        {"Ativo": "SBSP3", "Categoria": "Ações Brasil", "Qtd": 49, "PM": 13.91, "Preco": 32.80},
        {"Ativo": "TAEE4", "Categoria": "Ações Brasil", "Qtd": 58, "PM": 11.37, "Preco": 15.43},
        {"Ativo": "WEGE3", "Categoria": "Ações Brasil", "Qtd": 19, "PM": 34.82, "Preco": 48.37},

        # Ações Globais / Dólar (Meta: 30%)
        {"Ativo": "MUND11", "Categoria": "Ações Globais/Dólar", "Qtd": 40, "PM": 96.23, "Preco": 96.24},
        {"Ativo": "WRLD11", "Categoria": "Ações Globais/Dólar", "Qtd": 4, "PM": 144.23, "Preco": 143.05},
        {"Ativo": "IVVB11", "Categoria": "Ações Globais/Dólar", "Qtd": 1, "PM": 431.34, "Preco": 436.01},
        {"Ativo": "DIVO11", "Categoria": "Ações Globais/Dólar", "Qtd": 5, "PM": 122.18, "Preco": 147.09},
        {"Ativo": "SMAL11", "Categoria": "Ações Globais/Dólar", "Qtd": 12, "PM": 109.74, "Preco": 138.38},
        {"Ativo": "XINA11", "Categoria": "Ações Globais/Dólar", "Qtd": 65, "PM": 7.32, "Preco": 6.62},
        {"Ativo": "Trend Bolsa Amer.", "Categoria": "Ações Globais/Dólar", "Qtd": 741.46, "PM": 0.66, "Preco": 1.00},
        {"Ativo": "Dólar Inter (US$)", "Categoria": "Ações Globais/Dólar", "Qtd": 216.0, "PM": 5.50, "Preco": 5.50},

        # IPCA+ (Meta: 20%)
        {"Ativo": "AREA11", "Categoria": "IPCA+", "Qtd": 78, "PM": 102.91, "Preco": 112.67},
        {"Ativo": "Tesouro IPCA+ 2032", "Categoria": "IPCA+", "Qtd": 0.05, "PM": 2986.00, "Preco": 3185.20},
        {"Ativo": "Tesouro IPCA+ 2050", "Categoria": "IPCA+", "Qtd": 0.19, "PM": 930.42, "Preco": 982.16},
        {"Ativo": "Tesouro IPCA+ 2040", "Categoria": "IPCA+", "Qtd": 0.35, "PM": 1653.86, "Preco": 1858.40},
        {"Ativo": "Tesouro Renda+ 2040", "Categoria": "IPCA+", "Qtd": 0.71, "PM": 1025.85, "Preco": 1097.79},

        # Cripto (Meta: 5%)
        {"Ativo": "Bitcoin (BTC)", "Categoria": "Cripto", "Qtd": 0.00984121, "PM": 341231.78, "Preco": 415741.00},
        {"Ativo": "Ethereum (ETH)", "Categoria": "Cripto", "Qtd": 0.06013332, "PM": 9704.47, "Preco": 12313.98},
        {"Ativo": "HASH11", "Categoria": "Cripto", "Qtd": 3, "PM": 24.05, "Preco": 53.37},
        {"Ativo": "USDC", "Categoria": "Cripto", "Qtd": 106.95, "PM": 5.04, "Preco": 5.50},
        {"Ativo": "USDT", "Categoria": "Cripto", "Qtd": 5.08, "PM": 5.00, "Preco": 5.50},

        # Metais (Meta: 5%)
        {"Ativo": "Ouro Físico (g)", "Categoria": "Metais", "Qtd": 2.0, "PM": 711.98, "Preco": 711.98}
    ]

if "reserva_caixa" not in st.session_state:
    st.session_state.reserva_caixa = [
        {"Item": "Tesouro Selic 2029", "Tipo": "Reserva de Emergência", "Qtd": 0.90, "Valor Aplicado": 13416.39, "Valor Atual": 17337.30},
        {"Item": "AUPO11 (Planejado)", "Tipo": "Reserva de Emergência", "Qtd": 0.0, "Valor Aplicado": 0.0, "Valor Atual": 0.0},
        {"Item": "LFTB11", "Tipo": "Contas Mensais / Fluxo", "Qtd": 59.0, "Valor Aplicado": 7602.74, "Valor Atual": 7602.74}
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# METAS DEFINIDAS
METAS = {
    "Ações Brasil": 40.0,
    "Ações Globais/Dólar": 30.0,
    "IPCA+": 20.0,
    "Cripto": 5.0,
    "Metais": 5.0
}

# ==========================================
# PROCESSAMENTO DOS DADOS DA CARTEIRA
# ==========================================
df_carteira = pd.DataFrame(st.session_state.carteira)
df_carteira["Total Investido"] = df_carteira["Qtd"] * df_carteira["PM"]
df_carteira["Valor Atual"] = df_carteira["Qtd"] * df_carteira["Preco"]
df_carteira["Lucro R$"] = df_carteira["Valor Atual"] - df_carteira["Total Investido"]
df_carteira["Lucro %"] = (df_carteira["Lucro R$"] / df_carteira["Total Investido"]) * 100

patrimonio_investido = df_carteira["Valor Atual"].sum()

df_cat = df_carteira.groupby("Categoria")["Valor Atual"].sum().reset_index()
df_cat["% Atual"] = (df_cat["Valor Atual"] / patrimonio_investido) * 100
df_cat["Meta %"] = df_cat["Categoria"].map(METAS)
df_cat["Desvio %"] = df_cat["% Atual"] - df_cat["Meta %"]

# Garantir que todas as categorias apareçam
for cat, meta in METAS.items():
    if cat not in df_cat["Categoria"].values:
        nova_linha = pd.DataFrame([{"Categoria": cat, "Valor Atual": 0.0, "% Atual": 0.0, "Meta %": meta, "Desvio %": -meta}])
        df_cat = pd.concat([df_cat, nova_linha], ignore_index=True)

# ==========================================
# BARRA LATERAL (CHAT IA & CONFIGURAÇÃO API)
# ==========================================
st.sidebar.title("💬 Chat Assistente IA")
st.sidebar.caption("Pergunte sobre seus investimentos e obtenha análises em tempo real.")

api_key = st.sidebar.text_input("Chave API Gemini:", type="password", help="Insira sua chave do Google AI Studio para ativar o Chat.")

if api_key:
    genai.configure(api_key=api_key)

for msg in st.session_state.chat_history:
    st.sidebar.chat_message(msg["role"]).write(msg["content"])

user_input = st.sidebar.chat_input("Digite sua dúvida ou comando...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.sidebar.chat_message("user").write(user_input)
    
    if api_key:
        try:
            contexto = f"Você é um consultor financeiro. O patrimônio total em investimentos do usuário é R$ {patrimonio_investido:,.2f}.\n"
            contexto += f"Resumo por categorias:\n{df_cat.to_string(index=False)}\n"
            contexto += f"Responda à dúvida do usuário de forma concisa e objetiva:\n{user_input}"
            
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(contexto)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"Erro na consulta com IA: {str(e)}"
    else:
        bot_reply = "Por favor, insira uma chave API do Gemini válida no campo acima para ativar as respostas automáticas!"
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.sidebar.chat_message("assistant").write(bot_reply)

# ==========================================
# PÁGINA PRINCIPAL - PAINEL DE CONTROLE
# ==========================================
st.title("📊 Sistema de Acompanhamento de Investimentos")
st.markdown("---")

# METRICAS DE TOPO
col1, col2, col3, col4 = st.columns(4)
total_aplicado = df_carteira["Total Investido"].sum()
lucro_total = patrimonio_investido - total_aplicado
rentabilidade_pct = (lucro_total / total_aplicado) * 100 if total_aplicado > 0 else 0

col1.metric("Patrimônio Investido", f"R$ {patrimonio_investido:,.2f}")
col2.metric("Total Aplicado", f"R$ {total_aplicado:,.2f}")
col3.metric("Lucro Total", f"R$ {lucro_total:,.2f}", delta=f"{rentabilidade_pct:.2f}%")
col4.metric("Nº de Ativos", len(df_carteira))

st.markdown("---")

# ABAS DO SISTEMA
aba1, aba2, aba3, aba4 = st.tabs(["📌 Dashboard & Rebalanceamento", "🧮 Simulador de Aportes", "🔒 Reserva & Caixa", "📝 Gestão de Ativos"])

# ==========================================
# ABA 1: DASHBOARD & REBALANCEAMENTO
# ==========================================
with aba1:
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Distribuição Atual por Categoria")
        fig_donut = px.pie(
            df_cat, 
            values="Valor Atual", 
            names="Categoria", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c2:
        st.subheader("Atual vs. Meta Percentual (%)")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_cat["Categoria"], y=df_cat["% Atual"], name="% Atual", marker_color="#3366CC"))
        fig_bar.add_trace(go.Bar(x=df_cat["Categoria"], y=df_cat["Meta %"], name="Meta %", marker_color="#109618"))
        fig_bar.update_layout(barmode="group", xaxis_title="Categoria", yaxis_title="Porcentagem (%)")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Detalhamento de Rebalanceamento")
    st.dataframe(
        df_cat.style.format({
            "Valor Atual": "R$ {:,.2f}",
            "% Atual": "{:.2f}%",
            "Meta %": "{:.2f}%",
            "Desvio %": "{:.2f}%"
        }),
        use_container_width=True
    )

# ==========================================
# ABA 2: SIMULADOR DE APORTES
# ==========================================
with aba2:
    st.subheader("Simulador Inteligente de Aportes")
    st.write("Digite o valor que pretende investir para calcular a distribuição ideal focada nas metas:")
    
    valor_aporte = st.number_input("Valor total do aporte (R$):", min_value=0.0, value=1000.0, step=100.0)
    
    if valor_aporte > 0:
        novo_patrimonio = patrimonio_investido + valor_aporte
        
        df_sim = df_cat.copy()
        df_sim["Valor Meta (R$)"] = (df_sim["Meta %"] / 100) * novo_patrimonio
        df_sim["Falta (R$)"] = df_sim["Valor Meta (R$)"] - df_sim["Valor Atual"]
        df_sim["Falta (R$)"] = df_sim["Falta (R$)"].apply(lambda x: max(0.0, x))
        
        soma_faltas = df_sim["Falta (R$)"].sum()
        
        if soma_faltas > 0:
            df_sim["Sugestão Aporte (R$)"] = (df_sim["Falta (R$)"] / soma_faltas) * valor_aporte
        else:
            df_sim["Sugestão Aporte (R$)"] = (df_sim["Meta %"] / 100) * valor_aporte

        st.markdown(f"### Sugestão de Distribuição para R$ {valor_aporte:,.2f}")
        st.dataframe(
            df_sim[["Categoria", "% Atual", "Meta %", "Valor Atual", "Sugestão Aporte (R$)"]].style.format({
                "% Atual": "{:.2f}%",
                "Meta %": "{:.2f}%",
                "Valor Atual": "R$ {:,.2f}",
                "Sugestão Aporte (R$)": "R$ {:,.2f}"
            }),
            use_container_width=True
        )

# ==========================================
# ABA 3: RESERVA & CAIXA OPERACIONAL
# ==========================================
with aba3:
    st.subheader("🛡️ Reserva de Emergência & Caixa de Curto Prazo")
    st.info("Estes valores são mantidos em monitoramento isolado e NÃO afetam os gráficos e metas de investimentos.")
    
    df_rc = pd.DataFrame(st.session_state.reserva_caixa)
    st.dataframe(
        df_rc.style.format({
            "Qtd": "{:.2f}",
            "Valor Aplicado": "R$ {:,.2f}",
            "Valor Atual": "R$ {:,.2f}"
        }),
        use_container_width=True
    )

# ==========================================
# ABA 4: GESTÃO DE ATIVOS & NOVO APORTE (PM)
# ==========================================
with aba4:
    st.subheader("➕ Registrar Novo Aporte & Recalcular Preço Médio")
    
    with st.form("form_aporte"):
        c1, c2, c3 = st.columns(3)
        ativo_sel = c1.selectbox("Selecione o Ativo:", df_carteira["Ativo"].tolist())
        qtd_comprada = c2.number_input("Quantidade Comprada:", min_value=0.0, value=1.0)
        preco_compra = c3.number_input("Preço de Compra Unitário (R$):", min_value=0.0, value=10.0)
        
        btn_salvar = st.form_submit_button("Atualizar Carteira")
        
        if btn_salvar:
            for item in st.session_state.carteira:
                if item["Ativo"] == ativo_sel:
                    qtd_antiga = item["Qtd"]
                    pm_antigo = item["PM"]
                    
                    nova_qtd = qtd_antiga + qtd_comprada
                    novo_pm = ((qtd_antiga * pm_antigo) + (qtd_comprada * preco_compra)) / nova_qtd if nova_qtd > 0 else 0
                    
                    item["Qtd"] = nova_qtd
                    item["PM"] = novo_pm
                    item["Preco"] = preco_compra
                    
                    st.success(f"Aporte em **{ativo_sel}** atualizado! Nova Qtd: {nova_qtd:.2f} | Novo PM: R$ {novo_pm:.2f}")
                    st.rerun()

    st.markdown("---")
    st.subheader("Carteira de Ativos Completa")
    st.dataframe(
        df_carteira[["Ativo", "Categoria", "Qtd", "PM", "Preco", "Total Investido", "Valor Atual", "Lucro R$", "Lucro %"]].style.format({
            "Qtd": "{:.4f}",
            "PM": "R$ {:,.2f}",
            "Preco": "R$ {:,.2f}",
            "Total Investido": "R$ {:,.2f}",
            "Valor Atual": "R$ {:,.2f}",
            "Lucro R$": "R$ {:,.2f}",
            "Lucro %": "{:.2f}%"
        }),
        use_container_width=True
    )
