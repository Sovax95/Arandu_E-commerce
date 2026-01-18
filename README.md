# **Arandu Closer - Conversational Commerce com IA**

## **Descrição do Projeto**

O **Arandu Closer** é uma solução avançada de **vendas conversacionais** que utiliza **inteligência artificial (IA)** para **maximizar conversões de vendas** de forma rápida e eficiente. Utilizando o modelo **TinyLlama 1.1B** em **modo local**, e a metodologia de **SPIN Selling**, o sistema diagnostica a dor do cliente e oferece uma solução direta, com foco em **fechamento imediato de vendas**.

Este projeto foi desenvolvido para melhorar a experiência de **venda online**, aproveitando IA para fornecer respostas rápidas, personalizadas e com links de pagamento integrados, tudo em tempo real.

---

## **Funcionalidades**

- **Vendas Conversacionais**: A IA atua como um **"closer digital"**, conduzindo o usuário pela jornada de compra e sempre focando no fechamento rápido da venda.
- **Integração de Dados Reais (RAG)**: O sistema integra uma **base de dados simples** de produtos reais, garantindo respostas precisas e evitando **alucinações** típicas de modelos de IA.
- **Modelo de IA Local**: Usando o modelo **TinyLlama 1.1B**, rodando localmente em **CPU**, para reduzir custos e aumentar a **eficiência**.
- **Fechamento de Vendas em Tempo Real**: A IA é configurada para **diagnosticar rapidamente** o problema do cliente e **oferecer soluções imediatas** com links de pagamento.
- **Interface de Conversação com Streamlit**: A interface é construída usando o **Streamlit**, proporcionando uma experiência de chat interativa e de fácil uso.

---

## **Tecnologias Utilizadas**

- **OpenAI GPT** (para versão de IA baseada em nuvem)
- **TinyLlama 1.1B** (modelo local, rodando em CPU)
- **Streamlit** (para criação da interface de usuário)
- **ctransformers** (para carregar e executar o modelo TinyLlama)
- **Python** (para lógica e integração do sistema)

---

## **Como Funciona**

1. **Inicialização**: O sistema começa com uma **mensagem agressiva de vendas** para entender a dor do cliente.
2. **Consultando Estoque**: Quando o cliente faz uma pergunta, a IA consulta uma **base de dados de produtos reais** para fornecer respostas rápidas e precisas.
3. **Diagnóstico e Fechamento**: A IA diagnostica a dor do cliente e oferece a **solução perfeita** com links de pagamento prontos.
4. **Integração Local**: O modelo **TinyLlama** roda localmente em **CPU**, garantindo que o processo de vendas seja ágil e econômico.

---

## **Estrutura do Código**

- **`app_local.py`**: O arquivo principal que configura a aplicação e executa o modelo de IA.
- **`ESTOQUE_ARANDU`**: Um dicionário simples que simula um banco de dados de produtos.
- **`recuperar_contexto()`**: Função que busca palavras-chave do usuário e recupera os dados reais do estoque.
- **`formatar_prompt_tinyllama()`**: Função que formata o histórico da conversa para o modelo de IA TinyLlama.
- **`carregar_cerebro()`**: Função que carrega o modelo de IA **TinyLlama 1.1B** localmente.
- **Streamlit Interface**: Exibe a interface do chat onde o usuário pode interagir com o **Arandu Closer**.

---

## **Instruções de Execução**

### 1. **Configuração do Ambiente**

Primeiro, instale as dependências necessárias:

```bash
pip install -r requirements.txt
pip install streamlit ctransformers
streamlit run app_local.py

---

Esse **README.md** fornece uma descrição completa e detalhada do seu projeto, incluindo **tecnologias** utilizadas, **fluxo do sistema**, **instruções de execução** e **como contribuir**. Está pronto para ser usado em um repositório **GitHub** e ajudar a **documentar o desenvolvimento** e a **expansão futura** do **Arandu Closer**.
