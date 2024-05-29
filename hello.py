from pymongo import MongoClient
from bson import ObjectId  # Importar a classe ObjectId do módulo bson
import pandas as pd
from datetime import datetime 
from pymongo import MongoClient # Importe datetime para trabalhar com datas
from flask import Flask, render_template, request, redirect, url_for
# Conectar ao servidor MongoDB

client = MongoClient("mongodb://localhost:27017/")  # Substitua pelo seu URI

# Selecionar a database
db = client["os3miausbonitos"]

# Selecionar a coleção (collection)
collection = db["despesas_familia"]

# Função para adicionar uma despesa ao MongoDB
def adicionar_despesa(descricao, valor):
    # Obter a data atual
    data_atual = datetime.now()

    # Criar documento apenas com a descrição, valor e data
    documento = {"Descrição": descricao, "Valor": valor, "Data": data_atual}
    collection.insert_one(documento)
    print("Despesa adicionada com sucesso!")

# Função para remover uma despesa do MongoDB
def remover_despesa(descricao):
    despesa = collection.find_one({"Descrição": descricao})
    if despesa:
        collection.delete_one({"Descrição": descricao})
        print("Despesa removida com sucesso!")
    else:
        print("Esta despesa não existe.")

# Função para calcular o saldo restante
def calcular_saldo():
    total_despesas = sum(despesa['Valor'] for despesa in collection.find())
    saldo_restante = orcamento_inicial - total_despesas
    return saldo_restante

# Definindo o orçamento inicial da família
orcamento_inicial = 5000  # Valor em reais

# Exibindo a tabela de despesas
print("Tabela de Despesas:")
df_despesas = pd.DataFrame(collection.find())
print(df_despesas)

# Calculando e exibindo o saldo restante
saldo_restante = calcular_saldo()
print(f"\nSaldo Restante: R${saldo_restante:.2f}")

# Loop para adicionar ou remover despesas
while True:
    opcao = input("Deseja adicionar ou remover uma despesa? (adicionar/remover/sair): ")
    if opcao.lower() == 'sair':
        break
    elif opcao.lower() == 'adicionar':
        descricao = input("Digite a descrição da despesa: ")
        valor = float(input("Digite o valor da despesa: "))
        adicionar_despesa(descricao, valor)
    elif opcao.lower() == 'remover':
        descricao = input("Digite a descrição da despesa que deseja remover: ")
        remover_despesa(descricao)
    else:
        print("Opção inválida. Tente novamente.")

# Exibindo a tabela de despesas atualizada
print("\nTabela de Despesas Atualizada:")
df_despesas = pd.DataFrame(collection.find())
print(df_despesas)

# Calculando e exibindo o saldo restante
saldo_restante = calcular_saldo()
print(f"\nSaldo Restante: R${saldo_restante:.2f}")

# Gerar o arquivo HTML com a tabela de despesas atualizada
html_file_path = "tabela_despesas_atualizada.html"
df_despesas.to_html(html_file_path, index=False)

print(f"Arquivo HTML gerado: {html_file_path}")

# Fechando a conexão com o MongoDB
client.close()