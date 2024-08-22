import streamlit as st
import pandas as pd

# Tradução dos meses para português
MES_NOMES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# Estilos aplicados diretamente aos campos e ao fundo da página
st.markdown(
    """
    <style>
    /* Cor de fundo da página */
    .stApp {
        background-color: #f0f2f6;
    }

    /* Cor e estilo dos campos de entrada (input, select, textarea) */
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF;
        border: 2px solid #0B0C45;
        border-radius: 10px;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border: 2px solid #0B0C45;
        border-radius: 10px;
    }

    div[data-baseweb="textarea"] > div {
        background-color: #FFFFFF;
        border: 2px solid #0B0C45;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Exibir a imagem do logo no canto esquerdo com tamanho médio
st.image("logo.png", width=200)

# Exibir o título abaixo do logo
st.title("Cadastro de Associados")

# Inicializar o session_state para a lista de associados
if 'associados' not in st.session_state:
    st.session_state['associados'] = []

# Inicializar o session_state para os campos de entrada, se ainda não existirem
if 'numero_associado' not in st.session_state:
    st.session_state['numero_associado'] = 1

# Campo para o número do associado (primeiro campo)
numero_associado = st.number_input("Número do Associado", min_value=1, step=1, value=st.session_state['numero_associado'])

# Campos para cadastro de associados
nome = st.text_input("Nome do Associado")
mes_nome = st.selectbox("Mês", MES_NOMES_PT)
ano = st.text_input("Ano", value="2024")
situacao = st.selectbox("Situação Financeira", ["pago", "atrasado", "negociação"])
valor = st.number_input("Valor do Pagamento", min_value=0.0, step=0.01)

# Botão para cadastrar o associado
if st.button("Cadastrar"):
    associado = {
        "numero": numero_associado,
        "nome": nome,
        "mes_pagamento": mes_nome,
        "ano_pagamento": ano,
        "situacao": situacao,
        "valor": valor,
    }

    # Adiciona o associado à lista no session_state
    st.session_state['associados'].append(associado)

    # Exibe a mensagem de sucesso
    st.success(f"Associado {nome} cadastrado com sucesso!")

    # Incrementar o número do associado automaticamente
    st.session_state['numero_associado'] += 1

# Exibir tabela de associados cadastrados
data = []
for associado in st.session_state['associados']:
    valor_formatado = f"R$ {associado['valor']:,.2f}".replace('.', ',')
    data.append([associado['numero'], associado['nome'], associado['mes_pagamento'], associado['ano_pagamento'], associado['situacao'], valor_formatado])

# Criar DataFrame para exibir a tabela
df = pd.DataFrame(data, columns=["Número do Associado", "Nome do Associado", "Mês", "Ano", "Situação", "Valor do Pagamento"])

# Exibir a tabela
st.write(df)
