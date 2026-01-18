import streamlit as st
from openai import OpenAI
import time

# --- CONFIGURAÇÃO INICIAL (A BASE) ---
st.set_page_config(page_title="Arandu Closer", page_icon="⚡")

# Verifica se a API Key está nos segredos do Streamlit
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Cadê a chave, chefia? Configure o OPENAI_API_KEY nos secrets do Streamlit.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 2. A MEMÓRIA (RAG "CAMELÔ" / VETOR FAVELA) ---
# Em vez de um banco vetorial complexo e caro, usamos um dicionário hash rápido.
# Isso simula seu "Estoque Real".
ESTOQUE_ARANDU = {
    "tenis": {
        "produto": "Nike Dunk Low Retro - Vermelho/Branco",
        "preco": "R$ 899,90",
        "estoque": "Disponível nos tamanhos 39, 40 e 42",
        "link": "https://seusite.com/checkout/dunk-red"
    },
    "curso": {
        "produto": "Mentoria Tech-Estoicismo IA",
        "preco": "R$ 1.500,00",
        "estoque": "Apenas 3 vagas restantes",
        "link": "https://seusite.com/checkout/mentoria"
    },
    "software": {
        "produto": "SaaS Genesis-Ω Lite",
        "preco": "R$ 97,00/mês",
        "estoque": "Acesso imediato",
        "link": "https://seusite.com/checkout/genesis"
    }
}

def recuperar_contexto(mensagem_usuario):
    """
    Função de busca simples. Se o usuário falar a palavra-chave, 
    a IA 'lembra' do estoque e preço real. Sem alucinação.
    """
    mensagem_usuario = mensagem_usuario.lower()
    contexto = []
    
    for chave, dados in ESTOQUE_ARANDU.items():
        if chave in mensagem_usuario:
            contexto.append(f"DADOS REAIS (Use isso, não invente): Produto: {dados['produto']}, Preço: {dados['preco']}, Estoque: {dados['estoque']}, Link de Pagamento: {dados['link']}")
            
    if not contexto:
        return "Nenhum produto específico identificado no banco de dados. Foque em diagnosticar a dor do cliente."
    
    return "\n".join(contexto)

# --- 1. O CÉREBRO (PROMPT DE SISTEMA AGRESSIVO) ---
def gerar_prompt_sistema(contexto_rag):
    return f"""
    VOCÊ É: O Closer da Agência Arandu. Um especialista sênior em vendas.
    
    SUA MISSÃO: 
    1. Aplicar metodologia SPIN Selling (Situação, Problema, Implicação, Necessidade).
    2. Diagnosticar a dor do usuário rapidamente.
    3. Oferecer a solução baseada EXCLUSIVAMENTE nos dados abaixo.
    4. NÃO SEJA "GENTIL DEMAIS". Seja visionário, direto e focado em conversão.
    
    DADOS REAIS DO ESTOQUE (MEMÓRIA):
    {contexto_rag}
    
    REGRAS DE OURO:
    - Se tiver o link de pagamento nos dados, envie-o assim que o cliente mostrar interesse.
    - Sempre termine com uma PERGUNTA DE FECHAMENTO (Ex: "O que te impede de resolver isso agora?").
    - Se o cliente achar caro, use a técnica: "Caro comparado a continuar com esse problema?".
    """

# --- 3. A INTEGRAÇÃO (INTERFACE CHAT) ---

st.title("⚡ Arandu Sales Agent")
st.caption("Fale sua dor, eu tenho a cura.")

# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = []
    # A MICRO-AÇÃO PROATIVA (O "Pop-up" inicial)
    msg_inicial = "Vi que você está buscando evoluir. Qual o maior gargalo técnico ou financeiro que te impede de avançar hoje?"
    st.session_state.messages.append({"role": "assistant", "content": msg_inicial})

# Mostra histórico na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Captura input do usuário
if prompt := st.chat_input("Digita a visão..."):
    # 1. Mostra msg do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Processa a lógica (RAG + Prompt)
    contexto = recuperar_contexto(prompt)
    system_prompt = gerar_prompt_sistema(contexto)

    # 3. Chama a IA (O Vendedor)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        stream = client.chat.completions.create(
            model="gpt-4o-mini", # Modelo rápido e barato (ideal para escala)
            messages=[
                {"role": "system", "content": system_prompt},
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})