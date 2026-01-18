import streamlit as st
from ctransformers import AutoModelForCausalLM
import time

# --- 1. CONFIGURAÇÃO E CARREGAMENTO DO MODELO (NO FERRO) ---
st.set_page_config(page_title="Arandu Local Node", page_icon="💀")

@st.cache_resource
def carregar_cerebro():
    """
    Carrega o TinyLlama em formato GGUF (Quantizado).
    Roda em CPU tranquilamente.
    """
    print("Iniciando carregamento do modelo neural...")
    # Usando o TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
    # Ele vai baixar automaticamente na primeira vez.
    llm = AutoModelForCausalLM.from_pretrained(
        "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        model_file="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        model_type="llama",
        context_length=2048,
        gpu_layers=0 # Aumente se tiver placa de vídeo (ex: 10 ou 20)
    )
    return llm

try:
    llm = carregar_cerebro()
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    st.stop()

# --- 2. MEMÓRIA ESTÁTICA (O RAG FAVELA) ---
# TinyLlama é pequeno, então o contexto tem que ser curto e direto.
ESTOQUE_ARANDU = {
    "sistema": "Sistema Genesis-Ω Lite por R$ 97,00/mês. Link: /checkout/genesis",
    "mentoria": "Mentoria Tech-Estoicismo por R$ 1.500,00. Link: /checkout/mentoria",
    "consultoria": "Consultoria de Governança IA. Valor sob consulta. Link: /contato"
}

def recuperar_contexto(texto):
    texto = texto.lower()
    achados = []
    for k, v in ESTOQUE_ARANDU.items():
        if k in texto:
            achados.append(v)
    
    if not achados:
        return "Nenhum produto específico citado. Foque na dor do cliente."
    return " | ".join(achados)

# --- 3. ENGENHARIA DE PROMPT (ADAPTADO PARA TINYLLAMA) ---
# O TinyLlama usa formatacao específica: <|system|> ... <|user|> ... <|assistant|>
def formatar_prompt_tinyllama(historico, novo_input, contexto):
    
    system_prompt = f"""<|system|>
Você é o Vendedor Sênior da Arandu. Seja agressivo, curto e direto.
Venda APENAS o que está nos DADOS: [{contexto}].
Se não tiver produto, pergunte a dor do cliente.
Não escreva textos longos. Use no máximo 2 frases.
</s>
"""
    # Recria o histórico para o modelo não se perder
    chat_history = ""
    for msg in historico:
        role_tag = "<|user|>" if msg["role"] == "user" else "<|assistant|>"
        chat_history += f"{role_tag}\n{msg['content']}\n</s>\n"
    
    # Adiciona a nova pergunta
    full_prompt = f"{system_prompt}{chat_history}<|user|>\n{novo_input}\n</s>\n<|assistant|>\n"
    return full_prompt

# --- 4. INTERFACE STREAMLIT ---
st.title("💀 Arandu Local Ops")
st.caption("Rodando TinyLlama 1.1B - CPU Local")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem inicial agressiva
    st.session_state.messages.append({"role": "assistant", "content": "O sistema está online. Qual problema você quer resolver hoje?"})

# Renderiza histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do usuário
if prompt := st.chat_input("Comando..."):
    # Salva e mostra user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processamento
    with st.spinner("Processando neuralmente..."):
        contexto = recuperar_contexto(prompt)
        prompt_final = formatar_prompt_tinyllama(st.session_state.messages[:-1], prompt, contexto)
        
        # Geração (Inference)
        # Ajuste 'temperature' para criatividade (0.1 = robô, 0.8 = poeta)
        resposta_raw = llm(prompt_final, max_new_tokens=128, temperature=0.3, stop=["</s>", "<|user|>"])
        
        # Limpeza básica se o modelo se perder
        resposta_limpa = resposta_raw.replace("<|assistant|>", "").strip()

    # Mostra resposta da IA
    with st.chat_message("assistant"):
        st.markdown(resposta_limpa)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta_limpa})