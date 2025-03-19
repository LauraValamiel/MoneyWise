from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Conexão com o banco de dados
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._instance.connection = psycopg2.connect(
                    host='localhost',
                    database='MoneyWise',
                    user='postgres',
                    password='147258'
                )
                print("Conexão ao banco de dados estabelecida.")
            except Exception as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        return self.connection
    
# Geração de consultas no banco de dados
class QueryFactory:
    
    @staticmethod
    def select_query(table, columns='*', where_clause=None, order_by=None):
        query = f"SELECT {columns} FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        if order_by:
            query += f" ORDER BY {order_by}"
        return query

    @staticmethod
    def insert_query(table, columns, values):
        columns_str = ', '.join(columns)
        values_str = ', '.join([f"'{v}'" for v in values])
        return f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"

    @staticmethod
    def update_query(table, updates, where_clause=None):
        updates_str = ', '.join([f"{col} = '{val}'" for col, val in updates.items()])
        query = f"UPDATE {table} SET {updates_str}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return query

    @staticmethod
    def delete_query(table, where_clause):
        return f"DELETE FROM {table} WHERE {where_clause}"
    

# Outras funções para manipular o banco de dados
def consultar_db(query):
    try:
        con = DatabaseConnection().get_connection()
        cur = con.cursor()
        cur.execute(query)
        recset = cur.fetchall()
        cur.close()
        return recset
    except Exception as e:
        print(f"Erro na consulta: {e}")
        con.rollback()  # Rollback da transação em caso de erro
        cur.close()
        return []

def inserir_db(query):
    try:
        con = DatabaseConnection().get_connection()
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao inserir no banco de dados: {error}")
        con.rollback()  # Rollback da transação em caso de erro
        cur.close()
    finally:
        if con:
            cur.close()

# Inicializando o Flask
app = Flask(__name__)
CORS(app)

#Categorias:
dict_categorias: {'Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens'}


def receita(login):

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns="SUM(valor) AS valor",
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND cliente = '{login}' AND tipo = 'Receita'"
    )

    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()

    return df_bd

def despesa(login):

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns="SUM(valor) AS valor",
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND cliente = '{login}' AND tipo = 'Despesa'"
    )
    
    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
    return df_bd

def saldo_atual(receita, despesa):
    saldo_atual = receita(receita) - despesa(despesa)

    return saldo_atual

def resumo_mes_receita(ano, mes, login):
    query = QueryFactory.select_query(
        table='receita_despesa',
        columns="SUM(valor) AS valor",
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Receita'"
    )
    
    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
    return df_bd


def resumo_mes_despesa(ano, mes, login):
    query = QueryFactory.select_query(
        table='receita_despesa',
        columns="SUM(valor) AS valor",
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Despesa'"
    )

    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
    return df_bd


def despesas_por_categoria(categoria, login):

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    for categoria in dict_categorias:
        query = QueryFactory.select_query(
            table='receita_despesa',
            columns="SUM(valor) AS valor",
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND categoria = '{categoria}' AND cliente = '{login}' AND tipo = 'Despesa'"
        )
        resposta = consultar_db(query)

        df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
        return df_bd



def resumo_financeiro(ano, mes, login):
    query = QueryFactory.select_query(
        table='receita_despesa',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}'"
    )
    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['id', 'tipo', 'valor', 'descricao', 'categoria', 'data', 'cliente']).to_dict()
    
    return df_bd


def orcamento_mensal(ano, mes, login):
    query = QueryFactory.select_query(
        table='receita_despesa',
        columns="SUM(valor) AS valor",
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Despesa'"
    )
    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
    return df_bd


def relatorio_por_categoria(categoria, login):   
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    for categoria in dict_categorias:
        query = QueryFactory.select_query(
            table='receita_despesa',
            columns="SUM(valor) AS valor",
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND categoria = '{categoria}' AND cliente = '{login}' AND tipo = 'Despesa'"
        )
        resposta = consultar_db(query)

        df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
        return df_bd


def busca_cliente(cpf):
    query = QueryFactory.select_query(
        table='cliente',
        columns='cpf',
        where_clause=f"cpf = {cpf}"
    )
    resposta = consultar_db(query)

    df_bd = pd.DataFrame(resposta, columns=['cpf']).to_dict()
    
    return df_bd


def evolucao_despesas(login):
    
    meses = [(datetime.now() - relativedelta(months=i)).strftime('%Y-%m') for i in range(5)]

    despesas_meses = {}

    for mes in meses:
        ano, mes_numero = mes.split('-')

        query = QueryFactory.select_query(
            table='receita_despesa',
            columns="SUM(valor) AS valor",
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Despesa'"
        )
        resposta = consultar_db(query)

        df_bd = pd.DataFrame(resposta, columns=['valor']).to_dict()
    
        return df_bd


################ ROTAS ################

@app.route('/api/login', methods=['POST'])
def send_login():
    dados = request.json
    login = dados['login']
    senha = dados['senha']

    query = QueryFactory.select_query(
        table='cliente',
        columns='nome, cpf',
        where_clause=f"email = '{login}' AND senha = {senha}"
    )

    resp = consultar_db(query)
    if len(resp) > 0:
        df_bd = pd.DataFrame(resp, columns=['nome', 'cpf']).to_dict()
        return {'error': False, 'data': df_bd}
    else:
        return {'error': True, 'mensagem': 'Não foi possível encontrar o cliente'}

@app.route('/api/cadastro', methods=['POST'])
def create_cliente():
    dados = request.json
    nome = dados['nome']
    email = dados['email']
    cpf = dados['cpf'] 
    telefone = dados['telefone']
    senha = dados['senha']


    cliente = busca_cliente(cpf)

    if len(cliente) > 0:
        return jsonify({'error': True, 'mensagem': 'O cliente já existe'})
    else:
        query = QueryFactory.insert_query(
        table='cliente',
        columns=['nome', 'email', 'cpf', 'celular', 'senha'],
        values=[nome, email, cpf, telefone, senha]
    )
        inserir_db(query)

        return jsonify(dados)

@app.route('/api/editarCliente', methods=['POST'])
def edit_cliente(): #olhar de colocar o nome
    dados = request.json
    nome = dados['login']
    email = dados['email']
    cpf = dados['cpf']
    telefone = dados['telefone']

    updates = {}

    if(email):
        updates['email'] = email
    if(telefone):
        updates['telefone'] = telefone

    update_query = QueryFactory.update_query(
        table='cliente',
        updates=updates,
        where_clause=f"cpf = {cpf} AND nome = {nome}"
    )

    inserir_db(update_query)

    return jsonify(dados)

@app.route('/api/adicionarReceitaOuDespesa', methods=['POST'])
def adicionar_receita_despesa():
    dados = request.json
    tipo = dados['tipo']
    valor = dados['valor']
    descricao = dados['descricao']
    categoria = dados['categoria']
    data = dados['data']

    query = QueryFactory.insert_query(
        table='receita_despesa',
        columns=['tipo', 'valor', 'descricao', 'categoria', 'data'],
        values=[tipo, valor, descricao, categoria, data]
    )

    inserir_db(query)
    
    return jsonify(data)

@app.route('/api/receitas', methods=['GET'])
def receita_atual():

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year


    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='SUM(valor)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Receita'"
    )

    resultado = consultar_db(query)
    return jsonify(resultado)

@app.route('/api/despesas', methods=['GET'])
def despesa_atual():

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year


    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='SUM(valor)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Despesa'"
    )

    resultado = consultar_db(query)
    return jsonify(resultado)


@app.route('/api/saldoAtual', methods=['GET'])
def saldo_atual():
    saldo_atual = receita_atual() - despesa_atual()

    return jsonify(saldo_atual)

@app.route('/api/resumoDoMesReceita', methods=['GET'])
def resumo_do_mes_receita():
    dados = request.json
    login = dados['login']
    ano = dados['ano']
    mes = dados['mes']

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='SUM(valor)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Receita'"
    )

    resultado = consultar_db(query)

    return jsonify(resultado)

@app.route('/api/resumoDoMesDespesa', methods=['GET'])
def resumo_do_mes_despesa():
    dados = request.json
    login = dados['login']
    ano = dados['ano']
    mes = dados['mes']

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='SUM(valor)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Despesa'"
    )

    resultado = consultar_db(query)

    return jsonify(resultado)

@app.route('/api/despesasPorCategoria', methods=['GET'])
def despesas_por_categoria():
    dados = request.json
    login = dados['login']

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    resultados_categorias = {}

    for categoria in dict_categorias:
        query = QueryFactory.select_query(
            table='receita_despesa',
            columns='SUM(valor)',
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND categoria = '{categoria}' AND cliente = '{login}' AND tipo = 'Despesa'"
        )

        resultado = consultar_db(query)

        resultado_porcentagem = resultado / despesa_atual()

        resultados_categorias[categoria] = resultado_porcentagem

        df = pd.DataFrame(list(resultados_categorias.items()), columns=['Categoria', 'Valor'])

        df.set_index('Categoria').plot.pie(y ='Valor', autopct='%1.1f%%', startangle=90, legend=False)

        plt.title('Despesas por categoria')

        #exibir o grafico:
        #plt.ylabel('')
        #plt.show()


        return jsonify(resultado)
    
@app.route('/api/evolucaoDespesas', methods=['GET'])
def evolucao_despesas():

    meses = [(datetime.now() - relativedelta(months=i)).strftime('%Y-%m') for i in range(5)]

    despesas_meses = {}

    for mes in meses:
        ano, mes_numero = mes.split('-')#q isso? Pra que mes numero que não é usado?

        query = QueryFactory.select_query(
            table='receita_despesa',
            columns='SUM(valor)',
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes_numero}' AND cliente = '{login}' AND tipo = 'Despesa'"#login não existe aqui tem que receber ele
        )

        resultado = consultar_db(query)

        despesas_meses[mes] = resultado

    return despesas_meses



@app.route('/api/resumoFinanceiro', methods=['GET'])
def resumo_financeiro():
    dados = request.json
    login = dados['login']
    ano = dados['ano']
    mes = dados['mes']

    query = QueryFactory.select_query(
        table='receita_despesa',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}'"
    )

    resultado = consultar_db(query)
    #reatar com dataframe os dados
    return jsonify(resultado)


@app.route('/api/orcamentoMensal', methods=['GET'])
def orcamento_mensal():
    dados = request.json
    login = dados['login']
    ano = dados['ano']
    mes = dados['mes']

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='SUM(valor)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{login}' AND tipo = 'Despesa'"
    )

    resultado = consultar_db(query)

    return jsonify(resultado)

@app.route('/api/relatorio', methods=['GET'])
def relatorio_categorias():
    dados = request.json
    login = dados['login']

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    resultados_categorias = {}

    for categoria in dict_categorias:
        query = QueryFactory.select_query(
            table='receita_despesa',
            columns='SUM(valor)',
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND categoria = '{categoria}' AND cliente = '{login}' AND tipo = 'Despesa'"
        )

        resultado = consultar_db(query)

        resultado_porcentagem = resultado / despesa_atual()

        resultados_categorias[categoria] = resultado_porcentagem

        return jsonify(resultado)




# Rodando a aplicação
if __name__ == '__main__':
    app.run(debug=True)

    