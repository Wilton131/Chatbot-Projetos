import streamlit as st
import time
from dataclasses import dataclass
 
# ====================== CONFIG ======================
st.set_page_config(page_title="Guia IR 2025", page_icon="🦁", layout="wide")
 
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stage" not in st.session_state:
    st.session_state.stage = "menu_principal"
if "trail" not in st.session_state:
    st.session_state.trail = ["menu_principal"]
 
WELCOME = "Bem-vindo! Por favor, escolha uma das categorias de dúvida abaixo."
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": WELCOME})
 
# ====================== MODELO DE OPÇÕES ======================
@dataclass
class Option:
    label: str
    user_msg: str
    bot_msg: str
    next_stage: str | None
 
# ====================== TEXTINHOS ======================
EXTRA_TEXTS = {
    "menu_principal": "Escolha um caminho: impacto pessoal, efeitos na economia ou mudanças em relação à lei anterior.",
    "menu_afeta_pessoal": "Veja como a reforma impacta a renda e a declaração individual.",
    "menu_afeta_economia": "Impactos macroeconômicos: arrecadação, consumo, investimento e desigualdade.",
    "menu_mudancas_anteriores": "Comparativo entre o sistema atual e o proposto pelo PL 1.087/2025.",
    "submenu_renda": "Explore como salários, dividendos e aplicações financeiras são afetados. Abaixo, use a calculadora para simular o impacto.",
    "submenu_declaracao": "Mudanças na declaração para PF e PJ.",
    "submenu_sociedade": "Impactos sociais e redistributivos da reforma.",
    "submenu_pf_pj": "Pessoa Física: CLT e aposentados.",
    "submenu_pf_pj_pj": "Pessoa Jurídica: MEI e empresas.",
    "submenu_projeto": "Veja dados oficiais do IBRE, Tesouro e artigos do PL 1.087/2025.",
}
 
# ====================== ROTAS ======================
ROUTES: dict[str, list[Option]] = {
    "menu_principal": [
        Option("Como isso me afeta? 🙋", "Como a nova lei me afeta?",
               "Para entender como a nova lei te afeta diretamente, escolha uma categoria:", "menu_afeta_pessoal"),
        Option("Como isso afeta a economia? 📈", "Como a reforma afeta a economia?",
               "Para saber o impacto macro, selecione uma opção:", "menu_afeta_economia"),
        Option("Quais as mudanças em relação à lei anterior? 🔄", "Quais são as principais mudanças?",
               "Veja as principais diferenças e o texto do projeto:", "menu_mudancas_anteriores"),
    ],
 
    # --- IMPACTO PESSOAL ---
    "menu_afeta_pessoal": [
        Option("Como isso vai afetar minha renda? 💰", "Como a lei impacta minha renda?",
               "Selecione o tipo de rendimento para ver o impacto:", "submenu_renda"),
        Option("Como vai mudar minha declaração? 📄", "Como a lei muda a declaração?",
               "Escolha sua categoria de contribuinte:", "submenu_declaracao"),
    ],
 
    # --- RENDA ---
    "submenu_renda": [
        Option("Salário 💼", "Meu salário líquido vai mudar?",
               "A reforma eleva a isenção para quem ganha até **R$ 5 mil mensais** e concede **redução (alívio) até R$ 7 mil** a partir de 2026.\n\n"
               "Para quem está nessas faixas, o salário líquido tende a aumentar, já que o IR retido será menor. "
               "O **imposto mínimo (top-up)** só afeta quem tem rendas muito altas, acima de **R$ 1 milhão por ano**.\n\n"
               "**Fonte:** Estudo da SPE – *Impactos do PL 1.087/2025*; Ministério da Fazenda (jun/2025).",
               "submenu_renda"),
 
        Option("Dividendos 📈", "Vou ter que pagar imposto sobre dividendos das ações?",
               "Dividendos passam a ter **retenção na fonte de 10%** já em 2026, mas somente sobre a parcela acima de **R$ 50 mil por mês por fonte pagadora**.\n\n"
               "Esse recolhimento antecipa o acerto do **imposto mínimo (IRPFM)** no ajuste anual de 2027, referente às rendas de 2026.\n\n"
               "Caso a empresa comprove que pagou **IRPJ/CSLL efetivo de 34% (ou 45% se financeira)**, o sócio fica dispensado de pagar complemento.\n\n"
               "**Fonte:** PL nº 1.087/2025 – Câmara dos Deputados; Estudo da SPE – *Impactos do PL 1.087/2025*.",
               "submenu_renda"),
 
        Option("Juros / Poupança / CDB / Tesouro Direto 💰", "Como a reforma muda o imposto sobre poupança, CDB e Tesouro Direto?",
               "Poupança e LCI/LCA continuam **isentas**. CDB, Tesouro Direto e outras aplicações seguem com **tributação exclusiva na fonte (15%)**.\n\n"
               "A novidade é que esses impostos retidos passam a **entrar no cálculo do imposto mínimo (top-up)** no fim do ano — afetando apenas quem está no grupo de altíssima renda.\n\n"
               "**Fonte:** Estudo da SPE – *Impactos do PL 1.087/2025*.",
               "submenu_renda"),
 
        Option("Abrir calculadora 🧮", "Quero simular meu caso.",
               "Use a calculadora abaixo para simular o impacto na sua renda total:", "calculadora_ir"),
    ],
 
 
    # --- DECLARAÇÃO ---
    "submenu_declaracao": [
        Option("Pessoa Física 🧍", "Sou pessoa física, o que muda?",
               "Escolha entre trabalhador CLT ou aposentado:", "submenu_pf_pj"),
        Option("Pessoa Jurídica 🏢", "Sou pessoa jurídica, o que muda?",
               "Escolha seu tipo de empresa:", "submenu_pf_pj_pj"),
    ],
 
    # --- PESSOA FÍSICA ---
   "submenu_pf_pj": [
        Option("Trabalhador CLT 👷", "Sou trabalhador CLT, o que muda para mim?",
               "Em 2026, a retenção na fonte refletirá a **isenção até R$ 5 mil** e o **alívio até R$ 7 mil**. "
               "No ajuste de 2027 (ano-base 2026), só entra o **imposto mínimo (IRPFM)** para altíssima renda — "
               "portanto, trabalhadores CLT típicos **não são afetados**.\n\n"
               "PLR, 13º e impostos na fonte entram no cálculo do *top-up* apenas para quem está no topo da pirâmide.\n\n"
               "**Fonte:** Estudo da SPE – *Impactos do PL 1.087/2025*.",
               "submenu_declaracao"),
 
        Option("Aposentado 👴", "Sou aposentado, preciso declarar diferente?",
               "As regras gerais de declaração **não mudam** com o PL 1.087/2025. "
               "Benefícios **isentos por moléstia grave** continuam isentos e são tratados de forma específica nas simulações do imposto mínimo.\n\n"
               "**Fonte:** RIC 1141/2025 – *Respostas do Ministério da Fazenda ao Congresso*.",
               "submenu_declaracao"),
    ],
 
    # --- PESSOA JURÍDICA ---
   "submenu_pf_pj_pj": [
        Option("MEI 💼", "Sou MEI, vou pagar mais imposto?",
               "O **DAS do MEI não muda**, pois o PL 1.087/2025 trata apenas do IRPF. "
               "O impacto só ocorreria se o MEI **distribuísse lucros acima de R$ 50 mil por mês**, o que é raro. "
               "Nesse caso, incidiria **retenção de 10% sobre dividendos**.\n\n"
               "**Fonte:** Tramitação do PL 1.087/2025 – Câmara dos Deputados.",
               "submenu_declaracao"),
 
        Option("Empresas (Lucro Real / Presumido) 🏢", "Minha empresa vai pagar mais ou menos imposto?",
               "A **tributação pelo IRPJ/CSLL não muda**. O impacto é no **sócio pessoa física**, que passa a ter retenção de **10% sobre dividendos** "
               "e pode ter de complementar pelo **imposto mínimo (IRPFM)**.\n\n"
               "Se a empresa comprovar **IRPJ/CSLL efetivo de 34% (ou 45% se financeira)**, não há complemento na pessoa física.\n\n"
               "**Fonte:** Projeto de Lei nº 1.087/2025 – Câmara dos Deputados.",
               "submenu_declaracao"),
    ],
 
 
    # --- ECONOMIA ---
    "menu_afeta_economia": [
        Option("Arrecadação 📊", "A arrecadação vai subir ou cair?",
               "As simulações indicam **pequeno ganho fiscal**, sem risco de queda relevante. "
               "A desoneração para assalariados (custo estimado em até **R$ 25 bilhões em 2026**) será compensada pela **tributação de dividendos (10%)** "
               "e pelo novo **imposto mínimo sobre altas rendas**.\n\n"
               "Em 2026, por exemplo, a arrecadação prevista com dividendos (**R$ 34,3 bilhões**) deve superar o custo da isenção.\n\n"
               "**Fonte:** Estudo da SPE – *Impactos do PL 1.087/2025*; Ministério da Fazenda (jun/2025).",
               "menu_afeta_economia"),
 
        Option("Sociedade 🌐", "A reforma reduz desigualdade?",
               "Sim. A reforma **aumenta a progressividade** do sistema. "
               "Trabalhadores que ganham até **R$ 5 mil mensais** ficarão isentos, enquanto cerca de **230 mil contribuintes com renda superior a R$ 1,2 milhão por ano** "
               "serão atingidos pelo **imposto mínimo (IRPFM)**.\n\n"
               "Isso representa **redistribuição tributária** — redução da carga na base e aumento no topo da pirâmide.\n\n"
               "**Fonte:** Estudo da SPE – *Impactos do PL 1.087/2025*.",
               "menu_afeta_economia"),
    ],
 
 
    # --- COMPARAÇÃO E PROJETO ---
    "menu_mudancas_anteriores": [
        Option("Comparação com o sistema antigo 🔄", "Qual a maior diferença em relação ao sistema antigo?",
               "No modelo atual (pré-reforma), **dividendos são totalmente isentos desde 1996** e não existe tributação adicional sobre altas rendas.\n\n"
               "A reforma cria dois mecanismos principais:\n\n"
               "1️⃣ **Desconto especial**, que amplia a isenção até **R\\$ 5 mil** (com redução gradual até **R\\$ 7 mil**);  \n"
               "2️⃣ **Tributação de dividendos na fonte (10%)** acima de **R\\$ 50 mil por mês**, combinada com o **imposto mínimo (até 10%)** "
               "para rendas totais superiores a **R\\$ 1,2 milhão por ano**.\n\n"
               "Essas mudanças introduzem uma **tributação efetiva no topo da pirâmide**, inexistente no sistema anterior.\n\n"
               "**Fonte:** Estudo da SPE – *Impactos do PL 1.087/2025*.",
               "menu_mudancas_anteriores"),
    ],
 
    "submenu_projeto": [
        Option("Arrecadação oficial (IBRE) 💹", "Onde vejo os números oficiais?",
               "As estimativas estão no **Estudo da SPE – Impactos do PL 1.087/2025** e no **Observatório de Política Fiscal (IBRE-FGV)**.  \n\n**Fonte:** SPE; IBRE/FGV.",
               "submenu_projeto"),
 
        Option("Impacto da reforma no governo 🏛️", "Como isso muda o papel do governo?",
               "A reforma **reforça a sustentabilidade fiscal** e **melhora a equidade tributária**, fortalecendo o papel do governo na **redistribuição de renda**.  \n\n**Fonte:** RIC 1141/2025 – *Secretaria do Tesouro Nacional e SPE*.",
               "submenu_projeto"),
 
        Option("Trechos do PL ⚖️", "Qual artigo trata dos dividendos?",
               "O **PL nº 1.087/2025** prevê **tributação de dividendos na fonte (10%)** quando o valor ultrapassar **R\\$ 50 mil/mês por fonte pagadora**.  \n\n**Fonte:** Projeto de Lei nº 1.087/2025 – Câmara dos Deputados.",
               "submenu_projeto"),
    ],
}
 
# ====================== LABELS ======================
crumb_labels = {
    "menu_principal": "Início",
    "menu_afeta_pessoal": "Como me afeta",
    "submenu_renda": "Renda",
    "submenu_declaracao": "Declaração",
    "submenu_pf_pj": "PF",
    "submenu_pf_pj_pj": "PJ",
    "menu_afeta_economia": "Economia",
    "menu_mudancas_anteriores": "Comparação",
    "submenu_projeto": "Projeto de Lei",
}
 
# ====================== HELPERS ======================
def go(stage: str):
    st.session_state.stage = stage
    if not st.session_state.trail or st.session_state.trail[-1] != stage:
        st.session_state.trail.append(stage)
 
def handle_option(opt: Option):
    st.session_state.messages.append({"role": "user", "content": opt.user_msg})
    with st.chat_message("assistant"):
        with st.spinner("Consultando informações..."):
            time.sleep(0.2)
        st.markdown(opt.bot_msg)
    st.session_state.messages.append({"role": "assistant", "content": opt.bot_msg})
    go(opt.next_stage or st.session_state.trail[-2])
 
def back():
    if len(st.session_state.trail) > 1:
        st.session_state.trail.pop()
        st.session_state.stage = st.session_state.trail[-1]
 
def reset():
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
    st.session_state.stage = "menu_principal"
    st.session_state.trail = ["menu_principal"]
 
# ====================== CALCULADORA ======================
def calculators_panel():
    st.subheader("🧮 Calculadora Única: Salário + Dividendos + Juros/JCP")
 
    MESES = 12
    LIMIAR_MENSAL_DIV = 50_000.0   # por fonte pagadora
    ALIQ_DIV_FONTE = 0.10          # 10% sobre excedente
    ALIQ_JUROS_FONTE = 0.15        # 15% exclusivo na fonte
 
    # ---- Tabela de taxas MÉDIAS de IRRF por FAIXA (ajuste aqui quando quiser) ----
    # Faixas por salário MENSAL (R$) -> taxa efetiva média aplicada sobre o salário anual
    EFFECTIVE_IRRF_RATES = [
        (0,        5_000,   0.00),   # isento até 5k
        (5_000,    6_000,   0.02),   # alívio
        (6_000,    7_000,   0.04),   # alívio
        (7_000,    9_000,   0.075),
        (9_000,    15_000,  0.15),
        (15_000,   30_000,  0.225),
        (30_000,   float("inf"), 0.275),
    ]
 
    def estimativa_irrf_salario(salario_anual: float) -> float:
        """Estimativa de IRRF anual com base na taxa média por faixa (mensal)."""
        salario_mensal = salario_anual / MESES if salario_anual else 0.0
        for lo, hi, rate in EFFECTIVE_IRRF_RATES:
            if lo <= salario_mensal < hi:
                return salario_anual * rate
        return 0.0
 
    def aliquota_minima_irpfm(renda_total_anual: float) -> float:
        # Fórmula (C): cresce de 0% a 10% entre 600k e 1,2M
        return max(0.0, min(10.0, renda_total_anual / 60_000.0 - 10.0)) / 100.0
 
    with st.form("calc_ir_unica", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            salario_anual   = st.number_input("Salário anual (R$)",   min_value=0.0, value=120_000.00, step=1_000.00, format="%.2f")
            juros_anual     = st.number_input("Juros/JCP anual (R$)", min_value=0.0, value=12_000.00,  step=500.00,   format="%.2f")
        with c2:
            dividendos_anual = st.number_input("Dividendos anuais (R$)", min_value=0.0, value=300_000.00, step=5_000.00, format="%.2f")
            n_fontes = st.number_input("Nº de fontes de dividendos", min_value=1, value=1, step=1)
        submitted = st.form_submit_button("Calcular")
 
    if submitted:
        # --- IRRF do salário (automático por faixa) ---
        irrf_salario_anual = estimativa_irrf_salario(salario_anual)
 
        # --- Dividendos: base tributável acima de 50k/mês por fonte ---
        n_fontes = max(1, int(n_fontes))
        div_por_fonte_ano = dividendos_anual / n_fontes
        div_por_fonte_mes = div_por_fonte_ano / MESES
        excedente_mensal = max(0.0, div_por_fonte_mes - LIMIAR_MENSAL_DIV)
        base_div_tributavel_total = excedente_mensal * MESES * n_fontes
        ir_fonte_dividendos = base_div_tributavel_total * ALIQ_DIV_FONTE
 
        # --- Juros/JCP: exclusivo na fonte 15% ---
        ir_fonte_juros = juros_anual * ALIQ_JUROS_FONTE
 
        # --- Renda total e imposto mínimo (IRPFM) ---
        renda_total = salario_anual + dividendos_anual + juros_anual
        a_min = aliquota_minima_irpfm(renda_total)
        ir_minimo_devido = renda_total * a_min
 
        # --- Impostos compensáveis e total na fonte (inclui IRRF do salário) ---
        impostos_compensaveis = ir_fonte_juros + ir_fonte_dividendos
        impostos_na_fonte_total = irrf_salario_anual + impostos_compensaveis
 
        # --- Complemento anual (top-up) ---
        adicional_ajuste = max(0.0, ir_minimo_devido - impostos_compensaveis)
        # Observação: mantido sem compensar IRRF de salário no IRPFM, conforme uso pedagógico.
 
        total_imposto_ano = impostos_na_fonte_total + adicional_ajuste
 
        # --- Resultados ---
        st.subheader("Resultados")
        st.metric("Renda Total (anual)", f"R$ {renda_total:,.2f}")
        st.metric("Alíquota Mínima (IRPFM)", f"{a_min*100:.2f}%")
        st.metric("IR Mínimo devido (regra IRPFM)", f"R$ {ir_minimo_devido:,.2f}")
 
        st.metric("IRPF — Salário (estimado por faixa)", f"R$ {irrf_salario_anual:,.2f}")
        st.metric("IR na fonte — Dividendos (10%)", f"R$ {ir_fonte_dividendos:,.2f}")
        st.markdown(
            f"<p style='color:gray; font-size:0.9rem;'>"
            f"<b>Dividendos por fonte:</b> R$ {div_por_fonte_mes:,.2f}/mês &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Excedente tributável:</b> R$ {excedente_mensal:,.2f}/mês"
            f"</p>",
            unsafe_allow_html=True
        )
 
        st.metric("IR na fonte — Juros/JCP (15%)", f"R$ {ir_fonte_juros:,.2f}")
        st.metric("Impostos na fonte (total)", f"R$ {impostos_na_fonte_total:,.2f}")
 
        st.metric("Complemento no ajuste (IRPFM)", f"R$ {adicional_ajuste:,.2f}")
        st.markdown("### **TOTAL DO IMPOSTO NO ANO**")
        st.metric("Total (fonte + IRPFM)", f"R$ {total_imposto_ano:,.2f}")
 
        if a_min == 0:
            st.info("🟢 Sua renda total anual está abaixo de **R$ 600 mil**. "
                    "Por isso **não há incidência de IRPFM** (complemento). "
                    "Os valores mostrados vêm do IR na fonte (salário, juros e dividendos).")
        st.caption("Obs.: IRPF do salário é **estimado** por faixa.")
 
# ====================== INTERFACE ======================
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🦁 Guia Rápido: Imposto de Renda 2025")
    st.write("Sou seu assistente virtual sobre o IR. Use os botões para navegar.")
with col2:
    st.button("🔄 Reset", use_container_width=True, on_click=reset)
 
# ====================== BREADCRUMBS ======================
with st.container():
    bc = " / ".join(crumb_labels.get(s, s) for s in st.session_state.trail)
    st.caption(f"📍 {bc}")
 
# ====================== HISTÓRICO ======================
# ====================== HISTÓRICO (ESTILO WHATSAPP) ======================
chat_container = st.container()
with chat_container:
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(
                f"""
                <div style='display:flex; justify-content:flex-end; margin:8px 0;'>
                    <div style='background-color:#DCF8C6; color:#000;
                                padding:10px 14px; border-radius:16px 16px 0 16px;
                                max-width:70%; word-wrap:break-word; font-size:15px;'>
                        {m["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='display:flex; justify-content:flex-start; margin:8px 0;'>
                    <div style='background-color:#F1F0F0; color:#000;
                                padding:10px 14px; border-radius:0 16px 16px 16px;
                                max-width:70%; word-wrap:break-word; font-size:15px;'>
                        {m["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
 
 
st.chat_input("Use os botões abaixo.", disabled=True)
 
# ====================== ROTEAMENTO ======================
with st.container():
    if st.session_state.stage in EXTRA_TEXTS:
        with st.expander("Resumo", expanded=True):
            st.markdown(EXTRA_TEXTS[st.session_state.stage])
 
    if st.session_state.stage == "calculadora_ir":
        calculators_panel()
 
    options = ROUTES.get(st.session_state.stage, [])
    if options:
        cols = st.columns(2) if len(options) > 1 else [st.container()]
        for i, opt in enumerate(options):
            with cols[i % len(cols)]:
                st.button(opt.label, use_container_width=True, on_click=handle_option, args=(opt,))
 
    st.divider()
    st.button("⬅️ Voltar", on_click=back, use_container_width=True, disabled=len(st.session_state.trail) <= 1)
 
# ====================== DISCLAIMER ======================
st.divider()
st.caption("Aviso: ferramenta educativa baseada no PL 1.087/2025 e estudos da SPE/FGV. Não substitui aconselhamento profissional.")