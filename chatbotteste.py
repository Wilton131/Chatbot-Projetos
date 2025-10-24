import streamlit as st
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Guia IR 2025", page_icon="🦁", layout="wide")

# --- TÍTULO E INTRODUÇÃO ---
st.title("🦁 Guia Rápido: Imposto de Renda")
st.write("""
Olá! Sou seu assistente virtual para tirar dúvidas sobre o Imposto de Renda.
Por favor, **selecione um tópico abaixo para começar.**
""")

# --- GERENCIAMENTO DE ESTADO (MEMÓRIA E ESTÁGIO DA CONVERSA) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.session_state.messages.append(
        {"role": "assistant", "content": "Bem-vindo! Por favor, escolha uma das categorias de dúvida abaixo."}
    )

if "stage" not in st.session_state:
    st.session_state.stage = "menu_principal"

# --- FUNÇÕES DE CALLBACK ---
def set_stage(stage):
    st.session_state.stage = stage

def handle_option_click(user_choice, bot_response, next_stage):
    st.session_state.messages.append({"role": "user", "content": user_choice})
    
    with st.chat_message("assistant"):
        with st.spinner("Consultando informações..."):
            time.sleep(0.5)
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    set_stage(next_stage)


# --- EXIBIÇÃO DO HISTÓRICO DA CONVERSA ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE EXIBIÇÃO BASEADA NO ESTÁGIO ---
st.chat_input("Use os botões para navegar.", disabled=True)
button_container = st.container()

# ================== NÍVEL 1: INÍCIO ==================
if st.session_state.stage == "menu_principal":
    with button_container:
        st.button("Como isso me afeta? 🙋", on_click=handle_option_click,
                  args=["Como a nova lei me afeta?",
                        "Para entender como a nova lei te afeta diretamente, por favor, escolha uma das categorias abaixo:",
                        "menu_afeta_pessoal"])
        
        st.button("Como isso afeta a economia? 📈", on_click=handle_option_click,
                  args=["Como a reforma afeta a economia?",
                        "Para saber o impacto macro, selecione uma das opções:",
                        "menu_afeta_economia"])
        
        st.button("Quais as mudanças em relação à lei anterior? 🔄", on_click=handle_option_click,
                  args=["Quais são as principais mudanças?",
                        "Para te dar uma visão geral, preciso que você escolha uma opção abaixo:",
                        "menu_mudancas_anteriores"])

# ================== NÍVEL 2 ==================
elif st.session_state.stage == "menu_afeta_pessoal":
    with button_container:
        st.button("Como isso vai afetar a minha renda? 💰", on_click=handle_option_click,
                  args=["Como a lei impacta minha renda?",
                        "Para analisar o impacto na sua renda, selecione o tipo de rendimento:",
                        "submenu_renda"])
        
        st.button("Como vai mudar minha declaração? 📄", on_click=handle_option_click,
                  args=["Como a lei muda a declaração?",
                        "Para entender as mudanças na declaração, por favor, escolha sua categoria de contribuinte:",
                        "submenu_declaracao"])
        
        st.button("⬅️ Voltar", on_click=set_stage, args=["menu_principal"])

elif st.session_state.stage == "menu_afeta_economia":
    with button_container:
        st.button("Como será feita a arrecadação? 📊", on_click=handle_option_click,
                  args=["Como será a arrecadação?",
                        "**(Conteúdo em desenvolvimento)**\n\nEssa seção explicará as novas formas de arrecadação do governo com a reforma. Em breve, mais informações detalhadas.",
                        "menu_principal"])
        
        st.button("O que vai mudar na sociedade? 🌐", on_click=handle_option_click,
                  args=["O que muda para a sociedade?",
                        "Para entender o impacto social, por favor, escolha uma opção:",
                        "submenu_sociedade"])
        
        st.button("⬅️ Voltar", on_click=set_stage, args=["menu_principal"])

elif st.session_state.stage == "menu_mudancas_anteriores":
    with button_container:
        st.button("Projeto de Lei Explicado 📋", on_click=handle_option_click,
                  args=["Explique o Projeto de Lei.",
                        "**(Conteúdo em desenvolvimento)**\n\nEsta seção trará uma análise comparativa e detalhada do novo Projeto de Lei, explicando os pontos-chave e as principais diferenças em relação à legislação anterior.",
                        "menu_principal"])

        st.button("⬅️ Voltar", on_click=set_stage, args=["menu_principal"])


# ================== NÍVEL 3 ==================
elif st.session_state.stage == "submenu_renda":
    with button_container:
        st.button("Como juros serão tratados? 🏦", on_click=handle_option_click,
                  args=["Tratamento de juros.",
                        """
                        **Como os Juros serão tratados?** (Calculadora em desenvolvimento)
                        
                        **(Conteúdo em desenvolvimento)**
                        
                        A nova lei pode alterar a forma de tributação de juros sobre capital próprio (JCP) e outros rendimentos de juros. Em uma futura versão, esta funcionalidade terá uma calculadora interativa para simular o impacto.""",
                        "menu_afeta_pessoal"]) # Volta para o menu "Como isso me afeta?"

        st.button("Os dividendos serão taxados? 📈", on_click=handle_option_click,
                  args=["Tributação de dividendos.",
                        """
                        **Tributação de Dividendos** (Calculadora em desenvolvimento)
                        
                        **(Conteúdo em desenvolvimento)**
                        
                        A proposta de reforma prevê a tributação dos dividendos, que hoje são isentos de imposto para pessoa física. Esta funcionalidade terá uma calculadora interativa para simular o impacto.""",
                        "menu_afeta_pessoal"])

        st.button("Como afeta o meu Salário? 💼", on_click=handle_option_click,
                  args=["Impacto no salário.",
                        """
                        **Impacto no Salário** (Calculadora em desenvolvimento)
                        
                        **(Conteúdo em desenvolvimento)**
                        
                        A nova lei pode alterar as faixas de alíquotas e as deduções simplificadas, o que impactaria diretamente o imposto retido na fonte. Futuramente, teremos uma calculadora para simular o novo cálculo.""",
                        "menu_afeta_pessoal"])
        
        st.button("⬅️ Voltar", on_click=set_stage, args=["menu_afeta_pessoal"])

elif st.session_state.stage == "submenu_declaracao":
    with button_container:
        st.button("Sou PF, o que vai mudar? 🧍‍♂️", on_click=handle_option_click,
                  args=["Mudanças para Pessoa Física.",
                        "Para entender as mudanças para Pessoa Física, por favor, selecione seu tipo de rendimento:",
                        "submenu_pf_pj"])
        
        st.button("Sou PJ, o que vai mudar? 🏢", on_click=handle_option_click,
                  args=["Mudanças para Pessoa Jurídica.",
                        "Para entender as mudanças para Pessoa Jurídica, por favor, selecione seu tipo de empresa:",
                        "submenu_pf_pj_pj"]) # O nome do estágio é arbitrário, pode ser renomeado
        
        st.button("⬅️ Voltar", on_click=set_stage, args=["menu_afeta_pessoal"])
        
elif st.session_state.stage == "submenu_sociedade":
    with button_container:
        st.button("Impactos da reforma 📊", on_click=handle_option_click,
                  args=["Quais os impactos da reforma?",
                        "**(Conteúdo em desenvolvimento)**\n\nEsta seção detalhará o impacto da reforma em diferentes camadas da sociedade, incluindo mudanças sociais e o papel do governo na nova estrutura tributária.",
                        "menu_principal"])
        
        st.button("⬅️ Voltar", on_click=set_stage, args=["menu_afeta_economia"])

# ================== NÍVEL 4 ==================
elif st.session_state.stage == "submenu_pf_pj":
    with button_container:
        st.button("Mudanças para CLT", on_click=handle_option_click,
                  args=["Mudanças para CLT.",
                        "**(Conteúdo em desenvolvimento)**\n\nInformações sobre o impacto direto para trabalhadores com carteira assinada. Em breve, detalhes sobre novas faixas e alíquotas.",
                        "submenu_declaracao"])
        st.button("Mudanças para Aposentado", on_click=handle_option_click,
                  args=["Mudanças para Aposentado.",
                        "**(Conteúdo em desenvolvimento)**\n\nAnálise sobre as mudanças que afetam a renda de aposentados e pensionistas.",
                        "submenu_declaracao"])
        st.button("⬅️ Voltar", on_click=set_stage, args=["submenu_declaracao"])

elif st.session_state.stage == "submenu_pf_pj_pj":
    with button_container:
        st.button("Mudanças para MEI", on_click=handle_option_click,
                  args=["Mudanças para MEI.",
                        "**(Conteúdo em desenvolvimento)**\n\nInformações sobre as mudanças para Microempreendedores Individuais.",
                        "submenu_declaracao"])
        st.button("Mudanças para Empresas", on_click=handle_option_click,
                  args=["Mudanças para Empresas.",
                        "**(Conteúdo em desenvolvimento)**\n\nAnálise sobre o impacto da reforma para empresas de outros regimes tributários.",
                        "submenu_declaracao"])
        st.button("⬅️ Voltar", on_click=set_stage, args=["submenu_declaracao"])


# --- DISCLAIMER / AVISO LEGAL ---
st.divider()
st.caption("Aviso: As informações fornecidas por este assistente são para fins educacionais e de orientação. Elas não constituem aconselhamento jurídico ou financeiro e não substituem a consulta a um contador ou profissional qualificado. A legislação tributária está sujeita a alterações.")