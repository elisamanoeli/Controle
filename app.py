import streamlit as st
import pandas as pd
import calendar

# Tradução dos meses para português
MES_NOMES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

class Associado:
    def __init__(self, numero, nome, data_entrada):
        self.numero = numero
        self.nome = nome
        self.data_entrada = data_entrada
        self.pagamentos = []

    def adicionar_pagamento(self, valor, mes_pagamento, ano_pagamento, status):
        pagamento = {"valor": valor, "mes": mes_pagamento, "ano": int(ano_pagamento), "status": status}
        self.pagamentos.append(pagamento)

    def verificar_status(self, mes_atual, ano_atual):
        pagamentos_atrasados = [p for p in self.pagamentos if p['status'] == 'atrasado' and (p['ano'] < ano_atual or (p['ano'] == ano_atual and p['mes'] < mes_atual))]
        pagamentos_em_negociacao = [p for p in self.pagamentos if p['status'] == 'negociação']

        if pagamentos_atrasados:
            return 'inadimplente'
        elif pagamentos_em_negociacao:
            return 'em negociação'
        else:
            return 'adimplente'

class SistemaAssociados:
    def __init__(self):
        self.associados = []

    def cadastrar_associado(self, numero, nome, data_entrada):
        associado = Associado(numero, nome, data_entrada)
        self.associados.append(associado)
        return associado

    def buscar_associado(self, numero_associado):
        for associado in self.associados:
            if associado.numero == numero_associado:
                return associado
        return None

    def adicionar_pagamento_associado(self, numero_associado, nome_associado, valor, mes_pagamento, ano_pagamento, status):
        associado = self.buscar_associado(numero_associado)
        if associado:
            associado.adicionar_pagamento(valor, mes_pagamento, ano_pagamento, status)
        else:
            associado = self.cadastrar_associado(numero_associado, nome_associado, "2023-01-01")
            associado.adicionar_pagamento(valor, mes_pagamento, ano_pagamento, status)

# Inicializar sistema
sistema = SistemaAssociados()

st.title("Cadastro de Associados")

# Campo para número do associado
numero_associado = st.number_input("Número do Associado", min_value=1, step=1)

# Nome do Associado
nome = st.text_input("Nome do Associado")

# Dropdown de seleção do mês com o nome dos meses em português
mes_nome = st.selectbox("Mês", MES_NOMES_PT)  # Lista dos meses em português
mes = MES_NOMES_PT.index(mes_nome) + 1  # Converter o nome do mês para o número correspondente

# Ano do Pagamento (usando text_input para evitar formatação decimal)
ano = int(st.text_input("Ano", value="2023"))  # Garantir que o valor seja um número inteiro

# Situação Financeira
situacao = st.selectbox("Situação Financeira", ["pago", "atrasado", "negociação"])

# Valor do Pagamento
valor = st.number_input("Valor do Pagamento", min_value=0.0, step=0.01)

# Botão para adicionar pagamento
if st.button("Adicionar Pagamento"):
    sistema.adicionar_pagamento_associado(numero_associado, nome, valor, mes, ano, situacao)

# Exibir tabela de pagamentos
data = []
for associado in sistema.associados:
    for pagamento in associado.pagamentos:
        valor_formatado = f"R$ {pagamento['valor']:,.2f}".replace('.', ',')  # Formatar o valor em R$ com vírgula
        data.append([associado.numero, associado.nome, MES_NOMES_PT[pagamento['mes'] - 1], pagamento['ano'], pagamento['status'], valor_formatado])

# Criar DataFrame para exibir a tabela, incluindo a nova coluna "Valor do Pagamento"
df = pd.DataFrame(data, columns=["Número do Associado", "            Nome do Associado            ", "Mês", "Ano", "Situação", "Valor do Pagamento"])

# Exibir a tabela
st.write(df)
