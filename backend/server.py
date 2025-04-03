import os
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
    con = None
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
#CORS(app, resources={r"/api/*": {"origins": "*"}})


#Categorias:
#dict_categorias: {'Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens'}


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
    print(f"cpf recebido: {cpf}")
    query = QueryFactory.select_query(
        table='cliente',
        columns='cpf',
        where_clause=f"cpf = '{cpf}'"
    )
    print(f"Consulta sql: {query}")
    resposta = consultar_db(query)

    print(f"resposta do banco: {resposta}")

    #df_bd = pd.DataFrame(resposta, columns=['cpf']).to_dict()
    
    #return df_bd

    if resposta:
        return resposta[0][0]
    return None


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
        where_clause=f"email = '{login}' AND senha = '{senha}'"
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

    print(f"dados: {dados}")

    if not dados:
        return {'error': True, 'mensagem': 'Requisição malformada'}, 400
    
    nome = dados['nome']
    email = dados['email']
    cpf = dados['cpf'] 
    telefone = dados['telefone']
    senha = dados['senha']


    cliente = busca_cliente(cpf)

    if cliente is None:
        cliente = []

    print(f"cliente: '{cliente}'")

    print(f"lencliente: {len(cliente)}")

    #if len(cliente) > 1:
    #    return jsonify({'error': True, 'mensagem': 'O cliente já existe'})
    if cliente:
        return {'error': True, 'mensagem': 'O cliente já existe'}, 400
    elif not nome or not email or not cpf or not telefone or not senha:
        return {'error': True, 'mensagem': 'Dados incompletos para o cadastro'}
    else:
        query = QueryFactory.insert_query(
        table='cliente',
        columns=['nome', 'email', 'CPF', 'telefone', 'senha'],
        values=[nome, email, cpf, telefone, senha]
    )
        inserir_db(query)

        return jsonify({'success': True, 'mensagem': 'Cliente cadastrado com sucesso', 'cliente': dados}), 201


@app.route('/api/editarCliente', methods=['POST'])
def edit_cliente(): #olhar de colocar o nome
    dados = request.json
    nome = dados['nome']
    email = dados['email']
    cpf = dados['cpf']
    telefone = dados['telefone']

    updates = {}

    if(nome):
        updates['nome'] = nome
    if(email):
        updates['email'] = email
    if(telefone):
        updates['telefone'] = telefone

    update_query = QueryFactory.update_query(
        table='cliente',
        updates=updates,
        where_clause=f"cpf = '{cpf}' AND nome = '{nome}'"
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

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    # Consulta o total de receitas
    query_receita = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',  # Se for NULL, retorna 0
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Receita'"
    )
    receita_resultado = consultar_db(query_receita)
    receita_total = receita_resultado[0][0] if receita_resultado else 0  # Pega o valor da tupla

    
    # Consulta o total de despesas
    query_despesa = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',  # Se for NULL, retorna 0
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Despesa'"
    )
    despesa_resultado = consultar_db(query_despesa)
    despesa_total = despesa_resultado[0][0] if despesa_resultado else 0  # Pega o valor da tupla

    saldo_atual = receita_total - despesa_total  # Calcula o saldo

    return jsonify({"saldo": saldo_atual})

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

IMAGE_DIR = 'static/imagens'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/api/despesasPorCategoria', methods=['GET'])
def despesas_por_categoria():
    login = request.args.get('login')  # Pegando o login via query string

    categorias = ['Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens'] 

    if not login:
        return jsonify({"erro": "Login não fornecido"}), 400

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    resultados_categorias = {}

    query_despesa = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',  # Se for NULL, retorna 0
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Despesa'"
    )
    despesa_resultado = consultar_db(query_despesa)
    despesa_total = despesa_resultado[0][0] if despesa_resultado else 0

    for categoria in categorias:
        query = QueryFactory.select_query(
            table='receita_despesa',
            columns='SUM(valor)',
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND categoria = '{categoria}' AND cliente = '{login}' AND tipo = 'Despesa'"
        )

        resultado = consultar_db(query)

        if resultado is None:  # Verifica se a consulta retornou algum valor
            resultado = 0

        resultado_porcentagem = resultado / despesa_total

        resultados_categorias[categoria] = resultado_porcentagem

    df = pd.DataFrame(list(resultados_categorias.items()), columns=['Categoria', 'Valor'])

    df.set_index('Categoria').plot.pie(y ='Valor', autopct='%1.1f%%', startangle=90, legend=False)

    plt.title('Despesas por categoria')

    image_path = os.path.join(IMAGE_DIR, 'despesas_por_categoria.png')
    plt.savefig(image_path)

    # Fechar o gráfico
    plt.close()

    # Retornar a URL da imagem gerada
    image_url = f'http://localhost:5000/images/despesas_por_categoria.png'

    return jsonify({
        "resultados": resultados_categorias,
        "grafico_url": image_url
    })
        
        #exibir o grafico:
        #plt.ylabel('')
        #plt.show()

        #valor = float(resultado[0]) if resultado and resultado[0] is not None else 0  # Tratando possíveis valores nulos

        #resultados_categorias.append({"categoria": categoria, "valor": valor})

    #return jsonify(resultados_categorias)


    
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

    categorias = ['Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens'] 


    resultados_categorias = {}

    for categoria in categorias:
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

    