from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from datetime import datetime
import logging
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Chave secreta para mensagens flash

# Configurar logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Conectar ao servidor MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Substitua pelo seu URI

# Selecionar a database
db = client["os3miausbonitos"]

# Selecionar a coleção (collection)
collection = db["despesas_familia"]

# Definindo o orçamento inicial da família
orcamento_inicial = 5000  # Valor em reais

# Função para adicionar uma despesa ao MongoDB
def adicionar_despesa(descricao, valor):
    try:
        # Obter a data atual
        data_atual = datetime.now()

        # Criar documento com a descrição, valor e data
        documento = {"Descrição": descricao, "Valor": valor, "Data": data_atual}
        collection.insert_one(documento)
        logging.info("Despesa adicionada com sucesso: %s, R$ %.2f", descricao, valor)
        flash("Despesa adicionada com sucesso!", "success")
    except Exception as e:
        logging.error("Erro ao adicionar despesa: %s", e)
        flash("Erro ao adicionar despesa!", "danger")

# Função para remover uma despesa do MongoDB
def remover_despesa(despesa_id):
    try:
        despesa = collection.find_one({"_id": ObjectId(despesa_id)})
        if despesa:
            collection.delete_one({"_id": ObjectId(despesa_id)})
            logging.info("Despesa removida com sucesso: %s", despesa['Descrição'])
            flash("Despesa removida com sucesso!", "success")
        else:
            logging.warning("Tentativa de remover despesa inexistente.")
            flash("Esta despesa não existe.", "warning")
    except Exception as e:
        logging.error("Erro ao remover despesa: %s", e)
        flash("Erro ao remover despesa!", "danger")

# Função para editar uma despesa no MongoDB
def editar_despesa(despesa_id, nova_descricao, novo_valor):
    try:
        collection.update_one(
            {"_id": ObjectId(despesa_id)},
            {"$set": {"Descrição": nova_descricao, "Valor": novo_valor, "Data": datetime.now()}}
        )
        logging.info("Despesa editada com sucesso: %s, R$ %.2f", nova_descricao, novo_valor)
        flash("Despesa editada com sucesso!", "success")
    except Exception as e:
        logging.error("Erro ao editar despesa: %s", e)
        flash("Erro ao editar despesa!", "danger")

# Função para calcular o saldo restante
def calcular_saldo():
    try:
        total_despesas = sum(despesa['Valor'] for despesa in collection.find())
        saldo_restante = orcamento_inicial - total_despesas
        return saldo_restante
    except Exception as e:
        logging.error("Erro ao calcular saldo: %s", e)
        flash("Erro ao calcular saldo!", "danger")
        return orcamento_inicial

# Função para exportar despesas para CSV
def exportar_despesas():
    try:
        despesas = list(collection.find())
        df_despesas = pd.DataFrame(despesas)
        df_despesas.to_csv('despesas.csv', index=False)
        logging.info("Despesas exportadas com sucesso para despesas.csv")
        return 'despesas.csv'
    except Exception as e:
        logging.error("Erro ao exportar despesas: %s", e)
        flash("Erro ao exportar despesas!", "danger")
        return None

# Rota para a página inicial (página de login)
@app.route('/')
def login_page():
    return render_template('index.html')

# Rota para fazer login
@app.route('/login', methods=['POST'])
def login():
    # Lógica de verificação de login aqui
    # Neste exemplo, vamos apenas redirecionar para a página de tabela após o login bem-sucedido
    return redirect(url_for('tabela'))

# Rota para a página de tabela
@app.route('/tabela')
def tabela():
    try:
        # Obter os dados da coleção MongoDB
        df_despesas = pd.DataFrame(collection.find())
        saldo_restante = calcular_saldo()
        return render_template('tabela.html', df_despesas=df_despesas.to_dict(orient='records'), saldo_restante=saldo_restante)
    except Exception as e:
        logging.error("Erro ao carregar página de tabela: %s", e)
        flash("Erro ao carregar página de tabela!", "danger")
        return render_template('tabela.html', df_despesas=[], saldo_restante=orcamento_inicial)

# Rota para adicionar uma despesa
@app.route('/adicionar', methods=['POST'])
def adicionar():
    descricao = request.form['descricao']
    try:
        valor = float(request.form['valor'])
        adicionar_despesa(descricao, valor)
    except ValueError:
        logging.warning("Valor inválido para despesa: %s", request.form['valor'])
        flash("Valor inválido!", "danger")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
