import streamlit as st
import random
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Meu Primeiro Chatbot", page_icon="🤖")

st.title("🤖 Chatbot Assistente")
st.write("Este é um chatbot simples que usa regras para responder.")

# --- GERENCIAMENTO DE ESTADO (MEMÓRIA DO CHAT) ---
# Inicializa o histórico da conversa na sessão, se ainda não existir.
# st.session_state é um dicionário que persiste entre as re-execuções do script.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Como posso te ajudar hoje?"}
    ]

# --- EXIBIÇÃO DO HISTÓRICO DA CONVERSA ---
# Itera sobre todas as mensagens salvas no estado da sessão e as exibe.
for message in st.session_state.messages:
    # st.chat_message cria um container de mensagem com um avatar apropriado.
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ENTRADA DO USUÁRIO ---
# st.chat_input cria um campo de entrada de texto fixo na parte inferior da tela.
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # Adiciona a mensagem do usuário ao histórico e a exibe na tela.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- LÓGICA DE RESPOSTA DO BOT ---
    # Aqui entra a "inteligência" do nosso chatbot.
    # Por enquanto, será uma lógica baseada em regras simples (if/elif/else).
    
    # Adiciona a mensagem de resposta do assistente ao histórico e a exibe.
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Converte o prompt para minúsculas para facilitar a correspondência de regras.
        prompt_lower = prompt.lower()

        # Regras de resposta
        if "olá" in prompt_lower or "oi" in prompt_lower:
            response = "Olá! Tudo bem? Em que posso ser útil?"
        elif "qual o seu nome" in prompt_lower:
            response = "Eu sou um chatbot assistente, criado para te ajudar!"
        elif "como você está" in prompt_lower:
            response = "Estou funcionando perfeitamente, obrigado por perguntar!"
        elif "adeus" in prompt_lower or "tchau" in prompt_lower:
            response = "Até logo! Se precisar de algo, estarei por aqui."
        else:
            responses = [
                "Desculpe, não entendi. Pode reformular a pergunta?",
                "Interessante... Me diga mais sobre isso.",
                "Não tenho certeza sobre como responder a isso. Podemos falar sobre outra coisa?"
            ]
            response = random.choice(responses)

        # Simula um efeito de "digitação" para uma melhor experiência do usuário.
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Atualiza o conteúdo do placeholder a cada palavra.
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
    # Adiciona a resposta completa do bot ao histórico da sessão.
    st.session_state.messages.append({"role": "assistant", "content": full_response})