import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
from google import genai
import os

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Painel de Acompanhamento de Investimentos",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. SISTEMA DE AUTENTICAÇÃO E LOGIN
# -----------------------------------------------------------------------------
names = ['Caio Sertori']
usernames = ['sertcaio']
# Hash para a senha padrão: "Gabigol2019!"
hashed_passwords = ['$2b$12$eImiTXuWVxfM37uY4JANjO5E/CkWp/E0xTjG.2H1V11T3r8H.O8E2']

credentials = {
    'usernames': {
        usernames[0]: {
            'name': names[0],
            'password': hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'dashboard_invest_cookie',
    'chave_secreta_assinatura_12345',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('main', fields={'Form name': '🔒 Login do Painel de Investimentos'})

if authentication_status == False:
    st.error('❌ Usuário ou senha incorretos.')
    st.stop()
elif authentication_status == None:
    st.warning('👈 Por favor, digite suas credenciais para acessar o painel.')
    st.info('💡 **Credenciais de teste:** Usuário: `caio` | Senha: `invest123`')
    st.stop()

# -----------------------------------------------------------------------------
# 3. INTERFACE PRINCIPAL (AUTENTICADO)
# -----------------------------------------------------------------------------
st.sidebar.write(f"👤 Bem-vindo, **{name}**!")
authenticator.logout('🚪 Sair', 'sidebar')
st.sidebar.divider()

st.title("📈 Painel de Acompanhamento de Investimentos")
st.markdown("Acompanhe o rebalanceamento da sua carteira, simule novos aportes e monitore sua reserva.")

# -----------------------------------------------------------------------------
# 4. BASE DE DADOS DOS INVESTIMENTOS (CARTEIRA ATIVA)
# -----------------------------------------------------------------------------
data_investimentos = [
    # Ações Brasil (Meta 40%)
    {"Ativo": "ALUP11", "Categoria": "Ações Brasil", "Qtd": 27, "PM": 34.82, "PrecoAtual": 39.31},
    {"Ativo": "B3SA3", "Categoria": "Ações Brasil", "Qtd": 65, "PM": 12.28, "PrecoAtual": 23.49},
    {"Ativo": "BBAS3", "Categoria": "Ações Brasil", "Qtd": 109, "PM": 21.50, "PrecoAtual": 24.28},
    {"Ativo": "BBDC3", "Categoria": "Ações Brasil", "Qtd": 85, "PM": 11.90, "PrecoAtual": 18.27},
    {"Ativo": "BBSE3", "Categoria": "Ações Brasil", "Qtd": 26, "PM": 34.39, "PrecoAtual": 42.25},
    {"Ativo": "BPAC3", "Categoria": "Ações Brasil", "Qtd": 28, "PM": 18.39, "PrecoAtual": 28.89},
    {"Ativo": "CMIG4", "Categoria": "Ações Brasil", "Qtd": 88, "PM": 9.61, "PrecoAtual": 11.86},
    {"Ativo": "CSMG3", "Categoria": "Ações Brasil", "Qtd": 35, "PM": 19.46, "PrecoAtual": 63.87},
    {"Ativo": "CXSE3", "Categoria": "Ações Brasil", "Qtd": 29, "PM": 19.31, "PrecoAtual": 21.31},
    {"Ativo": "EQTL3", "Categoria": "Ações Brasil", "Qtd": 25, "PM": 40.19, "PrecoAtual": 50.09},
    {"Ativo": "ITUB4", "Categoria": "Ações Brasil", "Qtd": 14, "PM": 27.19, "PrecoAtual": 49.18},
    {"Ativo": "KLBN4", "Categoria": "Ações Brasil", "Qtd": 241, "PM": 4.22, "PrecoAtual": 3.66},
    {"Ativo": "PSSA3", "Categoria": "Ações Brasil", "Qtd": 27, "PM": 28.61, "PrecoAtual": 52.49},
    {"Ativo": "RAIZ4", "Categoria": "Ações Brasil", "Qtd": 4, "PM": 3.79, "PrecoAtual": 0.43},
    {"Ativo": "SAPR11", "Categoria": "Ações Brasil", "Qtd": 18, "PM": 23.80, "PrecoAtual": 41.02},
    {"Ativo": "SAPR3", "Categoria": "Ações Brasil", "Qtd": 27, "PM": 3.67, "PrecoAtual": 9.12},
    {"Ativo": "SBSP3", "Categoria": "Ações Brasil", "Qtd": 49, "PM": 13.91, "PrecoAtual": 32.80},
    {"Ativo": "TAEE4", "Categoria": "Ações Brasil", "Qtd": 58, "PM": 11.37, "PrecoAtual": 15.43},
    {"Ativo": "WEGE3", "Categoria": "Ações Brasil", "Qtd": 19, "PM": 34.82, "PrecoAtual": 48.37},
    {"Ativo": "DIVO11", "Categoria": "Ações Brasil", "Qtd": 5, "PM": 122.18, "PrecoAtual": 147.09},
    {"Ativo": "SMAL11", "Categoria": "Ações Brasil", "Qtd": 12, "PM": 109.74, "PrecoAtual": 138.38},

    # Ações Globais & Dólar (Meta 30% -> MUND11 25%, Dólar 5%)
    {"Ativo": "MUND11", "Categoria": "Ações Globais & Dólar", "Qtd": 40, "PM": 96.23, "PrecoAtual": 96.24},
    {"Ativo": "WRLD11", "Categoria": "Ações Globais & Dólar", "Qtd": 4, "PM": 144.23, "PrecoAtual": 143.05},
    {"Ativo": "IVVB11", "Categoria": "Ações Globais & Dólar", "Qtd": 1, "PM": 431.34, "PrecoAtual": 436.01},
    {"Ativo": "XINA11", "Categoria": "Ações Globais & Dólar", "Qtd": 65, "PM": 7.32, "PrecoAtual": 6.62},
    {"Ativo": "Trend Bolsa Amer. FI", "Categoria": "Ações Globais & Dólar", "Qtd": 1, "PM": 490.31, "PrecoAtual": 741.46},
    {"Ativo": "Dólar Banco Inter", "Categoria": "Ações Globais & Dólar", "Qtd": 216, "PM": 5.50, "PrecoAtual": 5.50},
    {"Ativo": "USDC", "Categoria": "Ações Globais & Dólar", "Qtd": 106.95, "PM": 5.04, "PrecoAtual": 5.50},
    {"Ativo": "USDT", "Categoria": "Ações Globais & Dólar", "Qtd": 5.08, "PM": 5.00, "PrecoAtual": 5.50},

    # IPCA+ (Meta 20%)
    {"Ativo": "AREA11", "Categoria": "IPCA+", "Qtd": 78, "PM": 102.91, "PrecoAtual": 112.67},
    {"Ativo": "Tesouro IPCA+ 2032", "Categoria": "IPCA+", "Qtd": 0.05, "PM": 2986.00, "PrecoAtual": 3185.20},
    {"Ativo": "Tesouro IPCA+ 2050", "Categoria": "IPCA+", "Qtd": 0.19, "PM": 930.42, "PrecoAtual": 982.15},
    {"Ativo": "Tesouro IPCA+ 2040", "Categoria": "IPCA+", "Qtd": 0.35, "PM": 1653.86, "PrecoAtual": 1858.40},
    {"Ativo": "Tesouro Renda+ 2040", "Categoria": "IPCA+", "Qtd": 0.71, "PM": 1025.85, "PrecoAtual": 1097.78},

    # Cripto (Meta 5%)
    {"Ativo": "Bitcoin (BTC)", "Categoria": "Cripto", "Qtd": 0.00984121, "PM": 341231.78, "PrecoAtual": 415739.50},
    {"Ativo": "Ethereum (ETH)", "Categoria": "Cripto", "Qtd": 0.06013332, "PM": 9704.47, "PrecoAtual": 12313.98},
    {"Ativo": "HASH11", "Categoria": "Cripto", "Qtd": 3, "PM": 24.05, "PrecoAtual": 53.37},

    # Metais (Meta 5%: Ouro 4%, Prata 1%)
    {"Ativo": "Ouro Físico (2g)", "Categoria": "Metais", "Qtd": 2, "PM": 711.98, "PrecoAtual": 711.98}
]

df = pd.DataFrame(data_investimentos)
df["TotalInvestido"] = df["Qtd"] * df["PM"]
df["ValorAtual"] = df["Qtd"] * df["PrecoAtual"]
df["LucroPrejuizo"] = df["ValorAtual"] - df["TotalInvestido"]

# -----------------------------------------------------------------------------
# 5. QUADRO DE METAS DA CARTEIRA ATIVA
# -----------------------------------------------------------------------------
metas = {
    "Ações Brasil": 0.40,
    "Ações Globais & Dólar": 0.30,
    "IPCA+": 0.20,
    "Cripto": 0.05,
    "Metais": 0.05
}

df_cat = df.groupby("Categoria")["ValorAtual"].sum().reset_index()
total_carteira_ativa = df_cat["ValorAtual"].sum()

df_cat["% Atual"] = df_cat["ValorAtual"] / total_carteira_ativa
df_cat["Meta (%)"] = df_cat["Categoria"].map(metas)
df_cat["Valor Ideal (R$)"] = total_carteira_ativa * df_cat["Meta (%)"]
df_cat["Desvio (R$)"] = df_cat["Valor Ideal (R$)"] - df_cat["ValorAtual"]

# -----------------------------------------------------------------------------
# 6. EXIBIÇÃO DE MÉTRICAS E GRÁFICOS
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Carteira Ativa Total", f"R$ {total_carteira_ativa:,.2f}")
col2.metric("Total Investido (PM)", f"R$ {df['TotalInvestido'].sum():,.2f}")
lucro_total = df['ValorAtual'].sum() - df['TotalInvestido'].sum()
col3.metric("Lucro / Prejuízo", f"R$ {lucro_total:,.2f}", delta=f"{(lucro_total/df['TotalInvestido'].sum())*100:.2f}%")

st.divider()

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("📊 Alocação Atual por Categoria")
    fig = px.pie(df_cat, names="Categoria", values="ValorAtual", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🎯 Comparativo: Alocação Atual vs. Meta")
    df_comp = df_cat.melt(id_vars=["Categoria"], value_vars=["% Atual", "Meta (%)"], var_name="Tipo", value_name="Porcentagem")
    df_comp["Porcentagem"] = df_comp["Porcentagem"] * 100
    fig_bar = px.bar(df_comp, x="Categoria", y="Porcentagem", color="Tipo", barmode="group", text_auto=".1f%")
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# 7. ÁREA DE MONITORAMENTO ISOLADA (RESERVA DE EMERGÊNCIA & CONTAS)
# -----------------------------------------------------------------------------
st.divider()
st.subheader("🛡️ Painel de Monitoramento Isolado (Fora da Carteira de Investimentos)")

m1, m2 = st.columns(2)

with m1:
    st.info("📌 **Reserva de Emergência**")
    st.write("• **Tesouro Selic 2029:** R$ 17.337,30 (0,90 cotas)")
    st.write("• **AUPO11:** R$ 0,00 (Reservado para aportes futuros)")
    st.metric("Total Reserva de Emergência", "R$ 17.337,30")

with m2:
    st.warning("📌 **Caixa / Contas Mensais**")
    st.write("• **LFTB11:** R$ 7.602,74 (59 cotas)")
    st.metric("Total Caixa Operacional", "R$ 7.602,74")

# -----------------------------------------------------------------------------
# 8. SIMULADOR DE APORTES
# -----------------------------------------------------------------------------
st.divider()
st.subheader("🧮 Simulador Inteligente de Aportes")
aporte_novo = st.number_input("Digite o valor que deseja aportar (R$):", min_value=0.0, value=2000.0, step=100.0)

if aporte_novo > 0:
    novo_total = total_carteira_ativa + aporte_novo
    df_cat["Meta Rebalanceada (R$)"] = novo_total * df_cat["Meta (%)"]
    df_cat["Necessidade (R$)"] = df_cat["Meta Rebalanceada (R$)"] - df_cat["ValorAtual"]
    df_cat["Sugestão Aporte (R$)"] = df_cat["Necessidade (R$)"].apply(lambda x: max(0.0, x))
    
    # Ajuste proporcional se o aporte não cobrir 100% da necessidade
    soma_sugestoes = df_cat["Sugestão Aporte (R$)"].sum()
    if soma_sugestoes > 0:
        df_cat["Aporte Recomendado (R$)"] = (df_cat["Sugestão Aporte (R$)"] / soma_sugestoes) * aporte_novo
    else:
        df_cat["Aporte Recomendado (R$)"] = 0.0

    st.write("**Sugestão de distribuição do novo aporte para manter o equilíbrio das metas:**")
    st.dataframe(df_cat[["Categoria", "ValorAtual", "% Atual", "Meta (%)", "Aporte Recomendado (R$)"]].style.format({
        "ValorAtual": "R$ {:,.2f}",
        "% Atual": "{:.1%}",
        "Meta (%)": "{:.1%}",
        "Aporte Recomendado (R$)": "R$ {:,.2f}"
    }), use_container_width=True)

# -----------------------------------------------------------------------------
# 9. CHAT INTEGRADO COM GEMINI API (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.subheader("🤖 Assistente de Investimentos")

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.sidebar.caption("⚠️ Para ativar o chat, configure a chave `GEMINI_API_KEY` nos Secrets do Streamlit.")
else:
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for msg in st.session_state.chat_messages:
        st.sidebar.chat_message(msg["role"]).write(msg["content"])

    user_input = st.sidebar.chat_input("Dúvida ou sugestão de alteração?")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.sidebar.chat_message("user").write(user_input)
        
        try:
            client = genai.Client(api_key=api_key)
            prompt_contexto = f"Você é o assistente do Caio. A carteira ativa atual é de R$ {total_carteira_ativa:,.2f} dividida em: Ações Brasil (40%), Ações Globais/Dólar (30%), IPCA+ (20%), Cripto (5%) e Metais (5%). Responda de forma breve: {user_input}"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_contexto
            )
            bot_reply = response.text
            st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
            st.sidebar.chat_message("assistant").write(bot_reply)
        except Exception as e:
            st.sidebar.error(f"Erro ao conectar com a API: {e}")
