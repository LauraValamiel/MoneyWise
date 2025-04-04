import locale
import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import datetime
import requests
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import make_response
from decimal import Decimal
from flask import send_from_directory


# Conexão com o banco de dados
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._instance.connection = psycopg2.connect(
                    host='localhost',
                    database='MoneyWise',
                    user='postgres',
                    password='147258'
                )
                print("Conexão ao banco de dados estabelecida.")
            except Exception as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                cls._instance.connection = None
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
        if con:
             con.rollback() 
        if cur:
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
CORS(app, origins=["http://localhost:5173"])
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
#CORS(app)
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



@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

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
    print("Dados recebidos:", dados)
    #nome = dados.get('nome', '')
    #email = dados.get('email', '')
    cpf = dados.get('cpf', '')
    #telefone = dados.get('telefone', '')

    updates = {}

    if 'nome' in dados:
        updates['nome'] = dados['nome']
    if 'email' in dados:
        updates['email'] = dados['email']
    if 'telefone' in dados:
        updates['telefone'] = dados['n_celular']

    if not updates:
        return jsonify({"error": True, "message": "Nenhum campo para atualizar"}), 400


    update_query = QueryFactory.update_query(
        table='cliente',
        updates=updates,
        where_clause=f"cpf = '{cpf}'"
    )

    inserir_db(update_query)

    select_query = QueryFactory.select_query(
        table='cliente',
        columns='cpf, nome, email, telefone',
        where_clause=f"cpf = '{cpf}'"
    )
    
    resultado = consultar_db(select_query)

    if not resultado:
        return jsonify({"error": True, "message": "Erro ao recuperar dados atualizados"}), 500

    cliente_atualizado = {
        "cpf": resultado[0][0],
        "nome": resultado[0][1],
        "email": resultado[0][2],
        "telefone": resultado[0][3],
    }

    return jsonify({
        "error": False,
        "message": "Dados atualizados com sucesso",
        "data": cliente_atualizado
    })


@app.route('/api/adicionarReceitaOuDespesa', methods=['POST'])
def adicionar_receita_despesa():
    dados = request.json
    print("📥 Recebido do frontend:", dados)

    #cpf = request.cookies.get('cpf')  # Aqui você deve obter o CPF do usuário logado
    #print(f"cpf recebido: {cpf}")

    cpf = dados['cpf']

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    tipo = dados['tipo']
    valor = float(dados['valor'])
    descricao = dados['descricao']
    categoria = dados['categoria'] if tipo == 'Despesa' else None
    data = dados['data']

    if tipo == 'Despesa' and not categoria:
        return jsonify({"error": True, "mensagem": "Categoria é obrigatória para despesas"}), 400

    query = QueryFactory.insert_query(
        table='receita_despesa',
        columns=['tipo', 'valor', 'descricao', 'categoria', 'data', 'cliente'],
        values=[tipo, valor, descricao, categoria, data, cpf]
    )

    inserir_db(query)
    
    return jsonify({"success": True, "mensagem": "Registro inserido com sucesso"})

@app.route('/api/receitas', methods=['GET'])
def receita_atual():
    #dados = request.json
    #print("📥 Recebido do frontend:", dados)

    #cpf = request.cookies.get('cpf')  # Aqui você deve obter o CPF do usuário logado
    #print(f"cpf recebido: {cpf}")

    cpf = request.args.get('cpf')

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400


    mes_atual = datetime.now().month
    ano_atual = datetime.now().year


    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Receita' AND cliente = '{cpf}'"
    )

    resultado = consultar_db(query)
    receita_total = resultado[0][0] if resultado else 0

    return jsonify({"sum": receita_total})

@app.route('/api/despesas', methods=['GET'])
def despesa_atual():

    #dados = request.json
    #print("📥 Recebido do frontend:", dados)

    #cpf = request.cookies.get('cpf')  # Aqui você deve obter o CPF do usuário logado
    #print(f"cpf recebido: {cpf}")

    cpf = request.args.get('cpf')

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400


    mes_atual = datetime.now().month
    ano_atual = datetime.now().year


    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Despesa' AND cliente = '{cpf}'"
    )

    resultado = consultar_db(query)
    despesa_total = resultado[0][0] if resultado else 0

    return jsonify({"sum": despesa_total})


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
    #dados = request.json
    cpf = request.args.get('cpf')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    if not ano or not mes:
        return jsonify({"error": "Parâmetros ausentes"}), 400

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{cpf}' AND tipo = 'Receita'"
    )

    resultado = consultar_db(query)
    receita_total = resultado[0][0] if resultado else 0

    return jsonify({"receitas": receita_total})

@app.route('/api/resumoDoMesDespesa', methods=['GET'])
def resumo_do_mes_despesa():
    #dados = request.json
    cpf = request.args.get('cpf')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    if not ano or not mes:
        return jsonify({"error": "Parâmetros ausentes"}), 400

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{cpf}' AND tipo = 'Despesa' "
    )

    resultado = consultar_db(query)
    despesa_total = resultado[0][0] if resultado else 0

    return jsonify({"despesas": despesa_total})

IMAGE_DIR = 'static/imagens'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/api/despesasPorCategoria', methods=['GET'])
def despesas_por_categoria():
    cpf = request.args.get('cpf')  # Pegando o login via query string

    categorias = ['Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens'] 

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    resultados_categorias = {}

    query_despesa = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',  # Se for NULL, retorna 0
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND tipo = 'Despesa' AND cliente = '{cpf}'"
    )
    despesa_resultado = consultar_db(query_despesa)
    despesa_total = despesa_resultado[0][0] if despesa_resultado else 0

    for categoria in categorias:
        query = QueryFactory.select_query(
            table='receita_despesa',
            columns='COALESCE(SUM(valor), 0)',
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano_atual}' AND EXTRACT(MONTH FROM Data) = '{mes_atual}' AND categoria = '{categoria}' AND cliente = '{cpf}' AND tipo = 'Despesa'"
        )

        resultado = consultar_db(query)

        valor = float(resultado[0][0]) if resultado and resultado[0] and resultado[0][0] is not None else 0  # Tratando possíveis valores nulos

        resultado_porcentagem = (valor / float(despesa_total) * 100) if despesa_total > 0 else 0  # Evitar divisão por zero

        resultados_categorias[categoria] = resultado_porcentagem

    df = pd.DataFrame(list(resultados_categorias.items()), columns=['Categoria', 'Valor'])

    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

    if df['Valor'].sum() == 0:
        return jsonify({"erro": "Nenhuma despesa encontrada"}), 400

    cores = ['#D8C4B6', '#c77e4a', '#213555', '#eee37c', '#F5EFE7', '#aeaeaa', '#6f2b62', '#3E5879', '#286853', '#7f3751']

    df_filtrado = df[df['Valor'] > 0]

    fig, ax = plt.subplots()

    wedges, texts, autotexts = ax.pie(
        df_filtrado['Valor'],
        labels=df_filtrado['Categoria'],  # Exibe os nomes das categorias
        autopct='%1.1f%%',  # Exibe as porcentagens
        startangle=140,
        colors=cores[:len(df_filtrado)],
        #wedgeprops={'edgecolor': 'white'}  # Borda branca nos setores
    )

    for text in texts + autotexts:
        text.set_color('white')
    ax.set_facecolor('#213555')

    #plt.title('Despesas por categoria')

    image_path = os.path.join(IMAGE_DIR, 'despesas_por_categoria.png')
    plt.savefig(image_path, transparent=True)
    print(f"Imagem salva em: {image_path}")

    # Fechar o gráfico
    plt.close()

    # Retornar a URL da imagem gerada
    image_url = f'http://localhost:5000/images/despesas_por_categoria.png'
    print(f"URL da imagem gerada: {image_url}")

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


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)



    
@app.route('/api/evolucaoDespesas', methods=['GET'])
def evolucao_despesas():

    cpf = request.args.get('cpf')  # Pegando o login via query string

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    meses = [(datetime.now() - relativedelta(months=i)).strftime('%Y-%m') for i in range(4, -1, -1)]
    nomes_meses = [(datetime.strptime(m, '%Y-%m')).strftime('%B').capitalize() for m in meses]

    despesas_meses = []

    for mes in meses:
        ano, mes_numero = mes.split('-')

        query = QueryFactory.select_query(
            table='receita_despesa',
            columns='SUM(valor)',
            where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes_numero}' AND cliente = '{cpf}' AND tipo = 'Despesa'"#login não existe aqui tem que receber ele
        )

        resultado = consultar_db(query)

        print("nomes_meses:", nomes_meses, "Tamanho:", len(nomes_meses))
        print("despesas_meses:", despesas_meses, "Tamanho:", len(despesas_meses))


        despesas_meses.append(resultado[0][0] if resultado and resultado[0][0] is not None else 0)

    while len(despesas_meses) < len(nomes_meses):
        despesas_meses.append(0)

    df = pd.DataFrame({'Mês': nomes_meses, 'Despesas': despesas_meses})

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(df['Mês'], df['Despesas'], color='#3E5879')

    ax.set_title("Evolução das despesas", fontsize=14, color='#F5EFE7')
    ax.set_facecolor('#213555')
    ax.spines['bottom'].set_color('#F5EFE7')
    ax.spines['left'].set_color('#F5EFE7')
    ax.xaxis.label.set_color('#F5EFE7')
    ax.yaxis.label.set_color('#F5EFE7')
    ax.tick_params(axis='x', colors='#F5EFE7', labelsize=10)
    ax.tick_params(axis='y', colors='#F5EFE7', labelsize=10)

    for bar, valor in zip(bars, df['Despesas']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(valor),
                ha='center', va='bottom', fontsize=10, color='white')

    image_path = os.path.join(IMAGE_DIR, 'evolucao_despesas.png')
    plt.savefig(image_path, transparent=True)
    plt.close()

    image_url = f'http://localhost:5000/images/evolucao_despesas.png'
    
    return jsonify({
        "resultado": resultado,
        "grafico_url": image_url
    })


@app.route('/api/resumoFinanceiro', methods=['GET'])
def resumo_financeiro():
    cpf = request.args.get('cpf', type=str)
    ano = request.args.get('ano', type=int)
    mes = request.args.get('mes', type=str)

    print(f"Parâmetros recebidos: CPF={cpf}, Ano={ano}, Mês={mes}")  # Log para depuração

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    if not ano or not mes:
        return jsonify({"error": "Parâmetros ausentes"}), 400
    

    meses_dict = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
    "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
    "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
    }

    if mes.isdigit():
        mes = int(mes)  # Se já for um número, converte diretamente
    else:
        mes = meses_dict.get(mes) 
    if mes is None:
        return jsonify({"error": "Mês inválido"}), 400


    query = QueryFactory.select_query(
        table='receita_despesa',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{cpf}'"
    )

    print("query:", query)  # Log para depuração

    resultado = consultar_db(query)
    print("resultado:", resultado)

    if not resultado:
        return jsonify([]) 

    if resultado is None:
        return jsonify({"error": "Erro ao buscar dados no banco"}), 500
   
    resultado_corrigido = [
        tuple(
            None if str(valor) == 'None' else float(valor) if isinstance(valor, Decimal) else valor
            for valor in linha
        )
        for linha in resultado
    ]

    print("Resultado corrigido:", resultado_corrigido)


    try:
        df = pd.DataFrame(resultado_corrigido, columns=['Id', 'Tipo', 'Valor', 'Descricao', 'Categoria', 'Data', 'Cliente'])
        print("df:", df)
        return jsonify(df.to_dict(orient='records'))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/api/orcamentoMensal', methods=['GET'])
def orcamento_mensal():
    cpf = request.args.get('cpf')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not cpf:
        return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400

    if not ano or not mes:
        return jsonify({"error": "Parâmetros ausentes"}), 400

    query = QueryFactory.select_query(
        table='receita_despesa',
        columns='COALESCE(SUM(valor), 0)',
        where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{cpf}' AND tipo = 'Despesa'"
    )

    resultado = consultar_db(query)
    valor_total_gasto = resultado[0][0] if resultado else 0

    return jsonify({"valor_gasto": valor_total_gasto})

@app.route('/api/relatorio', methods=['GET'])
def relatorio_categorias():
    try:
        cpf = request.args.get('cpf')  # Pegando o login via query string
        ano = request.args.get('ano')
        mes = request.args.get('mes')

        print(f"Parâmetros recebidos: CPF={cpf}, Ano={ano}, Mês={mes}")

        categorias = ['Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens'] 

        categorias_validas = [categoria for categoria in categorias if categoria is not None]

        if not cpf:
            return jsonify({"error": True, "mensagem": "CPF do usuário não encontrado"}), 400
        
        if not ano or not mes:
            return jsonify({"error": "Parâmetros ausentes"}), 400

        resultados_categorias = {}

        
        query_total_despesas = QueryFactory.select_query(
                table='receita_despesa',
                columns='COALESCE(SUM(valor), 0)',
                where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND cliente = '{cpf}' AND tipo = 'Despesa'"
        )

        print(f"Query total despesas: {query_total_despesas}")

        resultado_despesa = consultar_db(query_total_despesas)
        print(f"Resultado total despesas: {resultado_despesa}")

        despesa_total = float(resultado_despesa[0][0]) if resultado_despesa and resultado_despesa[0][0] is not None else 0

        # Evitar divisão por zero
        if despesa_total == 0:
            return jsonify({"erro": "Nenhuma despesa encontrada", "resultados": {}}), 200

        for categoria in categorias_validas:
            query_categoria = QueryFactory.select_query(
                table='receita_despesa',
                columns='COALESCE(SUM(valor), 0)',
                where_clause=f"EXTRACT(YEAR FROM Data) = '{ano}' AND EXTRACT(MONTH FROM Data) = '{mes}' AND categoria = '{categoria}' AND cliente = '{cpf}' AND tipo = 'Despesa'"
            )

            print(f"Query categoria ({categoria}): {query_categoria}")


            resultado_categoria = consultar_db(query_categoria)
            print(f"Resultado categoria ({categoria}): {resultado_categoria}")


            valor_categoria = float(resultado_categoria[0][0]) if resultado_categoria and resultado_categoria[0][0] is not None else 0  # Tratando possíveis valores nulos

            resultado_porcentagem = (valor_categoria /despesa_total) * 100

            resultados_categorias[categoria] = round(resultado_porcentagem, 2)

        df = pd.DataFrame(list(resultados_categorias.items()), columns=['Categoria', 'Porcentagem'])

        print("DataFrame:", df)

        #df['Porcentagem'] = pd.to_numeric(df['Porcentagem'], errors='coerce').fillna(0)

        if df['Porcentagem'].sum() == 0:
            print("Nenhuma despesa encontrada")
            
        return jsonify({
            "resultados": resultados_categorias,
        })
    
    except Exception as e:
        print(f"Erro no endpoint /api/relatorio: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500



# Rodando a aplicação
if __name__ == '__main__':
    app.run(debug=True)

    