import streamlit as st
from rag_chain import get_rag_chain

st.set_page_config(page_title="Copiloto B2B", page_icon="🍔")
st.title("🤖 Copiloto de Suporte (RAG Knowledge Base)")
st.markdown("Pergunte qualquer coisa sobre as regras operacionais da plataforma.")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura o input do usuário
if user_input := st.chat_input("Ex: Como funciona o repasse?"):
    # Salva e mostra a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gera a resposta via LangChain
    with st.chat_message("assistant"):
        with st.spinner("Buscando nos manuais internos..."):
            chain = get_rag_chain()
            response = chain.invoke(user_input)
            st.markdown(response)
    
    # Salva a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": response})